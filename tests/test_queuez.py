import struct

from old_school_d2_service.queuez import QueuezFamily, QueuezObject, encode_queuez_update


def test_encodes_one_empty_full_snapshot_family() -> None:
    family = QueuezFamily(type=4, root_soid=0x0102030405060708, version=0, flags=1, objects=())

    encoded = encode_queuez_update((family,))

    assert encoded == struct.pack(
        ">IIQiBI", 1, 4, 0x0102030405060708, 0, 1, 0
    )


def test_encodes_raw_object_with_little_endian_version_prefix() -> None:
    version = 0x1122334455667788
    payload = struct.pack("<Q", version) + b"fixture"
    family = QueuezFamily(
        type=4,
        root_soid=9,
        version=0,
        flags=1,
        objects=(QueuezObject(object_id=7, version=version, encoding=3, payload=payload),),
    )

    encoded = encode_queuez_update((family,))

    assert encoded == (
        struct.pack(">IIQiBI", 1, 4, 9, 0, 1, 1)
        + struct.pack(">IQII", 7, version, len(payload), 3)
        + payload
    )


import pytest


def test_rejects_raw_object_without_matching_little_endian_version_prefix() -> None:
    family = QueuezFamily(
        type=4,
        root_soid=9,
        version=0,
        flags=1,
        objects=(QueuezObject(object_id=7, version=2, encoding=3, payload=struct.pack("<Q", 1)),),
    )

    with pytest.raises(ValueError, match="version"):
        encode_queuez_update((family,))


def test_rejects_unknown_object_encoding() -> None:
    family = QueuezFamily(
        type=4,
        root_soid=9,
        version=0,
        flags=1,
        objects=(QueuezObject(object_id=7, version=1, encoding=99, payload=b"fixture"),),
    )

    with pytest.raises(ValueError, match="encoding"):
        encode_queuez_update((family,))


def test_rejects_raw_object_shorter_than_version_prefix() -> None:
    family = QueuezFamily(
        type=4,
        root_soid=9,
        version=0,
        flags=1,
        objects=(QueuezObject(object_id=7, version=2, encoding=3, payload=b"short"),),
    )

    with pytest.raises(ValueError, match="version"):
        encode_queuez_update((family,))
