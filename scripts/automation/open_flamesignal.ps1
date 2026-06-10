# FlameSignal Launcher Script
# Opens the pulled_143_evidence_viewer index.html in the default web browser.

$ErrorActionPreference = "Stop"

# Define the repository root and target HTML path
$repoRoot = "C:\firestarterspb"
$targetHtml = Join-Path $repoRoot "reports\html\pulled_143_evidence_viewer\index.html"

# Verify file existence
if (-not (Test-Path $targetHtml)) {
    Write-Error "Error: FlameSignal Evidence Viewer HTML file not found at '$targetHtml'."
    exit 1
}

# Launch default browser with target HTML
try {
    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Launching FlameSignal Evidence Viewer at '$targetHtml'..."
    Start-Process $targetHtml
} catch {
    Write-Error "Failed to open HTML file: $_"
    exit 1
}
