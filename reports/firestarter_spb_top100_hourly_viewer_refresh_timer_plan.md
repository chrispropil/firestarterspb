# Top 100 Evidence Viewer Hourly Refresh Timer Plan

This document details the deployment plan for scheduling the hourly Evidence Viewer refresh task on Windows.

## 1. Task Scheduler Registration Command

To schedule the task to run automatically every hour, execute the following command in an elevated Command Prompt or PowerShell:

```cmd
schtasks /Create /TN "FirestarterSPB_Top100_EvidenceViewer_HourlyRefresh" /SC HOURLY /MO 1 /TR "powershell.exe -ExecutionPolicy Bypass -File C:\firestarterspb\scripts\automation\refresh_top100_evidence_viewer_hourly.ps1" /F
```

## 2. Manual Invocation Command

To run the refresh script manually at any time to verify operations:

```powershell
powershell.exe -ExecutionPolicy Bypass -File C:\firestarterspb\scripts\automation\refresh_top100_evidence_viewer_hourly.ps1
```

## 3. Unregistration / Task Deletion Command

To delete and remove the scheduled task if needed:

```cmd
schtasks /Delete /TN "FirestarterSPB_Top100_EvidenceViewer_HourlyRefresh" /F
```

## 4. Verification Checkpoints
- Log file will accumulate timestamped records at: `reports/automation/top100_evidence_viewer_refresh.log`
- Rebuilt evidence HTML will be updated at: `reports/html/top100_evidence_viewer/index.html`
