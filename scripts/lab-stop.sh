#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PID_FILE="$ROOT/var/lab-server.pid"
if [ -f "$PID_FILE" ]; then
  pid=$(cat "$PID_FILE")
  if kill -0 "$pid" 2>/dev/null; then kill "$pid"; echo "stopped HTTPS/BAP listener pid $pid"; fi
  rm -f "$PID_FILE"
else echo 'no HTTPS/BAP pid file'; fi
