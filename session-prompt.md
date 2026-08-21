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
- For routine Legion process, runtime, log, and isolation operations, load the installed `windows-lab` skill and use `scripts/windows/` rather than authoring ad-hoc SSH/PowerShell commands. Repository-local skills are not auto-discovered: see `docs/operations/windows-lab-control.md` for the one-time MacBook Hermes installation command.

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

Recover the dedicated payload-free trace artifact source/build provenance and reproduce its recorded DLL digest in Windows CI before any deployment or client observation.

## Starting Evidence

The known-good external-validation DLL SHA-256 is 9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae. It differs from the trace artifact digest 3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e recorded for the Marionberry observation. The trace copy is absent after cleanup. The documented source commit is not in this repository and the documented CI run was not retrievable through either recorded remote. Binary identity is therefore the first evidenced pre-transport divergence, but causality and the external task/service differential remain UNKNOWN.

## Required Work

1. Do not deploy a trace runtime, launch Destiny, repeat a game observation, or add a protocol response.
2. Obtain the authorized source revision and build workflow record through an authorized source repository or retained local build evidence.
3. Rebuild in Windows CI and require DLL SHA-256 to equal 3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e. On mismatch, document a provenance break and stop.
4. Only on a matching rebuild, inspect trace-only startup/transport hooks and add payload-free, value-free stage metadata for module initialization, external-config lookup outcome class, and first outbound transport result class. Validate in Windows CI only.
5. Preserve baseline runtime and isolation. Document, validate, commit, push, and update the active session PR.

## PASS Criteria

- The trace artifact is reproducibly attributed to an authorized source/build record, or a documented digest mismatch falsifies that provenance.
- Any instrumentation is payload-free, value-free, Windows-CI validated, and no runtime deployment, game observation, or speculative protocol behavior occurs.
- Tests pass, documentation is updated, and the active session PR is updated.
