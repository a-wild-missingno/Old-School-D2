# Post-auth BAP oracle investigation

## Scope

This record separates public-reference source facts from the attempted controlled internal/default oracle run on 2026-08-16. It does not contain captured payloads, account data, session material, client binaries, or local-network identifiers.

## Source-backed outbound paths

The public Sunrise reference is pinned at `b12a9dab780f47c89f1c147d4a8ef3ddbc839734`. Metadata-only tracing was added in a separate local research checkout and compiled by its Windows CI build; that instrumentation is not copied into this repository.

| Candidate | Trigger | BAP classification | Required state | Confidence |
| --- | --- | --- | --- | --- |
| correlated reply | a handled encrypted client request with `ResponseMode::reply` | encrypted, correlated response | authenticated connection and request route | CONFIRMED from `encrypted_runtime.cpp` and `reply/bap_encrypted_reply.cpp` |
| Queuez update | `ServiceOutcome.hasSubscription`, `hasChangeCharacter`, or `hasSelectCharacter` | encrypted uncorrelated service 123 notification | authenticated connection plus the corresponding completed service outcome | CONFIRMED from `queuez/queuez_outcome_staging.cpp` and `push/queuez/queuez_update_frame.cpp` |
| deferred Queuez re-push | a previously armed family/banner re-push reaches its due time during a frame or poll | encrypted uncorrelated service 123 notification | authenticated connection plus previously published Queuez state | CONFIRMED from `bap_route.cpp` and `queuez/queuez_deferred_push.cpp` |
| activity notification | an activity transaction stages notifications | encrypted uncorrelated activity notification | authenticated connection plus an activity transaction | CONFIRMED from `encrypted_runtime.cpp` and `push/activity/activity_notification_frame.cpp` |

## Conclusion from source review

**CONFIRMED:** the reference contains no automatic post-auth Queuez publication simply because the BAP connection became authenticated. Service 123 is Queuez-related, but the source requires a subscription/selection/change outcome, while deferred Queuez sends require a prior armed publication.

**CONFIRMED:** the external baseline has no client service-12 request. Therefore there is no evidence that the external replacement should fabricate an unsolicited Queuez service-123 notification at the stable authenticated wait.

## Superseded preliminary limitation

The former statement that no full authenticated internal/default launch had been captured is superseded by the completed input-driven oracle in `docs/experiments/2026-08-16-internal-post-auth-oracle.md`. Its sanitized route ledger and the external stable-wait ledger share `30 -> 31`, `25 -> 26`, `121 -> 122`, `302 -> 303`, `304 -> 305`, and a second `302 -> 303`.

**CONFIRMED:** before internal client service `10`, the first actual route difference is five internal service-`29` requests with no correlated reply. The external ledger instead next contains `250 -> 251` keepalives and no service `29`. Public source at the pinned reference maps `notification29` to `ResponseMode::none` with the empty body codec. Thus a synthetic reply is contradicted by the oracle; the UNKNOWN is the condition that causes the external client not to issue service `29`. See `docs/experiments/2026-08-17-pre-service10-route-ledger.md`.

## Consequence for the external replacement

Do not wire `BapConnectionState.build_notification()` into the external runtime. The next bounded task is to instrument the dedicated oracle at the client-side transition immediately before its first service-`29` notification and compare that trigger with the external configuration/state.

## 2026-08-17 timestamped task/service-29 correlation

Dedicated-Oracle metadata correlates the first accepted service-29 request to the immediately prior client transition: `world_controller` task `ENUM(0)` completed 16 ms earlier. The Oracle accepted nine one-way service-29 requests with no reply and later observed service 10 while the client reached character select. This supports only ordered correlation; task `ENUM(0)` semantics and causal role are still unknown. External stable-wait evidence has no timestamped retail-task trace yet, so it cannot be equated with a missing task-0 transition.

**Superseded instrumentation privacy interpretation:** the prior dedicated trace source logged formatted retail text locally even though its BAP route tracing omitted packet bodies. It remains evidence for the documented Oracle ordering, but it is not acceptable for the payload-free external observation. The replacement trace artifact records only timestamped numeric task-completion metadata; see `docs/experiments/2026-08-17-external-task-trace-preflight.md`.
