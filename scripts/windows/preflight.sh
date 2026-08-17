#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
alias=${1:?usage: preflight.sh <runtime>}; runtime=$(require_runtime "$alias")
printf 'WINDOWS_SSH='; if win_ps "Write-Output 'ok'" >/dev/null 2>/dev/null; then echo PASS; else echo FAIL; exit 1; fi
echo "RUNTIME=$alias"
checks=$(win_ps "\$root=$(ps_quote "$runtime"); \$exe=Join-Path \$root $(ps_quote "$LEGION_DESTINY_EXE_RELATIVE"); Write-Output ('RUNTIME_EXISTS=' + \$(if(Test-Path -LiteralPath \$root -PathType Container){'PASS'}else{'FAIL'})); Write-Output ('DESTINY_EXECUTABLE=' + \$(if(Test-Path -LiteralPath \$exe -PathType Leaf){'PASS'}else{'FAIL'})); \$p=@(Get-CimInstance Win32_Process -Filter \"Name='destiny2.exe'\" -ErrorAction SilentlyContinue); Write-Output ('DESTINY_RUNNING=' + \$(if(\$p.Count -gt 0){'YES'}else{'NO'})); \$ports=$(ps_quote "${LEGION_RELEVANT_PORTS:-}"); if ([string]::IsNullOrWhiteSpace(\$ports)) { Write-Output 'CONFLICTING_LISTENERS=NONE' } else { \$wanted=\$ports.Split(',') | ForEach-Object {[int]\$_.Trim()}; \$found=Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { \$wanted -contains \$_.LocalPort } | ForEach-Object { \$_.LocalAddress + ':' + \$_.LocalPort + ':pid=' + \$_.OwningProcess }; Write-Output ('CONFLICTING_LISTENERS=' + (\$(if(\$found){\$found -join ','}else{'NONE'})) ) }")
printf '%s\n' "$checks"
hashes=$("$(dirname "$0")/hash-runtime.sh" "$alias" 2>&1 || true)
printf '%s\n' "$hashes" | awk '!/^RUNTIME=/{print}'
dll_hash=$(printf '%s\n' "$hashes" | awk -F'[=;]' '/FILE=.*steam_api64|FILE=.*dll/{print $NF; exit}')
settings_hash=$(printf '%s\n' "$hashes" | awk -F'[=;]' '/FILE=.*settings/{print $NF; exit}')
printf 'DLL_SHA256=%s\nSETTINGS_SHA256=%s\n' "${dll_hash:-MISSING}" "${settings_hash:-MISSING}"
isolation=$("$(dirname "$0")/verify-isolation.sh" 2>&1 || true)
printf '%s\n' "$isolation" | awk -F= '/^(IPV4_FORWARDING|IPV6_FORWARDING|ISOLATION)=/{print; if($1=="ISOLATION") print "INTERNET_ISOLATION=" $2}'
echo 'INTERACTIVE_CONTROL_VERIFIED=NO'
if grep -qx 'RUNTIME_EXISTS=PASS' <<<"$checks" && grep -qx 'DESTINY_EXECUTABLE=PASS' <<<"$checks" && grep -qx 'DESTINY_RUNNING=NO' <<<"$checks" && grep -qx 'CONFLICTING_LISTENERS=NONE' <<<"$checks" && grep -qx 'ISOLATION=PASS' <<<"$isolation" && [ -n "${dll_hash:-}" ] && [ "$dll_hash" != MISSING ] && [ -n "${settings_hash:-}" ] && [ "$settings_hash" != MISSING ]; then
  echo 'READY_FOR_PROCESS_LAUNCH=YES'
else
  echo 'READY_FOR_PROCESS_LAUNCH=NO'
fi
echo 'READY_FOR_AUTOMATED_UI_TEST=NO'
