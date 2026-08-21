#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
: "${OLD_SCHOOL_D2_CAPTURE_COMMAND:?set a reviewed local capture command in ignored .env}"
mkdir -p "$ROOT/var"
nohup sh -c "$OLD_SCHOOL_D2_CAPTURE_COMMAND" >"$ROOT/var/capture.stdout.log" 2>&1 < /dev/null & echo $! > "$ROOT/var/capture.pid"
echo "started capture pid $(cat "$ROOT/var/capture.pid")"
