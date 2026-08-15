"""Narrow BAP bootstrap helpers for the isolated lab listener."""

from __future__ import annotations

import struct


_OUTER_HEADER = struct.Struct(">BBI")
_REQUEST_HEADER = struct.Struct(">HI")
_RESPONSE_HEADER = struct.Struct(">HIH")
_MAGIC = 1
_PLAINTEXT_TYPES = frozenset((0, 2))
_START_REQUEST_SERVICE = 30
_START_RESPONSE_SERVICE = 31
_STATUS_OK = 200


def build_start_response(frame: bytes) -> bytes | None:
    """Return the source-documented plaintext service-31 reply for one service-30 frame.

    No other service is interpreted or answered.  In particular, this helper deliberately does
    not claim to implement SignOn-token validation, service-25, encryption, or later BAP routes.
    """
    if len(frame) < _OUTER_HEADER.size:
        return None
    magic, frame_type, payload_size = _OUTER_HEADER.unpack_from(frame)
    if magic != _MAGIC or frame_type not in _PLAINTEXT_TYPES or len(frame) != _OUTER_HEADER.size + payload_size:
        return None
    payload = frame[_OUTER_HEADER.size :]
    if len(payload) < _REQUEST_HEADER.size:
        return None
    service, task_id = _REQUEST_HEADER.unpack_from(payload)
    if service != _START_REQUEST_SERVICE:
        return None
    response_payload = _RESPONSE_HEADER.pack(_START_RESPONSE_SERVICE, task_id, _STATUS_OK) + payload[_REQUEST_HEADER.size :]
    return _OUTER_HEADER.pack(_MAGIC, frame_type, len(response_payload)) + response_payload
