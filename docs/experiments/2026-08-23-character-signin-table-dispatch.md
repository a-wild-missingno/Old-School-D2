# Character-signin table-dispatch observation

Status: COMPLETE — verified table slot is not reached on the external path

## Question

Does the uniquely identified relocation-backed, table-shaped reference dispatch to the character-signin enter handler during the external black-screen path?

## Trace-only change

A Windows-CI-built trace runtime from Sunrise external-lab commit `3671dcd` added a guarded and reversible wrapper around exactly one table slot. Installation required all of the following in the current main image:

- exactly one image-local pointer reference to the unique character-signin target;
- a base-relocation record for that reference;
- a read-only, non-writable table region with at least four consecutive executable-image entries; and
- the original slot value exactly matching the resolved target.

The wrapper forwarded the unmodified step pointer to the original target and emitted once-only labels only: `table_dispatch=seen` and `target_entry=seen`. It made no listener, BAP, server, Queuez, profile, package, account, content, or bootflow-policy change. It did not serialize object state, raw memory, pointer values, or client data.

## Preconditions

- ContentConfig identity: PASS.
- External-trace preflight: SSH/runtime/executable/isolation PASS, and Destiny absent.
- Gateway/client isolation: IPv4/IPv6 forwarding disabled and Legion public HTTPS blocked.
- Protected `external-validation` DLL hash was checked before and after and was unchanged: `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`.
- The staged trace artifact hash was `be4fd59683ac11e689653622e6ac7e15386431fdaedd0add381e9334e02b61ed`; deployment reported exact remote equality.

## Controlled observation

Capture and the isolated discovery/HTTPS/BAP listeners started before the project-managed interactive Destiny process. At the Human/UI gate, the operator pressed Enter once at the title/start screen, then waited approximately one minute without other input.

The client reported successful guarded table-probe installation:

```text
ev=external_trace stage=character_signin_table result=ok
```

It did **not** report either reachability event during the full bounded observation:

```text
table_dispatch=seen: absent
target_entry=seen: absent
```

The replacement listener recorded one connection that retained the known prefix: `30→31`, `25→26`, `121→122`, two `302→303`, `304→305`, nine one-way client service-29 notifications, then 15 `250→251` keepalive pairs. It recorded no client service 10.

A post-input desktop capture did not show a game surface and is not used as visual evidence of client state.

## Result

**CONFIRMED:** the specific verified table slot is not dispatched during the observed external route. The target method is also not entered. This rules out the previously highest-ranked hypothesis that this slot supplies the missing external character-signin transition.

**NOT ESTABLISHED:** the concrete table type, reachability of other entries, the exact upstream client-local gate, or a causal server-side correction. This result does not authorize changing service 29 behavior, Queuez service 123, profile state, package content, account handling, or any other listener behavior.

## Cleanup

The project-managed Destiny process, capture, HTTPS/BAP listener, and UDP discovery listeners were stopped. The trace DLL was restored to its pre-test hash `2bba67402c764db8616dde67cc51cbd1280d615262e704def9c4005dc3753ad5`. Isolation rechecked as PASS; the protected baseline hash remained unchanged.

## Next falsifiable step

Do not add another table-slot probe by guesswork. The next source-only investigation must move upstream of the character-signin table and identify a client-local precondition with an independent working/offline comparator. A new live launch requires a separately reviewed, bounded observation criterion.
