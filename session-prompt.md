# Old-School-D2 — AI Session Prompt

You are continuing **Old-School-D2**, a clean-room interoperability/preservation project for running a historical Destiny 2 client through Project Sunrise against an independently implemented local replacement server.

This file is the evergreen prompt given to a fresh agent each session. **The repository is project memory.** Use prior conversational memory only as a convenience; repository evidence is authoritative.

## Environment

- Agent runs on a MacBook.
- Commands execute on an Ubuntu OptiPlex.
- Destiny 2 runs on an Internet-isolated Windows 10 Legion.
- The Legion communicates only with the OptiPlex.
- Windows SSH credentials/config already exist.
- Machine-specific addresses, paths, and commands belong in `.hermes/HANDOFF.local.md` and must not be committed.

## Sources of Truth

- `session-prompt.md`: workflow + single mutable `CURRENT TODO`.
- `docs/PROJECT_STATE.md`: authoritative technical state/frontier.
- `docs/EXPERIMENTS.md`: experiment index; detailed evidence lives under `docs/`.
- `README.md`: public/user-facing overview only.
- `.hermes/HANDOFF.local.md`: private local lab details, if present.

If documentation conflicts, investigate before coding. Historical experiment records are evidence: correct interpretations by marking them superseded; do not silently rewrite observations.

---

# Operating Rules

1. **One TODO per session.** Complete or narrow the `CURRENT TODO`, then stop. Do not automatically continue into the next frontier.
2. **Move one evidenced boundary at a time.** Prefer: oracle → first divergence → smallest falsifiable change → controlled test → evidence.
3. **Freeze proven behavior.** Do not redesign working STUN, SignOn, ContentConfig, BAP crypto/services, etc. without contradictory evidence.
4. **Evidence over inference.**
   - `CONFIRMED`: directly supported by source, tests, captures, logs, instrumentation, or repeatable client behavior.
   - `LIKELY`: strongly supported but not demonstrated.
   - `SPECULATIVE`: hypothesis requiring a test.
   Unknown fields/semantics stay neutral.
5. Never claim code exists without opening it, tests pass without running them, services run without verifying them, packets/events occurred without evidence, or Git state without checking it.
6. Prefer instrumentation and known-good internal/default Sunrise behavior over guessing.
7. Keep experiments narrow: change one meaningful variable when practical.
8. Preserve known-good framing, AES-GCM, sequencing, and nonce ownership unless the TODO directly requires changes and regression coverage proves them.
9. Keep private lab data, credentials, keys, raw sensitive captures, Destiny binaries/assets, and proprietary dumps out of tracked files.
10. The client must remain isolated from Bungie/public production infrastructure. Never forward/NAT/proxy/tunnel it to live services; do not use leaked server code/keys or build live-service cheats.

---

# Session Startup

1. Locate the canonical repo and inspect Git:

```bash
git rev-parse --show-toplevel
git status --short --branch
git log --oneline --decorate -15
git remote -v
git fetch --prune origin
```

Preserve all unrelated staged/unstaged/untracked work.

2. Read:
   - `docs/PROJECT_STATE.md`
   - `docs/EXPERIMENTS.md`
   - `.hermes/HANDOFF.local.md` if present
   - documents/source explicitly referenced by `CURRENT TODO`

Do **not** load unrelated historical documents just for completeness. Read `README.md` only when needed to verify/update public-facing behavior.

3. Check for an existing open PR/session branch for this exact TODO. Do not duplicate active work.

4. If starting fresh, safely synchronize `main` and create a session branch:

```bash
git checkout main
git pull --ff-only origin main
git checkout -b session/YYYYMMDD-short-task-name
```

No destructive resets.

5. Run relevant baseline tests before behavioral changes and record pre-existing failures.

Before editing, establish:

```text
LAST CONFIRMED WORKING EVENT:
FIRST MISSING/FAILING EVENT:
EVIDENCE:
QUESTION THIS TODO MUST ANSWER:
```

---

# Research / Test Method

When a known-good internal/default Sunrise path exists, prefer:

```text
instrument known-good path
→ capture ordered behavior
→ align external behavior
→ identify FIRST semantic divergence
→ implement only that evidenced difference
→ regression test
→ one controlled client experiment if needed
```

Improve observability before guessing. Use structured logs, packet captures, payload hashes, sanitized fixtures, source instrumentation, and visual state where useful. Large/raw local artifacts may remain ignored with paths/hashes documented.

## Human / UI Interaction Gate

A running `destiny2.exe` does **not** prove a protocol test has started. The client may be waiting at a title screen, dialog, character screen, or other UI boundary.

