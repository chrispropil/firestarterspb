# Dual Evidence Viewer Refresh Script
$ErrorActionPreference = "Stop"

try {
    # 1. Set Location to repository root
    Set-Location "C:\firestarterspb"

    # 2. Run viewerog builder
    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting Rebuild of ViewerOG (Top 100)..."
    & py scripts/visualization/build_top100_evidence_viewer_og.py 2>&1 | Out-String -OutVariable ogOutput
    if ($LASTEXITCODE -ne 0) {
        throw "ViewerOG build failed. Output: $ogOutput"
    }
    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] ViewerOG built successfully."

    # 3. Run viewer143 builder
    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting Rebuild of Viewer143 (Pulled 143)..."
    & py scripts/visualization/build_top100_evidence_viewer.py 2>&1 | Out-String -OutVariable v143Output
    if ($LASTEXITCODE -ne 0) {
        throw "Viewer143 build failed. Output: $v143Output"
    }
    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Viewer143 built successfully."

    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Dual-viewer rebuild completed successfully."
} catch {
    Write-Error "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] ERROR: $_"
    exit 1
}
