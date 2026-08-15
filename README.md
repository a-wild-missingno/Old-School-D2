# Old-School-D2

Old-School-D2 is a clean-room, lab-only research project for documenting how a historical Destiny 2 client, configured with Sunrise external-server mode, interacts with replacement service boundaries. Its long-term preservation goal is an offline or preservation-focused PvE research environment—not access to Bungie services and not a general-purpose game server.

The project uses controlled client experiments, public Sunrise source as a behavioral reference, narrow independent implementations, and reproducible tests. It does **not** copy Destiny binaries, assets, account data, keys, packet captures, or proprietary service code into this repository.

## AI-assisted development disclosure

This repository is developed with substantial assistance from AI coding tools. AI is used for implementation, test drafting, documentation, and research synthesis; it can make mistakes or produce incomplete conclusions. Changes are intended to be evidence-backed, reviewed, tested, and constrained to the project safety rules below. Contributors and maintainers—not an AI system—remain responsible for review, security, licensing, and research decisions.

## Current progress

Status as of the current controlled lab experiment:

| Boundary | State | Evidence / scope |
| --- | --- | --- |
| Network isolation | Verified | The client lab has no forwarding, NAT, or WAN path. |
| UDP discovery | Implemented | Narrow Sunrise NatProbe replies with sanitized PostgreSQL event recording. |
| HTTPS SignOn | Implemented | Minimal protobuf success response issues ephemeral, in-memory session material. |
| ContentConfig | Implemented | Strict local manifest-cache parser and response encoder; cache stays outside Git. |
| BAP channel start | Implemented | Plaintext service 30 receives documented service-31 nonce echo. |
| BAP ServerHello | Implemented | Plaintext service 25 receives authenticated service-26 key/nonce envelope. |
| Post-hello BAP | Incrementally implemented | The first authenticated encrypted request was service 121 (register subscriber), task 2, empty body; the listener now returns the documented empty service-122 acknowledgement. Later encrypted services remain evidence-gathering only. |
| Accounts, profiles, inventory, matchmaking, activities, world state | Not implemented | Deliberately out of scope until each dependency is independently documented. |

The latest client run reached the post-ServerHello encrypted BAP boundary and remained at the loading screen because service 121 was capture-only. The next lab listener returns only the evidence-backed service-122 acknowledgement; it does not speculate about later encrypted services. This is progress relative to the original discovery-only baseline, not a claim of playable offline Destiny 2.

## Safety and research rules

- Never allow the research client to contact Bungie or public production infrastructure.
- Never forward, NAT, proxy, or tunnel client traffic to the Internet.
- Use only narrowly scoped, documented local interception and DNS mappings.
- Keep raw captures, certificates, local network details, database URLs, credentials, tokens, and generated session material outside the repository.
- Record observed facts separately from hypotheses.
- Implement one evidenced protocol boundary at a time; do not add speculative behavior merely to clear a screen.
- Preserve backups and rollback steps before changing client or network configuration.

## Architecture

```text
Historical client (isolated)
        |
        v
Lab gateway / DNS observer / packet capture
        |
        X  no forwarding, NAT, or WAN access
        |
        v
Local HTTPS + BAP lab listener
        |
        +-- clean-room Python protocol helpers
        +-- PostgreSQL sanitized experiment-event store
```

The repository contains the reusable clean-room Python components. The active HTTPS/BAP listener, TLS material, manifest cache, capture files, and lab configuration are runtime-local inputs and are intentionally not committed.

### Implemented repository components

- `discovery.py` — narrow UDP NatProbe request classification and local reply construction.
- `storage.py` and `migrations.py` — PostgreSQL migrations and sanitized append-only event storage.
- `signon.py` — minimal SignOn protobuf response and ephemeral session material.
- `content_config.py` — strict version-2 local manifest-cache parsing and ContentConfig response encoding.
- `bap.py` — BAP channel-start and ServerHello response helpers, including the authenticated ServerHello envelope.
- `server.py` — UDP discovery adapter.
- `tests/` — deterministic protocol-unit tests and local socket-oriented validation.

## Protocol progress

The documented sequence currently observed in the isolated Sunrise external-server experiment is:

1. UDP discovery / NatProbe
2. HTTPS `POST /SignOn`
3. HTTPS `GET /config/`
4. BAP plaintext channel start: service 30 → service 31
5. BAP plaintext ServerHello: service 25 → service 26
6. First AES-GCM encrypted BAP request — captured, not yet decoded or answered

Sunrise’s public implementation shows why the next step matters: after service 26, it arms per-connection send/receive nonces and authenticates encrypted frames with AES-GCM. The next research test is to decrypt the observed frame without recording secrets or raw payloads, record its service ID/task ID/body size, and add only the corresponding evidence-backed behavior after a fresh trace.

## Local development

Requirements:

- Python 3.11+
- PostgreSQL for discovery-event storage
- An isolated lab environment for live experiments

Create a development environment and run the test suite:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest
python3 -m compileall -q src
```

The package dependencies include `psycopg` for PostgreSQL and `cryptography` for the documented BAP cryptographic envelope. Do not commit database URLs or runtime secrets. For discovery migration and listener configuration, start from the checked-in systemd template under `deploy/systemd/` and provide a root-readable local environment file outside Git.

## Documentation

- `docs/architecture/service-foundation.md` — service constraints, storage decision, and validation gates.
- `docs/experiments/2026-08-15-external-signin.md` — evidence record for the current SignOn, ContentConfig, and BAP sequence.
- `docs/client-analysis/sunrise.md` — Sunrise external-server integration notes.
- `docs/experiments/sunrise-external-server.md` — controlled experiment template.

## Repository hygiene

This is a public research repository. Do not commit:

- Destiny binaries, extracted game assets, or copyrighted dumps
- encryption/signing keys, accounts, credentials, or session tokens
- raw packet captures, TLS material, database URLs, or local configuration files
- private IP addresses, hostnames, MAC addresses, router details, or other LAN identifiers
- unreviewed AI-generated material that lacks an evidence source or test

## Acknowledgements

[Sunrise](https://github.com/stanuwu/Sunrise) is used as a client-side research baseline. The working reference fork is [a-wild-missingno/Sunrise](https://github.com/a-wild-missingno/Sunrise). Sunrise retains its own authorship, license, notices, and project rules. Old-School-D2 does not copy Sunrise source into this repository; it independently documents and implements only the lab behavior required by controlled experiments.
