# External package-assert classifier observation

Date: 2026-08-22
Status: PARTIAL — local bootstrap/investment assertion classes observed; no service 10

## Question

Can a metadata-only classifier identify which known local package assertion families occur after the reconciled external bootstrap, without retaining package data or changing client/server behavior?

## Safety pre-check

- The client was isolated from public HTTPS; gateway IPv4/IPv6 forwarding remained disabled.
- The protected `external-validation` runtime was hash-checked before and after the run and was unchanged.
- The CI artifact was deployed only to `external-trace`, with source and remote SHA-256 equality verified.
- Local discovery, HTTPS, BAP, and the bounded capture were started before launch.

## Setup

Sunrise source commit `b5ab64c2d7307290b15d895c21cddb7a2676c078` added a once-per-class observer at the already-installed client assert handler. It recognizes only patchable-registration, patchable-bootstrap, and investment-globals assertion families. It emits a class plus the presence/value of the already-observed `-87` marker; it neither changes the handler return path nor retains assertion/package text in the new event.

Windows CI run `32575158529` compiled the artifact successfully. The deployed artifact SHA-256 was `2e8b62d003ca7aa7aff123d44af72b7b760aea7aa2e1bf97fa43dba7a9668722`.

## Observation

The operator reported the same black-screen outcome with no visible error. The listener recorded successful SignOn and ContentConfig, authenticated BAP (`30 -> 31`, `25 -> 26`, `121 -> 122`, `302 -> 303`, `304 -> 305`, then a second `302 -> 303`), nine client-originated no-reply service-29 notifications, and recurring `250 -> 251` keepalives. No client service 10 appeared in the bounded window.

The new client telemetry classified two local assertion families after the external ContentConfig route:

- `patchable_bootstrap`, with no `-87` marker (`result_code=0`, `code_present=0`)
- `investment_globals`, with no `-87` marker (`result_code=0`, `code_present=0`)

No patchable-registration-class assertion was observed in this run, so the run does not assign the historical `-87` to a specific assertion family.

## Evidence

- CI: `32575158529` completed successfully against the committed trace source.
- The managed trace deployment reported matching source and remote artifact SHA-256 values.
- Runtime metadata for the observation contains 51 events: SignOn, ContentConfig, authenticated BAP, nine service-29 requests, and thirteen `250 -> 251` keepalive pairs; it contains no service 10.
- The existing generic assert observer continued to report the two assertion texts, while the new classifier wrote only class/code metadata.
- After cleanup, Destiny, capture, discovery, HTTPS, and BAP listeners were stopped; protected baseline hashes and isolation checks passed.

## Result

**CONFIRMED:** the package assertions occur after successful external SignOn, ContentConfig, authenticated BAP, and service 29. They are local client observations and do not establish a missing server reply or authorize package content, account state, Queuez, or service changes.

**CONFIRMED:** this run's bootstrap and investment-global classes did not carry the observed `-87` marker. The registration-class assertion was not emitted in this bounded observation.

**UNKNOWN:** whether either local assertion is causal for the absent client service 10 or merely concurrent with the stable wait.

## Follow-up

Perform source-only comparison of the post-service-29/local-content transition between the internal/default oracle and external trace. Identify one testable, metadata-only ordering or readiness condition preceding client service 10. Do not add package content, service-29 replies, Queuez service 123, account state, or speculative responses.
