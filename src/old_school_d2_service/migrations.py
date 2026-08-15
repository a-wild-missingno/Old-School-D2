"""Small, ordered PostgreSQL migration runner for the local service."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Protocol

import psycopg


class Connection(Protocol):
    def cursor(self) -> Any: ...
    def __enter__(self) -> "Connection": ...
    def __exit__(self, *args: object) -> bool: ...


Connect = Callable[[str], Connection]


def apply_migrations(
    database_url: str, *, migration_dir: Path = Path("db/migrations"), connect: Connect = psycopg.connect
) -> list[str]:
    """Apply each unrecorded ``*.sql`` file in lexical order exactly once."""
    files = sorted(migration_dir.glob("*.sql"))
    with connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    filename TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute("SELECT filename FROM schema_migrations")
            applied = {row[0] for row in cursor.fetchall()}
            applied_now: list[str] = []
            for file in files:
                if file.name in applied:
                    continue
                cursor.execute(file.read_text())
                cursor.execute("INSERT INTO schema_migrations(filename) VALUES (%s)", (file.name,))
                applied_now.append(file.name)
    return applied_now
