#!/usr/bin/env bash
# Verify only the public identity relationship; never print cache/config values.
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
: "${OLD_SCHOOL_D2_MANIFEST_CACHE:?set local runtime configuration in .env}"
: "${OLD_SCHOOL_D2_CONFIG_GUID:?set local runtime configuration in .env}"

"$ROOT/.venv/bin/python" - <<'PY'
from pathlib import Path
from old_school_d2_service.content_config import derive_content_manifest_guid, parse_content_manifest_cache
import os

rows = parse_content_manifest_cache(Path(os.environ["OLD_SCHOOL_D2_MANIFEST_CACHE"]).read_bytes())
config_guid = os.environ["OLD_SCHOOL_D2_CONFIG_GUID"]
if derive_content_manifest_guid(rows) != config_guid:
    raise SystemExit("CONTENTCONFIG_IDENTITY=FAIL")
print("CONTENTCONFIG_IDENTITY=PASS")
PY
