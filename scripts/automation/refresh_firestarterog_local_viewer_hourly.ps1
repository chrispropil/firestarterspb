# Hourly FirestarterOG Local Viewer Refresh Script
$ErrorActionPreference = "Stop"

try {
    $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    $repoRoot = (Resolve-Path (Join-Path $scriptRoot "..\..")).Path
    Set-Location $repoRoot

    $logDir = Join-Path $repoRoot "logs\og_viewer"
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    $logFile = Join-Path $logDir "firestarterog_local_viewer_hourly_update.log"
    $srcOut = Join-Path $logDir "firestarterog_source_refresh_stdout.log"
    $srcErr = Join-Path $logDir "firestarterog_source_refresh_stderr.log"
    $buildOut = Join-Path $logDir "firestarterog_viewer_build_stdout.log"
    $buildErr = Join-Path $logDir "firestarterog_viewer_build_stderr.log"

    function Write-LogLine {
        param([string]$Message)
        $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
        Write-Output $line
        $line | Out-File -FilePath $logFile -Append -Encoding utf8
    }

    function Append-FileIfExists {
        param([string]$Path)
        if (Test-Path $Path) {
            Get-Content $Path | Out-File -FilePath $logFile -Append -Encoding utf8
            Remove-Item $Path -Force -ErrorAction SilentlyContinue
        }
    }

    $sourceRefreshOk = $true
    Write-LogLine 'Starting FirestarterOG local viewer hourly refresh...'

    $pythonExe = 'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (-not (Test-Path $pythonExe)) {
        throw "Bundled runtime Python was not found at '$pythonExe'."
    }
    Write-LogLine 'NOTE: using bundled runtime Python.'

    Write-LogLine 'Refreshing true OG source sample data from local repository files only...'
    $srcProc = Start-Process -FilePath $pythonExe -ArgumentList 'scripts/generate_historical_variance_from_local.py' -WorkingDirectory $repoRoot -NoNewWindow -PassThru -Wait -RedirectStandardOutput $srcOut -RedirectStandardError $srcErr
    Append-FileIfExists $srcOut
    Append-FileIfExists $srcErr
    if ($srcProc.ExitCode -ne 0) {
        $sourceRefreshOk = $false
        Write-LogLine "HOLD_TRUE_OG_SOURCE_REFRESH_LOCAL_REFRESH_FAILED: source refresh failed with exit code $($srcProc.ExitCode). Viewer rebuild will be treated as stale-display only if it succeeds."
    } else {
        Write-LogLine 'Source sample refresh completed from local files.'
    }

    Write-LogLine 'Rebuilding true OG local viewer HTML...'
    $buildProc = Start-Process -FilePath $pythonExe -ArgumentList 'scripts/firestarterog_binance_1m_local_viewer.py' -WorkingDirectory $repoRoot -NoNewWindow -PassThru -Wait -RedirectStandardOutput $buildOut -RedirectStandardError $buildErr
    Append-FileIfExists $buildOut
    Append-FileIfExists $buildErr
    if ($buildProc.ExitCode -ne 0) {
        throw "FirestarterOG local viewer build failed with exit code $($buildProc.ExitCode)."
    }

    if (-not $sourceRefreshOk) {
        Write-LogLine 'FirestarterOG local viewer rebuilt, but source data remained stale or unavailable.'
        exit 1
    }

    Write-LogLine 'FirestarterOG local viewer rebuild completed successfully.'
} catch {
    $errMsg = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] ERROR: $_"
    Write-Error $errMsg
    $errMsg | Out-File -FilePath $logFile -Append -Encoding utf8
    exit 1
}
