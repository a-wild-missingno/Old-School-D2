"""Clean-room ContentConfig encoder for the isolated external-server lab."""

from __future__ import annotations

from dataclasses import dataclass
import re
import struct


_CACHE_MAGIC = b"SUNCMANF"
_CACHE_VERSION = 2
_HEADER = struct.Struct("<8s5I32s32s")
_ROW = struct.Struct("<256sHHQ")
_GUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
_OFFER_KEY = 0xD0000448
_HANDLE_BASE = 0xE0200001
_ENTITLEMENTS = (
    "1085660", "STEAM_PAID_TIER", "STEAM_UGC_BLOCKED", "1090090", "1090091",
    "1090092", "1090093", "1090094", "1090095", "1090096", "1090150",
    "1090151", "1090152", "1090170", "1090171", "1090200", "1090201",
    "1090202", "1330040",
)


@dataclass(frozen=True)
class ContentManifestRow:
    """One validated public package descriptor from Sunrise's local manifest cache."""

    name: str
    package_id: int
    build_signature: int


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


def parse_content_manifest_cache(data: bytes) -> tuple[ContentManifestRow, ...]:
    """Parse the fixed public rows from a locally generated, version-2 cache.

    The cache is a local runtime input, never a repository artifact.  This parser deliberately
    accepts only the exact header and row layout observed in the Sunrise source.
    """
    if len(data) < _HEADER.size:
        raise ValueError("manifest cache is shorter than its header")
    magic, version, header_size, row_size, row_count, reserved, _, _ = _HEADER.unpack_from(data)
    if (
        magic != _CACHE_MAGIC
        or version != _CACHE_VERSION
        or header_size != _HEADER.size
        or row_size != _ROW.size
        or not 0 < row_count <= 4000
        or reserved != 0
        or len(data) != header_size + row_size * row_count
    ):
        raise ValueError("manifest cache header is invalid")

    rows: list[ContentManifestRow] = []
    for index in range(row_count):
        raw_name, name_length, package_id, build_signature = _ROW.unpack_from(
            data, header_size + index * row_size
        )
        if not 0 < name_length < len(raw_name) or not 0x0100 <= package_id <= 0x19FF:
            raise ValueError("manifest cache row is invalid")
        name_bytes = raw_name[:name_length]
        if b"\0" in name_bytes:
            raise ValueError("manifest cache row contains an embedded name terminator")
        try:
            name = name_bytes.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError("manifest cache row name is not ASCII") from exc
        rows.append(ContentManifestRow(name, package_id, build_signature))
    return tuple(rows)


def _encode_entitlement(name: str, handle: int) -> bytes:
    inner = _field_bytes(1, name.encode("ascii"))
    wrapper = _field_bytes(4, inner)
    return b"".join((
        _field_varint(1, handle),
        _field_varint(2, 0),
        _field_bytes(3, wrapper),
        _field_varint(4, 2),
        _field_varint(5, 0),
        _field_varint(7, 0),
    ))


def _encode_row(row: ContentManifestRow) -> bytes:
    if not row.name or not 0x0100 <= row.package_id <= 0x19FF or row.build_signature < 0:
        raise ValueError("manifest row is invalid")
    name = row.name.encode("ascii")
    if len(name) > 255:
        raise ValueError("manifest row name is too long")
    return b"".join((
        _field_varint(1, _OFFER_KEY),
        _field_bytes(2, name),
        _field_varint(3, row.package_id),
        _field_varint(4, row.build_signature),
    ))


def build_content_config_response(
    rows: tuple[ContentManifestRow, ...], guid: str
) -> bytes:
    """Build the externally fetched ContentConfig body for the configured GUID."""
    if _GUID.fullmatch(guid) is None:
        raise ValueError("guid must be canonical lowercase UUID text")
    parts = [
        _field_bytes(2, _encode_entitlement(name, _HANDLE_BASE + index))
        for index, name in enumerate(_ENTITLEMENTS)
    ]
    parts.extend(_field_bytes(3, _encode_row(row)) for row in rows)
    parts.append(_field_bytes(5, guid.encode("ascii")))
    return b"".join(parts)
