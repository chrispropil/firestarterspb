# Firestarter SPB: Top 100 Profile Viewer HTML Export Audit

## Overview
This document records the programmatic generation of the standalone HTML report/viewer representing the profiling results of the Binance Top 100 USDT Perpetual dataset (excluding core 5 baselines).

## 1. Export Command Details
The following nbconvert command was used to execute and compile the Jupyter notebook to HTML:
```powershell
py -m nbconvert --execute --to html notebooks/firestarter_spb_top100_profile_viewer.ipynb --output-dir reports/html
```

## 2. File Verification
- **Output File Path:** `reports/html/firestarter_spb_top100_profile_viewer.html`
- **File Size:** ~535 KB
- **Generated:** YES
- **Content Integrity:** Successfully executes all 14 cells including:
  - Dynamic dataset inventory table scanning 100 CSVs.
  - Ticker preview (latest 20 rows) for `BTCUSDT`.
  - Detailed numeric summary statistics (OHLCV, Volume, Volatility/Range).
  - 1-hour and 4-hour resampling aggregates.
  - Three visual charts (Close Price, Volume, Volatility Range %) rendered inline via matplotlib base64 embeddings.

## 3. Boundary & Security Verification
- **No Raw Data Leak:** The local 840,241 raw CSV telemetry records remain strictly local and unversioned. The generated HTML embeds only matplotlib plots, metadata metrics, and a 20-row preview, with no full row dumps.
- **Git Tracking:** The output HTML directory `reports/html/` is not targeted by git commits.
- **No Machine Learning/Trading Logic:** Notebook contains no Cell 2, labeling algorithms, predictive features, or execution policies.
