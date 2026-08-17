#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: tail-sunrise-log.sh <runtime> [lines]}; lines=${2:-100}; [[ $lines =~ ^[1-9][0-9]*$ ]] && [ "$lines" -le 500 ] || { echo 'line count must be 1..500' >&2; exit 64; }; runtime=$(require_runtime "$alias")
win_ps "\$path=Join-Path $(ps_quote "$runtime") $(ps_quote "$LEGION_SUNRISE_LOG_RELATIVE"); if (!(Test-Path -LiteralPath \$path -PathType Leaf)) { Write-Error 'SUNRISE_LOG=MISSING'; exit 2 }; Write-Output 'SUNRISE_LOG=BEGIN'; Get-Content -LiteralPath \$path -Tail $lines; Write-Output 'SUNRISE_LOG=END'"
