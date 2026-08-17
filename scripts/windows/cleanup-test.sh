#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
stop_destiny=false; [ "${1:-}" = --destiny ] && stop_destiny=true
if "$stop_destiny"; then "$(dirname "$0")/stop-destiny.sh"; else echo 'DESTINY_CLEANUP=SKIPPED (pass --destiny only for a project-started process)'; fi
win_ps "\$roots=@($(ps_quote "${ORACLE_RUNTIME:-}"),$(ps_quote "${EXTERNAL_VALIDATION_RUNTIME:-}"),$(ps_quote "${EXTERNAL_TRACE_RUNTIME:-}")); foreach(\$root in \$roots) { if ([string]::IsNullOrWhiteSpace(\$root)) { continue }; \$state=Join-Path \$root '.lab-control-state\\started-destiny.json'; if (!(Test-Path -LiteralPath \$state -PathType Leaf)) { continue }; try { \$record=Get-Content -LiteralPath \$state -Raw | ConvertFrom-Json; if (\$record.task_name -and \$record.task_name -like 'OldSchoolD2Lab-*') { Unregister-ScheduledTask -TaskName \$record.task_name -Confirm:\$false -ErrorAction SilentlyContinue; Write-Output ('REMOVED_MANAGED_LAUNCH_TASK=' + \$record.task_name) }; Remove-Item -LiteralPath \$state -Force; Write-Output ('REMOVED_MANAGED_LAUNCH_STATE=' + \$root) } catch { Write-Output ('MANAGED_LAUNCH_CLEANUP=FAILED:' + \$root) } }"
names=${LEGION_PROJECT_CLEANUP_PROCESS_NAMES:-}
if [ -z "$names" ]; then echo 'TEMPORARY_PROJECT_PROCESSES=NONE_CONFIGURED'; else
  win_ps "\$names=$(ps_quote "$names").Split(',') | ForEach-Object { \$_.Trim() }; foreach(\$name in \$names) { if ([string]::IsNullOrWhiteSpace(\$name)) {continue}; \$p=@(Get-Process -Name \$name -ErrorAction SilentlyContinue); foreach(\$x in \$p) { Stop-Process -Id \$x.Id -ErrorAction Stop; Write-Output ('STOPPED_PROJECT_PROCESS=' + \$name + ';PID=' + \$x.Id) } }"
fi
echo 'NETWORK_ISOLATION=UNCHANGED'; echo 'CLEANUP_TEST=PASS'
