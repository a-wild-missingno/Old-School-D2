"""PostgreSQL storage for sanitized controlled-service experiment events."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
from typing import Any, Callable, Protocol

import psycopg


class Connection(Protocol):
    def cursor(self) -> Any: ...
    def __enter__(self) -> "Connection": ...
    def __exit__(self, *args: object) -> bool: ...


Connect = Callable[[str], Connection]


def _timestamp() -> datetime:
    return datetime.now(UTC)


class PostgresEventStore:
    """Append-only event store that keeps payload hashes instead of raw packet data."""

    def __init__(self, database_url: str, *, connect: Connect = psycopg.connect) -> None:
        if not database_url.strip():
            raise ValueError("database_url must not be blank")
        self.database_url = database_url
        self._connect = connect

    def start_experiment(self, *, label: str) -> int:
        if not label.strip():
            raise ValueError("label must not be blank")
        with self._connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO experiments(label, started_at) VALUES (%s, %s) RETURNING id",
                    (label, _timestamp()),
                )
                row = cursor.fetchone()
        if row is None:
            raise RuntimeError("experiment insert returned no id")
        return int(row[0])

    def record_event(
        self,
        *,
        experiment_id: int,
        transport: str,
        direction: str,
        local_port: int,
        payload: bytes,
        decoded_kind: str | None = None,
    ) -> int:
        if transport not in {"udp", "tcp", "https"}:
            raise ValueError("unsupported transport")
        if direction not in {"inbound", "outbound"}:
            raise ValueError("unsupported direction")
        if not 1 <= local_port <= 65535:
            raise ValueError("local_port must be between 1 and 65535")
        digest = hashlib.sha256(payload).hexdigest()
        with self._connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO events(
                        experiment_id, occurred_at, transport, direction, local_port,
                        payload_size, payload_sha256, decoded_kind
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """,
                    (experiment_id, _timestamp(), transport, direction, local_port, len(payload), digest, decoded_kind),
                )
                row = cursor.fetchone()
        if row is None:
            raise RuntimeError("event insert returned no id")
        return int(row[0])
