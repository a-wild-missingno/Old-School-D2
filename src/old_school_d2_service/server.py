"""Socket adapter for the narrowly documented UDP discovery experiment."""

from __future__ import annotations

import socketserver
import threading

from .discovery import build_nat_probe_reply
from typing import Protocol


class EventStore(Protocol):
    def record_event(self, **event: object) -> int: ...


class _DiscoveryHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        payload, socket = self.request
        server: DiscoveryUDPServer = self.server
        reply = build_nat_probe_reply(payload, self.client_address)
        kind = "nat_probe" if reply is not None else "unknown"
        server.store.record_event(
            experiment_id=server.experiment_id,
            transport="udp",
            direction="inbound",
            local_port=server.server_address[1],
            payload=payload,
            decoded_kind=kind,
        )
        if reply is None:
            return
        server.store.record_event(
            experiment_id=server.experiment_id,
            transport="udp",
            direction="outbound",
            local_port=server.server_address[1],
            payload=reply,
            decoded_kind="nat_probe_reply",
        )
        socket.sendto(reply, self.client_address)


class DiscoveryUDPServer(socketserver.ThreadingUDPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address: tuple[str, int], store: EventStore, experiment_id: int) -> None:
        self.store = store
        self.experiment_id = experiment_id
        super().__init__(address, _DiscoveryHandler)


def start_discovery_server(
    host: str, port: int, store: EventStore, experiment_id: int
) -> tuple[DiscoveryUDPServer, threading.Thread]:
    """Start a UDP server in a daemon thread and return its handles for controlled shutdown."""
    server = DiscoveryUDPServer((host, port), store, experiment_id)
    thread = threading.Thread(target=server.serve_forever, daemon=True, name="discovery-udp")
    thread.start()
    return server, thread
