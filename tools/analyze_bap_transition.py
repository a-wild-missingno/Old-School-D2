#!/usr/bin/env python3
"""Reduce metadata-only listener events into a post-BAP transition summary."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

_BOOTSTRAP_AND_KEEPALIVE = frozenset((25, 30, 121, 302, 304, 250))


def summarize(events: Iterable[Mapping[str, Any]]) -> dict[str, object]:
    """Return a redacted transition summary without retaining input values."""
    services: list[int] = []
    responses: list[int] = []
    event_count = 0
    for event in events:
        event_count += 1
        service = event.get("service")
        response = event.get("response_service")
        if isinstance(service, int):
            services.append(service)
        if isinstance(response, int):
            responses.append(response)
    non_keepalive_services = [service for service in services if service != 250]
    later_services = [service for service in services if service not in _BOOTSTRAP_AND_KEEPALIVE]
    return {
        "outcome": "post_bap_transition_observed" if later_services else "post_bap_transition_absent",
        "services": services,
        "responses": responses,
        "non_keepalive_services": non_keepalive_services,
        "event_count": event_count,
    }


def summarize_between(
    events: Iterable[Mapping[str, Any]], start_utc: str, end_utc: str
) -> dict[str, object]:
    """Summarize events in one inclusive ISO-8601 UTC interval."""
    if start_utc > end_utc:
        raise ValueError("start timestamp must not be after end timestamp")
    selected: list[Mapping[str, Any]] = []
    for event in events:
        timestamp = event.get("timestamp")
        if not isinstance(timestamp, str):
            continue
        if start_utc <= timestamp <= end_utc:
            selected.append(event)
    return summarize(selected)


def _events_from_jsonl(path: Path) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        parsed = json.loads(line)
        if not isinstance(parsed, dict):
            raise ValueError("listener log record must be an object")
        events.append(parsed)
    return events


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize redacted BAP transition metadata")
    parser.add_argument("log", type=Path)
    parser.add_argument("--start-utc")
    parser.add_argument("--end-utc")
    args = parser.parse_args()
    events = _events_from_jsonl(args.log)
    if (args.start_utc is None) != (args.end_utc is None):
        parser.error("--start-utc and --end-utc must be supplied together")
    summary = summarize(events) if args.start_utc is None else summarize_between(events, args.start_utc, args.end_utc)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
