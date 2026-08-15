"""Narrow BAP bootstrap helpers for the isolated lab listener."""

from __future__ import annotations

import struct
from dataclasses import dataclass

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


_OUTER_HEADER = struct.Struct(">BBI")
_REQUEST_HEADER = struct.Struct(">HI")
_RESPONSE_HEADER = struct.Struct(">HIH")
_MAGIC = 1
_PLAINTEXT_TYPES = frozenset((0, 2))
_START_REQUEST_SERVICE = 30
_START_RESPONSE_SERVICE = 31
_STATUS_OK = 200
_SERVER_HELLO_REQUEST_SERVICE = 25
_SERVER_HELLO_RESPONSE_SERVICE = 26


@dataclass(frozen=True)
class BapEncryptedRequest:
    """Safe metadata derived from one authenticated encrypted BAP request."""

    service: int
    task_id: int
    body_size: int
    # Retained only by the live connection while a documented body codec needs it; never logged.
    body: bytes


def _encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("protobuf varint must be unsigned")
    encoded = bytearray()
    while value > 127:
        encoded.append((value & 127) | 128)
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


def _read_varint(data: bytes, offset: int) -> tuple[int, int] | None:
    value = 0
    for shift in range(0, 70, 7):
        if offset >= len(data):
            return None
        byte = data[offset]
        offset += 1
        value |= (byte & 127) << shift
        if byte < 128:
            return value, offset
    return None


def _first_length_delimited_field(data: bytes, *, wanted_field: int) -> bytes | None:
    """Return the first valid protobuf length-delimited field without retaining other fields."""
    offset = 0
    while offset < len(data):
        key = _read_varint(data, offset)
        if key is None:
            return None
        key_value, offset = key
        field_number, wire_type = key_value >> 3, key_value & 7
        if wire_type == 0:
            value = _read_varint(data, offset)
            if value is None:
                return None
            _, offset = value
        elif wire_type == 1:
            offset += 8
        elif wire_type == 2:
            length = _read_varint(data, offset)
            if length is None:
                return None
            length_value, offset = length
            end = offset + length_value
            if end > len(data):
                return None
            if field_number == wanted_field:
                return bytes(data[offset:end])
            offset = end
        elif wire_type == 5:
            offset += 4
        else:
            return None
        if offset > len(data):
            return None
    return None


class BapConnectionState:
    """In-memory receive-direction state for one authenticated BAP TCP connection."""

    def __init__(self, *, session_key: bytes, receive_nonce: bytes, send_nonce: bytes) -> None:
        if len(session_key) != 16 or len(receive_nonce) != 12 or len(send_nonce) != 12:
            raise ValueError("BAP session key and nonces must be 16 and 12 bytes")
        self._session_key = bytes(session_key)
        self._receive_nonce = bytearray(receive_nonce)
        self._send_nonce = bytearray(send_nonce)

    @classmethod
    def from_server_hello(cls, *, session_key: bytes, server_nonce: bytes) -> "BapConnectionState":
        if len(server_nonce) != 12:
            raise ValueError("BAP server nonce must be 12 bytes")
        receive_nonce = bytearray(server_nonce)
        receive_nonce[-1] ^= 1
        return cls(session_key=session_key, receive_nonce=bytes(receive_nonce), send_nonce=server_nonce)

    @property
    def receive_nonce(self) -> bytes:
        return bytes(self._receive_nonce)

    @property
    def send_nonce(self) -> bytes:
        return bytes(self._send_nonce)

    def open_encrypted_request(self, frame: bytes) -> BapEncryptedRequest | None:
        """Authenticate one type-1 frame and advance only after a valid inner request."""
        if len(frame) < _OUTER_HEADER.size:
            return None
        magic, frame_type, payload_size = _OUTER_HEADER.unpack_from(frame)
        if magic != _MAGIC or frame_type != 1 or len(frame) != _OUTER_HEADER.size + payload_size:
            return None
        payload = frame[_OUTER_HEADER.size :]
        if len(payload) < 16 + _REQUEST_HEADER.size:
            return None
        tag, ciphertext = payload[:16], payload[16:]
        try:
            plaintext = AESGCM(self._session_key).decrypt(bytes(self._receive_nonce), ciphertext + tag, None)
        except (InvalidTag, ValueError):
            return None
        if len(plaintext) < _REQUEST_HEADER.size:
            return None
        service, task_id = _REQUEST_HEADER.unpack_from(plaintext)
        self._advance_receive_nonce()
        return BapEncryptedRequest(service=service, task_id=task_id, body_size=len(plaintext) - _REQUEST_HEADER.size, body=bytes(plaintext[_REQUEST_HEADER.size:]))

    def build_register_subscriber_response(self, request: BapEncryptedRequest) -> bytes | None:
        """Return only the documented encrypted service-122 acknowledgement for service 121."""
        return self._build_empty_response(request, request_service=121, response_service=122)

    def build_register_relay_client_response(self, request: BapEncryptedRequest) -> bytes | None:
        """Return only the documented encrypted service-303 acknowledgement for service 302."""
        return self._build_empty_response(request, request_service=302, response_service=303)

    def build_echo_response(self, request: BapEncryptedRequest) -> bytes | None:
        """Return only the documented encrypted service-251 acknowledgement for service 250."""
        return self._build_empty_response(request, request_service=250, response_service=251)

    def build_notification(self, *, service: int, body: bytes) -> bytes | None:
        """Build one uncorrelated encrypted notification with fixed sequence zero.

        This is transport-only: callers must supply a separately evidenced service and body.
        Invalid inputs leave the connection send nonce unchanged.
        """
        if not 0 < service <= 0xFFFF or len(body) > 65508:
            return None
        plaintext = _REQUEST_HEADER.pack(service, 0) + bytes(body)
        sealed = AESGCM(self._session_key).encrypt(bytes(self._send_nonce), plaintext, None)
        payload = sealed[-16:] + sealed[:-16]
        self._advance_send_nonce()
        return _OUTER_HEADER.pack(_MAGIC, 1, len(payload)) + payload

    def build_sign_certificate_response(self, request: BapEncryptedRequest) -> bytes | None:
        """Rewrap only service-304 protobuf certificate field 3 in the documented service-305 body."""
        if request.service != 304:
            return None
        certificate = _first_length_delimited_field(request.body, wanted_field=3)
        if certificate is None:
            return None
        body = b"\x08\x00" + _encode_varint(26) + _encode_varint(len(certificate)) + certificate
        return self._seal_response(response_service=305, task_id=request.task_id, body=body)

    def _build_empty_response(self, request: BapEncryptedRequest, *, request_service: int, response_service: int) -> bytes | None:
        if request.service != request_service:
            return None
        return self._seal_response(response_service=response_service, task_id=request.task_id, body=b"")

    def _seal_response(self, *, response_service: int, task_id: int, body: bytes) -> bytes:
        plaintext = _RESPONSE_HEADER.pack(response_service, task_id, _STATUS_OK) + body
        sealed = AESGCM(self._session_key).encrypt(bytes(self._send_nonce), plaintext, None)
        payload = sealed[-16:] + sealed[:-16]
        self._advance_send_nonce()
        return _OUTER_HEADER.pack(_MAGIC, 1, len(payload)) + payload

    def _advance_receive_nonce(self) -> None:
        self._advance_nonce(self._receive_nonce)

    def _advance_send_nonce(self) -> None:
        self._advance_nonce(self._send_nonce)

    @staticmethod
    def _advance_nonce(nonce: bytearray) -> None:
        for index, value in enumerate(nonce):
            next_value = (value + 1) % 256
            nonce[index] = next_value
            if next_value != 0:
                return



