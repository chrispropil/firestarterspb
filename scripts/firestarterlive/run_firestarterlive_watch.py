import os
import sys
import json
import yaml
from datetime import datetime

# Governance Headers
print("==================================================")
print("NOTICE_ONLY | RESEARCH_ALERT | NO_AUTO_TRADE")
print("NO_EXCHANGE_KEYS | NO_ORDER_EXECUTION | MANUAL_REVIEW_REQUIRED")
print("==================================================")

# Paths
SCENARIOS_PATH = "C:/firestarterspb/configs/firestarterlive/firestarterlive_scenarios.yaml"
ALERT_SETTINGS_PATH = "C:/firestarterspb/configs/firestarterlive/firestarterlive_alert_settings.yaml"

def fail_closed(reason):
    print(f"FAIL CLOSED: {reason}")
    sys.exit(1)

def main():
    # Parse arguments
    args = sys.argv[1:]
    
    # 7. Fail closed if --send-alerts is provided or attempted
    if '--send-alerts' in args:
        fail_closed("--send-alerts is not implemented/allowed in Phase C. Notification delivery is forbidden.")

    # 2. Default mode must be dry-run
    # If no arguments are provided, or if --dry-run is provided, run in dry-run mode.
    # Note: Phase C is strictly dry-run.
    is_dry_run = True
    if '--dry-run' in args or len(args) == 0:
        is_dry_run = True
    
    write_audit = '--write-audit' in args
    
    print(f"Running FirestarterLive Watcher (Mode: {'Dry-Run' if is_dry_run else 'Production-Blocked'}).")
    
    # Load configs
    if not os.path.exists(SCENARIOS_PATH) or not os.path.exists(ALERT_SETTINGS_PATH):
        fail_closed("Configuration files missing.")
        
    try:
        with open(ALERT_SETTINGS_PATH, 'r') as f:
            alerts_config = yaml.safe_load(f)
        with open(SCENARIOS_PATH, 'r') as f:
            scenarios_config = yaml.safe_load(f)
    except Exception as e:
        fail_closed(f"Failed to load configs: {e}")

    # Enforce safety block checks
    safety = alerts_config.get('safety', {})
    if not safety.get('no_auto_trade', False) or not safety.get('no_order_execution', False):
        fail_closed("Safety settings do not block execution. Force-failing.")
    if alerts_config.get('runtime', {}).get('send_alerts', False):
        fail_closed("Configuration tries to enable send_alerts. Force-failing.")

    # 3. Invoke/reuse the Phase B evaluator logic
    print("Invoking Phase B Scenario Evaluator...")
    sys.path.append("C:/firestarterspb")
    try:
        import scripts.firestarterlive.evaluate_firestarterlive_scenarios as evaluator
        # Call the evaluator's main logic
        evaluator.main(write_reports=False)
    except Exception as e:
        fail_closed(f"Failed during scenario evaluation invocation: {e}")

    # 5. It may support --write-audit to write a local audit/status file
    if write_audit:
        print("Writing local audit and status files...")
        
        # Read paths from alert settings config or default
        outputs = alerts_config.get('outputs', {})
        events_path = os.path.join("C:/firestarterspb", outputs.get('alert_events_jsonl', 'reports/firestarterlive/firestarterlive_alert_events.jsonl'))
        status_path = os.path.join("C:/firestarterspb", outputs.get('latest_status_json', 'reports/firestarterlive/firestarterlive_latest_status.json'))
        daily_audit_path = os.path.join("C:/firestarterspb", outputs.get('daily_audit_md', 'reports/firestarterlive/firestarterlive_daily_audit.md'))
        
        os.makedirs(os.path.dirname(events_path), exist_ok=True)
        os.makedirs(os.path.dirname(status_path), exist_ok=True)
        os.makedirs(os.path.dirname(daily_audit_path), exist_ok=True)
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # 1. Append to JSONL events
        event_entry = {
            "timestamp": timestamp,
            "event": "watcher_run",
            "mode": "dry_run",
            "message": "Watcher run completed successfully in dry-run mode."
        }
        with open(events_path, 'a') as f:
            f.write(json.dumps(event_entry) + "\n")
            
        # 2. Write status JSON
        status_entry = {
            "last_run": timestamp,
            "status": "success",
            "mode": "dry_run",
            "scenarios_evaluated": len(scenarios_config.get('scenarios', []))
        }
        with open(status_path, 'w') as f:
            json.dump(status_entry, f, indent=2)
            
        # 3. Write/update daily audit markdown
        daily_audit_content = f"""# FirestarterLive Watcher Daily Audit

- **Last Run Timestamp**: {timestamp}
- **Status**: SUCCESS
- **Mode**: Dry-Run
- **Governance**: NOTICE_ONLY | RESEARCH_ALERT | NO_AUTO_TRADE | NO_EXCHANGE_KEYS | NO_ORDER_EXECUTION

Scenarios evaluated: {len(scenarios_config.get('scenarios', []))} (all disabled by default).
No orders placed, no notifications sent.
"""
        with open(daily_audit_path, 'w') as f:
            f.write(daily_audit_content)
            
        print("Audit files updated successfully.")
        
    print("Watcher execution finished cleanly.")

if __name__ == "__main__":
    main()
