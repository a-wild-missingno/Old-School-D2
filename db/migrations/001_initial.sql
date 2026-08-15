CREATE TABLE experiments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    label TEXT NOT NULL CHECK (length(trim(label)) > 0),
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    experiment_id BIGINT NOT NULL REFERENCES experiments(id),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transport TEXT NOT NULL CHECK (transport IN ('udp', 'tcp', 'https')),
    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    local_port INTEGER NOT NULL CHECK (local_port BETWEEN 1 AND 65535),
    payload_size INTEGER NOT NULL CHECK (payload_size >= 0),
    payload_sha256 CHAR(64) NOT NULL,
    decoded_kind TEXT
);

CREATE INDEX events_experiment_id ON events(experiment_id, id);
