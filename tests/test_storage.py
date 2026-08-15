from old_school_d2_service.storage import PostgresEventStore


class FakeCursor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[object, ...] | None]] = []
        self._row: tuple[object, ...] | None = None

    def execute(self, query: str, parameters: tuple[object, ...] | None = None) -> None:
        self.calls.append((query, parameters))
        if "INSERT INTO experiments" in query:
            self._row = (7,)
        elif "INSERT INTO events" in query:
            self._row = (11,)

    def fetchone(self):
        return self._row

    def fetchall(self):
        return []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_instance = FakeCursor()

    def cursor(self):
        return self.cursor_instance

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def test_records_sanitized_discovery_event_in_postgres() -> None:
    connections: list[FakeConnection] = []

    def connect(_: str) -> FakeConnection:
        connection = FakeConnection()
        connections.append(connection)
        return connection

    store = PostgresEventStore("postgresql://unused", connect=connect)
    experiment_id = store.start_experiment(label="sunrise-external-server")
    event_id = store.record_event(
        experiment_id=experiment_id,
        transport="udp",
        direction="inbound",
        local_port=3074,
        payload=b"\x00\x01\x00\x01",
        decoded_kind="nat_probe",
    )

    assert experiment_id == 7
    assert event_id == 11
    event_parameters = connections[1].cursor_instance.calls[0][1]
    assert event_parameters is not None
    assert event_parameters[5] == 4
    assert event_parameters[6] == "76cc5805dab9b4eacefdb477f498020fd82bccdbc9c6a2d9ce10586ac85512b4"
    assert event_parameters[7] == "nat_probe"
