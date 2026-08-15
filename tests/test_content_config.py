import struct

import pytest

from old_school_d2_service.content_config import (
    ContentManifestRow,
    build_content_config_response,
    parse_content_manifest_cache,
)


def _read_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, offset
        shift += 7


def _fields(data: bytes) -> dict[int, list[bytes | int]]:
    result: dict[int, list[bytes | int]] = {}
    offset = 0
    while offset < len(data):
        key, offset = _read_varint(data, offset)
        field, wire = key >> 3, key & 7
        if wire == 0:
            value, offset = _read_varint(data, offset)
        elif wire == 2:
            length, offset = _read_varint(data, offset)
            value = data[offset : offset + length]
            offset += length
        else:
            raise AssertionError(f"unsupported wire type {wire}")
        result.setdefault(field, []).append(value)
    return result


def _cache(rows: list[tuple[str, int, int]]) -> bytes:
    header_size = 92
    row_size = 268
    header = struct.pack(
        "<8s5I32s32s",
        b"SUNCMANF",
        2,
        header_size,
        row_size,
        len(rows),
        0,
        b"D" * 32,
        b"B" * 32,
    )
    encoded_rows = []
    for name, package_id, build_signature in rows:
        encoded_name = name.encode("ascii")
        encoded_rows.append(
            struct.pack("<256sHH", encoded_name, len(encoded_name), package_id) + struct.pack("<Q", build_signature)
        )
    return header + b"".join(encoded_rows)


def test_parses_validated_manifest_cache_rows() -> None:
    rows = parse_content_manifest_cache(_cache([("w64_test_001", 0x100, 99)]))

    assert rows == (ContentManifestRow("w64_test_001", 0x100, 99),)


@pytest.mark.parametrize(
    "cache",
    [
        b"",
        _cache([("w64_test_001", 0x100, 99)])[:-1],
        _cache([("w64_test_001", 0x100, 99)]).replace(b"SUNCMANF", b"BADCMANF", 1),
    ],
)
def test_rejects_malformed_manifest_cache(cache: bytes) -> None:
    with pytest.raises(ValueError):
        parse_content_manifest_cache(cache)


def test_builds_content_config_with_matching_guid_and_package_rows() -> None:
    response = build_content_config_response(
        rows=(
            ContentManifestRow("w64_test_001", 0x100, 99),
            ContentManifestRow("w64_test_002", 0x101, 100),
        ),
        guid="d2e1a0c0-0000-4000-8000-000000000001",
    )

    outer = _fields(response)
    assert outer[5] == [b"d2e1a0c0-0000-4000-8000-000000000001"]
    assert len(outer[2]) == 19
    package_rows = [_fields(value) for value in outer[3]]
    assert package_rows == [
        {1: [0xD0000448], 2: [b"w64_test_001"], 3: [0x100], 4: [99]},
        {1: [0xD0000448], 2: [b"w64_test_002"], 3: [0x101], 4: [100]},
    ]


@pytest.mark.parametrize(
    "guid",
    [
        "",
        "D2LEGACY-0000-0000-0000-000000000001",
        "d2legacy-0000-0000-0000-00000000001",
    ],
)
def test_rejects_noncanonical_config_guid(guid: str) -> None:
    with pytest.raises(ValueError):
        build_content_config_response((), guid)
