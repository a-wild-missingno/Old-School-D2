import subprocess
import sys


def test_module_exposes_discovery_service_command() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "old_school_d2_service", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--port" in result.stdout
    assert "--database-url" in result.stdout
    assert "--migrate" in result.stdout
