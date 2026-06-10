# Firestarter Dual Viewer Refresh Plan & Validation

Date: 2026-06-10T13:19:09-04:00  
Status: **VERIFIED_DUAL_VIEWER_WORKFLOW**

---

## 1. Dual-Viewer Architecture
To accommodate the parallel usage of both `viewerog` (the legacy Top 100 viewer) and `viewer143` (the inventory expanded 143-symbol viewer) without cross-contamination, we have established a dual-build workflow:
- **viewerog:** Built via `scripts/visualization/build_top100_evidence_viewer_og.py` and outputted to `reports/html/top100_evidence_viewer/index.html`.
- **viewer143:** Built via `scripts/visualization/build_top100_evidence_viewer.py` and outputted to `reports/html/pulled_143_evidence_viewer/index.html`.

Both scripts read from the same source folders under `data/research/` and run completely independently.

---

## 2. Files Created/Modified
- **Created:**
  - `scripts/visualization/build_top100_evidence_viewer_og.py` (Restored `viewerog` builder logic)
  - `scripts/automation/refresh_dual_evidence_viewers.ps1` (PowerShell wrapper that executes both scripts sequentially)
  - `reports/firestarterlive/dual_viewer_refresh_plan_and_validation.md` (This document)
- **Modified:**
  - `reports/html/VIEWER_ACTIVE_PATH.md` (Updated notice document listing both viewer HTML file entrypoints)

---

## 3. Verification Commands
To build the HTML pages and verify the refresh pipeline:
```powershell
# 1. Run the restored viewerog builder
py scripts/visualization/build_top100_evidence_viewer_og.py

# 2. Run the viewer143 builder
py scripts/visualization/build_top100_evidence_viewer.py

# 3. Test execution of the dual-refresh wrapper script
powershell -ExecutionPolicy Bypass -File scripts/automation/refresh_dual_evidence_viewers.ps1
```

---

## 4. Safety & Governance Checklist
- **No data pulls run?** PASS. No API fetching or data downloading was triggered.
- **No modifications to raw market data?** PASS. CSV files under `data/` remain untouched.
- **No deletions of old viewer folders?** PASS. Stale output folders are preserved.
- **No deprecated markers on viewerog?** PASS. `viewerog` is treated as a fully active parallel entrypoint.
- **No modifications to FirestarterLive alert scripts/configs?** PASS. Alert layer configuration and watcher scripts are untouched.
- **No task scheduler changes?** PASS. Scheduled task remains unmodified.
