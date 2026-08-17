# 2026-08-17 external task-0 / service-29 observation

## Question

During one Human/UI-gated external-validation run, does client task `ENUM(0)` complete before stable wait, and does service 29 follow?

## Controlled setup

- A dedicated trace copy was made from the known-good external-validation runtime; its trace DLL was the Windows-CI-built payload-free artifact documented in the prior preflight record.
- Before launch, the baseline DLL/settings hashes were recorded; external mode was enabled in the trace copy, and the copied settings initially matched the baseline.
- Replacement HTTPS/BAP listener and a capture were started only after OptiPlex forwarding/NAT/listener checks and a Legion isolation check. The Legion reached the lab HTTPS endpoint but not the tested public HTTPS endpoints.
- Human gate: the operator launched the dedicated trace copy and pressed Enter once at the title/start screen.

## Observation

Immediately after the title-screen action, the operator saw Marionberry. The trace log confirmed egress-hook and config-getter installation but had zero `retail_task` completion records. The replacement listener recorded no HTTP or BAP application event beyond its own startup, so it produced no authenticated service-29 metadata.

The run did not reach the task/service boundary. It is therefore not valid evidence that task 0 or service 29 is absent. The pre-existing non-task external stable-wait ledger remains historical evidence only; it cannot establish the earliest semantic differential.

## Result

**FAIL.** The single authorized observation was executed, but it failed before authenticated BAP application behavior.

- External task `ENUM(0)` completion: **UNKNOWN**
- External service 29 after task 0: **UNKNOWN**
- Earliest internal-vs-external semantic divergence: **UNKNOWN**

## Cleanup and evidence handling

The temporary trace runtime was removed, its Destiny process stopped, and the known-good external-validation DLL/settings hashes were unchanged after cleanup. The raw bounded capture was discarded because it included SSH control traffic. No raw client log, packet body, identity, endpoint, key, or asset was committed; this record contains only sanitized event facts.

## Next falsifiable step

Do not repeat the game observation yet. First diagnose, in the dedicated trace source/runtime, why the trace copy reaches Marionberry before the listener receives an HTTP or BAP application event. Add only metadata-only startup/transport observability if needed, compile it in Windows CI, and verify the trace runtime can reach the known external authenticated stable wait before another Human/UI-gated task-0/service-29 observation. Do not add service-29 replies, Queuez service 123, account state, or speculative notifications.
