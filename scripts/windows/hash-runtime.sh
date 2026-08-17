#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: hash-runtime.sh <oracle|external-validation|external-trace>}; runtime=$(require_runtime "$alias")
win_ps "\$root=$(ps_quote "$runtime"); if (!(Test-Path -LiteralPath \$root -PathType Container)) { Write-Error 'runtime missing'; exit 2 }; Write-Output 'RUNTIME=$(printf '%s' "$alias")'; foreach(\$rel in @($(ps_quote "$LEGION_SUNRISE_DLL_RELATIVE"),$(ps_quote "$LEGION_SETTINGS_RELATIVE"),$(ps_quote "$LEGION_MOVEMENT_RELATIVE"))) { if ([string]::IsNullOrWhiteSpace(\$rel)) { continue }; \$path=Join-Path \$root \$rel; if (Test-Path -LiteralPath \$path -PathType Leaf) { Write-Output ('FILE=' + \$rel + ';SHA256=' + (Get-FileHash -Algorithm SHA256 -LiteralPath \$path).Hash.ToLower()) } else { Write-Output ('FILE=' + \$rel + ';SHA256=MISSING') } }"
