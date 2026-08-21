# Project State

## Ultimate Goal

Build a clean-room, isolated-lab replacement service that documents and reproduces only evidence-backed historical-client service boundaries for preservation research. It must never contact, proxy, or provide access to production Bungie infrastructure.

## Current Client Frontier

**CONFIRMED:** The isolated external client reaches an authenticated encrypted BAP connection and remains in a stable black-screen wait while service `250 -> 251` keepalives continue. No later client request was observed during the documented window.

**CURRENT FRONTIER:** binary identity is the first directly evidenced trace-vs-baseline startup divergence: the trace artifact digest differs from the known-good external-validation DLL. Marionberry occurred before listener application traffic with that different DLL, but causality, the responsible hook, and the external semantic differential remain UNKNOWN.

## Confirmed Protocol Progress

- **CONFIRMED:** external Sunrise initialization, isolated routing, and two NatProbe exchanges.
- **CONFIRMED:** TLS, `POST /SignOn`, and accepted minimal SignOn response.
- **CONFIRMED:** `GET /config/` and accepted ContentConfig response.
- **CONFIRMED:** BAP plaintext `30 -> 31` and `25 -> 26`.
- **CONFIRMED:** encrypted `121 -> 122`, `302 -> 303`, `304 -> 305`, and recurring `250 -> 251`.
- **CONFIRMED (historical non-task record only):** one bounded external post-BAP observation recorded no later client-originated route.
- **CONFIRMED:** internal/default and external ledgers share `30 -> 31`, `25 -> 26`, `121 -> 122`, `302 -> 303`, `304 -> 305`, and a second `302 -> 303` before their first route difference.
- **CONFIRMED:** internal emits service-`29` requests with no correlated reply before its first `250 -> 251`. A historical external stable-wait ledger lacks service 29, but without equivalent task-timed evidence it does not establish the earliest semantic differential.

## Proven Working Components

`discovery.py`, `signon.py`, `content_config.py`, `bap.py`, `queuez.py` (encoder only), and `runtime/app.py` are clean-room components. The runtime uses ephemeral SignOn/BAP cryptographic material, metadata-only JSONL logging, a local manifest cache, and externally supplied TLS material.

## Current Missing Behavior

Account/character state, Queuez subscription/publication state, and the semantic condition that causes the client to issue its first no-reply service `29` notification are absent. A Queuez encoder and generic notification framing are foundations only; they are not authority to send a notification. Reference-source review confirms that Queuez service `123` requires a completed subscription/selection/change outcome or previously armed deferred state; it is not an automatic consequence of BAP authentication.

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

**CONFIRMED:** the first new uncorrelated publication in the complete internal/default run is encrypted service `123` (`queuez_update`), immediately after client service `10` and its correlated service `11` reply. This comes from metadata-only trace evidence, not captured payloads.

**SUPERSEDED interpretation:** the historical ledger made absent external service 29 the earliest *recorded route* difference before client service 10. It cannot establish the earliest semantic differential without a successful task-timed external observation.

**UNKNOWN:** which pre-service-`29` semantic condition in the internal/default configuration or client state causes the client to send that no-reply notification. The source route proves only that a response is not the missing behavior.

## Failed Hypotheses / Dead Ends

- The black screen is **not** evidence that an earlier `121`, `302`, or `250` acknowledgement should change; each is accepted in the confirmed run.
- An empty or invented Queuez frame is **not** a valid next step.
- No later client request was observed; implementing a guessed client-response route cannot advance this frontier.
- Service `29` is not a missing acknowledgement: the reference routes `notification29` as `ResponseMode::none` with an empty body codec, and the internal oracle progresses after five such no-reply requests. Adding a synthetic service-`29` reply would contradict the oracle.
- Service `123` must not be sent during the external stable wait: its first observed internal emission followed client service `10`, which is absent externally.

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
- `docs/experiments/2026-08-17-pre-service10-route-ledger.md`
- `src/old_school_d2_service/authenticated_route_ledger.py`

