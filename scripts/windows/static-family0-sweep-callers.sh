#!/usr/bin/env bash
# User-authorized, read-only aggregate static caller scan for the family-zero sweep.
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: static-family0-sweep-callers.sh <runtime>}
runtime=$(require_runtime "$alias")
local_script="$(dirname "$0")/family0-sweep-callers.ps1"
remote_script="C:/Users/${LEGION_SSH_USER}/AppData/Local/Temp/old-school-d2-family0-sweep-callers.ps1"
cleanup() { win_ps "Remove-Item -LiteralPath $(ps_quote "$remote_script") -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1 || true; }
trap cleanup EXIT
win_scp_to "$local_script" "$remote_script"
win_ps "\$exe=Join-Path $(ps_quote "$runtime") $(ps_quote "$LEGION_DESTINY_EXE_RELATIVE"); & $(ps_quote "$remote_script") -Exe \$exe"
