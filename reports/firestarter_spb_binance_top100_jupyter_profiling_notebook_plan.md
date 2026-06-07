# Gravity Next Lane — Jupyter Profiling Notebook Plan

This document outlines the design and implementation plan for a local Jupyter notebook dedicated to inspecting, profiling, and analyzing the Binance Top 100 USDT Perpetual dataset (excluding the five core baseline assets).

## 1. Core Target Directory & Path
- **Target Dataset Directory:** `data/research/binance_top100_excluding_existing_5_1month/`
- **Proposed Notebook Path:** `notebooks/firestarter_spb_top100_profile_viewer.ipynb`

## 2. Key Profiling Objectives
The notebook will perform high-precision data integrity audits and baseline profiling:
1. **Per-Symbol Row Counts:** Verify that each of the 100 target symbols has the expected number of 5m intervals (approximately 8,640 rows for a 30-day month).
2. **Missing Candle Audits:** Identify any gaps or missing timestamps within the expected range.
3. **Timestamp Continuity Checks:** Validate that the step difference between sequential index records is strictly $300,000\text{ ms}$ (5 minutes).
4. **Multi-Scale Resampling:** Aggregate the primary 5-minute data to 1-hour and 4-hour intervals using strict open-high-low-close (OHLC) and volume summation rules.

## 3. Visualization and Chart Design
The notebook will display visual summaries on a per-symbol basis using a dynamic symbol selector interface.
- **Interactive Selector:** Interactive dropdown or query filter to select one of the 100 symbols.
- **Visual Panels (Subplots):**
  - **Panel 1 (Price Line):** Close price tracking across the 1-month period.
  - **Panel 2 (Volume Bars):** Resampled bar chart representing trading volume.
  - **Panel 3 (Volatility/Range):** True range or high-low spread tracking.
  - **Panel 4 (Flow / Context):** Pure placeholder panels for custom structural metrics, with no trading or predictive logic.

## 4. Boundaries and Constraints
- **No Git Tracking of Data:** Raw CSV files, raw JSON files, and full notebook outputs containing extensive raw data will be excluded from git staging.
- **No Predictive/Labeling Logic:** No Cell 2, labeling, model training, or trading logic.
- **No Raw Row Dumps:** Summary tables and plots are exported locally, but raw datasets will not be dumped into the reports directory.
- **Approval Gate:** This plan must be approved prior to starting the notebook build.
