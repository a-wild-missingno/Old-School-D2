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

## Next session

1. Read the configured ContentConfig GUID after the client is fully stopped.
2. Inspect the Sunrise ContentConfig encoder and the locally installed package/entitlement metadata needed for a minimal valid manifest.
3. Add a narrowly scoped `/config/` response with regression tests and sanitized PostgreSQL observation metadata.
4. Retest and only then implement BAP behavior if the client reaches `30974`.

## Preservation

Raw packet captures, request bodies, TLS materials, database URLs, and generated SignOn session material remain local and are not committed.
