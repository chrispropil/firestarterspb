# Firestarter Optimizer Y_HANGER Diagnostic State Report

Run UTC: 2026-06-14T03:57:49Z

## Observation-Only Boundary

This diagnostic run analyzes Y_HANGER candidates. It does not create trade instructions, edge claims, exclusion rules, or automatic rule changes.

## Input Information

- **Input candidate ticket path:** `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\candidate_tickets.jsonl`
- **Tickets read:** `644`
- **Active candidate group count:** `101`

## Lifecycle State Distribution

- `NEW`: `20`
- `PERSISTENT_HANGER`: `81`

## Diagnostic State Distribution

- `Y_HANGER`: `101`

## Y_HANGER Reason Tags Distribution

- `Y_UNKNOWN_MISSING_INPUTS`: `101`

## Y_HANGER Missing Inputs Distribution

- `absorption`: `101`
- `btc_beta`: `101`
- `ema_structure`: `101`
- `fmlc_crowding`: `101`
- `liquidity_shelf`: `101`
- `market_risk_on`: `101`
- `price_position`: `101`
- `sell_trigger`: `101`
- `thin_liquidity`: `101`

## Data Quality Distribution

- `DATA_GAP_PARTIAL`: `101`

## Direction Bias Distribution

- `AVOID_LONG`: `63`
- `SHORT_REVIEW`: `38`

## Signal Family Distribution

- `SHORT_HANGER`: `101`

## Write Verification

- Event rows before run: `433`
- Event rows after run: `534`
- Confirmation append-only state events were preserved: `True`
- Confirmation active snapshot was atomically written: `confirmed by temp-file plus os.replace implementation`

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
