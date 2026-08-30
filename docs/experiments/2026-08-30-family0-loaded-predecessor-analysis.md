# 2026-08-30 family-zero loaded predecessor analysis

## Authorization and scope

The user authorized a bounded, read-only loaded-process analysis. The project scanner opened the running isolated historical client only with read/query access and emitted aggregate control-flow categories. It did not write process memory, control the UI, change the source list, or alter package, account, protocol, or server behavior.

## Initial loaded-process scanner result

The standalone loaded-process scanner reported zero exact target matches. This was explained by the target's already-installed detour: the source signature identifies the original prologue, which the detour replaces before an external scanner can observe it. The result is a representation limit of post-install scanning, not absence of the target.

## Pre-detour aggregate observer

A minimal external-trace observer was added at the only valid timing point: after the existing unique target match, but before the existing source-list getter publication and detour installation. It reads validated mapped sections and logs only three aggregate values:

- direct relative calls to the target;
- direct relative tail jumps to the target; and
- absolute pointer references to the target.

It logs no addresses, identities, bytes, hashes, package data, or payloads, and it neither adds a detour nor changes any existing return path. Dedicated source-contract tests passed; external-trace tests passed (23), and Windows CI run `33322062677` passed.

## Controlled result

With the CI artifact staged only in `external-trace`, normal ContentConfig/runtime/isolation preflight passed. No UI input was requested or used. The pre-detour observer reported:

- direct relative calls: **0**;
- direct relative tail jumps: **1**;
- absolute pointer references: **0**.

This establishes one direct static predecessor category: the family-zero sweep is reached only through a unique direct tail-jump site in the mapped main image. It does not identify the caller of that tail-jump wrapper or prove that the wrapper's own predecessor is the black-screen gate.

## Cleanup

The game, capture, HTTPS/BAP listener, and UDP discovery listeners were stopped. The temporary DLL was restored after the expected short post-stop file lock cleared. External-trace and protected validation runtime hashes were re-recorded, and isolation passed with forwarding disabled and public HTTPS blocked.

## Next boundary

Do not repeat the standalone loaded scanner or the pre-detour count unchanged. The next source-backed, aggregate-only candidate is a bounded pre-detour second-hop classifier: resolve the unique tail-jump wrapper internally and count only direct-call/tail-jump/pointer-reference categories to that wrapper. It must not log its address, add a hook, modify the wrapper, or alter client/server behavior. A separate implementation decision is required before further runtime work.
