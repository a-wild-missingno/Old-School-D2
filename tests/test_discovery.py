from old_school_d2_service.discovery import build_nat_probe_reply


def test_builds_reply_for_first_nat_probe_index() -> None:
    reply = build_nat_probe_reply(bytes.fromhex("00010001"), ("192.168.0.225", 3097))

    assert reply == bytes.fromhex("00010001b66bf65dfaa5000000000000")


def test_builds_reply_for_second_nat_probe_index() -> None:
    reply = build_nat_probe_reply(bytes.fromhex("00010002"), ("192.168.0.225", 3097))

    assert reply == bytes.fromhex("00010002b66bf65dfaa5000000000000")


def test_rejects_unrecognized_datagrams() -> None:
    assert build_nat_probe_reply(b"\x00\x01\x00\x03", ("192.168.0.225", 3097)) is None
    assert build_nat_probe_reply(b"\x00\x01", ("192.168.0.225", 3097)) is None
