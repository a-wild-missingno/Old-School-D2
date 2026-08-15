"""Minimal, clean-room SignOn success response for the external lab service."""

from __future__ import annotations

from dataclasses import dataclass

import ipaddress
import secrets
import time
from collections.abc import Callable


@dataclass(frozen=True)
class SignOnSession:
    """Ephemeral material shared only by the HTTPS and BAP handlers for one lab run."""

    encryption_key: bytes
    authentication_key: bytes
    session_token: bytes



def _varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("protobuf varints must be non-negative")
    encoded = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        encoded.append(byte | (0x80 if value else 0))
        if not value:
            return bytes(encoded)


def _field_varint(number: int, value: int) -> bytes:
    return _varint(number << 3) + _varint(value)


def _field_bytes(number: int, value: bytes) -> bytes:
    return _varint((number << 3) | 2) + _varint(len(value)) + value


def build_signon_response_with_session(
    *,
    relay_host: str,
    relay_port: int,
    owned_entitlement_ids: tuple[int, ...] = (),
    now_seconds: int | None = None,
    random_bytes: Callable[[int], bytes] = secrets.token_bytes,
) -> tuple[bytes, SignOnSession]:
    """Build a SignOn response and retain its ephemeral material for the local BAP handler."""
    if not 1 <= relay_port <= 65535:
        raise ValueError("relay_port must be between 1 and 65535")
    relay_address = int(ipaddress.IPv4Address(relay_host))
    now = int(time.time()) if now_seconds is None else now_seconds
    encryption_key = random_bytes(16)
    authentication_key = random_bytes(16)
    session_token = random_bytes(32)
    if (len(encryption_key), len(authentication_key), len(session_token)) != (16, 16, 32):
        raise ValueError("random_bytes returned an unexpected length")

    extended = _field_varint(1, 1) + _field_bytes(3, b"\x11" * 16) + _field_bytes(4, b"\x22" * 16)
    if any(not 0 <= identifier <= 0xFFFFFFFF for identifier in owned_entitlement_ids):
        raise ValueError("owned entitlement identifiers must be unsigned 32-bit values")
    ownership = b"".join(_field_varint(1, identifier) for identifier in owned_entitlement_ids)
    host = str(ipaddress.IPv4Address(relay_address))
    success = b"".join((
        _field_bytes(1, b"\x00" * 16),
        _field_bytes(2, encryption_key),
        _field_bytes(3, authentication_key),
        _field_bytes(4, session_token),
        _field_varint(5, now + 3600),
        _field_varint(6, relay_address),
        _field_varint(7, relay_port),
        _field_bytes(12, extended),
        _field_bytes(14, f"http://{host}/cfg_a/".encode()),
        _field_bytes(15, f"http://{host}/cfg_b/".encode()),
        _field_bytes(16, f"http://{host}/cfg_c/".encode()),
    ))
    common_info = _field_varint(1, 1) + _field_varint(2, 1)
    response = b"".join((
        _field_varint(1, 0),
        _field_bytes(2, success),
        _field_bytes(4, common_info),
        _field_varint(5, 1),
        _field_bytes(6, b"d2legacy"),
        _field_varint(8, 0),
        _field_bytes(10, ownership),
        _field_varint(12, now),
        _field_bytes(13, b"live"),
        _field_varint(14, relay_address),
    ))
    return response, SignOnSession(encryption_key, authentication_key, session_token)


def build_signon_response(
    *,
    relay_host: str,
    relay_port: int,
    owned_entitlement_ids: tuple[int, ...] = (),
    now_seconds: int | None = None,
    random_bytes: Callable[[int], bytes] = secrets.token_bytes,
) -> bytes:
    """Build the response body for callers that do not own the following BAP connection."""
    response, _ = build_signon_response_with_session(
        relay_host=relay_host,
        relay_port=relay_port,
        owned_entitlement_ids=owned_entitlement_ids,
        now_seconds=now_seconds,
        random_bytes=random_bytes,
    )
    return response
