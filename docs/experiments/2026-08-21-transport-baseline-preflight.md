# Full external transport baseline preflight

Date: 2026-08-21
Status: complete — PASS

## Question

Can the independently implemented UDP discovery responder, HTTPS listener, and BAP listener be started together with explicit lifecycle ownership, and can the Legion-facing interface demonstrate the responses required before another game observation?

## Safety pre-check

- No Destiny process was running before the probe.
- Legion public-HTTPS isolation passed.
- Gateway IPv4 and IPv6 forwarding were disabled.
- No relevant listener was present before the lab start command.
- A filtered capture was started before the Legion probe.

## Setup

`lab-start.sh` now starts the existing PostgreSQL-backed discovery service on both configured discovery ports as well as the existing HTTPS/BAP runtime. It receives its database configuration from an existing root-readable environment file; no database URL is placed in command-line arguments, logs, Git, or this record.

`scripts/windows/probe-transport-baseline.sh` uses the established Windows-lab transport to send recognized NatProbe requests from Legion and to make a bounded TCP connect to the configured HTTPS port. It never launches Destiny or changes runtime files.

## Observation

The Legion-side controlled probe received a correctly shaped 16-byte NatProbe reply on both configured discovery ports and completed the HTTPS TCP connection.

The filtered capture independently recorded two discovery UDP packets inbound and two replies outbound, plus one TCP SYN and one TCP SYN-ACK at HTTPS. It recorded five additional TCP control flags from the completed bounded connect. No application request was deliberately sent.

## Evidence

- Legion probe: `NAT_PROBE_REPLY=PASS` on each configured discovery port; `HTTPS_CONNECT=PASS`; `TRANSPORT_BASELINE=PASS`.
- Capture metadata: UDP inbound `2`, UDP outbound `2`, TCP SYN `1`, TCP SYN-ACK `1`.
- Ignored/local capture SHA-256: `e32cf55ba788e79891e58ed0c112db4801737382965c24bbfd52eb89e8eb8bea`; size: 863 bytes.
- Protected external-validation DLL/settings hashes remained unchanged after cleanup.
- All session-owned services and capture were stopped after the probe; no relevant local sockets and no Destiny process remained.

## Result

PASS. The previous incomplete transport-baseline diagnosis is resolved. This test establishes only reachability and response behavior; it does not establish trace instrumentation output, external client sign-on, BAP authentication, task completion, service 29, or service 10 behavior.

## Follow-up

Prepare one new isolated external-trace observation using this complete baseline. Do not add protocol behavior. After the Human/UI gate, collect the metadata-only trace timeline and listener/capture evidence, then stop the session-owned processes.
