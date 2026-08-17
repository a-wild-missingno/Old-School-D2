# 2026-08-17 service-29 trigger oracle

## Question

What is the nearest observable client-side transition before the internal/default client emits its first authenticated one-way service 29?

## Controlled setup

- Dedicated internal/default oracle copy only; the external-validation copy was hash-checked before and after preparation and was not modified.
- Oracle DLL came from the Windows validation build of `lab/validation/service29-trigger-trace` at `b4b01e8`.
- The Oracle used the internal/default route (`external_server.enabled=false`) with client and server informational logs enabled.
- The run began with no `destiny2.exe` process or local BAP listener. The prior Oracle log was archived, then a new log was opened.
- The client had its injected egress guard installed. With external-server mode disabled, the guard's source-selected target is loopback; no public endpoint was contacted.
- Human interaction: the operator launched the dedicated Oracle copy and pressed Enter at the title screen. The client reached and remained at character select.

## Evidence

The ignored local run log is retained as `service29-trigger-oracle-20260817/sunrise-after-enter.log` with SHA-256 `c7808bdaa5ade09d45a0312755d8df216c1183a2bb38823c2bdd8fe75277fe83`. It contains no retained packet-body extraction in this experiment.

Ordered metadata at the first service-29 boundary:

1. After the shared authenticated prefix through the second `302 -> 303`, the client retail log completed `world_controller` task `ENUM(0)` at tick `274771468`.
2. The new Oracle boundary instrumentation recorded the first authenticated `service 29` at tick `274771484`, **16 ms later**.
3. Nine service-29 requests followed, each accepted as `route=none`; no synthetic response was sent.
4. The client then completed later tasks and eventually emitted service 10. Six service-10 routes were observed in the bounded capture.

The external stable-wait ledger remains different: it has no observed service 29 before service 10 and remains at recurring `250 -> 251` traffic. It has no equivalently timestamped retail-task trace, so this result does **not** establish why external mode fails to enter the task-0/service-29 path.

## Result

**PARTIAL.** The direct ordering is CONFIRMED: completion of client task `ENUM(0)` is the nearest instrumented client transition before the first internal/default service 29. The relationship is temporal, not a demonstrated causal semantic.

This rules out a missing service-29 reply as an explanation: the same run accepted all nine one-way requests and proceeded through service 10 to character select.

## Next falsifiable step

Add the same timestamped retail-task metadata to an external-validation observation, then determine whether task `ENUM(0)` completes and whether service 29 follows. Do not add a service-29 reply or Queuez publication.
