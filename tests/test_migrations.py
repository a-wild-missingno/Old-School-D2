from pathlib import Path

from old_school_d2_service.migrations import apply_migrations


class FakeCursor:
    def __init__(self) -> None:
        self.queries: list[tuple[str, tuple[object, ...] | None]] = []

    def execute(self, query: str, parameters: tuple[object, ...] | None = None) -> None:
        self.queries.append((query, parameters))

    def fetchall(self):
        return []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_instance = FakeCursor()

    def cursor(self):
        return self.cursor_instance

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def test_applies_unrecorded_sql_migration(tmp_path: Path) -> None:
    migration_dir = tmp_path / "migrations"
    migration_dir.mkdir()
    (migration_dir / "001_initial.sql").write_text("CREATE TABLE example (id INTEGER);")
    connection = FakeConnection()

    applied = apply_migrations("postgresql://unused", migration_dir=migration_dir, connect=lambda _: connection)

    assert applied == ["001_initial.sql"]
    sql = [query for query, _ in connection.cursor_instance.queries]
    assert any("CREATE TABLE IF NOT EXISTS schema_migrations" in query for query in sql)
    assert "CREATE TABLE example (id INTEGER);" in sql
    assert any(parameters == ("001_initial.sql",) for _, parameters in connection.cursor_instance.queries)
