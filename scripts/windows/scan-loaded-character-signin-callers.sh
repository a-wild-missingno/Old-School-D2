#!/usr/bin/env bash
# User-authorized read-only loaded-main-module scan; does not write process memory.
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: scan-loaded-character-signin-callers.sh <runtime>}
require_runtime "$alias" >/dev/null
pid=$(win_ps "\$p=Get-CimInstance Win32_Process -Filter \"Name='destiny2.exe'\" -ErrorAction SilentlyContinue | Select-Object -First 1; if(\$null -eq \$p){throw 'DESTINY_RUNNING=NO'}; Write-Output \$p.ProcessId")
local_script="$(dirname "$0")/character-signin-loaded-module.ps1"
remote_script="C:/Users/${LEGION_SSH_USER}/AppData/Local/Temp/old-school-d2-character-signin-loaded-module.ps1"
cleanup() { win_ps "Remove-Item -LiteralPath $(ps_quote "$remote_script") -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1 || true; }
trap cleanup EXIT
win_scp_to "$local_script" "$remote_script"
win_ps "& $(ps_quote "$remote_script") -TargetProcessId $pid"