Before diagnosing “no traffic/no progress,” establish that required UI interaction occurred and expected bootflow began.

If verified interactive Windows visual/input automation is **not** available, fully prepare the experiment, then STOP and say:

```text
READY FOR GAME TEST

Action:
<exact minimum user interaction required>
```

Do not start the bounded observation interval until that action occurs.

SSH/PowerShell/process launch alone do not count as interactive desktop automation. Automation may replace the human gate only after it is verified to view and control the actual Windows interactive session and is documented/authorized.

If required UI progression was not established, classify the run as **procedurally inconclusive**, not as a protocol/runtime failure.

---

# Completing the TODO

For `PASS`, prove the stated completion criteria with evidence.

For `PARTIAL`, record what passed, what did not, the new evidence/frontier, and rewrite `CURRENT TODO` to the first remaining divergence.

For `FAIL`, record the failed hypothesis and replace `CURRENT TODO` with the next falsifiable diagnostic step. Do not tell the next session to blindly repeat the attempt.

At a meaningful result:

- update `docs/PROJECT_STATE.md`;
- update `docs/EXPERIMENTS.md` and the relevant detailed experiment/protocol document;
- update `README.md` **only** if public capabilities, architecture, setup, or major limitations changed;
- replace `CURRENT TODO` below with exactly one next task understandable by a fresh agent.

---

# Session End

Before finishing:

1. Stop only project/test processes started by this session: temporary Destiny instances, captures, listeners, instrumentation, observers. Preserve SSH and network isolation.
2. Preserve useful evidence in tracked sanitized form or local ignored artifacts with references/hashes.
3. Validate:

```bash
scripts/run-tests.sh
python3 -m compileall -q src
git diff --check
git status --short
git diff
git diff --staged
```

4. Confirm no unrelated changes, secrets/private lab data, accidental large artifacts, or documentation contradictions.
5. Commit focused changes, push the session branch, and create a PR into `main`.
6. The PR should concisely state: objective; PASS/PARTIAL/FAIL; changes; evidence; tests; new frontier; next TODO; repository-hygiene notes.
7. Do **not** begin the next TODO after opening the PR.

Final response:

```text
SESSION COMPLETE
TODO result: PASS / PARTIAL / FAIL
Branch / HEAD:
Tests:
Verified advancement:
New frontier:
Next TODO:
Documentation:
README: YES/NO — reason
Lab cleanup:
PR:
Human attention needed:
```

---

# CURRENT TODO

## Objective

Compare the captured authenticated internal/default BAP oracle with the external stable wait and identify the **earliest evidenced divergence before the internal client emits encrypted service `10`**.

## Starting Evidence

Use `docs/PROJECT_STATE.md` as authoritative state.

The external client is confirmed through stable authenticated encrypted BAP and recurring keepalive traffic, but does not advance to character selection.

`docs/experiments/2026-08-16-internal-post-auth-oracle.md` records an input-driven internal/default oracle that reached character select. Its first new uncorrelated service-123 publication followed client service `10`; the external baseline does not reach service `10`.

`docs/client-analysis/post-auth-oracle.md` confirms service `123` is not automatically emitted solely on authentication.

## Required Work

1. Reconstruct the ordered internal and external route/state ledgers through the point immediately before internal service `10`.
2. Preserve the existing external-validation runtime and use the dedicated oracle copy only.
3. Before any launch, verify trace DLL/settings, client Internet isolation, and that conflicting Old-School-D2 listeners are absent.
4. Identify one falsifiable candidate for the **earliest missing semantic condition/event before external service `10`**. Do not infer it from the later service-123 payload.
5. Add only instrumentation or deterministic coverage needed to test that candidate.
6. Run at most one controlled external experiment if necessary, following the Human/UI Interaction Gate.
7. Do **not** emit Queuez service `123` during the current external stable wait.
8. Restore any changed oracle files, verify the external-validation DLL/settings were unchanged, then document/validate/commit/push/open a PR.

## PASS Criteria

- The first actual divergence before external service `10` is evidenced.
- Any implementation is limited to that divergence and has deterministic regression coverage.
- A controlled external run accepts the change or establishes a deterministic new frontier.
- Tests pass, documentation is updated, the next TODO is written, and a session PR is opened.

## Non-Goals

Do not:
- alter proven external BAP crypto/listener behavior without evidence;
- implement Queuez, account/character state, activity, or speculative notifications;
- alter client Internet isolation or contact public/Bungie services;
- modify the external-validation installation in place;
- continue into the next discovered boundary.
