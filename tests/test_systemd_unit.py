from pathlib import Path


def test_discovery_systemd_template_uses_secret_environment_file() -> None:
    unit = Path("deploy/systemd/old-school-d2-discovery@.service").read_text()

    assert "EnvironmentFile=/etc/old-school-d2/discovery.env" in unit
    assert "--port %i" in unit
    assert "OLD_SCHOOL_D2_BIND_HOST" in unit
    assert "Restart=on-failure" in unit
    assert "postgresql.service" in unit
    assert "OLD_SCHOOL_D2_BIND_HOST" in Path(".env.example").read_text()
