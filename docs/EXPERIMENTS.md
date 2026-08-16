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
