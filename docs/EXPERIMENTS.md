# Experiment Index

Detailed records live in `docs/experiments/`. `PASS` means the stated boundary was directly observed in the isolated lab; it never means playable-game parity.

| Date | Experiment | Result | Frontier Advanced? | Document |
| --- | --- | --- | --- | --- |
| 2026-08-15 | External transport and SignOn validation | PASS | yes: SignOn to ContentConfig | `docs/experiments/2026-08-15-external-signin.md` |
| 2026-08-15 | ContentConfig parity and BAP bootstrap | PASS | yes: ContentConfig to encrypted BAP | `docs/experiments/2026-08-15-external-signin.md` |
| 2026-08-15 | Encrypted BAP bootstrap acknowledgements | PASS | yes: reached stable authenticated wait | `docs/experiments/2026-08-15-external-signin.md` |
| 2026-08-15 | Post-BAP transition baseline | PASS | no: confirmed absence of later client route | `docs/experiments/2026-08-15-post-bap-transition-baseline.md` |
| 2026-08-15 | External post-BAP differential | PARTIAL | no: identifies server-initiated state as the next boundary | `docs/experiments/2026-08-15-external-post-bap-differential.md` |
| 2026-08-16 | Internal/default post-auth oracle | PARTIAL | no: input-driven trace identifies later authenticated ordering | `docs/experiments/2026-08-16-internal-post-auth-oracle.md` |
| 2026-08-17 | Pre-service-10 authenticated route-ledger comparison | PARTIAL | yes: first route divergence is absent external service 29, not a missing reply | `docs/experiments/2026-08-17-pre-service10-route-ledger.md` |

## Superseded Records

The early SignOn-only and capture-only BAP observations are historical steps embedded in `2026-08-15-external-signin.md`; they are superseded as a current frontier by the stable authenticated post-BAP result. They remain evidence, not current instructions.

## Adding an Experiment

Start from `docs/experiments/template.md`. Link the record here only after recording its question, isolation pre-check, evidence, result, confidence, and follow-up. Store raw captures and local machine paths only in ignored local state.

