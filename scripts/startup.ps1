# AI Chief of Staff — Windows Startup Script
# Launches claude-mem worker + Claude Code in D:\ChiefStaff

# Clean stale claude-mem pid file (prevents worker from refusing to start)
$pidFile = Join-Path $env:USERPROFILE '.claude-mem\worker.pid'
if (Test-Path $pidFile) {
    Remove-Item $pidFile -Force
}

# Start claude-mem worker (hidden background process)
$env:CLAUDE_MEM_WORKER_PORT = '37777'
$bunExe = Join-Path $env:USERPROFILE '.bun\bin\bun.exe'
$workerScript = Join-Path $env:USERPROFILE '.claude\plugins\marketplaces\thedotmack\plugin\scripts\worker-wrapper.cjs'
$workerDir = Join-Path $env:USERPROFILE '.claude\plugins\marketplaces\thedotmack'

if (Test-Path $bunExe) {
    Start-Process -FilePath $bunExe -ArgumentList $workerScript -WorkingDirectory $workerDir -WindowStyle Hidden
    Start-Sleep -Seconds 5
}

# Launch Claude Code in a new PowerShell window
$claudeExe = Join-Path $env:USERPROFILE '.local\bin\claude.exe'
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'D:\ChiefStaff'; & '$claudeExe' --dangerously-skip-permissions"
