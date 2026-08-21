#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
DISCOVERY_PORTS=${OLD_SCHOOL_D2_DISCOVERY_PORTS:-"3074 3075"}
printf 'Git commit: '; git -C "$ROOT" rev-parse --short HEAD
if [ -f "$ROOT/var/lab-server.pid" ] && kill -0 "$(cat "$ROOT/var/lab-server.pid")" 2>/dev/null; then echo "HTTPS/BAP listener: running (pid $(cat "$ROOT/var/lab-server.pid"))"; else echo 'HTTPS/BAP listener: stopped'; fi
for port in $DISCOVERY_PORTS; do
  if [ -f "$ROOT/var/lab-discovery-$port.pid" ] && kill -0 "$(cat "$ROOT/var/lab-discovery-$port.pid")" 2>/dev/null; then echo "UDP discovery $port: running (pid $(cat "$ROOT/var/lab-discovery-$port.pid"))"; else echo "UDP discovery $port: stopped"; fi
done
printf 'Configured ports: HTTPS=%s BAP=%s discovery=%s
' "${OLD_SCHOOL_D2_HTTPS_PORT:-<unset>}" "${OLD_SCHOOL_D2_BAP_PORT:-<unset>}" "$DISCOVERY_PORTS"
printf 'Listener sockets:
'; ss -lntup 2>/dev/null | grep -E "${OLD_SCHOOL_D2_HTTPS_PORT:-^$}|${OLD_SCHOOL_D2_BAP_PORT:-^$}|$(printf '%s|' $DISCOVERY_PORTS | sed 's/|$//')" || true
printf 'Capture: '; [ -f "$ROOT/var/capture.pid" ] && kill -0 "$(cat "$ROOT/var/capture.pid")" 2>/dev/null && echo running || echo stopped
