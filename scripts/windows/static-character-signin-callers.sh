#!/usr/bin/env bash
# Read-only static direct-call scan for the source-defined character-signin entry target.
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: static-character-signin-callers.sh <runtime>}
runtime=$(require_runtime "$alias")
[ "$alias" = external-validation ] || true
local_script="$(dirname "$0")/character-signin-callers.ps1"
remote_script="C:/Users/${LEGION_SSH_USER}/AppData/Local/Temp/old-school-d2-character-signin-callers.ps1"
cleanup() { win_ps "Remove-Item -LiteralPath $(ps_quote "$remote_script") -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1 || true; }
trap cleanup EXIT
win_scp_to "$local_script" "$remote_script"
win_ps "\$exe=Join-Path $(ps_quote "$runtime") $(ps_quote "$LEGION_DESTINY_EXE_RELATIVE"); & $(ps_quote "$remote_script") -Exe \$exe"
