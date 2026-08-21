# Old-School-D2 — AI Session Prompt

You are continuing **Old-School-D2**, a clean-room interoperability/preservation project for running a historical Destiny 2 client through Project Sunrise against an independently implemented local replacement server.

This file is the evergreen prompt given to a fresh agent each session. **The repository is project memory.** Use prior conversational memory only as a convenience; repository evidence is authoritative.

## Project Goal / North Star

The ultimate goal is to build an **independently implemented local replacement server** that is sufficiently compatible with the historical Destiny 2 client/Sunrise path to run the game without Bungie production services. Progress should converge toward an end-to-end playable path: boot/sign-on → configuration → authenticated BAP/services → account/character state → character selection → world/activity entry → preserved gameplay.

Protocol research, instrumentation, provenance work, and lab tooling are means to that goal, not ends in themselves. Each session should either:

- advance the client across the **first currently missing semantic boundary**; or
- remove one concrete blocker that is necessary to run the next falsifiable advancement experiment.

Avoid multi-session archaeology or tooling loops that do not improve the ability to run the next controlled client/server experiment. When a fresh, provenance-known build from a known-good baseline can provide stronger evidence than recovering an old experimental artifact byte-for-byte, prefer the fresh controlled build.

The replacement server is for the isolated preservation/interoperability lab. Do not contact, impersonate, proxy, or depend on Bungie production infrastructure.

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
11. **Optimize for frontier movement.** Provenance/tooling work is justified only when it controls a variable needed for the next experiment. Do not require byte-identical reproduction of an obsolete experimental binary when a fresh build from the verified known-good baseline plus a reviewed minimal instrumentation diff provides a stronger controlled comparison.

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

If verified interactive Windows visual/input automation is **not** available, fully prepare the experiment, then **PAUSE THE CURRENT SESSION** and say:

```text
READY FOR GAME TEST

Action:
<exact minimum user interaction required>
```

A human interaction gate is an expected **mid-session synchronization point**. It is **not** a `PARTIAL` result, not a reason to clean up, not a reason to rewrite `CURRENT TODO`, and not a reason to commit/open a PR. Wait for the user's confirmation in the **same agent session**, then continue the prepared experiment.

Do not start the bounded observation interval until that action occurs.

SSH/PowerShell/process launch alone do not count as interactive desktop automation. Automation may replace the human gate only after it is verified to view and control the actual Windows interactive session and is documented/authorized. Lack of interactive automation is not a blocker when the user can perform the minimum required UI action.

If required UI progression was not established because the user action never occurred, classify the run as **procedurally inconclusive**, not as a protocol/runtime failure.

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

Create a **fresh provenance-controlled external trace build from the current known-good external-validation source baseline**, then run one controlled external observation to identify the earliest evidenced divergence that prevents the replacement-server path from progressing toward character selection.

The observation must determine, at minimum, whether external task `ENUM(0)` completes, whether service `29` follows, whether service `10` follows, and where the first meaningful internal/default-vs-external divergence occurs.

## Starting Evidence

Use `docs/PROJECT_STATE.md` and the relevant experiment records as authoritative state.

Confirmed evidence includes:

- The current known-good external-validation DLL SHA-256 is `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`.
- The earlier failed external trace observation used a different instrumented DLL, recorded as `3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e`.
- A differing DLL digest is expected for an instrumented build. **The problem is not that the hashes differ; the problem is that source/build equivalence between that historical trace artifact and the known-good external-validation baseline was not established.** Therefore the Marionberry result from that trace cannot be attributed to the listener, config lookup, transport, or any specific hook.
- The historical trace source/build provenance is incomplete. Exact byte-for-byte reproduction of that obsolete artifact is useful only if readily available; it is **not** required to move forward.
- The internal/default Oracle reached character select. It recorded `world_controller` task `ENUM(0)` completion 16 ms before the first accepted one-way service-29 request; nine service-29 requests required no synthetic reply, and service `10` followed.
- The known-good external path reaches stable authenticated encrypted BAP with recurring `250 -> 251` traffic but does not reach character selection; service `29`/`10` have not been established on that stable external path.

The project needs a comparable external timeline produced by a trace whose provenance and instrumentation delta are controlled.

## Required Work

1. **Anchor the trace to the known-good baseline.**
   - Identify the exact authorized source revision/build inputs corresponding to the current known-good external-validation runtime as far as repository/local evidence permits.
   - If the historical trace source is readily recoverable, inspect it for useful prior hooks, but do not make recovery or exact old-digest reproduction a prerequisite.
   - If exact historical provenance cannot be recovered promptly, create a new dedicated trace branch directly from the verified current known-good source baseline.

2. **Keep the instrumentation delta minimal and reviewable.**
   Add only metadata needed to locate the first divergence, such as:
   - module initialization reached/not reached;
   - external-config lookup outcome **class** without endpoint/config values;
   - first outbound transport result **class** without endpoint/payload values;
   - timestamped numeric retail-task completion metadata sufficient to detect `ENUM(0)`;
   - service number/timing metadata already available from the lab/server path for services such as `29`, `10`, and recurring `250/251`.

   Do **not** retain formatted retail-log text, packet/BAP bodies, identities, account values, endpoint values, secrets, or unrelated client data.

