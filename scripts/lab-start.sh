#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
: "${OLD_SCHOOL_D2_TLS_CERT:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_TLS_KEY:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_MANIFEST_CACHE:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_CONFIG_GUID:?set local runtime configuration in .env}"
export OLD_SCHOOL_D2_LOG_PATH="${OLD_SCHOOL_D2_LOG_PATH:-$ROOT/var/runtime-events.jsonl}"
DISCOVERY_PORTS=${OLD_SCHOOL_D2_DISCOVERY_PORTS:-"3074 3075"}
DISCOVERY_ENV_FILE=${OLD_SCHOOL_D2_DISCOVERY_ENV_FILE:-/etc/old-school-d2/discovery.env}
mkdir -p "$ROOT/var"

if [ -f "$ROOT/var/lab-server.pid" ] && kill -0 "$(cat "$ROOT/var/lab-server.pid")" 2>/dev/null; then
  echo 'lab listener already running' >&2
  exit 1
fi
for port in $DISCOVERY_PORTS; do
  case "$port" in (*[!0-9]*|'') echo "invalid discovery port: $port" >&2; exit 64;; esac
  if [ -f "$ROOT/var/lab-discovery-$port.pid" ] && kill -0 "$(cat "$ROOT/var/lab-discovery-$port.pid")" 2>/dev/null; then
    echo "discovery listener already running on port $port" >&2
    exit 1
  fi
done

cleanup_started() {
  "$ROOT/scripts/lab-stop.sh" >/dev/null 2>&1 || true
}
trap cleanup_started ERR

sudo -n --preserve-env=OLD_SCHOOL_D2_BIND_HOST,OLD_SCHOOL_D2_HTTPS_PORT,OLD_SCHOOL_D2_BAP_PORT,OLD_SCHOOL_D2_MANIFEST_CACHE,OLD_SCHOOL_D2_CONFIG_GUID,OLD_SCHOOL_D2_TLS_CERT,OLD_SCHOOL_D2_TLS_KEY,OLD_SCHOOL_D2_LOG_PATH "$ROOT/.venv/bin/python" -m old_school_d2_service.runtime.app >"$ROOT/var/lab-server.stdout.log" 2>&1 &
echo $! > "$ROOT/var/lab-server.pid"

for port in $DISCOVERY_PORTS; do
  sudo -n bash -c 'set -a; . "$1"; set +a; exec "$2" -m old_school_d2_service --host "$3" --port "$4" --label "lab-discovery-$4"' bash "$DISCOVERY_ENV_FILE" "$ROOT/.venv/bin/python" "${OLD_SCHOOL_D2_BIND_HOST:?set OLD_SCHOOL_D2_BIND_HOST in .env}" "$port" >"$ROOT/var/lab-discovery-$port.stdout.log" 2>&1 &
  echo $! > "$ROOT/var/lab-discovery-$port.pid"
done

sleep 1
kill -0 "$(cat "$ROOT/var/lab-server.pid")"
for port in $DISCOVERY_PORTS; do
  kill -0 "$(cat "$ROOT/var/lab-discovery-$port.pid")"
  ss -lnu "sport = :$port" | grep -q ":$port" || { echo "discovery socket missing on port $port" >&2; exit 1; }
done
trap - ERR
echo "started HTTPS/BAP listener pid $(cat "$ROOT/var/lab-server.pid")"
echo "started UDP discovery listeners on ports $DISCOVERY_PORTS"
