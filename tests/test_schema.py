from pathlib import Path


def test_initial_postgres_migration_defines_research_event_schema() -> None:
    migration = Path("db/migrations/001_initial.sql").read_text().lower()

    assert "create table experiments" in migration
    assert "create table events" in migration
    assert "payload_sha256" in migration
    assert "create index events_experiment_id" in migration
    assert "transport in ('udp', 'tcp', 'https')" in migration
    assert "direction in ('inbound', 'outbound')" in migration
    assert "sqlite" not in migration
