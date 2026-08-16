from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    path = Path(__file__).parents[1] / "tools" / "analyze_bap_transition.py"
    spec = importlib.util.spec_from_file_location("analyze_bap_transition", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reports_absent_post_bap_transition_without_sensitive_fields() -> None:
    module = _load_module()
    events = [
        {"timestamp": "2026-08-15T21:46:13+00:00", "event": "signon_session_issued"},
        {"timestamp": "2026-08-15T21:46:18+00:00", "event": "bap_start_replied", "service": 30, "response_service": 31, "task_id": 0, "status": 200, "peer": "192.0.2.20"},
        {"timestamp": "2026-08-15T21:46:18+00:00", "event": "bap_server_hello_replied", "service": 25, "response_service": 26, "task_id": 1, "status": 200},
        {"timestamp": "2026-08-15T21:46:18+00:00", "event": "bap_register_subscriber_replied", "service": 121, "response_service": 122, "task_id": 2, "status": 200},
        {"timestamp": "2026-08-15T21:46:23+00:00", "event": "bap_echo_replied", "service": 250, "response_service": 251, "task_id": 6, "status": 200},
    ]

    summary = module.summarize(events)

    assert summary == {
        "outcome": "post_bap_transition_absent",
        "services": [30, 25, 121, 250],
        "responses": [31, 26, 122, 251],
        "non_keepalive_services": [30, 25, 121],
        "event_count": 5,
    }
    assert "peer" not in repr(summary)


def test_summarize_between_excludes_other_launches() -> None:
    module = _load_module()
    events = [
        {"timestamp": "2026-08-15T20:00:00+00:00", "event": "bap_echo_replied", "service": 250, "response_service": 251},
        {"timestamp": "2026-08-15T21:46:13+00:00", "event": "bap_start_replied", "service": 30, "response_service": 31},
        {"timestamp": "2026-08-15T21:46:18+00:00", "event": "bap_server_hello_replied", "service": 25, "response_service": 26},
        {"timestamp": "2026-08-15T22:00:00+00:00", "event": "bap_echo_replied", "service": 250, "response_service": 251},
    ]

    summary = module.summarize_between(events, "2026-08-15T21:46:00+00:00", "2026-08-15T21:47:00+00:00")

    assert summary["services"] == [30, 25]
    assert summary["event_count"] == 2
