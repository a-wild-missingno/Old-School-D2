from pathlib import Path


def test_loads_runtime_configuration_from_environment_without_private_defaults(monkeypatch, tmp_path: Path) -> None:
    from old_school_d2_service.runtime.config import RuntimeConfig

    monkeypatch.setenv("OLD_SCHOOL_D2_BIND_HOST", "127.0.0.1")
    monkeypatch.setenv("OLD_SCHOOL_D2_HTTPS_PORT", "8443")
    monkeypatch.setenv("OLD_SCHOOL_D2_BAP_PORT", "30974")
    monkeypatch.setenv("OLD_SCHOOL_D2_MANIFEST_CACHE", str(tmp_path / "manifest.cache"))
    monkeypatch.setenv("OLD_SCHOOL_D2_CONFIG_GUID", "00000000-0000-0000-0000-000000000000")
    monkeypatch.setenv("OLD_SCHOOL_D2_TLS_CERT", str(tmp_path / "listener.crt"))
    monkeypatch.setenv("OLD_SCHOOL_D2_TLS_KEY", str(tmp_path / "listener.key"))
    monkeypatch.setenv("OLD_SCHOOL_D2_LOG_PATH", str(tmp_path / "events.jsonl"))

    config = RuntimeConfig.from_environment()

    assert config.bind_host == "127.0.0.1"
    assert config.https_port == 8443
    assert config.bap_port == 30974
    assert config.log_path == tmp_path / "events.jsonl"


def test_constructs_https_and_bap_servers_from_runtime_config(monkeypatch, tmp_path: Path) -> None:
    from old_school_d2_service.runtime.app import build_runtime_servers
    from old_school_d2_service.runtime.config import RuntimeConfig

    config = RuntimeConfig(
        bind_host="127.0.0.1", https_port=0, bap_port=0,
        manifest_cache=tmp_path / "manifest.cache",
        config_guid="00000000-0000-0000-0000-000000000000",
        tls_cert=tmp_path / "listener.crt", tls_key=tmp_path / "listener.key",
        log_path=tmp_path / "events.jsonl",
    )

    https_server, bap_server = build_runtime_servers(config, ssl_context_factory=lambda: None)
    try:
        assert https_server.server_address[1] > 0
        assert bap_server.server_address[1] > 0
    finally:
        https_server.server_close()
        bap_server.server_close()
