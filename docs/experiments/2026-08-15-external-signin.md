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

The listener now implements only the source-documented service-30 bootstrap: it returns service 31, status 200, preserves the task id and echoes the body, while keeping the connection open for the next frame. A local socket smoke test confirmed that exact response. It still does not answer later BAP services, including service 25 / ServerHello, until a fresh client run captures the next frame.

## Next session

1. Launch the client once with capture active and record whether `/config/` is requested and served.
2. Correlate the client-visible result with the sanitized listener event metadata.
3. Implement only the next observed boundary. If the client reaches `30974`, retain BAP as capture-only until its first frame is documented.

## Preservation

Raw packet captures, request bodies, TLS materials, database URLs, and generated SignOn session material remain local and are not committed.
