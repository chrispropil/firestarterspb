# FirestarterSPB Cloud Alert Bridge v1 Build Report

DATE: 2026-06-13
SYSTEM: FirestarterSPB Cloud
TASK: Cloud Alert Bridge v1
STATUS: READY_FOR_REVIEW
BRANCH: `feature/cloud-alert-bridge-v1`
BASE: `main`

---

## 1. Purpose

Restore the ntfy notification layer in a cloud-safe way before reconnecting scheduled alert loops or scaling the symbol universe.

This is a bridge layer only. It does not create, modify, or promote market-scoring logic.

---

## 2. Files Added

- `scripts/automation/ntfy_notify.py`
- `scripts/automation/cloud_alert_bridge.py`
- `configs/cloud_alert_bridge_v1.json`
- `reports/firestarter_spb_cloud_alert_bridge_v1_build_report.md`

## 3. Files Updated

- `scripts/automation/cloud_health_check.py`

---

## 4. New Capabilities

### ntfy notifier wrapper

`scripts/automation/ntfy_notify.py`:

- Loads ntfy secrets from `/root/.config/firestarter/ntfy.env`.
- Sends ntfy notifications using Bearer token auth.
- Supports dry-run mode.
- Does not print token contents.
- Does not store topic or token in repo.

### Cloud alert bridge

`scripts/automation/cloud_alert_bridge.py`:

- Builds local alert events.
- Appends events to `state/cloud_alert_bridge/events.jsonl`.
- Sends notifications only when `--send` is explicitly passed.
- Supports these manual event types:
  - `manual_test`
  - `health`
  - `baseline_audit`

### Baseline audit policy

`configs/cloud_alert_bridge_v1.json`:

- Uses `reports/cloud_data_pilot/v1/audit.json`.
- Expected full symbol row count: `8640`.
- Accepts `MATICUSDT` as a known zero-row symbol for the first Phase 2A baseline.
- Any other zero-row or short symbol emits HOLD.

---

## 5. Worker Routes Added

Fixed allowlisted routes only:

- `/run/cloud-alert-bridge-dryrun`
- `/run/cloud-alert-bridge-send-baseline-audit`
- `/run/cloud-alert-bridge-send-health`
- `/run/cloud-alert-bridge-send-manual-test`

No arbitrary command execution was added.

---

## 6. Explicit Non-Scope

Not included:

- n8n schedule activation
- live trading
- exchange credentials
- exchange order execution
- optimizer production
- scoring changes
- Cell 2 activation
- FMLC Hanger detector promotion
- Flow Fade detector promotion
- Slingshot detector promotion
- symbol universe expansion

Pattern alerts remain listed as future alert types until separately built and reviewed.

---

## 7. Validation

Local syntax validation performed before commit:

```bash
python3 -m py_compile /tmp/ntfy_notify.py /tmp/cloud_alert_bridge.py
```

Expected VPS validation after merge/deploy:

```bash
cd /opt/firestarterspb && git pull
python3 -m py_compile scripts/automation/ntfy_notify.py scripts/automation/cloud_alert_bridge.py scripts/automation/cloud_health_check.py
python3 scripts/automation/cloud_alert_bridge.py --event-type baseline_audit --dry-run
python3 scripts/automation/cloud_alert_bridge.py --event-type baseline_audit --send
curl -s -X POST http://127.0.0.1:8090/run/cloud-alert-bridge-send-manual-test
```

---

## 8. Safety Boundary

`raw_data_mutation=false`
`scoring_changes=false`
`trading_execution=false`
`exchange_credentials=false`
`optimizer_production=false`
`n8n_schedule_activation=false`

STATUS: `READY_FOR_REVIEW`
