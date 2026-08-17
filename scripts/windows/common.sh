#!/usr/bin/env bash
# Shared deterministic transport for the Windows Legion lab. Source; do not execute.
set -euo pipefail
WINDOWS_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(CDPATH= cd -- "$WINDOWS_DIR/../.." && pwd)
WINDOWS_LAB_CONFIG=${WINDOWS_LAB_CONFIG:-"$ROOT/.hermes/windows-lab.local.env"}
if [ -f "$WINDOWS_LAB_CONFIG" ]; then set -a; . "$WINDOWS_LAB_CONFIG"; set +a; fi
: "${LEGION_SSH_HOST:?set LEGION_SSH_HOST in ignored .hermes/windows-lab.local.env}"
: "${LEGION_SSH_USER:?set LEGION_SSH_USER in ignored .hermes/windows-lab.local.env}"
LEGION_SSH_PORT=${LEGION_SSH_PORT:-22}
WINDOWS_LAB_SSH_BIN=${WINDOWS_LAB_SSH_BIN:-ssh}
WINDOWS_LAB_SCP_BIN=${WINDOWS_LAB_SCP_BIN:-scp}
LEGION_DESTINY_EXE_RELATIVE=${LEGION_DESTINY_EXE_RELATIVE:-destiny2.exe}
LEGION_SUNRISE_DLL_RELATIVE=${LEGION_SUNRISE_DLL_RELATIVE:-steam_api64.dll}
LEGION_SETTINGS_RELATIVE=${LEGION_SETTINGS_RELATIVE:-settings.json}
LEGION_MOVEMENT_RELATIVE=${LEGION_MOVEMENT_RELATIVE:-movement.json}
LEGION_SUNRISE_LOG_RELATIVE=${LEGION_SUNRISE_LOG_RELATIVE:-sunrise.log}
ps_quote() { printf "'%s'" "${1//\'/\'\'}"; }
win_target() { printf '%s@%s' "$LEGION_SSH_USER" "$LEGION_SSH_HOST"; }
win_ssh() {
  local -a cmd=("$WINDOWS_LAB_SSH_BIN" -o BatchMode=yes -o LogLevel=ERROR -o ConnectTimeout=15 -p "$LEGION_SSH_PORT")
  [ -n "${LEGION_SSH_KEY:-}" ] && cmd+=(-i "$LEGION_SSH_KEY")
  "${cmd[@]}" "$(win_target)" "$@"
}
win_scp_to() {
  local source=$1 destination=$2
  local -a cmd=("$WINDOWS_LAB_SCP_BIN" -o BatchMode=yes -o LogLevel=ERROR -o ConnectTimeout=20 -P "$LEGION_SSH_PORT")
  [ -n "${LEGION_SSH_KEY:-}" ] && cmd+=(-i "$LEGION_SSH_KEY")
  "${cmd[@]}" "$source" "$(win_target):$destination"
}
win_ps() {
  local script=$1 encoded
  script="\$ProgressPreference='SilentlyContinue'; $script"
  encoded=$(printf '%s' "$script" | iconv -f UTF-8 -t UTF-16LE | base64 -w0)
  win_ssh "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -EncodedCommand $encoded" | tr -d '\r'
}
require_runtime() {
  local alias=${1:-} value=
  case "$alias" in
    oracle) value=${ORACLE_RUNTIME:-} ;;
    external-validation) value=${EXTERNAL_VALIDATION_RUNTIME:-} ;;
    external-trace) value=${EXTERNAL_TRACE_RUNTIME:-} ;;
    *) echo "unknown runtime alias: ${alias:-<empty>} (allowed: oracle, external-validation, external-trace)" >&2; return 64 ;;
  esac
  [ -n "$value" ] || { echo "runtime alias '$alias' is not configured privately" >&2; return 78; }
  printf '%s' "$value"
}
assert_trace_target() {
  local alias=$1
  require_runtime "$alias" >/dev/null
  [ "$alias" != external-validation ] || { echo "protected baseline: deploy-trace refuses external-validation" >&2; return 77; }
  case ",${LEGION_TRACE_DEPLOY_ALLOWED_RUNTIMES:-external-trace,oracle}," in
    *,"$alias",*) ;;
    *) echo "runtime alias '$alias' is not authorized for trace deployment" >&2; return 77 ;;
  esac
}
runtime_file_ps() { printf "Join-Path %s %s" "$(ps_quote "$1")" "$(ps_quote "$2")"; }