| 2026-08-17 | [service-29 trigger oracle](experiments/2026-08-17-service29-trigger-oracle.md) | Internal/default task-0 to service-29 correlation | PARTIAL: task `ENUM(0)` completion precedes service 29 by 16 ms; no causal/external equivalence claim |
| 2026-08-17 | [external task-trace preflight](experiments/2026-08-17-external-task-trace-preflight.md) | Payload-free external trace artifact and lab-gateway preflight | PARTIAL: artifact built; no Windows deployment or Human/UI-gated observation |
| 2026-08-17 | [external task-0/service-29 observation](experiments/2026-08-17-external-task0-service29-observation.md) | One Human/UI-gated external task/service differential | FAIL: Marionberry before authenticated application traffic; task 0/service 29/differential remain unknown |
| 2026-08-21 | [external trace provenance comparison](experiments/2026-08-21-external-trace-provenance.md) | Historical trace/baseline identity audit | PARTIAL: prior digest mismatch is not causal evidence; superseded for current trace provenance by the fresh CI artifact |
| 2026-08-21 | [fresh external trace observation](experiments/2026-08-21-fresh-external-trace-observation.md) | Fresh provenance-controlled trace timeline | PARTIAL: Marionberry before authenticated application traffic; discovery/TCP baseline incomplete, task/service differential unknown |
| 2026-08-21 | [full external transport baseline preflight](experiments/2026-08-21-transport-baseline-preflight.md) | No-game discovery and HTTPS reachability proof | PASS: UDP NatProbe replies and HTTPS SYN-ACK directly observed from Legion-facing interface |
| 2026-08-21 | [complete-baseline external trace observation](experiments/2026-08-21-complete-baseline-trace-observation.md) | Human/UI-gated trace run against proven transport baseline | PARTIAL: SignOn and ContentConfig served, but client reported turkey before BAP; ContentConfig acceptance is the frontier |
| 2026-08-21 | [ContentConfig acceptance audit](experiments/2026-08-21-contentconfig-acceptance-audit.md) | No-game source/cache identity comparison | PARTIAL: verified cache identity and configured listener response identity differ; reconciliation is the next bounded step |
| 2026-08-21 | [reconciled ContentConfig observation](experiments/2026-08-21-reconciled-contentconfig-observation.md) | Controlled run after cache-derived identity reconciliation | PARTIAL: reached authenticated BAP stable black-screen wait with no visible error |
| 2026-08-21 | [external bootstrap-handoff boundary](experiments/2026-08-21-external-bootstrap-handoff-boundary.md) | Controlled trace run after privacy-safe SignOn bootstrap handoff | PARTIAL: external client emitted nine one-way service-29 requests, then stable wait; service 10 remains absent |
| 2026-08-22 | [external package-assert classifier](experiments/2026-08-22-external-package-assert-classifier.md) | Metadata-only local package-assert classification | PARTIAL: bootstrap/investment classes occurred after service 29 without `-87`; service 10 remains absent |
| 2026-08-22 | [complete build-data readiness probe](experiments/2026-08-22-complete-build-data-readiness-probe.md) | Source-backed metadata-only readiness differential | PARTIAL: all eleven domains and persistence complete, yet black-screen/service-10 absence remains |
| 2026-08-22 | [post-investment bootflow boundary](experiments/2026-08-22-post-investment-bootflow-boundary.md) | Source-only native bootflow comparison | PARTIAL: external route never enters existing character-select handler; no duplicate probe added |
| 2026-08-22 | [character-signin predecessor source limit](experiments/2026-08-22-character-signin-predecessor-source-limit.md) | Source-only call-site review | COMPLETE: no unique predecessor encoded in authorized source |
| 2026-08-22 | [character-signin static call-site scan](experiments/2026-08-22-character-signin-static-callsite-scan.md) | User-authorized offline PE scan | COMPLETE: source target signature absent from on-disk executable; no caller inferred |
| 2026-08-22 | [character-signin loaded-module scan](experiments/2026-08-22-character-signin-loaded-module-scan.md) | User-authorized external read-only process-memory scan | COMPLETE: 145 MB / 11 sections read, but no target signature/caller recovered |
| 2026-08-22 | [in-process character-signin probe design](experiments/2026-08-22-in-process-character-signin-probe-design.md) | Bounded metadata probe | IMPLEMENTED/source-tested only; no Windows build, deploy, or run |

| 2026-08-22 | [in-process character-signin probe result](experiments/2026-08-22-in-process-character-signin-probe-result.md) | Built trace-only live observation | COMPLETE: unique target / zero direct callers; black screen unchanged |
| 2026-08-23 | [character-signin indirect-reference probe result](experiments/2026-08-23-character-signin-indirect-reference.md) | Built trace-only live observation | COMPLETE: one bounded image-local pointer reference; black screen unchanged |
| 2026-08-23 | [character-signin reference-role probe result](experiments/2026-08-23-character-signin-reference-role.md) | Built trace-only live observation | COMPLETE: reference is read-only; canonical RIP-indirect call/jump count is zero |
| 2026-08-23 | [account/profile bootflow contract audit](client-analysis/account-profile-bootflow-contract.md) | Source/config audit of profile setup and upstream PR #75 | COMPLETE: WS-701/profile completion is downstream of missing service 10; no adapter added |
| 2026-08-23 | [character-signin table-role observation](experiments/2026-08-23-character-signin-vtable-role.md) | Built trace-only live observation | COMPLETE: reference is relocation-backed with 4plus adjacent executable pointer slots; service 10 still absent |
| 2026-08-23 | [character-signin table-dispatch observation](experiments/2026-08-23-character-signin-table-dispatch.md) | Built guarded table-slot trace observation | COMPLETE: verified slot and target were both unreachable; service 10 still absent |
