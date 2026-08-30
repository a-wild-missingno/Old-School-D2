# 2026-08-30 family-zero seed-affordance observer

## Question

Can the existing family-zero source-seed path report the state that distinguishes the manager-key-only external implementation from the current reference fallback, without changing the source-list behavior?

## Implementation

The diagnostic runs inside the already-installed family-zero sweep immediately after the pre-existing seeding call and before the original sweep. It reports exactly three booleans:

- whether the existing manager-key capture is nonzero;
- whether the checked runtime account has a nonzero primary identity; and
- whether the pre-existing seed-completion marker is already set.

It serializes no identity value, source-list bytes, address, package data, network data, or payload. The observer performs atomic loads, takes the existing read-only runtime snapshot, and writes only a structured log event. It does not write the source list, install another detour, alter a return value, or change server/protocol/listener behavior.

## Source validation

The new source-regression tests first failed because the observer and its call site did not exist. After the minimal implementation, all three dedicated tests passed:

1. only the three aggregate affordances are emitted;
2. the observer body contains no state/source-list mutation primitive; and
3. the observer runs after the pre-existing seed and before the original sweep.

The complete external-trace source suite then passed: 22 tests.

## Controlled observation

Windows CI run `33320289289` completed successfully. Its DLL was staged only in the dedicated `external-trace` runtime after ContentConfig, runtime-hash, and isolation preflight all passed. The operator completed the required title-screen interaction and reported the same black screen with no visible error.

The trace again reached the known authenticated bootstrap/service-29 wait, but did not emit the new family-zero affordance event. Because that event is called on every execution of the already-installed family-zero sweep, the bounded run confirms that the family-zero sweep itself did not execute in this external path. It therefore cannot distinguish manager-key availability, runtime-account availability, or seed completion; the prior manager-key fallback candidate is upstream of an earlier execution gate.

No client service 10 was observed. No fallback, Queuez publication, account state, package data, integrity behavior, or server response was changed.

## Cleanup

The Destiny process, capture, HTTPS/BAP listener, and discovery listeners were stopped. The temporary DLL was restored after the post-stop file lock cleared. External-trace and protected validation-runtime hashes were re-recorded, and forwarding-disabled/public-HTTPS-blocked isolation passed.

## New frontier

Do not repeat this observer. The first newly confirmed local boundary is earlier than manager-key availability: the installed family-zero sweep is not invoked in the external path. The next step is source-only analysis of the family-zero sweep's invocation/eligibility condition in the known-good path versus external trace. A new runtime probe needs a unique, read-only target and must not seed the source list or modify Queuez behavior.
