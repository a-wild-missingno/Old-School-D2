# Old-School-D2 service foundation

## Goal

Build a clean-room, lab-only service that records and incrementally implements only the network behavior demonstrated by controlled Sunrise client experiments. The service must never proxy, forward, or contact production infrastructure.

## First vertical slice

The first implemented behavior is Sunrise external-server UDP discovery handling. The lab has observed two four-byte NatProbe requests on the discovery port. The service will validate that narrow request shape, record an event, and return the corresponding local mapping reply. It will not claim to implement the broader BAP/Demonware protocol.

## Service boundary

The service is a standalone Python process, independent of the Destiny client and Sunrise binary. It owns only explicitly configured lab addresses and ports. Unknown datagrams are logged as metadata and receive no response.

Initial components:

- `src/old_school_d2_service/discovery.py`: pure request classification and reply construction.
- `src/old_school_d2_service/storage.py`: SQLite schema and append-only experiment-event storage.
- `src/old_school_d2_service/server.py`: UDP adapter that binds configured discovery ports and passes data through the pure service boundary.
- `tests/`: unit tests plus a local loopback socket smoke test.

## SignOn boundary

The next observed client dependency is an HTTPS `POST /SignOn` request after UDP discovery. The service now has a minimal protobuf success-response encoder that issues per-response random session material, returns the OptiPlex relay address and BAP port, and does not persist session secrets. It intentionally stops at that boundary: BAP frames remain capture-only until a fresh client run demonstrates their required sequence.

## Database decision

Use PostgreSQL from the first service release, not SQLite and not a production account or world database. This avoids a storage-engine rebuild once the service needs concurrent listeners, migrations, queryable experiment history, and later service components. The initial schema contains only:

- `experiments`: sanitized metadata for a run.
- `events`: timestamped transport observations, request/reply sizes, hashes, and optional decoded metadata.

Raw packet captures, private addresses, account data, tokens, game assets, and proprietary client files remain outside the public repository. Connection URLs belong in local environment configuration and are never committed. The checked-in migration is `db/migrations/001_initial.sql`; apply it with `python -m old_school_d2_service --migrate` before starting the service.

Defer accounts, profiles, inventories, matchmaking, and migrations for gameplay state until a protocol experiment demonstrates a specific need. A repository abstraction keeps that future change possible without prematurely designing game data models.

## Validation gates

Every protocol response needs: a captured request, a narrow parser, a test that rejects malformed input, a local socket test, and a documented experiment record. No guessed response should be added merely to clear an error screen.
