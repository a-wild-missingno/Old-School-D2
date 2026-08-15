# External post-BAP differential and next-session handoff

## Verified completed work

- The external client hook automatically forwards the runtime bootstrap value only on the HTTPS SignOn route. The value remains in process memory and is not logged or stored.
- The isolated listener validates that handoff and inserts the source-matched optional SignOn config blob.
- The Windows x64 Sunrise client build passed in CI. The active Legion `D:\Sunrise\bin\x64\steam_api64.dll` matched the built artifact hash during the test setup.
- The fresh isolated external run completed SignOn, ContentConfig, BAP 30→31, 25→26, 121→122, 302→303 (twice), and 304→305, then only 250→251 keepalives.
- The listener accepted the real client handoff value (no format rejection). No raw bootstrap/session/account material was written to logs or this document.

## Result

The client passed the first white screen but remained at the black screen. It did not request service 12 or any later account/Queuez route in the captured launch interval.

## Default-config comparison

The bundled Sunrise default configuration runs the in-process server and defines a fixed local account plus character state. External mode redirects transport but the isolated Python listener does not yet provide the corresponding state layer.

The earliest verified BAP acknowledgements are not the discrepancy: the Sunrise reference routing table uses empty response bodies for services 121→122 and 302→303, as does the listener. Do not alter those acknowledgements speculatively.

## Next bounded investigation

1. Trace the first reference-server post-auth outbound send site reachable before the client emits an account/Queuez request.
2. Compare its trigger and state prerequisites with the listener, especially `bap_route.cpp`, `bap_connection_publication.cpp`, Queuez outcome staging, and push paths.
3. Add metadata-only listener instrumentation at the selected seam.
4. Write a red test and implement exactly one source-backed, synthetic/config-driven state publication or response adapter.
5. Run the full suite, static safety scan, independent review, listener restart, isolation check, and fresh capture before another Legion launch.

## Guardrails

- Do not copy default Sunrise account/character identifiers or player data into the external service.
- Do not emit unsolicited Queuez frames until a concrete reference trigger, service, and body layout are established.
- If one tested transition does not produce a new client route, return to the reference differential rather than combining another change.

## Artifacts

- Transition plan (local, intentionally untracked): `.hermes/plans/2026-08-15_215500-external-post-bap-unblock.md`
- Redacted baseline analyzer: `tools/analyze_bap_transition.py`
- Fresh bootstrap-handoff capture: `/home/syzygy/destiny-re/network/20260814-161330/captures/legion-20260815-214247Z.pcap`
