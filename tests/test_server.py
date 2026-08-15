import socket

from old_school_d2_service.server import start_discovery_server


def test_udp_server_records_probe_and_sends_reply(tmp_path) -> None:
    class RecordingStore:
        def __init__(self) -> None:
            self.events = []

        def record_event(self, **event) -> int:
            self.events.append(event)
            return len(self.events)

    store = RecordingStore()
    experiment_id = 1
    server, thread = start_discovery_server("127.0.0.1", 0, store, experiment_id)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(1)
            client.sendto(bytes.fromhex("00010001"), server.server_address)
            reply, _ = client.recvfrom(64)
        assert reply[:4] == bytes.fromhex("00010001")
        assert [(event["direction"], event["decoded_kind"]) for event in store.events] == [
            ("inbound", "nat_probe"),
            ("outbound", "nat_probe_reply"),
        ]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)
