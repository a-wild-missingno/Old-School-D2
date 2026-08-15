from old_school_d2_service.signon import build_signon_response, build_signon_response_with_session


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


def test_builds_minimal_successful_signon_response() -> None:
    response = build_signon_response(
        relay_host="192.168.0.129",
        relay_port=30974,
        now_seconds=1_700_000_000,
        random_bytes=lambda length: bytes(range(length)),
    )

    outer = _fields(response)
    assert outer[1] == [0]
    assert outer[5] == [1]
    assert outer[6] == [b"d2legacy"]
    assert outer[12] == [1_700_000_000]
    assert outer[13] == [b"live"]
    assert outer[14] == [0xC0A80081]

    success = _fields(outer[2][0])
    assert success[1] == [b"\x00" * 16]
    assert success[2] == [bytes(range(16))]
    assert success[3] == [bytes(range(16))]
    assert success[4] == [bytes(range(32))]
    assert success[6] == [0xC0A80081]
    assert success[7] == [30974]
    assert success[14] == [b"http://192.168.0.129/cfg_a/"]


def test_exposes_ephemeral_signon_material_only_to_the_calling_listener() -> None:
    response, session = build_signon_response_with_session(
        relay_host="192.168.0.129",
        relay_port=30974,
        now_seconds=1_700_000_000,
        random_bytes=lambda length: bytes(range(length)),
    )

    outer = _fields(response)
    success = _fields(outer[2][0])
    assert success[2] == [session.encryption_key]
    assert success[3] == [session.authentication_key]
    assert success[4] == [session.session_token]
