# Firestarter-Style Top 100 Chart Viewer Plan

This document outlines the design and implementation details for upgrading the Binance Top 100 profile viewer notebook and standalone HTML report to a Firestarter-style multi-panel interactive layout.

## 1. Objectives & Layout Structure
The viewer is designed to display premium visualizations of the target dataset with a multi-panel charting setup matching the Firestarter visual aesthetics:
1. **Interactive Selector & Time window:** Custom symbol selection (`SELECTED_SYMBOL`) and date range parameters (`START_DATE` / `END_DATE`) to slice the 30-day klines.
2. **Chart Panels (Four Subplots, sharing X-axis):**
   - **Panel 1 (Price & Trend):** 1-hour or 4-hour Close Price line, overlaid with a 20-period Simple Moving Average (SMA) and 50-period SMA for visual context.
   - **Panel 2 (Volume & Direction):** Color-coded volume bar chart (green for up-candles where close >= open, red for down-candles).
   - **Panel 3 (Intraday Spread):** High-Low candle range percentage `(High - Low) / Open * 100`.
   - **Panel 4 (Rolling Volatility):** 20-period rolling standard deviation of 1-hour Close returns.
3. **Exact-Number Data Tables:**
   - Previews of the latest 20 rows of 5m data.
   - Resampled 1-hour and 4-hour aggregated summary tables.
   - Comprehensive inventory summary table including symbols, total rows, start/end UTC datetimes, missing candles, and unicode warning flags.

## 2. Ingested Fields (Binance 5m data)
We parse the standard columns from the local CSVs:
- `open_time` / `close_time` (Unix milliseconds, converted to UTC datetime)
- `open`, `high`, `low`, `close` (Floats)
- `volume` (Float, base asset volume)
- `quote_asset_volume` (Float)
- `trades` (Integer)

## 3. Boundaries and Exclusions
- **No Predictive/Labeling Logic:** No Cell 2, target labels, machine learning features, or trading recommendations are generated.
- **No Custom Flow Indicators:** No ER/FMLC/Flowprint computations are added.
- **Zero Raw Data Staging:** Raw CSV data remains untracked in version control.
