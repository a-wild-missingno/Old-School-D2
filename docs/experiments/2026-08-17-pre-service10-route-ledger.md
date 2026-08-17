# Pre-service-10 authenticated route-ledger comparison

Date: 2026-08-17

Status: PARTIAL — the earliest ordered route divergence is identified; the condition that causes it remains unknown.

## Question

What is the first observed difference between the completed internal/default authenticated BAP trace and the external stable wait before internal client service `10`?

## Method

The comparison used only service/response identifiers from existing metadata-only local logs. It excluded bodies, encrypted buffers, account/character data, addresses, tokens, keys, and timings. The internal oracle remained a separate dedicated copy; no external listener, client configuration, or oracle file was changed for this comparison.

A deterministic sanitized ledger helper, `authenticated_route_ledger.first_divergence`, compares the ordered route pairs while stopping before internal service `10`.

## Ledgers

Shared prefix:

```text
30 -> 31
25 -> 26
121 -> 122
302 -> 303
304 -> 305
302 -> 303
```

First difference:

```text
internal: five client 29 -> no correlated reply, then 250 -> 251
external: 250 -> 251, with no observed client service 29 in the bounded stable wait
```

The internal trace subsequently reaches client service `10 -> 11`; the comparison intentionally stops before that downstream boundary.

## Source check

The public Sunrise reference pinned by `docs/client-analysis/post-auth-oracle.md` maps request service `29` (`notification29`) to `ResponseMode::none` and the empty body codec in `Sunrise/src/server/bap/encrypted/routing/bap_service_routing.cpp`. The internal trace independently records five `29 -> none` routes before its first keepalive and continues to service `10`.

## Result

**CONFIRMED:** absent external client service `29` is the first actual ordered divergence before internal service `10`.

**CONFIRMED:** service `29` does not need a server reply. A synthetic acknowledgement would contradict both the public reference route and the internal oracle.

**UNKNOWN:** which earlier semantic condition in the internal/default configuration or client state causes the client to emit service `29`, while the external client does not. The evidence does not justify inferring that condition from the later Queuez service-123 publications.

## Validation

- `scripts/run-tests.sh`: 57 passed, including the deterministic first-divergence regression.
- `python3 -m compileall -q src`: passed.
- No game/client launch was performed: the comparison used already captured metadata and introduced no safe external runtime change to accept or reject.

## Follow-up

Instrument the dedicated oracle at the client-side state transition immediately before service `29`, then compare that trigger with the external client. Preserve the external validation runtime and do not add a service-29 reply or Queuez service 123.
