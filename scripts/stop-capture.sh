#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd); PID_FILE="$ROOT/var/capture.pid"
[ -f "$PID_FILE" ] || { echo 'no capture pid file'; exit 0; }
pid=$(cat "$PID_FILE"); kill -0 "$pid" 2>/dev/null && kill "$pid" || true; rm -f "$PID_FILE"; echo "stopped capture pid $pid"
