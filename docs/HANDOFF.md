# Current Handoff

## Current Frontier

The client is stably authenticated on BAP and only performs recurring `250 -> 251` keepalives. The missing boundary is the first proven server-initiated authenticated state publication.

## Last Confirmed Successful Experiment

The bounded external post-BAP experiment completed SignOn, ContentConfig, BAP bootstrap, encrypted `121/122`, `302/303`, `304/305`, and recurring `250/251`, then observed no later client route. See the final row of `docs/EXPERIMENTS.md`.

## Current Failure / Missing Behavior

Stable black-screen wait; no account/character state or evidenced publication is implemented.

## What Is Frozen / Do Not Revisit

Do not modify discovery, SignOn, ContentConfig, BAP handshake, accepted BAP acknowledgements, nonce advancement, or Queuez runtime behavior without contradictory new evidence.

## What Is Already Prepared

The repository now contains the runtime listener, configuration template, scripts, deterministic protocol tests, sanitized oracle metadata, and structured JSONL event logging.

## Exact Next Engineering Task

Read the public-reference post-auth outbound path and record the first reachable send trigger, service, prerequisites, and body source. Add only metadata instrumentation; do not send a state publication.

## Exact Next Game Experiment

After source analysis and an approved one-variable implementation, start capture first, verify isolation, run one client launch, and stop at the first new boundary.

## Important Paths

- Runnable listener: `src/old_school_d2_service/runtime/app.py`
- State: `docs/PROJECT_STATE.md`
- Experiment index: `docs/EXPERIMENTS.md`
- Local-only substitutions: `.hermes/HANDOFF.local.md`

## Repository Branch / Commit

Run `git status --short --branch` and `git rev-parse --short HEAD`; do not trust this document for a moving commit ID.

## Windows SSH / Lab Addresses

Read `.hermes/HANDOFF.local.md` if it exists. Never add its values to a committed file.

## How To Start The Lab

1. Copy `.env.example` to a local ignored `.env` and fill it with local paths/addresses.
2. Verify isolation and start capture using local commands recorded in `.hermes/HANDOFF.local.md`.
3. Run `scripts/lab-start.sh` (the HTTPS/BAP listener) and, when discovery is needed, the configured discovery service.

## How To Stop The Lab

Run `scripts/lab-stop.sh`; then stop capture using the local command and verify listeners are gone with `scripts/lab-status.sh`.

## First Commands For A Fresh Session

```text
git status --short --branch
git log --oneline --decorate -20
cat docs/PROJECT_STATE.md
cat docs/HANDOFF.md
test -f .hermes/HANDOFF.local.md && cat .hermes/HANDOFF.local.md
scripts/run-tests.sh
```
