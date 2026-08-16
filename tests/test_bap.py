import struct

from old_school_d2_service.bap import BapConnectionState, build_server_hello_response, build_start_response


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


def _encrypted_frame(key: bytes, receive_nonce: bytes, service: int, task_id: int, body: bytes = b"") -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    plaintext = struct.pack(">HI", service, task_id) + body
    sealed = AESGCM(key).encrypt(receive_nonce, plaintext, None)
    payload = sealed[-16:] + sealed[:-16]
    return b"\x01\x01" + struct.pack(">I", len(payload)) + payload


def test_decrypts_one_connection_scoped_encrypted_request_and_advances_receive_nonce() -> None:
    key = bytes(range(16))
    server_nonce = bytes(range(12))
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=server_nonce)
    expected_receive_nonce = server_nonce[:-1] + bytes([server_nonce[-1] ^ 1])

    request = state.open_encrypted_request(_encrypted_frame(key, expected_receive_nonce, 250, 7))

    assert request is not None
    assert (request.service, request.task_id, request.body_size) == (250, 7, 0)
    assert state.receive_nonce == bytes([expected_receive_nonce[0] + 1]) + expected_receive_nonce[1:]


def test_rejects_unauthenticated_encrypted_frame_without_advancing_receive_nonce() -> None:
    state = BapConnectionState.from_server_hello(session_key=b"K" * 16, server_nonce=b"N" * 12)
    before = state.receive_nonce
    frame = bytearray(_encrypted_frame(b"K" * 16, before, 250, 7))
    frame[-1] ^= 1

    assert state.open_encrypted_request(bytes(frame)) is None
    assert state.receive_nonce == before


def test_answers_authenticated_register_subscriber_with_empty_response_122() -> None:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes(range(16))
    server_nonce = bytes(range(12))
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=server_nonce)
    receive_nonce = state.receive_nonce
    request = state.open_encrypted_request(_encrypted_frame(key, receive_nonce, 121, 2))
    assert request is not None

    response = state.build_register_subscriber_response(request)

    assert response is not None
    payload_size = struct.unpack(">I", response[2:6])[0]
    assert (response[0], response[1], payload_size) == (1, 1, 24)
    payload = response[6:]
    plaintext = AESGCM(key).decrypt(server_nonce, payload[16:] + payload[:16], None)
    assert struct.unpack(">HIH", plaintext) == (122, 2, 200)


def test_refuses_to_reply_to_a_different_encrypted_service() -> None:
    state = BapConnectionState.from_server_hello(session_key=b"K" * 16, server_nonce=b"N" * 12)
    request = state.open_encrypted_request(_encrypted_frame(b"K" * 16, state.receive_nonce, 250, 2))
    assert request is not None
    assert state.build_register_subscriber_response(request) is None


def test_answers_authenticated_register_relay_client_with_empty_response_303() -> None:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes(range(16))
    server_nonce = bytes(range(12))
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=server_nonce)
    request = state.open_encrypted_request(_encrypted_frame(key, state.receive_nonce, 302, 3, b"R" * 94))
    assert request is not None

    response = state.build_register_relay_client_response(request)

    assert response is not None
    payload = response[6:]
    plaintext = AESGCM(key).decrypt(server_nonce, payload[16:] + payload[:16], None)
    assert struct.unpack(">HIH", plaintext) == (303, 3, 200)


def test_rewraps_certificate_field_for_authenticated_sign_certificate_response() -> None:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes(range(16))
    server_nonce = bytes(range(12))
    request_body = b"\x1a\x03abc"  # protobuf: field 3, length-delimited certificate wrapper
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=server_nonce)
    request = state.open_encrypted_request(_encrypted_frame(key, state.receive_nonce, 304, 4, request_body))
    assert request is not None

    response = state.build_sign_certificate_response(request)

    assert response is not None
    payload = response[6:]
    plaintext = AESGCM(key).decrypt(server_nonce, payload[16:] + payload[:16], None)
    assert plaintext[:8] == struct.pack(">HIH", 305, 4, 200)
    assert plaintext[8:] == b"\x08\x00\x1a\x03abc"


def test_answers_authenticated_subscribe_family_with_empty_response_13() -> None:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes(range(16))
    server_nonce = bytes(range(12))
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=server_nonce)
    request = state.open_encrypted_request(
        _encrypted_frame(key, state.receive_nonce, 12, 6, b"\x00" + (b"R" * 8))
    )
    assert request is not None

    response = state.build_subscribe_family_response(request)

    assert response is not None
    payload = response[6:]
    assert AESGCM(key).decrypt(server_nonce, payload[16:] + payload[:16], None) == struct.pack(">HIH", 13, 6, 200)


def test_refuses_subscribe_family_response_for_other_service() -> None:
    state = BapConnectionState.from_server_hello(session_key=b"K" * 16, server_nonce=b"N" * 12)
    request = state.open_encrypted_request(_encrypted_frame(b"K" * 16, state.receive_nonce, 250, 2))
    assert request is not None
    assert state.build_subscribe_family_response(request) is None


def test_answers_authenticated_echo_with_empty_response_251() -> None:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = bytes(range(16)); nonce = bytes(range(12))
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=nonce)
    request = state.open_encrypted_request(_encrypted_frame(key, state.receive_nonce, 250, 6))
    assert request is not None
    response = state.build_echo_response(request)
    assert response is not None
    payload = response[6:]
    assert AESGCM(key).decrypt(nonce, payload[16:] + payload[:16], None) == struct.pack(">HIH", 251, 6, 200)


def test_builds_uncorrelated_notification_with_sequence_zero_and_advances_send_nonce() -> None:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes(range(16))
    server_nonce = bytes(range(12))
    state = BapConnectionState.from_server_hello(session_key=key, server_nonce=server_nonce)

    response = state.build_notification(service=123, body=b"queuez-fixture")

    assert response is not None
    payload = response[6:]
    plaintext = AESGCM(key).decrypt(server_nonce, payload[16:] + payload[:16], None)
    assert plaintext == struct.pack(">HI", 123, 0) + b"queuez-fixture"
    assert state.send_nonce == bytes([server_nonce[0] + 1]) + server_nonce[1:]


def test_rejects_invalid_notification_without_advancing_send_nonce() -> None:
    state = BapConnectionState.from_server_hello(session_key=b"K" * 16, server_nonce=b"N" * 12)
    before = state.send_nonce

    assert state.build_notification(service=0, body=b"ignored") is None

    assert state.send_nonce == before
