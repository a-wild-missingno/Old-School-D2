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

Use the dedicated internal/default oracle to identify the client-side state transition or configuration condition that immediately precedes its first encrypted service-`29` notification, then compare that condition with the external stable-wait client.

## Starting Evidence

`docs/PROJECT_STATE.md` is authoritative. `docs/experiments/2026-08-17-pre-service10-route-ledger.md` confirms that the internal and external authenticated BAP ledgers share the bootstrap through the second `302 -> 303`; internal then sends five `29 -> no reply` routes before keepalive and later service `10`, while external proceeds directly to recurring `250 -> 251` and has no observed service `29`.

The pinned public Sunrise source routes `notification29` with `ResponseMode::none` and an empty body codec. A server reply is therefore contradicted by the oracle and is not a candidate implementation.

## Required Work

1. Inspect the dedicated oracle’s ignored local handoff/evidence and public source call paths for client service `29`; do not use later service-123 payloads as evidence.
2. Add metadata-only instrumentation in the dedicated oracle only at the client-side transition/call path that produces service `29`. Do not retain payloads, identities, addresses, keys, tokens, or assets.
3. Before any launch, verify the dedicated trace DLL/settings, original external-validation DLL/settings hashes, Internet isolation, and absence of conflicting Old-School-D2 listeners.
4. Run one input-gated internal/default oracle observation only if the instrumentation is ready. Establish title-screen progression before beginning the bounded window.
5. Compare the recorded service-29 trigger/state with the external client’s documented stable wait and identify one falsifiable external semantic candidate.
6. Restore oracle files, re-check the untouched external-validation DLL/settings, document the result, validate, commit, push, and open a PR. Do not run an external replacement-server experiment unless the candidate requires exactly one safe controlled test.

## PASS Criteria

- Metadata-only evidence identifies the internal client-side trigger/state immediately preceding service `29`.
- The external comparison produces one falsifiable semantic candidate without inventing a service-29 reply or Queuez notification.
- Any controlled run satisfies the Human/UI Interaction Gate; tests pass; documentation and this next TODO are updated; and a session PR is opened.

## Non-Goals

Do not:
- modify the external-validation installation in place;
- change proven external BAP crypto, framing, or accepted replies;
- add a service-29 response;
- emit Queuez service `123`, account/character state, activity, or speculative notifications;
- alter client Internet isolation or contact public/Bungie services;
- continue into the next discovered boundary.
