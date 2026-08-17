#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
win_ps "\$procs=@(Get-CimInstance Win32_Process -Filter \"Name='destiny2.exe'\" -ErrorAction SilentlyContinue); if (\$procs.Count -eq 0) { Write-Output 'STOP_DESTINY=NO_APPROVED_PROCESS_RUNNING'; exit 0 }; foreach(\$p in \$procs) { Stop-Process -Id \$p.ProcessId -ErrorAction Stop; Write-Output ('STOPPED_APPROVED_PROCESS=destiny2.exe;PID=' + \$p.ProcessId) }; Write-Output 'STOP_DESTINY=PASS'"
