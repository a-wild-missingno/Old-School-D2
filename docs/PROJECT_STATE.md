# Project State

## Ultimate Goal

Build a clean-room, isolated-lab replacement service that documents and reproduces only evidence-backed historical-client service boundaries for preservation research. It must never contact, proxy, or provide access to production Bungie infrastructure.

## Current Client Frontier

**CONFIRMED:** The isolated external client reaches an authenticated encrypted BAP connection and remains in a stable black-screen wait while service `250 -> 251` keepalives continue. No later client request was observed during the documented window.

**CURRENT FRONTIER:** the internal/default oracle now proves that client task `ENUM(0)` completion is immediately followed (16 ms) by one-way service 29; external stable wait lacks both observed service 29 and equivalent task-timed evidence.

## Confirmed Protocol Progress

- **CONFIRMED:** external Sunrise initialization, isolated routing, and two NatProbe exchanges.
- **CONFIRMED:** TLS, `POST /SignOn`, and accepted minimal SignOn response.
- **CONFIRMED:** `GET /config/` and accepted ContentConfig response.
- **CONFIRMED:** BAP plaintext `30 -> 31` and `25 -> 26`.
- **CONFIRMED:** encrypted `121 -> 122`, `302 -> 303`, `304 -> 305`, and recurring `250 -> 251`.
- **CONFIRMED:** no later client-originated route in the bounded external post-BAP observation.
- **CONFIRMED:** internal/default and external ledgers share `30 -> 31`, `25 -> 26`, `121 -> 122`, `302 -> 303`, `304 -> 305`, and a second `302 -> 303` before their first route difference.
- **CONFIRMED:** internal then emits five service-`29` requests with no correlated reply before its first `250 -> 251`; external instead next emits `250 -> 251` and does not emit service `29` in its bounded stable-wait record.

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

**CONFIRMED:** the first actual ordered route divergence before client service `10` is the absent external service `29` notification.

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

Deploy the dedicated payload-free external trace artifact to a separate Windows runtime copy, prove the known-good external-validation copy unchanged, and run one Human/UI-gated external observation. Determine whether `ENUM(0)` completes before stable wait and whether service 29 follows. Do not add a service-29 reply or emit Queuez service `123`.

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
