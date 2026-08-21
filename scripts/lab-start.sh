#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
: "${OLD_SCHOOL_D2_TLS_CERT:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_TLS_KEY:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_MANIFEST_CACHE:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_CONFIG_GUID:?set local runtime configuration in .env}"
export OLD_SCHOOL_D2_LOG_PATH="${OLD_SCHOOL_D2_LOG_PATH:-$ROOT/var/runtime-events.jsonl}"
mkdir -p "$ROOT/var"
if [ -f "$ROOT/var/lab-server.pid" ] && kill -0 "$(cat "$ROOT/var/lab-server.pid")" 2>/dev/null; then echo 'lab listener already running'; exit 1; fi
sudo -n --preserve-env=OLD_SCHOOL_D2_BIND_HOST,OLD_SCHOOL_D2_HTTPS_PORT,OLD_SCHOOL_D2_BAP_PORT,OLD_SCHOOL_D2_MANIFEST_CACHE,OLD_SCHOOL_D2_CONFIG_GUID,OLD_SCHOOL_D2_TLS_CERT,OLD_SCHOOL_D2_TLS_KEY,OLD_SCHOOL_D2_LOG_PATH "$ROOT/.venv/bin/python" -m old_school_d2_service.runtime.app >"$ROOT/var/lab-server.stdout.log" 2>&1 &
echo $! > "$ROOT/var/lab-server.pid"
echo "started HTTPS/BAP listener pid $(cat "$ROOT/var/lab-server.pid")"
