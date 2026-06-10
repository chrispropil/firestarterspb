# FirestarterOG Binance 1-Month Local Viewer Report

## Execution Status
The script has generated a static HTML viewer containing all analytical traces.

## Package Gap Report
- **Flask + Plotly Available:** No
- **Action Taken:** A pure JavaScript static HTML export (using Plotly CDN) was generated to ensure the viewer works without requiring a local Python package install.

## Processing Summary
- **Input File:** `firestarterog_real_historical_variance_sample.csv`
- **Output Artifact:** `reports/firestarterog_binance_1m_local_viewer.html`
- **Total Valid Rows Processed:** 3520
- **Unique Symbols Found:** 8

## Features Evaluated
- **Regime Calculation:** Derived dynamically from average `change_24h_%` per timestamp.
- **Entry C Markers:** Explicitly marked where the regime is bearish AND 4h FMLC rise >= 2 AND 4h Flowprint rise >= 2.
- **Fake Recovery Markers:** Highlighted where FMLC is rising but Flowprint is weak.
- **Visual Isolation:** ER sits independently as a bar chart on the bottom pane.

**PASS: PASS_FIRESTARTEROG_BINANCE_1M_LOCAL_VIEWER_READY**
