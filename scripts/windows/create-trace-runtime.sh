#!/usr/bin/env bash
# Create a fresh dedicated trace copy without changing the protected external-validation source.
set -euo pipefail
source "$(dirname "$0")/common.sh"
source_alias=${1:?usage: create-trace-runtime.sh external-validation external-trace}
target_alias=${2:?usage: create-trace-runtime.sh external-validation external-trace}
[ "$source_alias" = external-validation ] || {
  echo 'trace source must be protected external-validation' >&2
  exit 64
}
[ "$target_alias" = external-trace ] || {
  echo 'trace target must be dedicated external-trace' >&2
  exit 64
}
assert_trace_target "$target_alias"
source_runtime=$(require_runtime "$source_alias")
target_runtime=$(require_runtime "$target_alias")
[ "$source_runtime" != "$target_runtime" ] || {
  echo 'trace source and target runtime paths must differ' >&2
  exit 64
}
result=$(win_ps "\$source=$(ps_quote "$source_runtime"); \$target=$(ps_quote "$target_runtime"); \$dll=Join-Path \$source $(ps_quote "$LEGION_SUNRISE_DLL_RELATIVE"); \$settings=Join-Path \$source $(ps_quote "$LEGION_SETTINGS_RELATIVE"); if (!(Test-Path -LiteralPath \$source -PathType Container)) { Write-Error 'TRACE_SOURCE_RUNTIME=MISSING'; exit 2 }; if (Test-Path -LiteralPath \$target) { Write-Error 'TRACE_TARGET_RUNTIME=EXISTS'; exit 3 }; if (!(Test-Path -LiteralPath \$dll -PathType Leaf) -or !(Test-Path -LiteralPath \$settings -PathType Leaf)) { Write-Error 'TRACE_SOURCE_RUNTIME=INCOMPLETE'; exit 4 }; \$destiny=@(Get-CimInstance Win32_Process -Filter "Name='destiny2.exe'" -ErrorAction SilentlyContinue); if (\$destiny.Count -ne 0) { Write-Error 'DESTINY_RUNNING=YES'; exit 5 }; \$sourceDllHash=(Get-FileHash -Algorithm SHA256 -LiteralPath \$dll).Hash.ToLower(); \$sourceSettingsHash=(Get-FileHash -Algorithm SHA256 -LiteralPath \$settings).Hash.ToLower(); Copy-Item -LiteralPath \$source -Destination \$target -Recurse -ErrorAction Stop; Remove-Item -LiteralPath (Join-Path \$target '.lab-control-state') -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -LiteralPath (Join-Path \$target '.lab-control-backups') -Recurse -Force -ErrorAction SilentlyContinue; \$targetDll=Join-Path \$target $(ps_quote "$LEGION_SUNRISE_DLL_RELATIVE"); \$targetSettings=Join-Path \$target $(ps_quote "$LEGION_SETTINGS_RELATIVE"); \$targetDllHash=(Get-FileHash -Algorithm SHA256 -LiteralPath \$targetDll).Hash.ToLower(); \$targetSettingsHash=(Get-FileHash -Algorithm SHA256 -LiteralPath \$targetSettings).Hash.ToLower(); if (\$targetDllHash -ne \$sourceDllHash -or \$targetSettingsHash -ne \$sourceSettingsHash) { Remove-Item -LiteralPath \$target -Recurse -Force -ErrorAction SilentlyContinue; Write-Error 'TRACE_COPY_HASH_MISMATCH'; exit 6 }; Write-Output 'CREATE_TRACE_RUNTIME=PASS'; Write-Output ('SOURCE_DLL_SHA256=' + \$sourceDllHash); Write-Output ('SOURCE_SETTINGS_SHA256=' + \$sourceSettingsHash); Write-Output ('TARGET_DLL_SHA256=' + \$targetDllHash); Write-Output ('TARGET_SETTINGS_SHA256=' + \$targetSettingsHash)")
printf '%s\n' "$result"
