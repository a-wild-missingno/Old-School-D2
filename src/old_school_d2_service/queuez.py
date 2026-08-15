"""Minimal clean-room Queuez family-update encoder for the isolated lab."""

from __future__ import annotations

from dataclasses import dataclass
import struct


@dataclass(frozen=True)
class QueuezObject:
    """A future Queuez object operation; object bodies are not encoded yet."""

    object_id: int
    version: int
    encoding: int
    payload: bytes


@dataclass(frozen=True)
class QueuezFamily:
    """One versioned Queuez family update."""

    type: int
    root_soid: int
    version: int
    flags: int
    objects: tuple[QueuezObject, ...]


def encode_queuez_update(families: tuple[QueuezFamily, ...]) -> bytes:
    """Encode one or more evidence-backed Queuez family updates.

    Header fields are network byte order. Raw object payloads retain their required native
    little-endian version prefix; payload bytes are otherwise copied unchanged.
    """
    if not families:
        raise ValueError("at least one family is required")
    encoded = bytearray(struct.pack(">I", len(families)))
    for family in families:
        encoded.extend(
            struct.pack(
                ">IQiBI",
                family.type,
                family.root_soid,
                family.version,
                family.flags,
                len(family.objects),
            )
        )
        for object_ in family.objects:
            if object_.encoding not in (1, 2, 3, 4):
                raise ValueError("Queuez object encoding is unsupported")
            if object_.encoding == 3 and (
                len(object_.payload) < 8
                or struct.unpack("<Q", object_.payload[:8])[0] != object_.version
            ):
                raise ValueError("raw Queuez object payload version does not match its header")
            encoded.extend(
                struct.pack(
                    ">IQII",
                    object_.object_id,
                    object_.version,
                    len(object_.payload),
                    object_.encoding,
                )
            )
            encoded.extend(object_.payload)
    return bytes(encoded)
