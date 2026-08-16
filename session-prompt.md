# Old-School-D2 Hermes Operating Manual

## AUTHORITATIVE CURRENT STATE

Read `docs/PROJECT_STATE.md`.

## CURRENT RESTART/HANDOFF

Read `docs/HANDOFF.md`.

These files override any stale current-state information elsewhere in this prompt. If present, read `.hermes/HANDOFF.local.md` for local-only substitutions; never commit its contents.

## Project Objective

Maintain a clean-room, lab-only replacement service for preservation research. Never contact, proxy, tunnel, NAT, or forward traffic to Bungie or public production infrastructure.

## Hardware and Network Architecture

The isolated historical client talks only to a non-forwarding lab gateway/DNS/capture point and local replacement listeners. Private values belong in the ignored local handoff file. Read `docs/network/isolation-plan.md` before a live run.

## Evidence Standards and Anti-Hallucination Rules

- Label claims `CONFIRMED`, `LIKELY`, or `SPECULATIVE`.
- A response is confirmed only with source/reference evidence plus a controlled client result.
- HTTP success, unit-test success, or a UI change alone is insufficient.
- Never infer a missing message body, account identity, character state, or Queuez publication from a screen state.
- Preserve raw evidence locally; commit only sanitized metadata, hashes, and reproducible tests.

## Git Workflow

Inspect `git status --short --branch`, recent history, and diffs before coding. Preserve unrelated work. Keep commits focused. Do not push automatically. Audit staged content for local paths, IPs, secrets, captures, keys, binaries, and copyrighted data.

## Experiment Methodology

1. Define one bounded question and a tight deterministic test where possible.
2. Verify client isolation, disabled forwarding/NAT, listeners, and capture before launch.
3. Change one evidenced variable.
4. Correlate capture, structured server log, reference evidence, and visual client state by time.
5. Stop at the first new boundary and record it in `docs/experiments/`.

## Source Versus Hypothesis Discipline

Keep source locations, observed behavior, and hypotheses separate. A public-reference route is not proof that it is reachable in this client state. A serializer or encrypted transport helper is not authorization to send a message.

## Monotonic Protocol Progress

Do not regress or casually revisit previously accepted stages. Preserve BAP nonce ownership in its single authoritative implementation. Never combine a structural refactor with a protocol behavior change.

## Fresh-Session Reading Order

1. `docs/PROJECT_STATE.md`
2. `docs/HANDOFF.md`
3. `.hermes/HANDOFF.local.md` if present
4. `docs/EXPERIMENTS.md` and the linked detailed record
5. Git history, source, and tests
