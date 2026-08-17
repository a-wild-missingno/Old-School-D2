from __future__ import annotations


def test_reports_first_pre_service_10_internal_only_no_reply_route() -> None:
    from old_school_d2_service.authenticated_route_ledger import first_divergence

    internal = [
        (30, 31),
        (25, 26),
        (121, 122),
        (302, 303),
        (304, 305),
        (302, 303),
        (29, None),
        (29, None),
        (29, None),
        (29, None),
        (29, None),
        (250, 251),
        (10, 11),
    ]
    external = [
        (30, 31),
        (25, 26),
        (121, 122),
        (302, 303),
        (304, 305),
        (302, 303),
        (250, 251),
    ]

    divergence = first_divergence(internal, external, stop_before_service=10)

    assert divergence == {
        "shared_prefix": [
            (30, 31),
            (25, 26),
            (121, 122),
            (302, 303),
            (304, 305),
            (302, 303),
        ],
        "internal_next": (29, None),
        "external_next": (250, 251),
        "internal_index": 6,
        "external_index": 6,
    }
