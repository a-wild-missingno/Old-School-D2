"""Sanitized comparison helpers for authenticated BAP route ledgers."""

from __future__ import annotations

from collections.abc import Iterable

Route = tuple[int, int | None]


def _before_service(routes: Iterable[Route], service: int) -> list[Route]:
    result: list[Route] = []
    for route in routes:
        if route[0] == service:
            break
        result.append(route)
    return result


def first_divergence(
    internal: Iterable[Route], external: Iterable[Route], *, stop_before_service: int
) -> dict[str, object] | None:
    """Return the first ordered route difference before a named internal boundary.

    Ledgers contain service/response identifiers only.  A ``None`` response means that the
    observed route was accepted without a correlated reply; payloads, identities, and timing are
    intentionally outside this diagnostic.
    """
    internal_routes = _before_service(internal, stop_before_service)
    external_routes = _before_service(external, stop_before_service)
    shared = 0
    while (
        shared < len(internal_routes)
        and shared < len(external_routes)
        and internal_routes[shared] == external_routes[shared]
    ):
        shared += 1
    if shared == len(internal_routes) and shared == len(external_routes):
        return None
    return {
        "shared_prefix": internal_routes[:shared],
        "internal_next": internal_routes[shared] if shared < len(internal_routes) else None,
        "external_next": external_routes[shared] if shared < len(external_routes) else None,
        "internal_index": shared,
        "external_index": shared,
    }
