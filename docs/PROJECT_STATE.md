# Project State

## Current client frontier

Last confirmed working state: the isolated client completed local SignOn, ContentConfig, BAP 30→31, 25→26, 121→122, 302→303 twice, 304→305, and repeated 250→251 on one authenticated BAP connection.

First confirmed failing state: after the 304→305 reply, the visible client moved from white loading to a black screen and did not issue a later route during the fresh two-minute capture window.

Current blocker: no client family-subscription request was observed after the authenticated bootstrap. Character select is not reached.

## Last successful test

- Latest live evidence: 2026-08-15 fresh isolated launch; redacted ledger in `docs/experiments/2026-08-15-post-bap-transition-baseline.md`.
- Latest automated diagnostic test: `tests/test_post_bap_probe.py` (prepared 2026-08-16; run before the next launch).

## Confirmed findings

- UDP discovery services are system-managed and active on their two lab ports.
- The local HTTPS/BAP listener is a separate runtime-local script, not a systemd service. It was not running at session reconstruction.
- The BAP external listener authenticates the documented bootstrap requests and records only metadata for them.
- In Sunrise, encrypted deferred Queuez sends are evaluated from `bap_route.cpp` after a frame or on a transport poll, but `queuez_deferred_push.cpp` requires previously armed per-session Queuez state. The shown startup path does not establish that state before a subscription/outcome.
- Sunrise contains a client Queuez family-zero hook whose source comments state that an empty source list results in no family-zero record and no subscription. The controlled client was running with its client log threshold at `warn` and file sink disabled, so its installation/seed status was not observable in the completed launch.
- On 2026-08-16, a fresh launch reproduced the boundary with 304→305 followed only by a second 302→303 and 250→251 keepalives. The TCP BAP connection remained established through capture stop; no service 12 arrived.
- The controlled-client settings were backed up and changed only to enable the Sunrise file sink and `client=info` logging for the next launch. The artifact and external-server endpoint fields were not changed. An initial full JSON reserialization exceeded Sunrise's 64 KiB settings-loader cap and caused a local launch-content error; it was rolled back immediately. The final edit changes two existing scalar values in place and is 45,186 bytes, below the cap.

## Active hypotheses

1. **Likely:** the client-side Queuez family-zero hook is not installed or not seeded for the actual deployed client, so it never sends the candidate service-12 subscription. The next launch will distinguish this through now-enabled client runtime logs while the listener records the 304→305 post-BAP boundary.
2. **Possible:** the Queuez hook seeds successfully but another client-side readiness condition suppresses the first subscription.
3. **Possible:** a still-unidentified pre-subscription response/state semantic is incomplete. No Queuez frame will be fabricated to test this.

## Failed hypotheses / dead ends

- Empty replies for 121→122 and 302→303 are not the known discrepancy: Sunrise maps both to empty reply bodies.
- A server-initiated Queuez push is not justified merely by the black screen. Reference deferred Queuez publication requires prior per-session Queuez state.

## Current server architecture

- Systemd-managed clean-room UDP discovery package: `old_school_d2_service`.
- Runtime-local TLS/SignOn/ContentConfig/BAP listener: `/home/syzygy/destiny-re/network/20260814-161330/listener/sunrise_lab_listener.py`.
- Listener runtime inputs (certificate/key, local manifest cache, configured GUID) remain outside Git.
- The listener now emits one redacted `post_bap_wait` event after sending 304→305. It changes no wire behavior and is intended to align the next capture with the client-side Queuez diagnostic.

## Known services / ports

- UDP discovery: 3074 and 3075.
- HTTPS: 443 when the runtime-local listener is running.
- BAP TCP: 30974 when the runtime-local listener is running.
- No forwarding is enabled on the lab gateway; verify before each launch.

## Recent important commits

- `c2a2299` docs: record external post-BAP differential
- `36030e5` test: record external post-BAP transition baseline
- `264c4ab` feat: support external SignOn bootstrap handoff

## Next experiment

Question: does the controlled client log a Queuez family-zero installation/seed result after the documented 304→305 boundary, and does it emit service 12?

One change since the reproduced 2026-08-16 launch: client settings now enable the existing Sunrise file sink and `client=info` diagnostics. The listener retains metadata-only `post_bap_wait` logging. No protocol body, account, character, entitlement, or Queuez notification is added.

## How to start the lab

1. Confirm the client is stopped and capture is not active.
2. Verify gateway forwarding is disabled and run `scripts/verify-legion-isolation.sh`.
3. Start the runtime-local listener with its local runtime inputs; confirm TCP 443 and 30974 are bound.
4. Confirm both discovery systemd units are active and own UDP 3074/3075.
5. Start `scripts/start-legion-capture.sh`; record the printed capture path.
6. Launch exactly one client test.

## How to stop the lab

1. Run `scripts/stop-legion-capture.sh`.
2. Stop only the runtime-local listener started for the experiment; do not stop SSH, DNS isolation, or discovery services unless an experiment specifically requires it.

## How to capture traffic

- Start: `/home/syzygy/destiny-re/network/20260814-161330/scripts/start-legion-capture.sh`
- Stop: `/home/syzygy/destiny-re/network/20260814-161330/scripts/stop-legion-capture.sh`
- Analyze only redacted metadata or local, non-Git artifacts.

## Important paths

- Repository: `/home/syzygy/dev/old-school-d2-service`
- Sunrise reference: `/home/syzygy/dev/Sunrise-reference`
- Lab runtime root: `/home/syzygy/destiny-re/network/20260814-161330`
- Listener log: `logs/sunrise-lab-listener.jsonl`
- Captures: `captures/`

## Windows SSH command

`ssh -i ~/.ssh/hermes_legion missingno@192.168.0.225`
