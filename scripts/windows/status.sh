#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
printf 'WINDOWS_SSH='
if win_ps "Write-Output 'ok'" >/dev/null 2>/dev/null; then echo PASS; else echo FAIL; exit 1; fi
win_ps "\
\$procs=@(Get-CimInstance Win32_Process -Filter \"Name='destiny2.exe'\" -ErrorAction SilentlyContinue);\
if (\$procs.Count -eq 0) { Write-Output 'DESTINY_RUNNING=false'; Write-Output 'DESTINY_PIDS=NONE'; Write-Output 'RUNTIME=unknown' } else { Write-Output 'DESTINY_RUNNING=true'; Write-Output ('DESTINY_PIDS=' + ((\$procs | ForEach-Object { \$_.ProcessId }) -join ',')); foreach(\$p in \$procs) { \$runtime='unknown'; \$path=(\$p.ExecutablePath.Replace([char]92,[char]47)); \$oracle=($(ps_quote "${ORACLE_RUNTIME:-__unconfigured__}").Replace([char]92,[char]47)); \$validation=($(ps_quote "${EXTERNAL_VALIDATION_RUNTIME:-__unconfigured__}").Replace([char]92,[char]47)); \$trace=($(ps_quote "${EXTERNAL_TRACE_RUNTIME:-__unconfigured__}").Replace([char]92,[char]47)); if (\$path) { if (\$path.StartsWith(\$oracle,[StringComparison]::OrdinalIgnoreCase)) {\$runtime='oracle'} elseif (\$path.StartsWith(\$validation,[StringComparison]::OrdinalIgnoreCase)) {\$runtime='external-validation'} elseif (\$path.StartsWith(\$trace,[StringComparison]::OrdinalIgnoreCase)) {\$runtime='external-trace'} }; Write-Output ('RUNTIME=' + \$runtime); Write-Output ('DESTINY_PROCESS=pid:' + \$p.ProcessId + ';runtime:' + \$runtime + ';path:' + \$path) } };\
Write-Output 'RELEVANT_WINDOWS_PROCESSES=destiny2.exe';\
\$ports=$(ps_quote "${LEGION_RELEVANT_PORTS:-}"); if ([string]::IsNullOrWhiteSpace(\$ports)) { Write-Output 'RELEVANT_LISTENERS=NONE_CONFIGURED' } else { \$wanted=\$ports.Split(',') | ForEach-Object {[int]\$_.Trim()}; \$found=Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { \$wanted -contains \$_.LocalPort } | ForEach-Object { \$_.LocalAddress + ':' + \$_.LocalPort + ':pid=' + \$_.OwningProcess }; Write-Output ('RELEVANT_LISTENERS=' + (\$(if(\$found){\$found -join ','}else{'NONE'})) ) };\
"
printf 'INTERACTIVE_CONTROL_VERIFIED=NO\nUI_STATE=unknown\n'
