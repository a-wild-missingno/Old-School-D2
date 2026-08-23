# Character-signin reference-role probe result

Status: COMPLETE — reference is read-only; no canonical RIP-relative indirect branch reads it

## Question

Does the one image-local pointer-sized reference to the unique character-sign-in handler lie in an executable, writable, or read-only mapped PE section, and does any canonical x64 RIP-relative indirect call or jump read that exact reference?

## Method

The trace-only classifier retained existing executable ranges for target resolution and exposed only validated PE-section flags and RVAs for metadata classification. It reused the existing handler signature and pointer-reference scan. Only when exactly one reference existed, it reported that reference's section class and scanned executable sections for the two canonical six-byte RIP-relative indirect forms: `FF 15 disp32` (call) and `FF 25 disp32` (jump), whose operand RVA equalled the reference RVA. It retained at most four branch RVAs. It did not serialize raw bytes, instruction text, addresses, arguments, native strings, package data, identities, payloads, or network data, and it did not alter resolver, detour, bootflow, package, or protocol behavior.

Windows CI run `32641784421` built source commit `8260cab` successfully. The deployed artifact SHA-256 was `2bba67402c764db8616dde67cc51cbd1280d615262e704def9c4005dc3753ad5`, verified identical on the dedicated external-trace runtime before the Human/UI-gated observation.

## Result

**CONFIRMED:** the once-only event was:

```text
ev=external_trace stage=character_signin_image matches=1 direct_callers=0 indirect_references=1 reference_section=readonly rip_indirect_calls=0 rip_indirect_jumps=0 reference_rva0=0x1C29788
```

After the user pressed Enter once and waited about one minute, the client again completed isolated SignOn, ContentConfig, authenticated BAP, nine no-reply service-29 notifications, and recurring `250 -> 251` keepalives. Client service 10 was not observed; the user saw the same black screen with no visible error.

**CONCLUSION:** this read-only occurrence is not reached by either canonical RIP-relative indirect-call/jump form scanned here. It remains neither a proven executable predecessor nor a causal condition.

**LIMIT:** the classifier does not decode other indirect transfer forms, address-materialization instructions, relocations, table semantics, or surrounding control flow. Those possibilities remain unknown; the zero result does not prove the reference is unused.

## Cleanup and isolation

Destiny, HTTPS/BAP, UDP discovery, and capture were stopped. IPv4/IPv6 forwarding remained disabled and public HTTPS remained blocked from Legion. The protected external-validation DLL SHA-256 remained `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`.

## Next falsifiable step

No game run is selected. Before another launch, select one separately scoped source-backed hypothesis for a non-canonical reference use; do not infer an indirect caller, add server behavior, or send Queuez/account/package state from this result.
