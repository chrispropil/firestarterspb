# Hourly Top 100 Evidence Viewer Refresh Script
$ErrorActionPreference = "Stop"

try {
    # 1. cd C:\firestarterspb
    Set-Location "C:\firestarterspb"

    # 2. Run Python script
    $logMsg = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting hourly rebuild..."
    Write-Output $logMsg
    
    # Ensure reports/automation directory exists
    New-Item -ItemType Directory -Force -Path "C:\firestarterspb\reports\automation" | Out-Null
    
    # Append start event to log file
    $logMsg | Out-File -FilePath "C:\firestarterspb\reports\automation\top100_evidence_viewer_refresh.log" -Append -Encoding utf8

    # Execute build script
    & py scripts/visualization/build_top100_evidence_viewer.py 2>&1 | Out-String -OutVariable buildOutput

    if ($LASTEXITCODE -ne 0) {
        throw "Python build script failed with exit code $LASTEXITCODE. Output: $buildOutput"
    }

    # 3. Write timestamped log
    $successMsg = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Rebuild completed successfully."
    Write-Output $successMsg
    $successMsg | Out-File -FilePath "C:\firestarterspb\reports\automation\top100_evidence_viewer_refresh.log" -Append -Encoding utf8

} catch {
    # 4. Fail closed on error
    $errMsg = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] ERROR: $_"
    Write-Error $errMsg
    $errMsg | Out-File -FilePath "C:\firestarterspb\reports\automation\top100_evidence_viewer_refresh.log" -Append -Encoding utf8
    exit 1
}
