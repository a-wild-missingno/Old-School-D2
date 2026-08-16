# Continuation prompt — external Sunrise parity

Continue the isolated external Sunrise validation on syzygy. Read this entire prompt first, then inspect the named primary artifacts instead of relying only on this summary. Do not ask Emily to repeat the completed evidence.

## Completed, frozen boundaries

External STUN, TLS, SignOn, and ContentConfig are confirmed working and must not be modified without direct contradictory evidence.

```text
STUN → TLS → POST /SignOn → HTTP 200 SignOn protobuf → SignOn _success
→ GET /config/ → ContentConfig accepted → package_registration → BAP sign-in
```

The latest external ContentConfig run is a PASS. The external client accepted the exact internal/default ContentConfig artifact, left `bootflow:content_check`, completed `bootflow:package_registration`, entered `bootflow:bap_signin`, and opened TCP to the passive BAP observer.

## Current frontier / stop boundary

The first next observed boundary is BAP TCP at `192.168.0.129:30974`. The client opened one connection and sent a 140-byte payload. The observer intentionally returned nothing. The client timed out after about 10 seconds in `bootflow:bap_signin`, then entered cleanup. The white/class-icon UI was the resulting BAP timeout, not a ContentConfig failure.

No BAP behavior was implemented or changed during the ContentConfig validation. Do not resume BAP work automatically unless the new user request explicitly authorizes that next boundary.

## Exact confirmed ContentConfig facts

- Internal/default request bytes: `sunrise://local/config` (22 bytes); it is in-process, so it has no native HTTP headers/framing.
- External client request: `GET /config/ HTTP/1.1` through TLS to the configured `https://192.168.0.129/config/`.
- Exact accepted body: 105,232 bytes; SHA-256 `ba9288666f5871f51e8300392d10b06a611ff74803b31394aad49e532d9ef572`.
- Field-5 manifest GUID: `09d54b23-9aec-88c0-8d21-69e89d62197a`.
- Body composition: 19 entitlement definitions and 2,199 package rows.
- External `config_guid` was changed by a bounded settings edit to the exact field-5 GUID, with a timestamped backup first. Never bulk-reserialize Sunrise settings: the loader has a 64 KiB limit.

## Key source and result documents

1. `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/docs/CONTENT_CONFIG_ORACLE.md` — source-backed internal contract, captured body semantics, GUID relationship, and external comparison.
2. `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/docs/EXTERNAL_CONTENTCONFIG_RESULT.md` — final pass report and exact stop boundary.
3. `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/external-contentconfig/raw/sunrise.log` — client proof: `content_config stage=external result=ok`, then package registration and BAP timeout.
4. `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/logs/contentconfig-tls.jsonl` — SignOn and successful `/config/` request/response metadata.
5. `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/logs/contentconfig-bap-observer.jsonl` — initial BAP accept and 140-byte client payload.
6. `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/captures/contentconfig-external.pcap` — capture SHA-256 `550fc28780509b4fa83582f6793b54ffe76089991df281f00922c9ebaaf5cf13`.

## Harness and source locations

- External SignOn/ContentConfig harness: `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/signon_parity/`.
  - `signon_server.py` handles only demonstrated SignOn and exact `/config/`; unknown routes are explicitly logged/404.
  - `content_config.py` validates the fixture’s field-5 GUID before serving.
  - Fixture: `fixtures/internal-contentconfig-response.bin`; checksum in `fixtures/SHA256SUMS`.
  - Tests: `6 passed` using `/home/syzygy/dev/old-school-d2-service/.venv/bin/python -m pytest -q` from that harness directory.
- Clean upstream source checkout: `/home/syzygy/dev/Sunrise-upstream-clean`, source oracle base `b12a9dab780f47c89f1c147d4a8ef3ddbc839734`.
- Instrumented internal oracle commit: `c82d3a6`, pushed to `jules-the-ai/sunrise-external-lab` branch `validation/upstream-b12a9da`. This added only request/response artifact capture and built successfully.
- Pristine external runtime: `C:\Sunrise-ExternalValidation`; exact deployed DLL SHA-256 `9F2FD0EF85B818EEB74E92A4DC33D151E242499CFCCEF08FA2E96FA45DC5C9AE`.
- Internal oracle runtime: `C:\Sunrise-InternalConfigOracle`.
- Legion / D2 client: `192.168.0.225`; OptiPlex harness: `192.168.0.129`.

## Repository state

This repository has the documented state in `docs/PROJECT_STATE.md` and `docs/EXPERIMENTS.md`; ContentConfig documentation commit is `3f2c119`. Keep unrelated untracked `.hermes/` and `0001-feat-add-encrypted-BAP-notification-foundation.patch` untouched.

## Safety and launch discipline

- Preserve all existing work, settings backups, and packet captures.
- Confirm Legion SSH and Internet isolation before any future run.
- Confirm no stale TCP/443, UDP/3074/3075, or TCP/30974 listeners before starting controlled services.
- Start capture before launching Destiny.
- Do not log or retain passwords, credentials, tokens, or SSH secrets.
- Do not infer success from HTTP 200 alone; inspect client state and request/response artifacts.
- Stop after the first authorized boundary and document exact evidence.

## Suggested next task only if explicitly authorized

Build a known-good internal BAP oracle for the captured 140-byte initial client request, compare it with the passive external observation, and implement only the minimal proven response required to reach the next state. Do not alter STUN, SignOn, or ContentConfig.
