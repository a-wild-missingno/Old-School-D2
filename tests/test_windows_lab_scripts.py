"""Offline contract tests for the Windows lab-control shell interface."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = ROOT / "scripts" / "windows"


def run_script(script: str, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(WINDOWS / script), *args], cwd=ROOT,
        env={**os.environ, **env}, text=True, capture_output=True, check=False,
    )


def test_shell_scripts_have_valid_bash_syntax() -> None:
    scripts = sorted(WINDOWS.glob("*.sh"))
    assert scripts, "Windows lab-control scripts must exist"
    for script in scripts:
        result = subprocess.run(["bash", "-n", str(script)], text=True, capture_output=True, check=False)
        assert result.returncode == 0, f"{script}: {result.stderr}"


def test_runtime_aliases_are_private_config_only_and_unknown_aliases_fail(tmp_path: Path) -> None:
    config = tmp_path / "windows-lab.local.env"
    config.write_text("\n".join([
        "LEGION_SSH_HOST=lab-host", "LEGION_SSH_USER=lab-user",
        "ORACLE_RUNTIME=C:/lab/oracle", "EXTERNAL_VALIDATION_RUNTIME=C:/lab/external-validation",
        "EXTERNAL_TRACE_RUNTIME=C:/lab/external-trace", "LEGION_DESTINY_EXE_RELATIVE=destiny2.exe",
    ]) + "\n")
    result = run_script("hash-runtime.sh", "not-a-runtime", env={
        "WINDOWS_LAB_CONFIG": str(config), "WINDOWS_LAB_SSH_BIN": "/bin/false"})
    assert result.returncode != 0
    assert "unknown runtime alias" in result.stderr.lower()


def test_trace_deploy_refuses_protected_external_validation_before_remote_work(tmp_path: Path) -> None:
    config = tmp_path / "windows-lab.local.env"
    config.write_text("\n".join([
        "LEGION_SSH_HOST=lab-host", "LEGION_SSH_USER=lab-user",
        "ORACLE_RUNTIME=C:/lab/oracle", "EXTERNAL_VALIDATION_RUNTIME=C:/lab/external-validation",
        "EXTERNAL_TRACE_RUNTIME=C:/lab/external-trace", "LEGION_DESTINY_EXE_RELATIVE=destiny2.exe",
    ]) + "\n")
    artifact = tmp_path / "trace.dll"
    artifact.write_bytes(b"prepared-test-artifact")
    result = run_script("deploy-trace.sh", "external-validation", str(artifact), env={
        "WINDOWS_LAB_CONFIG": str(config), "WINDOWS_LAB_SSH_BIN": "/bin/false"})
    assert result.returncode != 0
    assert "protected baseline" in result.stderr.lower()


def test_status_keeps_process_and_interactive_desktop_claims_separate(tmp_path: Path) -> None:
    config = tmp_path / "windows-lab.local.env"
    config.write_text("\n".join([
        "LEGION_SSH_HOST=lab-host", "LEGION_SSH_USER=lab-user",
        "ORACLE_RUNTIME=C:/lab/oracle", "EXTERNAL_VALIDATION_RUNTIME=C:/lab/external-validation",
        "EXTERNAL_TRACE_RUNTIME=C:/lab/external-trace", "LEGION_DESTINY_EXE_RELATIVE=destiny2.exe",
    ]) + "\n")
    mock_ssh = tmp_path / "mock-ssh"
    mock_ssh.write_text("#!/usr/bin/env bash\nprintf 'DESTINY_RUNNING=false\\nDESTINY_PIDS=NONE\\nRELEVANT_WINDOWS_PROCESSES=destiny2.exe\\nRELEVANT_LISTENERS=NONE_CONFIGURED\\n\\n'\n")
    mock_ssh.chmod(0o755)
    result = run_script("status.sh", env={
        "WINDOWS_LAB_CONFIG": str(config), "WINDOWS_LAB_SSH_BIN": str(mock_ssh)})
    assert result.returncode == 0, result.stderr
    assert "WINDOWS_SSH=PASS" in result.stdout
    assert "DESTINY_RUNNING=" in result.stdout
    assert "INTERACTIVE_CONTROL_VERIFIED=NO" in result.stdout
    assert "UI_STATE=unknown" in result.stdout


def test_start_destiny_targets_the_actual_interactive_windows_session() -> None:
    script = (WINDOWS / "start-destiny.sh").read_text()
    assert "-LogonType Interactive " in script
    assert "GetOwner" in script
    assert "Register-ScheduledTask" in script
    assert "LAUNCH_CONTEXT=interactive-task" in script


def test_status_normalizes_windows_path_separators_for_runtime_inference() -> None:
    script = (WINDOWS / "status.sh").read_text()
    assert "Replace([char]92,[char]47)" in script


def test_cleanup_removes_only_managed_interactive_launch_tasks() -> None:
    script = (WINDOWS / "cleanup-test.sh").read_text()
    assert "OldSchoolD2Lab-" in script
    assert "Unregister-ScheduledTask" in script


def test_screenshot_capture_uses_the_interactive_windows_session_and_retrieves_png() -> None:
    script = (WINDOWS / "screenshot.sh").read_text()
    common = (WINDOWS / "common.sh").read_text()
    assert "GetOwner" in script
    assert "-LogonType Interactive" in script
    assert "CopyFromScreen" in script
    assert "SCREENSHOT_CAPTURE=PASS" in script
    assert "win_scp_from" in script
    assert "win_scp_from" in common


def test_scp_download_normalizes_windows_paths_for_openssh() -> None:
    common = (WINDOWS / "common.sh").read_text()
    assert 'source=${source//' + chr(92) * 2 + '//}' in common


def test_trace_runtime_creation_is_copy_only_and_rejects_any_non_dedicated_alias() -> None:
    script = (WINDOWS / "create-trace-runtime.sh").read_text()
    assert 'source_alias" = external-validation' in script
    assert 'target_alias" = external-trace' in script
    assert 'TRACE_TARGET_RUNTIME=EXISTS' in script
    assert r'Copy-Item -LiteralPath \$source -Destination \$target -Recurse' in script
    assert 'Get-FileHash -Algorithm SHA256' in script
    assert 'DESTINY_RUNNING=YES' in script


def test_lab_start_uses_noninteractive_privilege_for_default_https_port() -> None:
    script = (ROOT / "scripts" / "lab-start.sh").read_text()
    assert 'sudo -n --preserve-env=OLD_SCHOOL_D2_BIND_HOST' in script
    assert 'OLD_SCHOOL_D2_LOG_PATH' in script


def test_capture_start_detaches_the_reviewed_local_command() -> None:
    script = (ROOT / "scripts" / "start-capture.sh").read_text()
    assert 'nohup sh -c "$OLD_SCHOOL_D2_CAPTURE_COMMAND"' in script
    assert '< /dev/null' in script
