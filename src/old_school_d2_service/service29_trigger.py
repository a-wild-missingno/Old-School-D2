"""Payload-free correlation at the client service-29 boundary."""

from __future__ import annotations

from collections.abc import Iterable

# (monotonic tick in milliseconds, event category, task enum or route identifier)
Observation = tuple[int, str, int | None]


def nearest_pre_service29_transition(observations: Iterable[Observation]) -> dict[str, object] | None:
    """Return the nearest completed client task before the first observed service 29.

    This helper accepts sanitized event metadata only.  It deliberately does not parse logs or
    retain packet bodies, account data, endpoint addresses, or retail-log text.
    """
    ordered = list(observations)
    for index, (service_tick, category, _) in enumerate(ordered):
        if category != "service29_received":
            continue
        for transition_tick, transition, task_enum in reversed(ordered[:index]):
            if transition != "task_completed" or task_enum is None:
                continue
            if transition_tick > service_tick:
                return None
            return {
                "event": "service29_transition_correlation",
                "transition": transition,
                "task_enum": task_enum,
                "service29_offset_ms": service_tick - transition_tick,
            }
        return None
    return None
