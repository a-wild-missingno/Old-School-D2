#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
stop_destiny=false; [ "${1:-}" = --destiny ] && stop_destiny=true
if "$stop_destiny"; then "$(dirname "$0")/stop-destiny.sh"; else echo 'DESTINY_CLEANUP=SKIPPED (pass --destiny only for a project-started process)'; fi
names=${LEGION_PROJECT_CLEANUP_PROCESS_NAMES:-}
if [ -z "$names" ]; then echo 'TEMPORARY_PROJECT_PROCESSES=NONE_CONFIGURED'; else
  win_ps "\$names=$(ps_quote "$names").Split(',') | ForEach-Object { \$_.Trim() }; foreach(\$name in \$names) { if ([string]::IsNullOrWhiteSpace(\$name)) {continue}; \$p=@(Get-Process -Name \$name -ErrorAction SilentlyContinue); foreach(\$x in \$p) { Stop-Process -Id \$x.Id -ErrorAction Stop; Write-Output ('STOPPED_PROJECT_PROCESS=' + \$name + ';PID=' + \$x.Id) } }"
fi
echo 'NETWORK_ISOLATION=UNCHANGED'; echo 'CLEANUP_TEST=PASS'
