' run_firesignal_hidden.vbs
Set shell = CreateObject("WScript.Shell")
' Run the PowerShell script hidden (0 = hide window, True = wait for completion)
powershellCmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\firestarterspb\scripts\firesignal\run_firesignal_silent.ps1"""
exitCode = shell.Run(powershellCmd, 0, True)
WScript.Quit(exitCode)
