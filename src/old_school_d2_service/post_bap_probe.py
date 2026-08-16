"""Redacted metadata for the post-auth Queuez-subscription diagnostic."""

from __future__ import annotations


def build_post_bap_probe(
    *,
    authenticated: bool,
    service: int,
    response_service: int,
    outbound_notification_sent: bool,
) -> dict[str, object] | None:
    """Describe only the documented 304->305 boundary without retaining payload data."""
    if not authenticated or service != 304 or response_service != 305:
        return None
    return {
        "event": "post_bap_wait",
        "authenticated": True,
        "certificate_reply_sent": True,
        "outbound_notification_sent": outbound_notification_sent,
        "candidate_client_service": 12,
    }
