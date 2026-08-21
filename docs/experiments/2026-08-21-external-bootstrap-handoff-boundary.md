# External bootstrap-handoff boundary

Date: 2026-08-21
Status: PARTIAL — external route advanced to one-way service 29, then stable wait

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

## Follow-up

Compare the post-service-29 trigger/state conditions with the internal oracle using metadata-only instrumentation. Do not add a service-29 response, Queuez service 123, package content, account state, or another client launch until a new source-backed boundary is identified.
