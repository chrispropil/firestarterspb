# Binance 25 Symbol 1 Month Historical Scoring Gate

STATUS: READY_FOR_CLOUD_SCORING_RUN

## Purpose

Convert the Binance one-month historical pull into scored Firestarter research output.

## Script

- `scripts/binance_spb/score_binance_25_symbol_1month_history.py`

## Inputs

- `data/research/binance_25_symbol_1month/*_futures_klines_1h.csv`
- `data/research/binance_25_symbol_1month/*_futures_klines_4h.csv`
- `data/research/binance_25_symbol_1month/*_funding_rate_history.csv`
- `configs/cloud_data_pilot_v1_symbols.json`

## Outputs

- `data/research/binance_25_symbol_1month_scored/binance_25_symbol_1month_firestarter_scored.csv`
- `data/research/binance_25_symbol_1month_scored/binance_25_symbol_1month_firestarter_scored.jsonl`
- `reports/cloud_pattern_watch/v1/binance_25_symbol_1month_scored_manifest.csv`
- `reports/cloud_pattern_watch/v1/binance_25_symbol_1month_scored_audit.md`

## Output Columns

- symbol
- timestamp_utc
- source_exchange
- scoring_mode
- price
- price_position
- er
- fmlc
- flowprint
- raw_score
- rvol_1h
- rvol_4h_window
- funding
- open_interest
- range_pos_20
- range_pos_50_4h
- near_breakout
- clean_reclaim
- above_4h_trend
- er_parent_status
- fmlc_parent_status
- flowprint_parent_status
- raw_score_parent_status
- data_quality_flags

## Known Caveat

The one-month history pull showed historical open-interest statistics unavailable. The scoring converter therefore uses `historical_research_no_oi_history` mode, omits the OI point from Flowprint, and marks rows with `OI_HISTORY_UNAVAILABLE`.

## Safety Boundary

This is research/backfill only. It does not write:

- `state/cloud_pattern_watch/current_metrics.json`
- `state/cloud_pattern_watch/current_snapshot.json`
- Pattern Watch send state
- n8n state
- trading/execution state

## Cloud Validation Command

```bash
cd /opt/firestarterspb
git fetch origin
git reset --hard origin/main
source .venv/bin/activate
python -m py_compile scripts/binance_spb/score_binance_25_symbol_1month_history.py
python scripts/binance_spb/score_binance_25_symbol_1month_history.py
cat reports/cloud_pattern_watch/v1/binance_25_symbol_1month_scored_audit.md
```

## Pass Condition

`PASS_BINANCE_25_SYMBOL_1MONTH_HISTORY_SCORED_READY_FOR_REVIEW`
