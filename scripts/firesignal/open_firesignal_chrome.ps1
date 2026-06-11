# open_firesignal_chrome.ps1
# Set working directory to project root
Set-Location -Path "C:\firestarterspb"

$port = 8765
$url = "http://127.0.0.1:$port/index.html"

# 1. Check if port is already in use
$portOpen = $false
try {
    $tcp = New-Object System.Net.Sockets.TcpClient
    $tcp.Connect("127.0.0.1", $port)
    $portOpen = $true
    $tcp.Close()
} catch {
    $portOpen = $false
}

if (-not $portOpen) {
    Write-Output "Local viewer server is not running. Starting server on port $port..."
    Start-Process -FilePath "py" -ArgumentList "scripts\firesignal\serve_firesignal_viewer.py" -WorkingDirectory "C:\firestarterspb" -WindowStyle Hidden
    # Wait briefly for server readiness
    Start-Sleep -Seconds 2
} else {
    Write-Output "Local viewer server is already running on port $port. Reusing existing server."
}

# 2. Chrome Path Detection
$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

$chromeLaunched = $false
foreach ($p in $chromePaths) {
    if (Test-Path $p) {
        Write-Output "Chrome detected at $p. Launching viewer..."
        Start-Process -FilePath $p -ArgumentList $url
        $chromeLaunched = $true
        break
    }
}

if (-not $chromeLaunched) {
    Write-Output "[NOTICE] Google Chrome was not found at the expected paths. Falling back to default browser."
    Start-Process $url
}

# 3. Create Desktop Shortcut if missing
$desktopFolder = [System.Environment]::GetFolderPath("Desktop")
if ($desktopFolder) {
    $shortcutPath = Join-Path $desktopFolder "FireSignal Viewer.lnk"
    if (-not (Test-Path $shortcutPath)) {
        try {
            $wshell = New-Object -ComObject Wscript.Shell
            $shortcut = $wshell.CreateShortcut($shortcutPath)
            $shortcut.TargetPath = "C:\firestarterspb\scripts\firesignal\open_firesignal_chrome.bat"
            $shortcut.WorkingDirectory = "C:\firestarterspb"
            $shortcut.Description = "Launch FireSignal Viewer in Google Chrome"
            $icoPath = "C:\firestarterspb\reports\html\pulled_143_evidence_viewer\firesignal.ico"
            if (Test-Path $icoPath) {
                $shortcut.IconLocation = "$icoPath,0"
            }
            $shortcut.Save()
            Write-Output "Created Desktop Shortcut: FireSignal Viewer.lnk"
        } catch {
            Write-Output "Warning: Could not create Desktop Shortcut: $_"
        }
    }
}
