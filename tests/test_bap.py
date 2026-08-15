import struct

from old_school_d2_service.bap import build_server_hello_response, build_start_response


def _frame(frame_type: int, service: int, task_id: int, body: bytes) -> bytes:
    payload = struct.pack(">HI", service, task_id) + body
    return b"\x01" + bytes((frame_type,)) + struct.pack(">I", len(payload)) + payload


def test_echoes_observed_plaintext_start_request_as_status_200() -> None:
    request = _frame(2, 30, 0, b"N" * 128)

    response = build_start_response(request)

    assert response == _frame(2, 31, 0, b"\x00\xc8" + b"N" * 128)


def test_rejects_non_start_and_incomplete_frames() -> None:
    assert build_start_response(_frame(2, 25, 7, b"x")) is None
    assert build_start_response(_frame(2, 30, 7, b"x")[:-1]) is None


def test_builds_authenticated_server_hello_response() -> None:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes, hmac

    encryption_key = bytes(range(16))
    authentication_key = bytes(range(16, 32))
    nonce = bytes(range(12))
    session_key = bytes(range(32, 48))
    envelope_iv = bytes(range(48, 64))
    hello_body = b"\x0a\x20" + (b"T" * 32) + b"\x10\x01"

    response = build_server_hello_response(
        _frame(2, 25, 1, hello_body),
        encryption_key=encryption_key,
        authentication_key=authentication_key,
        nonce=nonce,
        session_key=session_key,
        envelope_iv=envelope_iv,
    )

    assert response is not None
    outer_size = struct.unpack(">I", response[2:6])[0]
    assert outer_size == len(response) - 6
    service, task_id, status = struct.unpack(">HIH", response[6:14])
    assert (response[0], response[1], service, task_id, status) == (1, 2, 26, 1, 200)
    envelope = response[14:]
    assert len(envelope) == 84
    assert struct.unpack(">I", envelope[:4])[0] == 80
    mac = hmac.HMAC(authentication_key, hashes.SHA256())
    mac.update(envelope[:52])
    mac.verify(envelope[52:])
    decryptor = Cipher(algorithms.AES(encryption_key), modes.CBC(envelope[4:20])).decryptor()
    assert decryptor.update(envelope[20:52]) + decryptor.finalize() == nonce + session_key + (b"\x04" * 4)


def test_rejects_non_server_hello_frame() -> None:
    assert build_server_hello_response(
        _frame(2, 30, 1, b"x"),
        encryption_key=b"a" * 16,
        authentication_key=b"b" * 16,
        nonce=b"c" * 12,
        session_key=b"d" * 16,
        envelope_iv=b"e" * 16,
    ) is None
