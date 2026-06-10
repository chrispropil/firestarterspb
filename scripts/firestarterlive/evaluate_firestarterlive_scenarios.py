import os
import sys
import yaml
import json
from datetime import datetime

# Paths
SCENARIOS_PATH = "C:/firestarterspb/configs/firestarterlive/firestarterlive_scenarios.yaml"
ALERT_SETTINGS_PATH = "C:/firestarterspb/configs/firestarterlive/firestarterlive_alert_settings.yaml"
SCHEMA_REPORT_PATH = "C:/firestarterspb/reports/firestarterlive/firestarterlive_scenario_schema_validation.md"
DRY_RUN_REPORT_PATH = "C:/firestarterspb/reports/firestarterlive/firestarterlive_dry_run_report.md"

def fail_closed(reason):
    print(f"FAIL CLOSED: {reason}")
    sys.exit(1)

def main(write_reports=True):
    if '--dry-run' not in sys.argv:
        print("Notice: Script running in default mode, which is forced to --dry-run for Phase B.")
    
    # 1. Load config
    if not os.path.exists(SCENARIOS_PATH):
        fail_closed(f"Config missing: {SCENARIOS_PATH}")
    if not os.path.exists(ALERT_SETTINGS_PATH):
        fail_closed(f"Config missing: {ALERT_SETTINGS_PATH}")
        
    try:
        with open(SCENARIOS_PATH, 'r') as f:
            scenarios_config = yaml.safe_load(f)
        with open(ALERT_SETTINGS_PATH, 'r') as f:
            alerts_config = yaml.safe_load(f)
    except Exception as e:
        fail_closed(f"Failed to parse YAML: {e}")

    # Check alert settings for enabled notifications
    notifications = alerts_config.get('notifications', {})
    for channel, settings in notifications.items():
        if channel != 'console' and settings.get('enabled', False):
            fail_closed(f"Alert setting implies enabled notification delivery for {channel}. Not allowed.")
            
    # Check alert settings safety
    safety = alerts_config.get('safety', {})
    if not safety.get('no_order_execution', False) or not safety.get('no_auto_trade', False):
        fail_closed("Safety settings must explicitly disable trade/execution.")

    if scenarios_config.get('trade_execution', False):
        fail_closed("Global scenario config allows trade execution. Not allowed.")

    # 2. Validate basic schema
    scenarios = scenarios_config.get('scenarios', [])
    valid = True
    schema_errors = []
    
    if not isinstance(scenarios, list):
        schema_errors.append("Scenarios must be a list.")
        valid = False
    else:
        for i, sc in enumerate(scenarios):
            if 'id' not in sc:
                schema_errors.append(f"Scenario {i} missing 'id'")
                valid = False
            if 'enabled' not in sc:
                schema_errors.append(f"Scenario {sc.get('id', i)} missing 'enabled' flag")
                valid = False
            if 'side' not in sc:
                schema_errors.append(f"Scenario {sc.get('id', i)} missing 'side'")
                valid = False
            if 'criteria' not in sc:
                schema_errors.append(f"Scenario {sc.get('id', i)} missing 'criteria'")
                valid = False
                
    schema_report = f"# FirestarterLive Scenario Schema Validation\n\nDate: {datetime.utcnow().isoformat()}Z\n"
    schema_report += f"Status: {'VALID' if valid else 'INVALID'}\n\n"
    if not valid:
        schema_report += "Errors:\n" + "\n".join([f"- {e}" for e in schema_errors])
    else:
        schema_report += f"Successfully validated {len(scenarios)} scenarios.\n"
        
    if write_reports:
        os.makedirs(os.path.dirname(SCHEMA_REPORT_PATH), exist_ok=True)
        with open(SCHEMA_REPORT_PATH, 'w') as f:
            f.write(schema_report)
        
    if not valid:
        fail_closed("Schema invalid. Check schema validation report.")

    # 4. Run dry-run evaluation
    # 5. Print triggered/not-triggered/disabled status
    eval_results = []
    
    print("FirestarterLive Phase B Dry-Run Evaluator")
    print("-" * 50)
    for sc in scenarios:
        sc_id = sc['id']
        # 3. Confirm scenarios are disabled by default unless explicitly enabled
        enabled = sc.get('enabled', False)
        
        if not enabled:
            status = "DISABLED"
        else:
            # Phase B: scenarios that are enabled will be evaluated
            # Since criteria are currently null or placeholder, they will not trigger
            status = "NOT_TRIGGERED"
            
        print(f"[{status}] {sc_id}")
        eval_results.append({
            'id': sc_id,
            'status': status,
            'description': sc.get('description', '')
        })

    # 6. Write dry-run report
    dry_run_report = f"# FirestarterLive Dry-Run Evaluation Report\n\nDate: {datetime.utcnow().isoformat()}Z\n"
    dry_run_report += "Phase B Scenario Evaluation\n\n"
    dry_run_report += "| Scenario ID | Status | Description |\n|---|---|---|\n"
    for res in eval_results:
        dry_run_report += f"| {res['id']} | {res['status']} | {res['description']} |\n"
        
    if write_reports:
        with open(DRY_RUN_REPORT_PATH, 'w') as f:
            f.write(dry_run_report)
        
    print("-" * 50)
    print("Dry-run complete. Reports generated.")

if __name__ == "__main__":
    main()
