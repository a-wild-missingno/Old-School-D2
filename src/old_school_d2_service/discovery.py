"""Narrow UDP discovery behavior observed in Sunrise external-server experiments."""

from __future__ import annotations

import ipaddress
import struct
from typing import Final

_NAT_PROBE_MAGIC: Final = 1
_NAT_PROBE_INDICES: Final = {1, 2}
_ADDRESS_MASK: Final = 0x76C3F6BC
_PORT_MASK: Final = 0xF6BC


def build_nat_probe_reply(payload: bytes, peer: tuple[str, int]) -> bytes | None:
    """Return a reply for a recognized NatProbe request, otherwise ``None``."""
    if len(payload) != 4:
        return None
    magic, index = struct.unpack(">HH", payload)
    if magic != _NAT_PROBE_MAGIC or index not in _NAT_PROBE_INDICES:
        return None
    address = int(ipaddress.IPv4Address(peer[0]))
    port = peer[1]
    if not 0 <= port <= 65535:
        return None
    return payload + struct.pack(">IH", address ^ _ADDRESS_MASK, port ^ _PORT_MASK) + (b"\x00" * 6)
