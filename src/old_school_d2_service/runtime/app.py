"""Runnable HTTPS and BAP replacement listener for the isolated laboratory."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import http.server
import json
import secrets
import socket
import socketserver
import ssl
import struct
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from ..bap import BapConnectionState, build_server_hello_response, build_start_response
from ..content_config import build_content_config_response, parse_content_manifest_cache
from ..entitlements import SUNRISE_DEFAULT_OWNED_ENTITLEMENT_IDS
from ..post_bap_probe import build_post_bap_probe
from ..signon import build_signon_response_with_session, parse_bootstrap_token_hex
from .config import RuntimeConfig

_MAX_FRAME = 65536


class JsonlLogger:
    """Metadata-only, append-only local runtime logger; raw protocol buffers stay out of logs."""
    def __init__(self, path: Path) -> None:
        self.path, self.lock = path, threading.Lock()
        path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, **fields: object) -> None:
        item = {"timestamp": dt.datetime.now(dt.UTC).isoformat(), "event": event, **fields}
        with self.lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(item, sort_keys=True) + "\n")


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class _HTTPSHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *_: object) -> None: pass

    def _respond(self) -> None:
        runtime: RuntimeConfig = self.server.runtime_config  # type: ignore[attr-defined]
        logger: JsonlLogger = self.server.logger  # type: ignore[attr-defined]
        sessions: dict[str, object] = self.server.sessions  # type: ignore[attr-defined]
        target = urlsplit(self.path)
        length = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(min(length, _MAX_FRAME)) if length else b""
        logger.emit("https_request", direction="inbound", transport="https", route=target.path,
                    payload_length=length, payload_hash=_hash(body), query_present=bool(target.query))
        status, message = 503, b""
        if target.path.startswith("/SignOn"):
            values = parse_qs(target.query, keep_blank_values=True).get("sunrise_bootstrap", [])
            try:
                token = None if not values else parse_bootstrap_token_hex(values[0])
                if len(values) > 1: raise ValueError("multiple bootstrap values")
            except ValueError:
                status = 400
                logger.emit("signon_bootstrap_rejected", result="format_rejected")
            else:
                message, session = build_signon_response_with_session(
                    relay_host=runtime.bind_host, relay_port=runtime.bap_port,
                    owned_entitlement_ids=SUNRISE_DEFAULT_OWNED_ENTITLEMENT_IDS, bootstrap_token=token)
                sessions["active"] = session
                status = 200
                logger.emit("signon_session_issued", state_before="SIGNON", result="success", state_after="BAP_CONNECT")
        elif target.path == "/config/":
            try:
                message = build_content_config_response(
                    parse_content_manifest_cache(runtime.manifest_cache.read_bytes()), runtime.config_guid)
                status = 200
                logger.emit("content_config_served", state_before="CONTENT_CONFIG", result="success", state_after="BAP_CONNECT", payload_length=len(message), payload_hash=_hash(message))
            except (OSError, ValueError) as error:
                logger.emit("content_config_error", result=type(error).__name__)
        else:
            message = b"Old-School-D2 lab listener: no protocol response implemented.\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/octet-stream" if status != 503 else "text/plain")
        self.send_header("Content-Length", str(len(message))); self.send_header("Connection", "close")
        self.end_headers(); self.wfile.write(message)
    do_GET = _respond; do_POST = _respond; do_PUT = _respond; do_DELETE = _respond


class _BAPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        server = self.server; logger: JsonlLogger = server.logger  # type: ignore[attr-defined]
        state = "BAP_CONNECT"; bap: BapConnectionState | None = None; buffered = bytearray(); connection_id = secrets.token_hex(8)
        self.request.settimeout(30)
        try:
            while data := self.request.recv(_MAX_FRAME):
                buffered.extend(data)
                while len(buffered) >= 6:
                    size = struct.unpack(">I", buffered[2:6])[0]; total = 6 + size
                    if total > _MAX_FRAME: logger.emit("bap_frame_rejected", connection_id=connection_id, result="size_rejected"); return
                    if len(buffered) < total: break
                    frame = bytes(buffered[:total]); del buffered[:total]
                    frame_type = frame[1]; service = struct.unpack(">H", frame[6:8])[0] if frame_type in (0, 2) and size >= 6 else None
                    task_id = struct.unpack(">I", frame[8:12])[0] if frame_type in (0, 2) and size >= 6 else None
                    if frame_type == 1:
                        request = bap.open_encrypted_request(frame) if bap else None
                        if request is None:
                            logger.emit("bap_encrypted_frame_rejected", connection_id=connection_id, state_before=state, direction="inbound", transport="bap", payload_length=total, payload_hash=_hash(frame), result="authentication_rejected", state_after=state); continue
                        replies = ((121, bap.build_register_subscriber_response), (12, bap.build_subscribe_family_response), (302, bap.build_register_relay_client_response), (304, bap.build_sign_certificate_response), (250, bap.build_echo_response))
                        response = next((handler(request) for route, handler in replies if request.service == route), None)
                        logger.emit("bap_request", connection_id=connection_id, state_before=state, direction="inbound", transport="bap", service=request.service, message_id=request.task_id, payload_length=request.body_size, result="authenticated", state_after=state)
                        if response:
                            self.request.sendall(response)
                            logger.emit("bap_response", connection_id=connection_id, state_before=state, direction="outbound", transport="bap", service={121:122,12:13,302:303,304:305,250:251}[request.service], message_id=request.task_id, payload_length=len(response), payload_hash=_hash(response), result="sent", state_after=state)
                        continue
                    response = build_start_response(frame)
                    if response is not None: state = "BAP_CONNECT"; response_service = 31
                    elif service == 25:
                        session = server.sessions.get("active")  # type: ignore[attr-defined]
                        nonce, session_key = secrets.token_bytes(12), secrets.token_bytes(16)
                        response = build_server_hello_response(frame, encryption_key=session.encryption_key, authentication_key=session.authentication_key, nonce=nonce, session_key=session_key, envelope_iv=secrets.token_bytes(16)) if session else None
                        if response: bap = BapConnectionState.from_server_hello(session_key=session_key, server_nonce=nonce); state = "BAP_AUTHENTICATED"
                        response_service = 26
                    else: response_service = None
                    logger.emit("bap_frame", connection_id=connection_id, state_before=state, direction="inbound", transport="bap", service=service, message_id=task_id, payload_length=total, payload_hash=_hash(frame), result="accepted" if response else "unhandled", state_after=state)
                    if response: self.request.sendall(response); logger.emit("bap_response", connection_id=connection_id, state_before=state, direction="outbound", transport="bap", service=response_service, message_id=task_id, payload_length=len(response), payload_hash=_hash(response), result="sent", state_after=state)
        except socket.timeout: logger.emit("bap_timeout", connection_id=connection_id, state_before=state, result="timeout", state_after=state)


class _ThreadingTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True; daemon_threads = True


def build_runtime_servers(config: RuntimeConfig, ssl_context_factory: object = ssl.SSLContext) -> tuple[http.server.ThreadingHTTPServer, _ThreadingTCP]:
    logger = JsonlLogger(config.log_path); sessions: dict[str, object] = {}
    https = http.server.ThreadingHTTPServer((config.bind_host, config.https_port), _HTTPSHandler)
    bap = _ThreadingTCP((config.bind_host, config.bap_port), _BAPHandler)
    for server in (https, bap): server.logger, server.sessions, server.runtime_config = logger, sessions, config  # type: ignore[attr-defined]
    return https, bap


def main() -> None:
    config = RuntimeConfig.from_environment(); https, bap = build_runtime_servers(config)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); context.load_cert_chain(config.tls_cert, config.tls_key)
    https.socket = context.wrap_socket(https.socket, server_side=True)
    threads = [threading.Thread(target=server.serve_forever, daemon=True) for server in (https, bap)]
    for thread in threads: thread.start()
    try: threading.Event().wait()
    except KeyboardInterrupt: pass
    finally:
        for server in (https, bap): server.shutdown(); server.server_close()

if __name__ == "__main__": main()