3. **Prove the source delta, not historical binary identity.**
   - Review and document the source diff from the known-good baseline to the trace build.
   - The trace should differ only by the narrowly required observability changes and unavoidable build metadata.
   - Build in controlled Windows CI.
   - Record source commit, base commit, workflow/run identity, compiler/build context where practical, artifact SHA-256, and the reviewed instrumentation diff.
   - Exact reproduction of `3b72...b65e` is **not required**. If it reproduces naturally, record that fact; otherwise continue with the fresh provenance-known artifact.

4. **Preserve the known-good runtime.**
   - Use the installed `windows-lab` skill and `scripts/windows/` for routine Legion operations.
   - Record hashes of the original `external-validation` DLL/settings before the experiment.
   - Deploy instrumentation only to an approved dedicated `external-trace` copy.
   - Never instrument or overwrite `external-validation` in place.

5. **Preflight the controlled external experiment.**
   Verify before launch:
   - trace artifact hash matches the freshly built artifact;
   - trace settings match the intended external configuration except for controlled trace-only differences;
   - Legion Internet isolation passes;
   - OptiPlex IPv4/IPv6 forwarding remains disabled;
   - only the intended replacement-server listeners/capture are running;
   - no conflicting Destiny process is running;
   - original external-validation hashes remain unchanged.

6. **Run exactly one controlled external observation.**
   - Start the known-good replacement-server baseline behavior; do not add speculative protocol responses.
   - Start the dedicated trace runtime.
   - If interactive automation is not verified, use the Human / UI Interaction Gate above and **wait in the same session** for the user to start/advance the game.
   - Do not interpret absence of traffic until expected UI/bootflow progression is confirmed.

7. **Produce an aligned timeline.**
   Determine with evidence:

   ```text
   MODULE INITIALIZATION:       YES / NO
   EXTERNAL CONFIG LOOKUP:      success-class / failure-class / not reached
   FIRST OUTBOUND TRANSPORT:    success-class / failure-class / not reached
   AUTHENTICATED BAP:           YES / NO
   ENUM(0) COMPLETE:            YES / NO
   FIRST SERVICE 29:            timestamp / NONE
   SERVICE 29 COUNT:            value / NONE
   FIRST SERVICE 10:            timestamp / NONE
   SERVICE 10 COUNT:            value / NONE
   RECURRING 250 -> 251:        YES / NO
   FINAL OBSERVED CLIENT STATE: ...
   FIRST EVIDENCED DIVERGENCE:  ...
   ```

   Align this against the internal/default Oracle and the known-good external baseline. Do not force `ENUM(0)` to be the answer; if an earlier startup/config/transport/state divergence appears, that earlier boundary becomes authoritative.

8. **Interpret conservatively but move the frontier.**
   - If the fresh trace itself fails before the known-good external baseline, identify the earliest trace-vs-baseline startup/transport divergence and make the next TODO about that controlled instrumentation delta—not about resurrecting the old artifact hash.
   - If external never completes `ENUM(0)`, move the frontier to the nearest preceding semantic/task-state difference.
   - If external completes `ENUM(0)` but emits no service `29`, narrow the frontier to the condition between task completion and service `29`.
   - If service `29` occurs but service `10` does not, move the frontier between `29` and `10`.
   - If service `10` occurs, advance to the next first divergence toward character selection.

9. **Do not implement speculative server behavior in this observation session.**
   In particular, do not add:
   - service-29 acknowledgements;
   - Queuez service `123`;
   - guessed account/character state;
   - activity/world state;
   - speculative notifications.

   The purpose of this session is to establish the next semantic boundary the replacement server must implement.

10. After the observation:
    - stop only processes/captures/listeners started by this session;
    - restore the dedicated trace copy as appropriate;
    - verify original external-validation DLL/settings hashes are unchanged;
    - preserve raw evidence only in ignored/local form with hashes/references;
    - update project state/experiment documentation;
    - validate, commit, push, and open/update one PR;
    - write exactly one next TODO at the newly evidenced boundary;
    - do **not** begin implementing that next boundary in the same session.

## PASS Criteria

- A fresh external trace artifact is attributable to a known-good authorized source baseline with a reviewed minimal instrumentation diff and recorded CI artifact digest.
- One correctly started, isolated external observation is completed unless a deterministic earlier trace-vs-baseline failure itself establishes the first controlled divergence.
- The session establishes the earliest evidenced divergence relevant to advancing the replacement server toward character selection, including explicit `ENUM(0)`, service `29`, and service `10` results when those stages are reached.
- The original external-validation runtime remains unchanged.
- No speculative server behavior is introduced.
- Tests pass, documentation is updated, exactly one next TODO is written, and one session PR is opened/updated.

## Non-Goals

Do not:

- spend the session trying to reproduce an obsolete experimental DLL byte-for-byte unless that happens naturally from the recovered authorized build;
- treat a trace-vs-baseline hash difference by itself as a causal protocol divergence;
- contact or depend on Bungie/public production services;
- modify the known-good external-validation installation in place;
- implement Queuez/account/character/activity behavior without first evidencing that boundary;
- continue into the next discovered protocol boundary after this session completes.
