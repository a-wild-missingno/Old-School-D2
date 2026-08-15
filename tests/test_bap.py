import struct

from old_school_d2_service.bap import build_start_response


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
