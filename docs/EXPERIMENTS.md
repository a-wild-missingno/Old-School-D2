# Experiment Index

Detailed records live in `docs/experiments/`. `PASS` means the stated boundary was directly observed in the isolated lab; it never means playable-game parity.

| Date | Experiment | Result | Frontier Advanced? | Document |
| --- | --- | --- | --- | --- |
| 2026-08-15 | External transport and SignOn validation | PASS | yes: SignOn to ContentConfig | `docs/experiments/2026-08-15-external-signin.md` |
| 2026-08-15 | ContentConfig parity and BAP bootstrap | PASS | yes: ContentConfig to encrypted BAP | `docs/experiments/2026-08-15-external-signin.md` |
| 2026-08-15 | Encrypted BAP bootstrap acknowledgements | PASS | yes: reached stable authenticated wait | `docs/experiments/2026-08-15-external-signin.md` |
| 2026-08-15 | Post-BAP transition baseline | PASS | no: confirmed absence of later client route | `docs/experiments/2026-08-15-post-bap-transition-baseline.md` |
| 2026-08-15 | External post-BAP differential | PARTIAL | no: identifies server-initiated state as the next boundary | `docs/experiments/2026-08-15-external-post-bap-differential.md` |

## Superseded Records

The early SignOn-only and capture-only BAP observations are historical steps embedded in `2026-08-15-external-signin.md`; they are superseded as a current frontier by the stable authenticated post-BAP result. They remain evidence, not current instructions.

## Adding an Experiment

Start from `docs/experiments/template.md`. Link the record here only after recording its question, isolation pre-check, evidence, result, confidence, and follow-up. Store raw captures and local machine paths only in ignored local state.
