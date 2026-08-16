from __future__ import annotations


def test_post_bap_probe_marks_authenticated_certificate_boundary_without_payload_data() -> None:
    from old_school_d2_service.post_bap_probe import build_post_bap_probe

    probe = build_post_bap_probe(
        authenticated=True,
        service=304,
        response_service=305,
        outbound_notification_sent=False,
    )

    assert probe == {
        "event": "post_bap_wait",
        "authenticated": True,
        "certificate_reply_sent": True,
        "outbound_notification_sent": False,
        "candidate_client_service": 12,
    }
    assert "body" not in repr(probe)
    assert "token" not in repr(probe)


def test_post_bap_probe_rejects_non_certificate_boundary() -> None:
    from old_school_d2_service.post_bap_probe import build_post_bap_probe

    assert (
        build_post_bap_probe(
            authenticated=True,
            service=302,
            response_service=303,
            outbound_notification_sent=False,
        )
        is None
    )
