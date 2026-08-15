# Queuez / server-initiated BAP bootstrap notes

## Scope and evidence boundary

This note records a public-source review of Sunrise at revision
`b12a9dab780f47c89f1c147d4a8ef3ddbc839734` (2026-08-14). It is a behavioral
reference for the isolated lab, not a specification for any production Destiny
service. Raw captures, session material, and client payloads remain outside
this repository.

## Confirmed live prerequisite state

In the isolated external-server experiment, the client has accepted the
client-driven encrypted BAP bootstrap through `121 -> 122`, `302 -> 303`,
`304 -> 305`, and recurring `250 -> 251`. A two-minute observation produced
24 acknowledged keepalives and no later client request. Therefore the next
boundary is server-initiated, not an unhandled client response.

## Public-reference findings

| Finding | Public source location | Confidence |
| --- | --- | --- |
| Deferred outbound BAP work runs after frame handling and during a transport poll. | `src/server/bap/bap_route.cpp` (`consume_frame`, `consume_poll`) | High |
| Queuez updates are encrypted notifications with service 123 and uncorrelated sequence 0. | `src/server/bap/encrypted/push/queuez/queuez_update_frame.cpp` (`append`) | High |
| Each complete outbound frame consumes one connection-owned send nonce; failures do not commit it. | `queuez_update_frame.cpp`; `queuez_deferred_push.cpp` | High |
| Queuez data is produced from a prepared family snapshot, not an empty generic response. | `push/queuez/queuez_subscription.cpp` | High |
| Publication depends on per-connection Queuez state plus selected account/character and subscription/activity transitions. | `bap_connection_publication.*`, `push/queuez/queuez_subscription.cpp` | High |

## Minimal family-body format now modeled

The public reference encodes a Queuez notification body as a big-endian family
count followed by packed family records. A family record contains its 32-bit
type, 64-bit root key, signed 32-bit version, one-byte flags, and 32-bit object
count. Each object record contains a 32-bit definition id, 64-bit version,
32-bit payload size, 32-bit encoding selector, then unchanged payload bytes.

The clean-room implementation now supports deterministic empty families and
object records using the documented encodings 1 through 4. For encoding 3
(raw), it validates that the payload starts with that object's 64-bit version
in little-endian form. It remains deliberately disconnected from the runtime
listener: producing a well-framed family body is not evidence that it names
valid account, character, or activity state for this client.

## Implications for Old-School-D2

1. A service-123 transport envelope alone is insufficient. Its body must be a
   validated Queuez family update backed by state that this project does not
   yet model.
2. The live listener must not emit an empty or invented Queuez update merely to
   clear the black screen.
3. The reusable next increment is transport-only: provide an authenticated,
   uncorrelated notification builder that uses the active connection send
   nonce, fixed sequence zero, and no implicit service/body selection.
4. A later Queuez body codec needs a separately evidenced family schema and
   deterministic fixtures before it can be wired to the lab listener.

## Trigger analysis

The public route maps client service 12 to the family-subscription response
service 13 and appends Queuez publications only as a side effect of that
subscription. A Family-3 subscription may also cause its Family-4 companion
and a banner update. Deferred re-pushes are armed only after a prior
subscription publication.

The observed isolated-client trace contains no service-12 request after BAP
bootstrap; it transitions directly to service-250 keepalives. Therefore the
minimal body encoder is a verified framing component, not authority to send a
notification. The missing boundary to investigate is what prevents this client
configuration from entering the client-driven subscription path.

## Next evidence required

- Identify the first trigger that supplies the required Queuez subscription or
  state transition for this exact client path.
- Derive a minimal, deterministic family body from public-source structure,
  without importing client assets or proprietary record data.
- Test frame construction/decryption locally before an explicit, disabled by
  default one-message lab experiment.
