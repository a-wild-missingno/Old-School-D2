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

## Build boundary

Windows CI run `33320289289` was started from the committed trace source. At this record's creation it was still running; no artifact has been staged, no runtime has been modified, and no game observation has started.

## Interpretation rule

This probe can distinguish whether the external wait is consistent with a missing manager key despite a usable runtime account, and whether the old seed has completed. It cannot itself prove that the current-reference fallback would cause service 10 or character select. Do not port the fallback, send Queuez state, or modify account/package/integrity behavior based solely on this observer.
