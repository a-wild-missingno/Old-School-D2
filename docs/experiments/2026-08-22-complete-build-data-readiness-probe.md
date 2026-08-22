# Complete build-data readiness metadata probe

Status: READY FOR CONTROLLED DEPLOYMENT — source-backed, metadata-only; no client run in this investigation

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

Windows validation build `32575906197` completed successfully with MSBuild and artifact upload. No artifact is deployed and no game was launched during the source-only investigation.

## Falsifiable next observation

After the Windows build has passed and the probe is deployed only to the dedicated trace runtime, run one bounded external observation.

- If `all_ready=0` persists before the black screen, the next investigation is the first omitted false domain and remains local/content-readiness-only.
- If `all_ready=1` occurs before the black screen with no client service 10, full build-data readiness is ruled out as the missing pre-service-10 condition for this run.
- Any result preserves the existing no-reply service-29, no-Queuez, and no-package-data constraints.

## Validation

- Red test first: the new source guard failed because the report omitted `spawn_sets_ready`.
- Focused and complete trace source suite: `6` tests passed.
- `git diff --check` passed.
- Windows CI `32575906197`: passed (MSBuild and artifact upload).
