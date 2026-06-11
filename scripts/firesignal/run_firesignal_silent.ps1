# run_firesignal_silent.ps1
$workingDir = "C:\firestarterspb"
$logDir = "$workingDir\logs\firesignal"
$logFile = "$logDir\firesignal_scheduled_update.log"

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
}

$timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
"--- Update started at $timestamp ---" | Out-File -FilePath $logFile -Append -Encoding utf8

Set-Location $workingDir
try {
    # Run python update script via cmd.exe to merge stdout and stderr cleanly
    $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c py scripts\firesignal\run_firesignal_once.py >> logs\firesignal\firesignal_scheduled_update.log 2>&1" -NoNewWindow -PassThru -Wait
    
    $exitCode = $process.ExitCode
    $endTimestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    "--- Update finished at $endTimestamp with exit code $exitCode ---" | Out-File -FilePath $logFile -Append -Encoding utf8
    exit $exitCode
} catch {
    $errTimestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    "--- Update failed at $errTimestamp with error: $_ ---" | Out-File -FilePath $logFile -Append -Encoding utf8
    exit 1
}
