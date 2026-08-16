# Project State

## Ultimate Goal

Build a clean-room, isolated-lab replacement service that documents and reproduces only evidence-backed historical-client service boundaries for preservation research. It must never contact, proxy, or provide access to production Bungie infrastructure.

## Current Client Frontier

**CONFIRMED:** The isolated external client reaches an authenticated encrypted BAP connection and remains in a stable black-screen wait while service `250 -> 251` keepalives continue. No later client request was observed during the documented window.

**CURRENT FRONTIER:** a metadata-only instrumented internal/default runtime has been built and its local transport startup was observed, but the prior bounded run did not include the required title/start-screen Enter-equivalent input. It did not test whether the dedicated runtime can reach BAP authentication. The ordered internal post-auth outbound oracle is therefore still UNKNOWN; no external publication has been implemented.

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

Account/character state, Queuez subscription/publication state, and any initial authenticated state publication are absent. A Queuez encoder and generic notification framing are foundations only; they are not authority to send a notification. Reference-source review confirms that Queuez service `123` requires a completed subscription/selection/change outcome or previously armed deferred state; it is not an automatic consequence of BAP authentication.

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

**LIKELY:** the stable wait requires an additional source-backed authenticated state transition, but the transition need not be an unsolicited publication.

**DISPROVEN for the current evidence:** authentication alone causes an automatic Queuez service-123 publication. The public reference only stages Queuez on a completed subscription/selection/change outcome or from previously armed deferred state.

**UNKNOWN:** the first server-originated event in a full known-good internal/default authenticated run. The 2026-08-16 dedicated runtime did not receive the required title/start input and did not reach BAP authentication, so it cannot establish the required ordering.

## Failed Hypotheses / Dead Ends

- The black screen is **not** evidence that an earlier `121`, `302`, or `250` acknowledgement should change; each is accepted in the confirmed run.
- An empty or invented Queuez frame is **not** a valid next step.
- No later client request was observed; implementing a guessed client-response route cannot advance this frontier.
- A dedicated runtime that starts the Sunrise transport but does not receive title/start input is **not** a post-auth oracle; its lack of a trace event cannot be interpreted as launcher failure or evidence of no publication.

## Important Runtime Findings

Raw captures, certificate material, manifest caches, session material, and local addresses are intentionally outside Git. JSONL logs contain metadata and hashes, not plaintext encrypted buffers or bootstrap values.

## Relevant Source Locations

- `src/old_school_d2_service/runtime/app.py`
- `src/old_school_d2_service/bap.py`
- `src/old_school_d2_service/queuez.py`
- `docs/client-analysis/queuez-bootstrap.md`
- `docs/client-analysis/post-auth-oracle.md`
- `docs/experiments/2026-08-15-external-post-bap-differential.md`
- `docs/experiments/2026-08-16-internal-post-auth-oracle.md`

## Relevant Commits

See `git log --oneline --decorate -30`. Historical commits record each confirmed boundary; this stabilization checkpoint records the authoritative documentation and runnable-source consolidation.

## Important Evidence / Artifacts

Detailed experiment documents are indexed by `docs/EXPERIMENTS.md`. Local evidence locations belong only in `.hermes/HANDOFF.local.md`; capture files are never committed.

## Next Experiment

Run the already-prepared dedicated internal/default oracle runtime with its metadata-only trace DLL and `external_server.enabled=false`; perform exactly one Enter-equivalent title/start input and leave the client running for bounded observation. The run must reach authenticated BAP and produce an ordered metadata-only trace (or a deterministic earlier failure after input). Only then compare that oracle with the external stable wait; do not change the external listener or emit any publication first.

## Things That Must Not Be Reopened Without New Evidence

Do not change discovery, SignOn, ContentConfig, BAP nonce ownership, or the accepted `121/122`, `302/303`, `304/305`, and `250/251` behavior. Do not add Queuez bootstrap/account state as part of repository maintenance.
