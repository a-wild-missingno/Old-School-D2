# Complete-baseline external trace observation

Date: 2026-08-21
Status: complete — PARTIAL

## Question

With the complete local discovery/HTTPS/BAP transport baseline running, what is the first metadata-supported client boundary reached by the fresh provenance-controlled trace runtime?

## Safety and setup

- Trace DLL/source/CI provenance remained the documented fresh artifact; it was installed only in `external-trace`.
- Protected external-validation hashes were recorded before and after the run and remained unchanged.
- Legion public-HTTPS isolation passed; gateway IPv4/IPv6 forwarding was disabled.
- The session-owned discovery responders, HTTPS/BAP listener, and filtered capture were started before the client.
- The process was launched in the confirmed Windows interactive session. Interactive visual/input automation remains unverified, so the operator performed the required title-screen action.

## Observation

After the Human/UI gate, the operator reported: “Failed to download configuration files from bungie servers,” error code **turkey**. The post-report screenshot captured the Windows desktop rather than a Destiny error surface, so it is not used to independently verify the UI text.

## Metadata-only evidence

- Runtime JSONL recorded two inbound HTTPS requests, one `signon_session_issued`, and one `content_config_served`; both state-after values were `BAP_CONNECT`.
- The capture recorded TCP HTTPS traffic and no BAP-port packet. No BAP frame, authenticated BAP state, task completion, service 29, service 10, or `250 -> 251` was observed.
- Trace marker classification: config lookup `success_class` once; first outbound transport `pending_class` once; module-init marker absent; retail-task completions zero.
- Ignored/local capture SHA-256: `2b3498b775b3af8ab826785aa4c676f77f0454618e796c0c7a5fe9a281b27d2a`; size: 114,707 bytes.

## Aligned timeline

```text
MODULE INITIALIZATION:       NOT OBSERVED (marker absent; not proof of non-execution)
EXTERNAL CONFIG LOOKUP:      success-class
FIRST OUTBOUND TRANSPORT:    pending-class
HTTPS SignOn:                served; client continued to /config/
CONTENT CONFIG:              served by local runtime; client did not proceed to BAP
AUTHENTICATED BAP:           NO
ENUM(0) COMPLETE:            NO (not reached)
FIRST SERVICE 29:            NONE (not reached)
FIRST SERVICE 10:            NONE (not reached)
RECURRING 250 -> 251:        NO
FINAL OBSERVED CLIENT STATE: operator-reported configuration-download error, turkey
FIRST EVIDENCED DIVERGENCE:  client does not accept/proceed after the local ContentConfig response
```

## Interpretation

The discovery and TCP transport baseline is no longer the failure. The local runtime served a ContentConfig response, but server-side success only proves that it generated and sent bytes. It does not prove client acceptance. No evidence supports changing BAP, service 29, Queuez, account, or world behavior.

## Follow-up

Perform an evidence-only ContentConfig acceptance audit: compare the local response's structural metadata and manifest/cache-derived fields against the authorized known-good external baseline/source behavior without retaining response bodies, config values, identities, or manifests. Establish the first validated mismatch or prove the response-equivalence claim before another game observation.
