# 2026-08-30 family-zero offline static caller analysis

## Authorization and scope

The user explicitly authorized this separate read-only offline control-flow task. The scanner reads only the locally installed executable file through the project-managed Windows transport. Its output is deliberately aggregate-only: target-signature cardinality, direct relative-call count, direct tail-jump count, and absolute pointer-reference count. It does not emit hashes, RVAs, addresses, bytes, identities, payloads, package data, or arbitrary executable content. The temporary scanner is removed from the Windows host after each invocation.

## Validation

A source-contract test was added before implementation and failed because the scanner did not exist. The implementation then passed its dedicated tests. The canonical project suite passed with 78 tests, Python compilation passed, and `git diff --check` passed.

## Result

The exact family-zero target signature used by the running hook produced **zero offline file matches** in both protected `external-validation` and dedicated `external-trace` executable files.

This prevents target resolution and makes every caller/predecessor count inapplicable. The result is not a claim that the target does not exist at runtime: the source scanner operates over executable mapped sections, and the prior controlled run proved that the hook resolved and attached the target in a loaded process. It is a precise representation boundary: the required target bytes are not recoverable from the offline executable file with the source-defined signature.

## Conclusion

**COMPLETE / OFFLINE-ANALYSIS LIMIT.** No further offline file analysis is justified for this target. Do not loosen the signature, scan unrelated regions, extract raw content, or infer callers from a zero-match file scan.

The only remaining controlled route would be a separate authorization for a bounded read-only loaded-process scan while the already isolated historical client is running. It would have to retain aggregate-only output and not alter process memory, package data, protocol, server behavior, or client control flow. Do not start that route automatically.
