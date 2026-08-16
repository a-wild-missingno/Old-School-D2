# Experiments

## EXPERIMENT ID: 2026-08-15-post-bap-baseline

**DATE/TIME:** 2026-08-15T21:46:00Z–21:48:00Z

**QUESTION:** Does the external listener receive a route after the authenticated BAP bootstrap?

**CLIENT CONFIG:** Controlled Sunrise external-server experiment. Raw settings and runtime identifiers remain local.

**SERVER CONFIG:** External SignOn bootstrap handoff branch at `c2a2299`; documented replies only through 250→251.

**CHANGE:** Existing 304→305 and echo handling were active; no unsolicited Queuez message was sent.

**OBSERVATION:** Title/start → white loading → black screen; character select did not appear.

**NETWORK EVIDENCE:** SignOn, ContentConfig, 30→31, 25→26, 121→122, 302→303 twice, 304→305, then only 250→251 in the launch interval. Redacted ledger: `docs/experiments/2026-08-15-post-bap-transition-baseline.md`.

**SERVER EVIDENCE:** Metadata-only listener events corroborate each listed reply. No later client request was recorded.

**RESULT:** The client advanced from the previous white-screen timeout to an open authenticated black-screen wait, but not to character select.

**CONCLUSION:** This is a server-initiated/client-readiness investigation boundary, not evidence to fabricate Queuez or account data.

**CONFIDENCE:** Confirmed.

**NEXT TEST:** 2026-08-16 diagnostic launch with a metadata-only `post_bap_wait` listener event after the unchanged 304→305 reply. Determine whether a client-side Queuez hook signal or a non-keepalive route occurs.

## EXPERIMENT ID: 2026-08-16-post-bap-client-log-baseline

**DATE/TIME:** 2026-08-16T12:36Z

**QUESTION:** Does a fresh external launch issue service 12 after the authenticated BAP bootstrap?

**CLIENT CONFIG:** External-server mode was confirmed enabled. At this launch the Sunrise file sink was disabled and client log level was `warn`, so information-level Queuez hook diagnostics were not available.

**SERVER CONFIG:** Listener metadata probe from `2247a0e`; unchanged protocol behavior.

**CHANGE:** Added only `post_bap_wait` listener metadata after the existing 304→305 reply.

**OBSERVATION:** Title/start → white loading → black screen; character select did not appear.

**NETWORK EVIDENCE:** The client completed SignOn/ContentConfig and BAP 30→31, 25→26, 121→122, 302→303, 304→305, then a second 302→303 and only 250→251 keepalives. The BAP TCP connection remained established. Capture: `captures/legion-20260816-123302Z.pcap`; metadata log: `logs/post-bap-probe-20260816-123132Z.jsonl`.

**SERVER EVIDENCE:** `post_bap_wait` was emitted immediately after the 304→305 send. No service 12 was received.

**RESULT:** No visible or protocol advance.

**CONCLUSION:** The prior no-service-12 observation is reproducible. It does not establish whether the Queuez hook failed to attach, failed to seed, or was gated elsewhere because required client diagnostics were disabled.

**CONFIDENCE:** Confirmed.

**NEXT TEST:** Enable existing Sunrise file logging and the client information-level threshold only; repeat one controlled launch and inspect the Queuez hook records plus BAP metadata.

## EXPERIMENT ID: 2026-08-16-client-log-config-repair

**DATE/TIME:** 2026-08-16T12:42Z–12:48Z

**QUESTION:** Can existing client Queuez diagnostics be enabled without changing the protocol or exceeding Sunrise's settings-loader limit?

**CHANGE:** Backed up the controlled-client settings. An initial full JSON serializer rewrite was rejected by the client because it expanded the file beyond the 64 KiB loader cap; it was immediately restored. The final edit changed only `file_sink: false` → `true` and the existing logging `client: warn` → `info` tokens in place.

**OBSERVATION:** Final settings parse, preserve external-server mode, and measure 45,186 bytes.

**RESULT:** The diagnostics probe is configured. No game protocol launch has yet occurred with it.

**CONCLUSION:** Do not reserialize Sunrise settings documents wholesale. Make bounded in-place scalar edits and verify the 64 KiB cap before launch.

**CONFIDENCE:** Confirmed.

**NEXT TEST:** One controlled launch; inspect the local Sunrise file log for Queuez hook-install and source-seed records, then correlate with the external listener/capture.

## Queuez source-list fallback / service-12 acknowledgement (prepared)

**Observed boundary:** encrypted BAP completed through services 121/122, 302/303, 304/305, and 250/251. Client logging confirmed Queuez hook installation but no family-zero source-list seed.

**Minimal change:** prefer the client manager's observed key; only when it is zero, seed from Sunrise's checked authored primary SOID. The isolated listener now returns the reference empty acknowledgement for service 12 as service 13. No Queuez notification payload is fabricated.

**Acceptance evidence for the next run:** `result=seeded source=state` (or `source=manager`) in the client log, followed by an authenticated BAP service-12 request and a listener service-13 response.


## EXPERIMENT ID: 2026-08-16-external-contentconfig-parity

**DATE/TIME:** 2026-08-16T14:27Z

**QUESTION:** Does externally hosted `/config/` match internal/default Sunrise ContentConfig sufficiently for the client to advance beyond `bootflow:content_check`?

**CLIENT CONFIG:** Isolated pristine external-validation runtime; `external.config_url=https://192.168.0.129/config/`; `external.config_guid=09d54b23-9aec-88c0-8d21-69e89d62197a`.

**SERVER CONFIG:** Frozen STUN and SignOn behavior; TLS `/config/` returned the exact internal oracle protobuf body with only HTTP framing. No BAP reply behavior was enabled.

**OBSERVATION:** White loading advanced to a black screen, then returned to class-icon loading after BAP timeout; character select did not appear.

**NETWORK EVIDENCE:** The TLS service logged `GET /config/ HTTP/1.1` and `content_config_ok`, returning 105,232 bytes. The passive BAP observer accepted one connection and received a 140-byte payload. Capture: `/home/syzygy/destiny-re/network/20260814-161330/validation/upstream-b12a9da/captures/contentconfig-external.pcap`.

**CLIENT EVIDENCE:** `content_config stage=external result=ok`; 549 ms in `bootflow:content_check`; subsequent `bootflow:package_registration`; then `bootflow:bap_signin`. BAP failed only because the observer intentionally did not respond.

**RESULT:** External ContentConfig accepted.

**CONCLUSION:** This closes the external ContentConfig boundary. BAP is now the next observed protocol/state boundary; it was not changed during this experiment.

**CONFIDENCE:** Confirmed.

**NEXT TEST:** A separately authorized BAP-parity investigation, beginning with the captured 140-byte client payload and known-good internal BAP behavior.
