"""Evidence-backed Sunrise entitlement policy for the isolated lab."""

from __future__ import annotations

# Derived from the configured Sunrise `server.entitlements` policy supplied for the lab:
# indices 0 and 1 use manifest handles; index 2 is explicitly unowned; later entries use
# their numeric application identifiers.
SUNRISE_DEFAULT_OWNED_ENTITLEMENT_IDS: tuple[int, ...] = (
    0xE0200001,
    0xE0200002,
    1090090,
    1090091,
    1090092,
    1090093,
    1090094,
    1090095,
    1090096,
    1090150,
    1090151,
    1090152,
    1090170,
    1090171,
    1090200,
    1090201,
    1090202,
    1330040,
)
