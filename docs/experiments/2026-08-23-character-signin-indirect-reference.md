# Character-signin indirect-reference probe result

Status: COMPLETE — one image-local target reference, black screen unchanged

## Question

After the prior in-process scan found a unique character-sign-in handler target with no direct `E8 rel32` callers, does the running external trace image contain a bounded image-local pointer-sized reference to that target?

## Method

The trace-only probe reused the existing unique handler signature. It continued to scan executable sections for direct calls, then—only when that match was unique—scanned the validated mapped main-image extent for pointer-sized values equal to the target address. It retained at most four image-relative reference offsets and logged only count classes and those capped offsets. It did not serialize image bytes, addresses, native text, arguments, package data, identities, payloads, or network data; it ran before the existing detour installation and did not alter resolver, handler, bootflow, or protocol control flow.

Windows CI run `32640515793` built source commit `3b86718`. Its artifact SHA-256 was `945f8dba3b19f466facffca8f8a7f6fe5fd6b0385e38924e070d53f0ed691161`; the dedicated external-trace runtime reported the identical deployed hash before the Human/UI-gated observation.

## Result

**CONFIRMED:** the once-only probe emitted:

```text
ev=external_trace stage=character_signin_image matches=1 direct_callers=0 indirect_references=1 reference_rva0=0x1C29788
```

The user pressed Enter once, waited approximately one minute, and observed the same black screen with no visible error. The client completed isolated SignOn, ContentConfig, authenticated BAP, nine no-reply service-29 notifications, and recurring `250 -> 251` keepalives. Client service 10 was not observed.

**LIMIT:** a pointer-sized occurrence in a mapped image is not itself a proven executable call site, vtable, dispatch table, or causal condition. The probe does not decode surrounding instructions or identify the reference's PE section role. It therefore does not justify a service change, Queuez publication, package/account state, or new bootflow intervention.

## Cleanup and isolation

Destiny, HTTPS/BAP, UDP discovery, and capture processes were stopped. IPv4/IPv6 forwarding remained disabled and public HTTPS remained blocked from Legion. The protected external-validation DLL SHA-256 remained `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`.

## Next falsifiable step

Classify the one bounded reference by its mapped PE section and whether an image-local executable indirect branch reads that reference, using metadata only. Do not launch a new game test until that classification selects a single source-backed probe.
