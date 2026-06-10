# Firestarter Viewer Refresh Pipeline Diagnostic

Date: 2026-06-10T12:45:35-04:00  
Status: **DIAGNOSTIC_COMPLETE**

---

## 1. Active Viewer Entrypoint
- **Path:** [pulled_143_evidence_viewer/index.html](file:///C:/firestarterspb/reports/html/pulled_143_evidence_viewer/index.html)
- **Description:** This is the current active dashboard. It processes and visualizes all 143 symbols from the inventory.

---

## 2. Stale Old Viewer Path
- **Path:** `reports/html/top100_evidence_viewer/index.html`
- **Description:** This output directory is no longer updated by the build script as of commit `a68280da`. It remains in the tree with stale content from `2026-06-10 09:49:10 AM`.
- **Other Stale Paths:**
  - `reports/html/core88_evidence_viewer/index.html`
  - `reports/html/top100_dashboard/index.html`

---

## 3. Data Freshness Issue
- **Findings:** The source CSV datasets inside the folders `data/research/binance_top100_excluding_existing_5_1month` and `data/research/binance_core88_missing_1month` have not been updated since **`2026-06-09 07:33:15`** (over 29 hours ago).
- **Result:** Although the hourly scheduled task runs and successfully regenerates the HTML viewer pages, the charts do not advance or show new metrics because the underlying source data is static.

---

## 4. Rebuild Commands

### Rebuilding the Viewer
To manually rebuild the active viewer index file, run:
```powershell
py scripts/visualization/build_top100_evidence_viewer.py
```

### Refreshing the Source Data
To query and update the public Binance derivatives datasets (which will pull fresh funding rates, open interest, and long/short account metrics), run:
```powershell
# 1. Update top 100 derivatives context
py scripts/binance_spb/pull_binance_top100_derivatives_context.py --approved-live-pull

# 2. Update missing core 88 derivatives context
py scripts/binance_spb/pull_core88_missing_derivatives_context.py --approved-live-pull
```
*(Note: Ensure corresponding OHLCV data pullers are run if candle data also needs backfilling).*

---

## 5. Scheduled Task Check
The scheduled task `FirestarterSPB_Top100_EvidenceViewer_HourlyRefresh` is properly configured and active. It executes `powershell.exe -ExecutionPolicy Bypass -File C:\firestarterspb\scripts\automation\refresh_top100_evidence_viewer_hourly.ps1`, which successfully builds `reports/html/pulled_143_evidence_viewer/index.html` using the `py` launcher. No modifications to the scheduled task are required.
