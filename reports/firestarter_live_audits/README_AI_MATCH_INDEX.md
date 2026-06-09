# Firestarter Live Audits — AI Match Index

## Status

Layout/specification document. Research-only.

## Goal

Create a compact AI-readable derived table so ChatGPT can quickly compare a symbol/date anomaly against the Top100 universe without manual screenshots.

Example request:

```text
Check HYPEUSDT from 2026-05-17 to 2026-05-22 against all others.
```

The intended workflow is:

```text
Local Top100 data
-> build_ai_match_index.py
-> ai_match_index.csv
-> ChatGPT/internal sandbox comparison
-> Firestarter Live Audits review note
```

## Output location

Generated full index should remain local by default:

```text
reports/firestarter_live_audits/ai_match_index.csv
reports/firestarter_live_audits/ai_match_index_summary.md
```

The full `ai_match_index.csv` should not be committed by default. Commit only docs, the builder script, and small samples if needed.

## Required columns

```text
timestamp
symbol
close
er
fmlc
flowprint
raw_score
x2_candidate
hollow_breakout
fake_recovery
domino_deterioration
entry_c_recovery
primary_event_type
secondary_tags
data_quality_flags
nan_pct_score
deriv_available
```

## Optional helper columns

These may be added if they are compact and derived from already-approved profile logic:

```text
fmlc_delta_1h
flowprint_delta_1h
raw_score_delta_1h
price_return_1h
price_return_4h
price_return_24h
fmlc_persistence_6h
raw_score_persistence_6h
flowprint_confirmation_state
```

## Minimum summary fields

`ai_match_index_summary.md` should report:

```text
run_timestamp_utc
source_candle_dir
source_derivatives_dir
symbols_seen
symbols_written
row_count
first_timestamp
last_timestamp
symbols_missing_candles
symbols_missing_derivatives
nan_warning_symbols
output_path
```

## Query patterns this enables

### Reference window search

```text
symbol = HYPEUSDT
start = 2026-05-17
end = 2026-05-22
```

### Cross-symbol comparison

Find other symbols with similar profile behavior:

```text
fmlc rising
raw_score rising
fmlc persistence
price continuation
```

### Failure-pattern comparison

Find symbols where price climbed but support metrics failed:

```text
price up
flowprint weak
fmlc weak
raw_score weak
```

## Safety rules

- This file is derived research data only.
- It is not a signal table.
- It is not a strategy table.
- It must not contain buy/sell/trade/action language.
- It must not include raw 5-minute source rows.
- It must not mutate source data.
- It must not overwrite historical raw files.
- It must not create Cell 2 labels.

## Recommended script path

```text
scripts/firestarter_live_audits/build_ai_match_index.py
```

## Recommended command

```powershell
python scripts\firestarter_live_audits\build_ai_match_index.py `
  --candles-dir C:\firestarterspb\data\research\binance_top100_excluding_existing_5_1month `
  --derivatives-dir C:\firestarterspb\data\research\binance_top100_derivatives_context_1month `
  --output reports\firestarter_live_audits\ai_match_index.csv
```

## Commit policy

Commit:

```text
scripts/firestarter_live_audits/build_ai_match_index.py
reports/firestarter_live_audits/README.md
reports/firestarter_live_audits/README_AI_MATCH_INDEX.md
reports/firestarter_live_audits/templates/*.md
reports/firestarter_live_audits/samples/*.csv
```

Do not commit by default:

```text
reports/firestarter_live_audits/ai_match_index.csv
reports/firestarter_live_audits/review_packets/
reports/firestarter_live_audits/screenshots/
```
