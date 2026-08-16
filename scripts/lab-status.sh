#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
printf 'Git commit: '; git -C "$ROOT" rev-parse --short HEAD
if [ -f "$ROOT/var/lab-server.pid" ] && kill -0 "$(cat "$ROOT/var/lab-server.pid")" 2>/dev/null; then echo "HTTPS/BAP listener: running (pid $(cat "$ROOT/var/lab-server.pid"))"; else echo 'HTTPS/BAP listener: stopped'; fi
printf 'Configured ports: HTTPS=%s BAP=%s discovery=%s
' "${OLD_SCHOOL_D2_HTTPS_PORT:-<unset>}" "${OLD_SCHOOL_D2_BAP_PORT:-<unset>}" "${OLD_SCHOOL_D2_DISCOVERY_PORTS:-<managed separately>}"
printf 'Listener sockets:
'; ss -lntup 2>/dev/null | grep -E "${OLD_SCHOOL_D2_HTTPS_PORT:-^$}|${OLD_SCHOOL_D2_BAP_PORT:-^$}" || true
printf 'Capture: '; [ -f "$ROOT/var/capture.pid" ] && kill -0 "$(cat "$ROOT/var/capture.pid")" 2>/dev/null && echo running || echo stopped