def build_start_response(frame: bytes) -> bytes | None:
    """Return the source-documented plaintext service-31 reply for one service-30 frame.

    No other service is interpreted or answered.  In particular, this helper deliberately does
    not claim to implement SignOn-token validation, service-25, encryption, or later BAP routes.
    """
    if len(frame) < _OUTER_HEADER.size:
        return None
    magic, frame_type, payload_size = _OUTER_HEADER.unpack_from(frame)
    if magic != _MAGIC or frame_type not in _PLAINTEXT_TYPES or len(frame) != _OUTER_HEADER.size + payload_size:
        return None
    payload = frame[_OUTER_HEADER.size :]
    if len(payload) < _REQUEST_HEADER.size:
        return None
    service, task_id = _REQUEST_HEADER.unpack_from(payload)
    if service != _START_REQUEST_SERVICE:
        return None
    response_payload = _RESPONSE_HEADER.pack(_START_RESPONSE_SERVICE, task_id, _STATUS_OK) + payload[_REQUEST_HEADER.size :]
    return _OUTER_HEADER.pack(_MAGIC, frame_type, len(response_payload)) + response_payload


def build_server_hello_response(
    frame: bytes,
    *,
    encryption_key: bytes,
    authentication_key: bytes,
    nonce: bytes,
    session_key: bytes,
    envelope_iv: bytes,
) -> bytes | None:
    """Build the source-documented plaintext service-26 envelope for one service-25 frame.

    The caller owns the SignOn and BAP material and must keep it in process memory only.
    This function intentionally does not log, retain, or interpret those secret values.
    """
    if (
        len(encryption_key) != 16
        or len(authentication_key) != 16
        or len(nonce) != 12
        or len(session_key) != 16
        or len(envelope_iv) != 16
        or len(frame) < _OUTER_HEADER.size
    ):
        return None
    magic, frame_type, payload_size = _OUTER_HEADER.unpack_from(frame)
    if magic != _MAGIC or frame_type not in _PLAINTEXT_TYPES or len(frame) != _OUTER_HEADER.size + payload_size:
        return None
    payload = frame[_OUTER_HEADER.size :]
    if len(payload) < _REQUEST_HEADER.size:
        return None
    service, task_id = _REQUEST_HEADER.unpack_from(payload)
    if service != _SERVER_HELLO_REQUEST_SERVICE:
        return None
    plaintext = nonce + session_key + (b"\x04" * 4)
    encryptor = Cipher(algorithms.AES(encryption_key), modes.CBC(envelope_iv)).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    envelope = struct.pack(">I", 80) + envelope_iv + ciphertext
    signer = hmac.HMAC(authentication_key, hashes.SHA256())
    signer.update(envelope)
    envelope += signer.finalize()
    response_payload = _RESPONSE_HEADER.pack(_SERVER_HELLO_RESPONSE_SERVICE, task_id, _STATUS_OK) + envelope
    return _OUTER_HEADER.pack(_MAGIC, frame_type, len(response_payload)) + response_payload
