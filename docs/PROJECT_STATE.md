# Project State

## Ultimate Goal

Build a clean-room, isolated-lab replacement service that documents and reproduces only evidence-backed historical-client service boundaries for preservation research. It must never contact, proxy, or provide access to production Bungie infrastructure.

## Current Client Frontier

**CONFIRMED:** The isolated external client reaches an authenticated encrypted BAP connection, emits no-reply service `29` notifications, and remains in a stable black-screen wait while service `250 -> 251` keepalives continue. Client service `10` was not observed during the documented windows.

**CURRENT FRONTIER:** repeated trace-only runs after the privacy-safe SignOn bootstrap handoff reach authenticated BAP and no-reply service 29, but not client service 10 or Queuez service 123. A metadata-only retail callback marker confirms that the task observer receives native callbacks, yet it does not observe the internal-oracle `ENUM(0)` completion diagnostic. A later metadata-only assert classifier observed patchable-bootstrap and investment-globals local load failures after service 29, neither carrying `-87`; it did not observe the registration class. Source review then found that the existing build-data report exposes only eight of eleven prerequisites used by the investment worker completion predicate. The completed eleven-domain probe recorded `all_ready=1` before the same external black-screen/service-10 absence, ruling out incomplete local build-data readiness for that run. Discovery, ContentConfig acceptance, BAP acknowledgement, task-observer installation, and service-29 no-reply behavior remain unchanged.

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

Account/character state, Queuez subscription/publication state, and the semantic condition that advances the client from its no-reply service `29` notifications to client service `10` are absent. A Queuez encoder and generic notification framing are foundations only; they are not authority to send a notification. Reference-source review confirms that Queuez service `123` requires a completed subscription/selection/change outcome or previously armed deferred state; it is not an automatic consequence of BAP authentication.

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

**SUPERSEDED interpretation:** absent external service 29 was once the earliest recorded route difference. Repeated external observations now reach service 29, but not service 10.

**UNKNOWN:** which post-service-`29` semantic condition in the internal/default configuration or client state causes the client to emit service `10`. The source route proves only that a service-29 response is not the missing behavior.

## Failed Hypotheses / Dead Ends

- The black screen is **not** evidence that an earlier `121`, `302`, or `250` acknowledgement should change; each is accepted in the confirmed run.
- An empty or invented Queuez frame is **not** a valid next step.
- Client service `10` was not observed after service 29; implementing a guessed reply or Queuez publication cannot advance this frontier.
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

Compare metadata-only post-service-29 state/trigger conditions between the internal oracle and the external trace. Identify the first evidence-backed condition required for client service 10; do not add a service-29 reply, Queuez service 123, package content, account state, or speculative response.

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

## 2026-08-21 fresh external trace observation

**PARTIAL / pre-semantic failure:** a new trace DLL built by controlled Windows CI was installed only into the dedicated trace runtime. After the required Human/UI gate, the operator reported an immediate Marionberry error. The protected external-validation DLL and settings hashes were unchanged after cleanup.

**CONFIRMED:** the bounded filtered capture contains ten UDP packets at the discovery port and nine TCP SYN packets at the HTTPS port; it contains no TCP SYN-ACK flags, no BAP-port packet, and no runtime HTTPS/BAP JSONL event. At launch, HTTPS/BAP were listening, but the project lab-start command had not started the separately owned UDP discovery responder.

**LIMIT:** the fresh trace log contains no expected trace metadata markers (module, config-lookup, transport, or numeric retail-task completion). Therefore its absence is an instrumentation-observability result, not proof that module initialization or a lookup did not execute. The run cannot establish ENUM(0), service 29, service 10, or an external semantic differential.

**NEXT:** prove the complete, known-good transport baseline (discovery UDP reply and TCP SYN-ACK) before another game observation.

## 2026-08-21 full external transport preflight

**CONFIRMED:** the existing discovery responder was restored to the lab lifecycle beside HTTPS/BAP. A bounded no-game Legion probe directly received recognized NatProbe replies on both configured discovery ports and completed HTTPS TCP connection. The filtered capture recorded two inbound discovery datagrams, two outbound replies, one HTTPS SYN, and one HTTPS SYN-ACK.

**CONFIRMED hygiene:** forwarding remained disabled, public HTTPS remained blocked from Legion, protected external-validation hashes remained unchanged, and all session-owned listeners/capture were stopped.