## Relevant Commits

See `git log --oneline --decorate -30`. Historical commits record each confirmed boundary; this stabilization checkpoint records the authoritative documentation and runnable-source consolidation.

## Important Evidence / Artifacts

Detailed experiment documents are indexed by `docs/EXPERIMENTS.md`. Local evidence locations belong only in `.hermes/HANDOFF.local.md`; capture files are never committed.

## Next Experiment

Diagnose why the dedicated external trace runtime reaches a client-visible Marionberry error before it produces an authenticated application event. First establish, with metadata-only trace/source evidence, whether the trace DLL changes the external transport/startup path relative to the known-good external-validation runtime. Do not add a service-29 reply or emit Queuez service `123`.

## Things That Must Not Be Reopened Without New Evidence

Do not change discovery, SignOn, ContentConfig, BAP nonce ownership, or the accepted `121/122`, `302/303`, `304/305`, and `250/251` behavior. Do not add Queuez bootstrap/account state as part of repository maintenance.


## 2026-08-17 service-29 trigger oracle

**CONFIRMED:** The dedicated internal/default Oracle reached character select after task `ENUM(0)` completed and then emitted nine accepted one-way service-29 requests. The first request was observed 16 ms after the completion. The same bounded run emitted service 10 afterward. Service 29 needs no reply; adding one remains contraindicated.

**LIMIT:** This is a temporal correlation, not proof that `ENUM(0)` causes service 29. External stable wait still has no equivalent client task timing, so its first missing semantic condition remains unresolved.

**NEXT:** Instrument the external-validation observation with the same timestamped retail-task metadata and compare the task-0/service-29 boundary.

## 2026-08-17 external task-trace preflight

**CONFIRMED:** inspection found the prior dedicated trace source wrote formatted retail-log text, so it could not meet the payload-free external-observation constraint. The dedicated trace branch now emits only timestamped numeric task-completion metadata; Windows CI build `32069461540` succeeded for source commit `d025f3d`, producing the documented artifact digest.

**CONFIRMED:** immediately before any client launch, the replacement listener and capture were stopped, relevant local listener ports were unoccupied, and the OptiPlex reported IPv4/IPv6 forwarding disabled.

**NOT OBSERVED:** no external client run occurred. The Windows validation baseline's DLL/settings hashes, trace-copy deployment, client isolation, task `ENUM(0)`, and service 29 status remain unverified because this session had no configured Windows target or verified Legion interactive control. This is procedurally inconclusive.

## 2026-08-17 external task-0/service-29 observation

**FAIL (bounded observation):** after the Human/UI gate, the operator immediately observed Marionberry. The dedicated trace log recorded external-hook and config-getter installation, but zero `retail_task` completion records. The local replacement listener recorded no HTTP or BAP application event beyond its own startup, so no authenticated service 29 metadata was observed.

**LIMIT:** this does not demonstrate absent task 0 or absent service 29. The run failed before the task/service boundary. The historical non-task external ledger remains evidence of its own capture but does not establish the earliest semantic divergence.

**CONFIRMED hygiene:** the dedicated trace copy was removed, its client process was stopped after the observation, and the known-good external-validation DLL/settings hashes remained unchanged. The bounded raw capture was discarded because it included SSH control traffic; only sanitized metadata is documented.


## 2026-08-21 external trace provenance comparison

**CONFIRMED:** current metadata shows the known-good external-validation DLL SHA-256 is 9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae, while the trace artifact recorded for the failed observation has SHA-256 3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e. This binary-identity difference precedes configuration lookup, transport, and listener application traffic.

**LIMIT:** the trace copy is correctly absent after cleanup. The documented trace source commit is unavailable in this repository and its CI run was not retrievable through either recorded remote, so source-level hook and installed-trace-settings comparison are unavailable. This does not prove the trace DLL caused Marionberry.

**NEXT:** recover an authorized source/build record and require a Windows-CI rebuild to reproduce the documented trace DLL digest before adding metadata-only startup/transport stage markers.
