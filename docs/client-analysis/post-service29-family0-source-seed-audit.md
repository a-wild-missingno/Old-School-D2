# Post-service-29 family-zero source-seed audit

## Question

What concrete source-level difference remains after the observed one-way service-29 boundary and can plausibly gate the first client service-10 request without inventing a server response?

## Compared sources

- Current working/reference branch: `feat/external-bootstrap-handoff` at `8d2b6c8`.
- Controlled external-trace lineage: `lab/diagnostic/package-trust-compat` at `daf0bf0`, based on the older seed implementation.

The external SignOn bootstrap handoff is already present in both trees. The comparison found one remaining post-service-29 behavioral difference in the family-zero Queuez source seed.

## Confirmed source difference

Both trees install the same two family-zero hooks. The family-zero hook seeds the client-owned source list before it calls the original sweep; the manager hook attempts to capture an account key before it calls the original manager sweep.

The external-trace seed obtains its source-list key only from the live manager capture. If that capture remains zero, it returns without seeding. The current reference adds one fallback: when the manager key is not yet observable, it reads the already checked local runtime account snapshot and uses its primary identity. It preserves the manager value when present.

This is not a protocol response, a package-integrity change, or an account-state invention. It is a client-local source-list write that enables the already-installed family-zero subscribe sweep when the normal manager observation is late.

## Runtime correlation

The controlled compatibility run logged successful installation of the family-zero hooks, but did not log the seed's once-only success event. The same run reached authenticated BAP, emitted the known service-29 notifications, and remained black with no client service 10. Log absence alone does not prove the manager key was zero, but it is consistent with the older seed's explicit no-key return condition.

The current reference documents that the client Web Service requests drive its Queuez state machine. The family-zero seed's own comments identify the subscription as the downstream state the sweep must reach. Therefore the missing fallback is a concrete, source-backed prerequisite candidate for the still-absent service-10 transition. It is not causal proof.

## Boundary and next step

The fallback changes client-local source-list bytes, so it is not eligible for the prior read-only classifier lane. Do not deploy it or run a game test based on this audit alone. First make a source-level implementation decision: either (a) add a separate aggregate-only observation that distinguishes manager-key availability, runtime-account availability, and seed completion without changing the source list; or (b) explicitly authorize a tightly scoped behavioral experiment that ports only this non-integrity fallback and compares the service-10 boundary against the same isolated baseline.

No service-29 reply, Queuez publication, package data, account-state change, or integrity behavior is authorized by this audit.