**LIMIT:** this proves transport baseline only. It does not establish the missing trace metadata, any authenticated route, task completion, or task/service divergence.

## 2026-08-21 complete-baseline external trace observation

**PARTIAL:** after the Human/UI gate, the operator reported configuration-download error `turkey`. The complete local baseline recorded two HTTPS requests, successful SignOn issuance, and a locally served ContentConfig response, but no BAP-port traffic or authenticated application event.

**CONFIRMED trace metadata:** config lookup emitted `success_class`; first outbound transport emitted `pending_class`; module-init and retail-task markers were absent. This absence is not proof of non-execution.

**NEXT:** audit ContentConfig response acceptance structurally against authorized known-good external evidence before another game run.

## 2026-08-21 ContentConfig acceptance audit

**CONFIRMED:** the version-2 local manifest cache's stored build fingerprint matches its complete canonical row set under Sunrise's published fingerprint and UUID derivation. The cache itself is therefore not the first structural mismatch.

**FIRST MISMATCH:** the ContentConfig UUID derived from that verified cache does not equal the separately configured external listener response UUID. The reference encoder writes the cache-derived UUID into top-level field 5, while the Python listener served the configured value. Values and payload bodies are intentionally omitted.

**LIMIT:** this is a source-backed explanation for the observed `turkey` failure, not proof of sole causality. No post-reconciliation game observation has run and BAP/later services remain out of scope.

**NEXT:** reconcile the external runtime's fetch token and listener field-5 UUID to the same verified cache-derived identity, add a preflight identity guard, then perform one new bounded observation. Do not change BAP or later services absent new evidence.

## 2026-08-21 reconciled ContentConfig observation

**CONFIRMED:** after the cache-derived ContentConfig identity was reconciled, the client passed the prior `turkey` boundary and reached the known authenticated encrypted-BAP stable black-screen wait. Metadata recorded `30 -> 31`, `25 -> 26`, `121 -> 122`, `302 -> 303`, `304 -> 305`, and recurring `250 -> 251`.

**LIMIT:** no retail-task completion marker or later client route was observed in this bounded window. Do not change later service behavior without new evidence.

## 2026-08-21 external bootstrap-handoff boundary

**CONFIRMED:** the external trace run carried a SignOn query (value not logged), completed the existing BAP bootstrap, then sent nine service-29 notifications with no listener reply before stable keepalives. This is the first direct external service-29 observation.

**LIMIT:** the user-visible result remained a black screen; client service 10 and server Queuez service 123 were not observed. Local package-load assertions were observed but do not justify copying package data or changing server behavior.

**NEXT:** use the now-aligned service-29 boundary for a metadata-only post-29 differential; preserve the listener's no-reply behavior.

## 2026-08-22 complete build-data readiness probe

**CONFIRMED:** before the probe, external, reference, and upstream-clean source share the same eight-field readiness reporter. The investment worker's actual completion predicate requires three additional flags: spawn sets, hash names, and investment constants. An all-one eight-field log therefore does not prove the worker is complete.

**PROBE RESULT:** the trace-only reporter emitted all eleven bounded booleans and `all_ready=1` before the same service-29/keepalive black-screen route. The CI-built probe changed no refresh, persistence, package handling, or protocol state.

**CONCLUSION:** incomplete investment-worker build-data readiness is ruled out for this run. The result is not evidence that package assertions are causal and does not authorize package or server changes.

**NEXT:** source-only inspect the first native readiness/transition after all-ready that differentiates the internal/default oracle from the external service-10 absence; select one metadata-only probe before another game run.

## 2026-08-22 external package-assert classifier observation

**CONFIRMED:** a Windows-CI-built metadata-only assert classifier ran only in the dedicated external trace runtime. After successful SignOn, ContentConfig, authenticated BAP, and nine no-reply service-29 requests, it classified local `patchable_bootstrap` and `investment_globals` failures. Neither event carried the observed `-87` marker; no registration-class assertion appeared in the bounded run. Client service 10 remained absent.

**LIMIT:** these local assertions are temporally post-bootstrap observations, not proof of a causal service-10 prerequisite. They do not justify package data, server replies, Queuez, or account state.

**NEXT:** source-only compare the post-service-29/local-content ordering between the internal/default oracle and external trace to select one metadata-only readiness/ordering probe before another game run.
