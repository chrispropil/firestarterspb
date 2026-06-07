# Top 100 Evidence Viewer Light Blue Build Plan

This plan outlines the architecture, data pipeline, and visual specifications for the Top 100 Evidence Viewer.

## 1. Objective & Scope
The goal is to build a unified research-only viewer for 100 symbols using the 1-month 5m Binance dataset and derivatives context, displaying indicators in the Evidence Viewer layout with a light-blue theme.

## 2. Technical Design
- **Data Pipeline:**
  - Discover files in `data/research/binance_top100_excluding_existing_5_1month/`.
  - For each symbol, read 5m CSV, resample to 1-Hour intervals.
  - Load derivatives context (funding rate, open interest, taker ratio) from `data/research/binance_top100_derivatives_context_1month/` and merge.
  - Compute Cell 1 metrics (ER, FMLC, Flowprint, raw_score) exactly matching current specifications.
  - Downsample/aggregate all symbol datasets into a JSON structure embedded in a single self-contained `index.html`.
- **UI & Visualization:**
  - Page Background: Light-blue `#eef4f8`.
  - Layout: Single header, dropdown symbol selector, hover readout panel, and a triple-pane Plotly chart.
  - Plotly Panes:
    - Top Pane: Price Proxy
    - Middle Pane: FMLC, Flowprint, and Raw Score
    - Bottom Pane: Evidence Ratio (ER) as a bar chart
- **Exclusions:**
  - No volume panels, no moving averages (SMA 20/50), no transaction metrics.
  - No live trading buttons, recommendation badges, or Cell 2 labels.

## 3. Verification & Safety Boundaries
- Confirm all 100 symbols load successfully.
- Ensure all metric values are calculated correctly without modifying baseline formulas.
- Verify no raw data CSV files are committed.
