# Post-BAP Reference Differential

## Question

What source-backed outbound action can occur after authenticated BAP bootstrap and before the first client family subscription?

## Confirmed reference behavior

- `src/server/bap/bap_route.cpp:101-112` calls `encrypted::consume_deferred` after a handled frame when output room remains; `:122-133` also calls it on a timed transport poll.
- `src/server/bap/encrypted/queuez/queuez_deferred_push.cpp:101-115` emits nothing unless the authenticated session has an armed Family-4 re-push or an activity keepalive is due.
- `src/server/bap/encrypted/queuez/queuez_outcome_staging.cpp:20-86` arms Queuez publication only from a subscription, unsubscription, or character-selection outcome.
- `src/server/bap/encrypted/routing/bap_service_routing.cpp:40-45` maps client request service 12 to response 13 and its subscription body codec.
- `src/client/hooks/queuez/queuez_hook_lifecycle.h:5-10` states that an empty family-zero source list leaves no family-zero record and no subscription. `family0_subscription.cpp:116-138` logs hook installation; `family0_source_seed.cpp:64-92` logs the first successful seed.

## Differential conclusion

The external listener has no Queuez session state and does not send deferred frames. The available reference call chain does **not** show a generic startup Queuez push that can be safely copied before a client subscription. Therefore an unsolicited service-123 push is not an evidence-backed next change.

The earliest falsifiable candidate is client request service 12, not a fabricated account publication. The next live probe retains all protocol replies and adds only redacted listener metadata after 304→305. Client-side Sunrise diagnostics are required to decide whether the family-zero hook did not attach/seed or whether another readiness gate prevents subscription.

## Probe prediction

- If the Queuez hook is not installed or not seeded, no service 12 will arrive and client diagnostics should show an installation failure or omit the seeded event.
- If it is seeded, the next capture may contain service 12; only then should the external service implement the separately evidenced response/body path.
- If it is seeded but no service 12 occurs, the missing prerequisite remains unknown; do not add a Queuez push.
