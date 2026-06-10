# Firestarter A4 Evidence Viewer Recovery Plan

## Objective
Recreate the missing `firestarter_a4_evidence_viewer.py` as a localized, simple viewer focused entirely on A4 evidence research without touching production or live trading infrastructure.

## Scope & Boundaries
- **Research Only:** Strictly for viewing historical A4 replay/audit data.
- **No Production UI:** Simple charts and terminal printouts using matplotlib, plotly, or a basic Dash/Streamlit script without production-grade styling.
- **No Trading/Action Labels:** Exclude all action flags, trading logic, alert components, or signals.
- **No Formulas Changed:** Purely visualization; use pre-calculated columns.
- **No Data Mutation:** Read-only access to CSV/JSONL/parquet data. 

## Core Requirements
1. **Data Source:** Read A4 source CSV directly (e.g., `firestarter_lane_a4_25_symbol_cell1_replay_output.csv`).
2. **Selectors:**
   - **Symbol Selector:** Command-line argument or simple dropdown.
   - **Timestamp Window Selector:** Arguments for `--event-ts` and `--window-hours` to isolate specific events.
3. **Visualization (Charts & Printouts):**
   - **ER (Event Ratio / Evidence Ratio):** Display as a bottom-pane bar chart on a separate Y-axis. Do NOT plot as a top-pane line.
   - **FMLC & Flowprint:** Display as lines on the top pane, alongside price/candles.
   - **raw_score & trigger:** Include in the chart or printout metrics table.
   - **Hover Information:** Exact row, timestamp, and raw values must be visible on hover.
4. **Crash-Start Forensic Markers:**
   - Clearly delineate where crash sequences or high ER spikes begin using vertical dashed lines or highlighted regions.

## Next Steps
- Validate the required A4 source data files are present.
- Draft the Python script based on `pandas` and `plotly` to achieve interactive HTML outputs.
- Test against `NEARUSDT` using an established timestamp window.
