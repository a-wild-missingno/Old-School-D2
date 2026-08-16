# Project State

## Ultimate Goal

Build a clean-room, isolated-lab replacement service that documents and reproduces only evidence-backed historical-client service boundaries for preservation research. It must never contact, proxy, or provide access to production Bungie infrastructure.

## Current Client Frontier

**CONFIRMED:** The isolated external client reaches an authenticated encrypted BAP connection and remains in a stable black-screen wait while service `250 -> 251` keepalives continue. No later client request was observed during the documented window.

**CURRENT FRONTIER:** the first proven server-initiated authenticated state publication needed after this stable wait has not been identified or implemented.

## Confirmed Protocol Progress

- **CONFIRMED:** external Sunrise initialization, isolated routing, and two NatProbe exchanges.
- **CONFIRMED:** TLS, `POST /SignOn`, and accepted minimal SignOn response.
- **CONFIRMED:** `GET /config/` and accepted ContentConfig response.
- **CONFIRMED:** BAP plaintext `30 -> 31` and `25 -> 26`.
- **CONFIRMED:** encrypted `121 -> 122`, `302 -> 303`, `304 -> 305`, and recurring `250 -> 251`.
- **CONFIRMED:** no later client-originated route in the bounded post-BAP observation.

## Proven Working Components

`discovery.py`, `signon.py`, `content_config.py`, `bap.py`, `queuez.py` (encoder only), and `runtime/app.py` are clean-room components. The runtime uses ephemeral SignOn/BAP cryptographic material, metadata-only JSONL logging, a local manifest cache, and externally supplied TLS material.

## Current Missing Behavior

Account/character state, Queuez subscription/publication state, and any initial authenticated state publication are absent. A Queuez encoder and generic notification framing are foundations only; they are not authority to send a notification.

## Confirmed Network Architecture

`isolated historical client -> non-forwarding lab gateway/DNS/capture -> local discovery + HTTPS + BAP listener`

The gateway must have no forwarding, NAT/masquerade, tunnel, or WAN route for client traffic. See `docs/network/isolation-plan.md`.

## Server Architecture

- `src/old_school_d2_service/runtime/app.py`: runnable HTTPS/BAP listener.
- `src/old_school_d2_service/runtime/config.py`: environment-only runtime configuration.
- `src/old_school_d2_service/server.py`: PostgreSQL-backed UDP discovery listener.
- `src/old_school_d2_service/bap.py`: one owner for BAP AES-GCM nonces, framing, encryption, and documented responses.

`bap.py` is intentionally not split further in this checkpoint: at 273 lines it is a cohesive, fully covered cryptographic state owner. Splitting it now would create unnecessary nonce-ownership risk without changing behavior.

## Known Protocols / Services / Ports

Configured ports are local configuration, not repository constants: UDP discovery typically uses the documented Sunrise discovery ports; HTTPS and BAP ports are set through `OLD_SCHOOL_D2_*` environment variables. Confirm the live configuration before every experiment.

## Known Client State Model

`DISCOVERY -> SIGNON -> CONTENT_CONFIG -> BAP_CONNECT -> BAP_HANDSHAKE -> BAP_AUTHENTICATED -> INITIAL_STATE_PUBLICATION (not implemented) -> CHARACTER_SELECT (not reached)`

The runtime logs state-before/event/state-after metadata. An unhandled route is diagnostic evidence, not permission to guess a response.

## Current Hypotheses

**LIKELY:** the stable wait requires a source-backed server-initiated authenticated publication tied to per-connection state and account/character prerequisites.

**SPECULATIVE:** the first publication is a Queuez service-123 update. Public-reference structure supports Queuez as an outbound mechanism, but the trigger and valid state body for this exact client path are not proven.

## Failed Hypotheses / Dead Ends

- The black screen is **not** evidence that an earlier `121`, `302`, or `250` acknowledgement should change; each is accepted in the confirmed run.
- An empty or invented Queuez frame is **not** a valid next step.
- No later client request was observed; implementing a guessed client-response route cannot advance this frontier.

## Important Runtime Findings

Raw captures, certificate material, manifest caches, session material, and local addresses are intentionally outside Git. JSONL logs contain metadata and hashes, not plaintext encrypted buffers or bootstrap values.

## Relevant Source Locations

- `src/old_school_d2_service/runtime/app.py`
- `src/old_school_d2_service/bap.py`
- `src/old_school_d2_service/queuez.py`
- `docs/client-analysis/queuez-bootstrap.md`
- `docs/experiments/2026-08-15-external-post-bap-differential.md`

## Relevant Commits

See `git log --oneline --decorate -30`. Historical commits record each confirmed boundary; this stabilization checkpoint records the authoritative documentation and runnable-source consolidation.

## Important Evidence / Artifacts

Detailed experiment documents are indexed by `docs/EXPERIMENTS.md`. Local evidence locations belong only in `.hermes/HANDOFF.local.md`; capture files are never committed.

## Next Experiment

First trace and document the earliest reference-server post-auth outbound send site reachable before a client subscription request. Add metadata-only instrumentation at that seam, then run exactly one isolated experiment. Do not emit a notification until its trigger, route, and body are independently evidenced.

## Things That Must Not Be Reopened Without New Evidence

Do not change discovery, SignOn, ContentConfig, BAP nonce ownership, or the accepted `121/122`, `302/303`, `304/305`, and `250/251` behavior. Do not add Queuez bootstrap/account state as part of repository maintenance.
