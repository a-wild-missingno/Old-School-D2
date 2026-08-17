from __future__ import annotations


def test_reports_nearest_client_transition_before_first_service29() -> None:
    from old_school_d2_service.service29_trigger import nearest_pre_service29_transition

    observations = [
        (274771328, "task_started", 0),
        (274771328, "task_started", 1),
        (274771453, "route_reply", 303),
        (274771468, "task_completed", 0),
        (274771484, "service29_received", None),
        (274771500, "service29_received", None),
    ]

    correlation = nearest_pre_service29_transition(observations)

    assert correlation == {
        "event": "service29_transition_correlation",
        "transition": "task_completed",
        "task_enum": 0,
        "service29_offset_ms": 16,
    }
    assert "payload" not in repr(correlation)
    assert "identity" not in repr(correlation)


def test_requires_a_completed_client_task_before_service29() -> None:
    from old_school_d2_service.service29_trigger import nearest_pre_service29_transition

    assert nearest_pre_service29_transition([(100, "route_reply", 303), (116, "service29_received", None)]) is None
