# Firestarter Optimizer State Monitor Data-Quality Separation Report

Run UTC: 2026-06-14T03:57:49Z

## Observation-Only Boundary

This pass separates lifecycle state from data quality. It does not create trade instructions, edge claims, exclusion rules, or automatic rule changes.

## Input

- Candidate ticket input path: `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\candidate_tickets.jsonl`
- Tickets read: `644`
- Active candidate groups: `101`

## Lifecycle State Distribution

- `NEW`: `20`
- `PERSISTENT_HANGER`: `81`

## Data Quality Distribution

- `DATA_GAP_PARTIAL`: `101`

## Action Label Distribution

- `SHORT_HANGER_REVIEW_DATA_GAP`: `101`

## Direction Bias Distribution

- `AVOID_LONG`: `63`
- `SHORT_REVIEW`: `38`

## Signal Family Distribution

- `SHORT_HANGER`: `101`

## Data Gap Fields Distribution

- `price_position`: `101`

## Write Behavior

- Event rows before write-run: `433`
- Event rows after write-run: `534`
- Append-only state events preserved: `True`
- State events appended this run: `101`
- Active snapshot atomic write: `confirmed by temp-file plus os.replace implementation`

## Commands Run

```powershell
python scripts/firestarter_optimizer/update_candidate_states.py --input reports/firestarter_optimizer/candidate_tickets.jsonl --dry-run
python scripts/firestarter_optimizer/update_candidate_states.py --input reports/firestarter_optimizer/candidate_tickets.jsonl
python -m py_compile scripts/firestarter_optimizer/update_candidate_states.py
```

## Files Changed

- `scripts/firestarter_optimizer/update_candidate_states.py`
- `reports/firestarter_optimizer/active_candidates.jsonl`
- `reports/firestarter_optimizer/candidate_state_events.jsonl`
- `reports/firestarter_optimizer/expired_or_changed_candidates.jsonl`
- `reports/firestarter_optimizer/update_candidate_states_report.md`
- `reports/firestarter_optimizer/update_candidate_states_data_quality_separation_report.md`
- `reports/firestarter_optimizer/y_hanger_diagnostic_state_report.md`

## Boundary Check

No raw scanner files, live scanner files, Bitget/order/trading logic, historical JSONL/parquet/OHLCV/Tardis files, `candidate_rules.yaml`, ML files, `signal_discovery.py`, Slack/n8n files, Google Drive sync logic, cloud optimizer queue activation, or Google Drive active outputs were modified.
