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
