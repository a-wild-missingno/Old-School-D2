# Complete build-data readiness metadata probe

Status: PARTIAL — all eleven local readiness domains complete; black screen and absent service 10 remain

## Question

Can the external trace distinguish full local build-data completion from the earlier eight-field readiness report before another service-10 comparison?

## Source evidence

The three reviewed source worktrees share the same pre-probe `content_readiness_report.cpp` and `investment_refresh.cpp` (identical SHA-256s). The reporter exposed eight flags: named catalog, items, details, buckets, sockets, abilities, progressions, and scenarios.

However, `client/content/investment/investment_refresh.cpp::ready()` requires eleven flags before persistence/completion: those eight plus spawn sets, hash names, and investment constants. Therefore the earlier external line with all eight reported flags set does not establish that the worker is complete. It cannot distinguish a fully ready external run from one stalled in one of the three omitted local-only readiness domains.

This is an observability gap, not evidence that package assertions caused the absent service 10.

## Controlled probe

Commit `8506f35d45a90d4ca35f0f89cdf940c579f2bbf8` changes only the existing once-per-change readiness line in the dedicated trace source:

- adds `spawns`, `hash_names`, and `constants` boolean flags;
- adds `all_ready`, derived from the same complete eleven-domain mask;
- preserves no package names, package data, assertion text, identities, payloads, or protocol fields;
- does not change the investment worker, refresh order, persistence, assertions, BAP, service 29, Queuez, account state, or replacement service behavior.

Windows validation build `32575906197` completed successfully with MSBuild and artifact upload. The artifact was hash-verified and deployed only to the dedicated trace runtime for one bounded observation.

## Observation result

The operator again observed a persistent black screen with no visible error. The trace log recorded exactly one complete readiness state before external SignOn and ContentConfig:

`ev=build_data stage=domains named=1 items=1 details=1 buckets=1 sockets=1 abilities=1 progressions=1 scenarios=1 spawns=1 hash_names=1 constants=1 all_ready=1`

The listener then recorded the established authenticated BAP prefix, nine no-reply service-29 notifications, and recurring `250 -> 251` keepalives; it did not record client service 10. The same local patchable-bootstrap and investment-globals assertions recurred with `result_code=0`, not `-87`.

**Conclusion:** complete build-data readiness is not the missing pre-service-10 condition in this external run. This does not prove the local package assertions are causal or authorize changes to packages, Queuez, account state, service 29, or the replacement service.

## Next falsifiable step

Use source-only review to find the earliest metadata-safe native readiness/transition after the all-ready state and before the service-10 branch. The next candidate must differentiate the internal/default oracle from this external trace without recording package data or changing behavior.

## Validation

- Red test first: the new source guard failed because the report omitted `spawn_sets_ready`.
- Focused and complete trace source suite: `6` tests passed.
- `git diff --check` passed.
- Windows CI `32575906197`: passed (MSBuild and artifact upload).
