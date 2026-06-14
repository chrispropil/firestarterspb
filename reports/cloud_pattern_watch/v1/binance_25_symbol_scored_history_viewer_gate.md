# Binance 25 Symbol Scored History Viewer Gate

STATUS: READY_FOR_CLOUD_VIEWER_BUILD

## Purpose

Build a static anytime-viewer for the Binance 25-symbol one-month historical Firestarter scoring output.

## Script

- `scripts/visualization/build_binance_25_symbol_scored_history_viewer.py`

## Input

- `data/research/binance_25_symbol_1month_scored/binance_25_symbol_1month_firestarter_scored.csv`

## Output

- `reports/cloud_pattern_watch/v1/binance_25_symbol_1month_scored_viewer.html`
- `reports/cloud_pattern_watch/v1/binance_25_symbol_1month_scored_viewer_report.md`

## Viewer Features

- Symbol dropdown
- Symbol search
- Hover readout with exact metrics
- Price panel
- FMLC / Flowprint / Raw Score panel
- ER bar panel
- Funding panel
- Right-side y-axis mirrors for chart readability
- Research-only banner

## Boundary

Static viewer only.

Does not write:

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
python -m py_compile scripts/visualization/build_binance_25_symbol_scored_history_viewer.py
python scripts/visualization/build_binance_25_symbol_scored_history_viewer.py
cat reports/cloud_pattern_watch/v1/binance_25_symbol_1month_scored_viewer_report.md
```

## Optional Local Access

```bash
cd /opt/firestarterspb/reports/cloud_pattern_watch/v1
python -m http.server 8088 --bind 127.0.0.1
```

Open via SSH tunnel or local browser depending on machine access.

## Pass Condition

`PASS_BINANCE_25_SYMBOL_SCORED_HISTORY_VIEWER_READY`
