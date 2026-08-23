# Character-signin table-role observation

Status: COMPLETE — table-shaped reference confirmed; no causal handler entry

## Question

Is the sole read-only image reference to the unique character-signin enter handler consistent with a relocated function-pointer table, explaining why no direct call or canonical RIP-relative indirect branch referenced it?

## Trace-only change

The dedicated external-trace runtime was built from `jules-the-ai/sunrise-external-lab` commit `d27c39f`. It added no game, bootflow, protocol, account, Queuez, package, network, or detour behavior. It emitted only two bounded values from the already inspected current process image:

- whether the reference RVA was a 64-bit PE base-relocation target; and
- the capped (`0|1|2|3|4plus`) forward run of adjacent slots that point into executable image ranges.

It did not emit pointer values, raw image bytes, native strings, identities, payloads, capture contents, or account data.

## Preconditions

- ContentConfig identity guard: PASS.
- `external-trace` preflight: SSH/runtime/executable/isolation PASS; Destiny initially absent.
- Gateway/client isolation: IPv4 and IPv6 forwarding disabled; public HTTPS blocked from Legion.
- The staged artifact SHA-256 was `d05c48440c9bb3db65f96e90930158185c40cbf167538b7294e6e5b0c9f502c5`; deployment reported exact remote equality.
- The protected `external-validation` DLL was checked before and after the observation and remained `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`.

## Controlled observation

Listeners and bounded capture were started before the project-managed interactive Destiny process. At the required Human/UI gate, the operator pressed Enter once at the title/start screen and waited approximately one minute. No other input or server behavior was introduced.

The once-only trace result was:

```text
ev=external_trace stage=character_signin_image matches=1 direct_callers=0 indirect_references=1 reference_section=readonly reference_relocation=1 reference_table_code_slots=4plus rip_indirect_calls=0 rip_indirect_jumps=0
```

The replacement listener independently recorded one complete external connection with the already-known prefix: `30→31`, `25→26`, `121→122`, two `302→303`, `304→305`, nine one-way client service-29 notifications, then 24 `250→251` keepalive pairs during the bounded wait. It recorded no client service 10.

The character-select hook installed, but did not report its held/entered event. A post-input desktop screenshot did not show a game surface and is not used as visual evidence of client state.

## Result and confidence

**CONFIRMED:** the single reference is relocation-backed and begins at least a four-slot run of executable-image pointers. This is consistent with a function-pointer table/vtable-like layout and explains why the prior direct-call and canonical RIP-relative-indirect scans could both be zero.

**NOT CONFIRMED:** the table's concrete type, any virtual-call site, its dispatch predicate, or a causal relationship to the external black screen. The result does not authorize a server-side change, synthetic service, Queuez publication, profile state, or package behavior.

## Cleanup

The project-managed Destiny process was stopped. HTTPS/BAP, UDP discovery, and capture were stopped. The trace DLL was restored to its pre-test SHA-256 `2bba67402c764db8616dde67cc51cbd1280d615262e704def9c4005dc3753ad5`. Isolation remained PASS and the protected baseline hash was unchanged.

## Next falsifiable step

Treat the target as a likely virtual/table-dispatched method rather than a direct callable. Before another game run, design one source-only, bounded observation that can distinguish table-entry reachability from the method's actual entry without logging a pointer, object state, code bytes, or client data. Require an unambiguous event criterion and a new build before requesting another live test.
