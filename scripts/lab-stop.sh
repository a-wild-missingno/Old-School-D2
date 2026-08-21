#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
DISCOVERY_PORTS=${OLD_SCHOOL_D2_DISCOVERY_PORTS:-"3074 3075"}
for port in $DISCOVERY_PORTS; do
  pid_file="$ROOT/var/lab-discovery-$port.pid"
  if [ -f "$pid_file" ]; then
    pid=$(cat "$pid_file")
    if kill -0 "$pid" 2>/dev/null; then kill "$pid"; echo "stopped UDP discovery listener port $port pid $pid"; fi
    rm -f "$pid_file"
  else echo "no UDP discovery pid file for port $port"; fi
done
PID_FILE="$ROOT/var/lab-server.pid"
if [ -f "$PID_FILE" ]; then
  pid=$(cat "$PID_FILE")
  if kill -0 "$pid" 2>/dev/null; then kill "$pid"; echo "stopped HTTPS/BAP listener pid $pid"; fi
  rm -f "$PID_FILE"
else echo 'no HTTPS/BAP pid file'; fi
