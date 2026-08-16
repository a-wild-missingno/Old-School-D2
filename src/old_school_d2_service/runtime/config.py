"""Runtime-only configuration for the isolated replacement listener."""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class RuntimeConfig:
    bind_host: str
    https_port: int
    bap_port: int
    manifest_cache: Path
    config_guid: str
    tls_cert: Path
    tls_key: Path
    log_path: Path

    @classmethod
    def from_environment(cls) -> "RuntimeConfig":
        required = {
            "manifest_cache": "OLD_SCHOOL_D2_MANIFEST_CACHE",
            "config_guid": "OLD_SCHOOL_D2_CONFIG_GUID",
            "tls_cert": "OLD_SCHOOL_D2_TLS_CERT",
            "tls_key": "OLD_SCHOOL_D2_TLS_KEY",
            "log_path": "OLD_SCHOOL_D2_LOG_PATH",
        }
        values = {name: os.environ.get(env) for name, env in required.items()}
        missing = [env for name, env in required.items() if not values[name]]
        if missing:
            raise ValueError("Missing required runtime configuration: " + ", ".join(missing))
        https_port = int(os.environ.get("OLD_SCHOOL_D2_HTTPS_PORT", "443"))
        bap_port = int(os.environ.get("OLD_SCHOOL_D2_BAP_PORT", "30974"))
        if not all(1 <= port <= 65535 for port in (https_port, bap_port)):
            raise ValueError("runtime ports must be between 1 and 65535")
        return cls(
            bind_host=os.environ.get("OLD_SCHOOL_D2_BIND_HOST", "127.0.0.1"),
            https_port=https_port,
            bap_port=bap_port,
            manifest_cache=Path(str(values["manifest_cache"])),
            config_guid=str(values["config_guid"]),
            tls_cert=Path(str(values["tls_cert"])),
            tls_key=Path(str(values["tls_key"])),
            log_path=Path(str(values["log_path"])),
        )
