# 2026-08-17 external task-trace preflight

## Question

Can a dedicated external trace runtime record payload-free timestamped task-completion metadata and establish whether task `ENUM(0)` completes before the authenticated external stable wait or service 29?

## Result

**PARTIAL — no external client observation was launched.** The prior trace source was inspected before deployment and found to retain formatted retail-log text (`ev=retail ... text=...`), contrary to this experiment's payload-free requirement. The trace branch was corrected in its dedicated source/runtime path only: it now emits only `ev=retail_task` records containing a monotonic timestamp, a numeric task enum, and `transition=completed`. It does not write the formatted retail line, BAP body, identity, endpoint, or account data.

The dedicated trace source commit is `d025f3d`. Its Windows build completed successfully in GitHub Actions run `32069461540`; the released DLL artifact digest is `sha256:3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e`.

## Server-side preflight

Before any client launch, the replacement listener and capture were stopped, no listener occupied the relevant lab ports, and both IPv4 and IPv6 forwarding were `0`. These are server/lab-gateway checks only; they do not prove the Windows trace copy's DLL/settings hashes or its client-side isolation state.

## Limitation

The current Ubuntu session has no configured Windows SSH target or verified interactive control of the Legion. The observed Moonlight session is labelled for the OptiPlex, not a verified Legion interactive desktop. Therefore the trace DLL could not safely be deployed to a dedicated Windows copy, the untouched external-validation DLL/settings could not be hash-checked, and the Human/UI gate could not be satisfied. No Destiny process, client settings, trace runtime, listener, capture, or client packet observation was started in this session.

This is procedurally inconclusive, not evidence that task `ENUM(0)` is absent or that service 29 does not follow externally.

## Next falsifiable step

Using the current Windows operator access, hash the known-good external-validation DLL and settings, create a dedicated trace copy, install only the artifact identified above, set only that copy for external validation with informational task/server logging, and re-hash the baseline. Re-verify client isolation, disabled forwarding, and no conflicting listener; then, after the operator performs the title-screen start action, run one bounded external observation and compare `retail_task task_enum=0 transition=completed` and any service-29 metadata with the documented Oracle ordering. Restore/remove the trace copy afterward. Do not add service-29 replies, Queuez service 123, account state, or speculative notifications.

## Superseding bounded observation

The following run supersedes the statement above that no client observation had occurred. After the stated Human/UI action, the operator immediately saw Marionberry. The dedicated trace log had recorded successful external egress-hook and config-getter installation but contained zero `retail_task` completion records. The replacement listener recorded no HTTP or BAP application event beyond listener startup, and therefore no service-29 metadata.

**FAIL for the stated differential, not a negative protocol result.** This observation ended before authenticated BAP/task progression, so task `ENUM(0)`, service 29 after task 0, and the earliest semantic differential are all UNKNOWN. The trace copy and bounded raw capture were removed after collecting only sanitized metadata; the original external-validation DLL/settings hashes were unchanged after cleanup.
