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

**UNKNOWN:** the ordered authenticated traffic in a full, instrumented internal/default launch has not yet been captured. The internal oracle process launched during this session initialized the instrumented local transport but did not reach BAP authentication, so it produced no `post_auth_send` record. See `docs/experiments/2026-08-16-internal-post-auth-oracle.md`.

## Consequence for the external replacement

Do not wire `BapConnectionState.build_notification()` into the external runtime. The next bounded task is to obtain a full internal/default BAP-authenticated trace first, then compare the first source-emitted outbound event with the external stable wait.