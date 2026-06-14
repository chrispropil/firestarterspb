# Binance 25 Symbol 1 Month History Gate

STATUS: READY_FOR_CLOUD_PULL

## Purpose

Capture a Binance USD-M one-month historical baseline for the governed 25-symbol Cell 1 universe.

## Scope

Adds a research/backfill puller only:

- `scripts/binance_spb/pull_binance_25_symbol_1month_history.py`

Expected outputs when run on cloud:

- `data/research/binance_25_symbol_1month/`
- `reports/cloud_pattern_watch/v1/binance_25_symbol_1month_manifest.csv`
- `reports/cloud_pattern_watch/v1/binance_25_symbol_1month_pull_audit.md`

## Data Pulled

For each governed symbol:

- Binance USD-M 1h klines
- Binance USD-M 4h klines
- Binance USD-M funding history
- Binance USD-M open-interest history, where available
- Binance USD-M open-interest current snapshot, where available

## Safety Boundary

This does not mutate:

- `state/cloud_pattern_watch/current_metrics.json`
- `state/cloud_pattern_watch/current_metrics.csv`
- `state/cloud_pattern_watch/current_snapshot.json`
- Pattern Watch send state
- n8n state
- trading/execution logic

## Validation Command

```bash
cd /opt/firestarterspb
source .venv/bin/activate
python -m py_compile scripts/binance_spb/pull_binance_25_symbol_1month_history.py
python scripts/binance_spb/pull_binance_25_symbol_1month_history.py
cat reports/cloud_pattern_watch/v1/binance_25_symbol_1month_pull_audit.md
```

## Pass Condition

`PASS_BINANCE_25_SYMBOL_1MONTH_HISTORY_READY_FOR_REVIEW`
