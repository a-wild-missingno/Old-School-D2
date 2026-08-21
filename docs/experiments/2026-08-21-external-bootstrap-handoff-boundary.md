# External bootstrap-handoff boundary

Date: 2026-08-21
Status: PARTIAL — repeated external service-29 route; no task-completion marker or service 10

## Question

Does a trace-only SignOn bootstrap-token handoff move the reconciled external client beyond its prior authenticated-BAP stable wait without altering BAP or Queuez behavior?

## Safety pre-check

- Legion public-HTTPS isolation passed.
- Gateway IPv4/IPv6 forwarding remained disabled.
- The protected external-validation runtime was not modified.
- The CI-built DLL was installed only in the dedicated external-trace runtime with a managed backup and matching SHA-256 verification.
- Local discovery, HTTPS, BAP, and filtered capture were started before launch.

## Setup

The trace-only client hook appends the process-local bootstrap value only to the rewritten SignOn URL. The listener records only that a query exists; neither the value, SignOn body, package data, account data, nor encrypted BAP buffers are retained here.

## Observation

The operator again saw the white loading screen followed by a persistent black screen. The client completed the known bootstrap routes, then emitted nine one-way encrypted service-29 requests before recurring `250 -> 251` keepalives. The listener correctly sent no service-29 reply. No client service 10 or server Queuez service 123 was observed in the bounded window.

The client assertion observer also reported local patchable-bootstrap and investment-globals package-load failures. These are local-client observations, not authorization to copy package data or fabricate a server response.

## Evidence

- The listener recorded that the SignOn request carried a query, while no query value was logged.
- Metadata-only BAP ledger: `30 -> 31`, `25 -> 26`, `121 -> 122`, `302 -> 303`, `304 -> 305`, `302 -> 303`, nine client `29 -> none`, then recurring `250 -> 251`.
- The source regression test was RED before the handoff code and GREEN after it.
- Windows CI compiled the trace artifact successfully; the dedicated runtime's deployed hash matched the artifact hash.

## Result

**CONFIRMED:** the external client now reaches and emits service 29 under the isolated listener. This supersedes the historical claim that external service 29 was absent.

**CONFIRMED:** service 29 requires no reply; the listener did not invent one.

**UNKNOWN:** why this external run does not continue to client service 10 after service 29, despite the internal oracle's later progression.

## Follow-up diagnostic

A second isolated run used a CI-built trace artifact with a once-only, metadata-only retail callback-presence marker. The marker was observed, which confirms that the retail observer received native callbacks. No numeric `retail_task` completion event was emitted, while the client again reached service 29 and did not emit service 10. The internal oracle's `ENUM(0)` completion is therefore not a universal prerequisite demonstrated by this external route; the external observer did not observe that diagnostic before or during service 29.

The client again showed the same local patchable-bootstrap and investment-globals package-load assertions. Those assertions remain evidence for a local content/loading boundary, not authority to copy package data, alter package identity, or fabricate protocol state.

## Follow-up

Do not schedule another client launch from the current evidence. Preserve no-reply service 29 and no unsolicited Queuez behavior. The next offline work, if resumed, is a source-backed audit of the local bootstrap/package-loading boundary and its relation to the absent service-10 route, using only structural metadata and no package-content retention.
