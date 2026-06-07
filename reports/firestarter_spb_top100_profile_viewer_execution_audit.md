# Firestarter SPB: Top 100 Profile Viewer Execution Audit

## Overview
This document records the programmatic validation and local execution check of the Jupyter profile viewer notebook (`notebooks/firestarter_spb_top100_profile_viewer.ipynb`) against the 1-month 5m klines dataset.

## 1. Inventory Summary Audit
- **Total CSV Files Scanned:** 100
- **Total Rows Ingested Across All Files:** 840,241
- **Average Rows per Symbol:** 8402.41 (Expected: ~8,640 for 30 days)
- **Non-Standard Tickers Detected:** 2 (币安人生USDT, 龙虾USDT)
- **Missing Candle Integrity:** Total missing 5m candles across all 100 files is 0.

## 2. Triple Ticker Deep-Dive Profiles
We executed resample, statistic, and plot renders for the three validation targets:

### Ticker Profile: BTCUSDT
- **Row Count (5m):** 8640
- **Total Base Asset Volume:** 4,840,420.7660
- **Average Candle Range (High-Low %):** 0.1600%
- **1-Hour Resampled Rows:** 721
- **4-Hour Resampled Rows:** 181
- **Unicode Encoding Target:** NO
- **Matplotlib Render Check:** PASSED

### Ticker Profile: ETHUSDT
- **Row Count (5m):** 8640
- **Total Base Asset Volume:** 132,014,430.8620
- **Average Candle Range (High-Low %):** 0.2098%
- **1-Hour Resampled Rows:** 721
- **4-Hour Resampled Rows:** 181
- **Unicode Encoding Target:** NO
- **Matplotlib Render Check:** PASSED

### Ticker Profile: 币安人生USDT
- **Row Count (5m):** 8640
- **Total Base Asset Volume:** 3,315,103,861.0000
- **Average Candle Range (High-Low %):** 0.6759%
- **1-Hour Resampled Rows:** 721
- **4-Hour Resampled Rows:** 181
- **Unicode Encoding Target:** YES
- **Matplotlib Render Check:** PASSED

## 3. Jupyter Notebook Structure Validation
- **Local CSV Load Integrity:** Confirm loading is dynamic using the relative configured data path.
- **Embedded Telemetry Prevention:** All output blocks in version control are strictly purged, preventing raw telemetry leakage.
- **Selector Interface:** Variable `SELECTED_SYMBOL` successfully resolved at top of block.
- **Warnings & Gates:** Notebook contains clear headers explicitly noting the local research scope, zero labeling, zero model training, and zero execution policies.

## 4. Boundary Compliance Check
- **No Data Commit:** Verified.
- **No Cell 2 / Labels:** Verified.
- **No Model Training:** Verified.
- **No Trading Logic:** Verified.
