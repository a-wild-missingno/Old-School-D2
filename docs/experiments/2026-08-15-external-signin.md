# External sign-in experiment — 2026-08-15

## Scope

Controlled Sunrise external-server experiment with the client isolated from the Internet. The OptiPlex remains non-forwarding; the lab service only responds on explicitly configured local endpoints.

## Observed sequence

1. The client completed the two observed UDP NatProbe exchanges with the PostgreSQL-backed discovery responders.
2. The prior missing HTTPS listener caused TCP resets and the client showed a generic server-unavailable result.
3. With the TLS listener restored, the client completed TLS and issued `POST /SignOn`.
4. A controlled `503` SignOn response kept the client at the generic server-unavailable result.
5. After the minimal binary `200` SignOn response was enabled, the client immediately issued `GET /config/`.
6. The current generic handler returned `503` for `/config/`; the client again showed the generic server-unavailable result.
7. No TCP connection to the configured BAP port followed this config request.

## Interpretation

The client accepted the SignOn transport/response far enough to attempt its separate configured ContentConfig fetch. The next evidenced boundary is ContentConfig, not BAP. A guessed empty config body is intentionally not deployed: the request requires a correctly formed manifest tied to the configured fetch GUID and the locally installed content inventory.

## ContentConfig preflight

Before the next client run, the external ContentConfig boundary was prepared from the public Sunrise source and a locally generated manifest cache. The earlier configured fetch token was not canonical UUID text, while the documented encoder requires a canonical lowercase UUID and the client compares the configured token with ContentConfig field 5. With the client stopped, a byte-preserving settings edit replaced that token with a canonical local UUID and retained a timestamped settings backup.

The lab listener now validates and reads only the exact version-2 local manifest-cache layout, encodes the documented entitlement and package-row protobuf fields, and returns the same configured UUID in field 5. The cache remains a local runtime input and is ignored by Git. A local TLS request received HTTP 200 and a response with the expected field-5 UUID and package-row count. This is a service smoke test, not evidence that the client accepts the response.

## BAP bootstrap observation

The next live attempt passed SignOn and ContentConfig, then opened the configured BAP TCP port. Its first complete frame was a 140-byte plaintext-type-2 request for service 30 with task id 0 and a 128-byte body. The previous capture-only listener read that frame and immediately closed the connection, which explains the client waiting at the white loading screen.

The listener now implements only the source-documented service-30 bootstrap: it returns service 31, status 200, preserves the task id and echoes the body, while keeping the connection open for the next frame. A local socket smoke test confirmed that exact response.

The subsequent live run captured plaintext service 25 (ServerHello), task id 1, with the documented 36-byte body. The service now keeps the ephemeral SignOn keys and token only in listener memory for the active lab run and returns the source-documented service-26 envelope: AES-128-CBC encrypted nonce/key material authenticated with HMAC-SHA256. A local SignOn-to-BAP smoke test verified the sequence through service 26 without logging or persisting key material. Post-hello encrypted BAP frames remain capture-only until a fresh client run identifies the next request.

## Current encrypted-BAP boundary

The latest controlled run completed services 30 and 25/26, then sent one 28-byte type-1 encrypted BAP frame (22-byte payload: the fixed 16-byte authentication tag plus 6 ciphertext bytes). The listener correctly recorded only its framing metadata and did not answer it; the client closed that BAP connection after its timeout. The client-visible result remained the white loading screen.

Sunrise's public BAP path indicates that the next request uses AES-GCM with a connection-owned receive nonce: it starts from the service-26 nonce with the final byte direction-marked, authenticates/decrypts the frame with the generated BAP session key, and advances the nonce after a valid frame. The current lab listener generated this material for service 26 but does not yet retain it per TCP connection, so it cannot safely decode the captured request.

## Next session

1. Add a deterministic, non-secret test harness for connection-scoped BAP nonce/key state and AES-GCM frame opening.
2. Retain BAP state only for the active TCP connection, decrypt the first encrypted request in memory, and log only service ID, task ID, body length, and authentication outcome.
3. Run one controlled client attempt and implement only the identified response route if the decrypted request and Sunrise reference agree.

## Preservation

Raw packet captures, request bodies, TLS materials, database URLs, and generated SignOn session material remain local and are not committed.

## Prepared encrypted-frame observation

Before the next run, the lab listener was changed to retain the generated BAP session key and receive nonce only inside the active TCP handler. It validates a type-1 outer frame, authenticates and decrypts it with AES-GCM, advances the little-endian receive nonce only after a valid request, and records only authentication outcome, service ID, task ID, and body length. It deliberately sends no encrypted response. Unit tests cover successful decryption/nonce advancement and rejected-tag behavior; a deterministic local encrypted-frame smoke test passed.
