# Fresh external trace observation

Date: 2026-08-21
Status: complete — PARTIAL (pre-semantic transport baseline failure)

## Question

Can a fresh, provenance-controlled external trace reach the first missing semantic boundary after the known-good external baseline, including numeric task `ENUM(0)`, service 29, and service 10 timing?

## Controlled trace provenance

- Known-good external-validation DLL SHA-256: `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`.
- Trace source base: `fd54fe6b94b54d39b3806afad68e57c00b7d4740`.
- Trace source commit: `5d73e4356efc20d6c68306bab9d1b03041e182ce`.
- Windows CI run: `32490948274` (successful).
- Trace artifact and deployed DLL SHA-256: `fbebb7f40a2177d5c63babc4fe376a747190812d2ad000e0c671ef23d46f4f65`.
- Reviewed delta: deferred module marker, config-lookup outcome class, first redirected-connect result class, and numeric task-completion metadata; no packet bodies, identity values, or formatted retail-task text were intentionally added.

## Safety and preflight

- The dedicated trace copy was separate from external-validation.
- External-validation DLL/settings hashes matched their preserved values before and after the run.
- Legion public-HTTPS isolation passed; IPv4 and IPv6 forwarding were disabled.
- HTTPS/BAP listeners and a filtered capture were running; no Destiny process was present before launch.
- Interactive automation was not verified. The human operator confirmed pressing Enter at the title screen before the observation interval began.

## Observation

The operator reported an immediate Marionberry error. The process remained present until session cleanup. A screenshot collected after the report did not capture a Destiny error surface and is not used as evidence of the reported UI state.

## Metadata-only evidence

- The filtered local capture has SHA-256 `26d723599cf04dcd72884cde02443e5dd90f2627ed07678f70e8b943fbda3b86` and size 1,522 bytes; it remains ignored/local.
- Capture classification: 10 UDP packets at the discovery port; 9 HTTPS-port TCP SYN packets; zero TCP SYN-ACK flags; zero BAP-port packets.
- The HTTPS/BAP runtime JSONL file had zero events.
- The trace log had zero expected fresh-trace metadata markers for module initialization, config lookup, outbound transport, or numeric retail-task completion.
- No authenticated BAP, `ENUM(0)`, service 29, service 10, or recurring `250 -> 251` event was observed.

## Aligned timeline

```text
MODULE INITIALIZATION:       NOT OBSERVED (no trace marker; not proof of non-execution)
EXTERNAL CONFIG LOOKUP:      not observed
FIRST OUTBOUND TRANSPORT:    UDP discovery packets and HTTPS SYNs observed; no TCP SYN-ACK
AUTHENTICATED BAP:           NO
ENUM(0) COMPLETE:            NO (not reached)
FIRST SERVICE 29:            NONE (not reached)
SERVICE 29 COUNT:            NONE
FIRST SERVICE 10:            NONE (not reached)
SERVICE 10 COUNT:            NONE
RECURRING 250 -> 251:        NO
FINAL OBSERVED CLIENT STATE: operator-reported immediate Marionberry
FIRST EVIDENCED DIVERGENCE:  incomplete local transport baseline: discovery responder absent and no HTTPS SYN-ACK in the filtered capture
```

## Interpretation

This is not evidence that task 0, service 29, or service 10 is absent in an otherwise known-good external run. It is also not evidence that the trace DLL caused the error: trace observability did not emit, and the local replacement-server transport baseline was not equivalent to the known-good external setup.

## Follow-up

Without launching Destiny, start the existing discovery component with HTTPS/BAP and prove a NatProbe reply plus HTTPS SYN-ACK on the lab interface. If either is absent, diagnose the host firewall/interface/socket-namespace mismatch. Only then prepare another controlled trace observation.
