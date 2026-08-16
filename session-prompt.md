# Old-School-D2 — AI Development Session Prompt

You are continuing development of **Old-School-D2**, a clean-room research project whose long-term goal is to make a historical Destiny 2 client running through Project Sunrise function against an independently implemented local replacement server.

This `session-prompt.md` file (located at a-wild-missingno/Old-School-D2 on GitHub) is intentionally designed to be copied into a **fresh AI-agent session at the beginning of every development session**.

The repository is the project memory and is located at a-wild-missingno/Old-School-D2 on GitHub.

Keep this setup in mind:
* You are running on a MacBook
* You execute on an Optiplex running Ubuntu
* Destiny 2 runs on a Legion Cube running Windows 10.

The Windows machine is isolated from the internet and communicates only and directly to the Optiplex (which you execute on).

SSH keys already exist for connecting to Windows from the Optiplex

Do **not** rely on memories of previous conversations, prior agent sessions, compressed context, or undocumented assumptions.

Everything needed to understand, operate, investigate, and continue this project should ultimately be represented in:

- source code
- tests
- scripts
- repository documentation
- experiment records
- sanitized fixtures/evidence
- local ignored configuration where machine-specific information is necessary

---

# Repository Roles

There are three authoritative layers.

## 1. `session-prompt.md`

This file defines:

- how you must work
- the current single development TODO
- session startup procedure
- evidence standards
- completion requirements
- cleanup requirements
- Git/PR workflow

The `CURRENT TODO` near the end of this file is the authoritative instruction for what this session should accomplish.

Do **not** replace it with a broader goal.

## 2. `docs/PROJECT_STATE.md`

This is the authoritative detailed technical state.

It should contain:

- confirmed protocol progress
- current frontier
- frozen working behavior
- current architecture
- proven protocol facts
- active hypotheses
- disproven hypotheses
- important evidence
- known unknowns

If this prompt and `PROJECT_STATE.md` disagree about a technical fact, investigate the discrepancy before coding.

## 3. Experiment records

`docs/EXPERIMENTS.md` indexes the individual records under `docs/experiments/`.

Experiments are evidence.

Do not silently rewrite historical observations simply because a newer hypothesis exists.

If an earlier interpretation becomes incorrect, mark it superseded and document the newer evidence.

---

# Public Documentation

`README.md` is the **only file intended primarily for ordinary GitHub users**.

Keep it readable and relatively concise.

It should explain:

- what Old-School-D2 is
- what it is not
- current high-level progress
- architecture at a useful level
- what currently works
- major limitations
- how to run/test the project where appropriate
- project safety/research principles

Do not turn README.md into an agent handoff, raw research notebook, or exhaustive protocol ledger.

Technical details belong under `docs/`.

Update README.md only when a session materially changes what a public visitor should understand about the project's capabilities, architecture, setup, or progress.

---

# Private / Local State

If present, read:

```text
.hermes/HANDOFF.local.md
```

This file is gitignored and may contain:

- current machine IPs
- SSH commands
- Windows paths
- certificate paths
- capture directories
- lab-specific launch commands
- local environment details

Never copy private/local values from this file into tracked files.

A committed template may exist at:

```text
.hermes/HANDOFF.local.example.md
```

---

# Core Engineering Principle

Do not try to:

> make Destiny work

as one large task.

Instead:

> Move the historical client forward by one evidenced state/protocol boundary at a time.

The preferred loop is:

```text
known-good behavior
        ↓
observe
        ↓
identify first divergence / missing event
        ↓
form one falsifiable hypothesis
        ↓
implement smallest evidenced change
        ↓
test locally
        ↓
run one controlled game experiment if needed
        ↓
inspect evidence
        ↓
confirm or reject hypothesis
        ↓
record result
        ↓
advance CURRENT TODO by one boundary
```

Prefer **monotonic progress**.

Once a protocol boundary is proven working, treat it as frozen unless later evidence directly contradicts it.

Do not repeatedly redesign already-working STUN, SignOn, ContentConfig, cryptography, BAP services, etc. merely because a later state is failing.

---

# Evidence Standard

Every important conclusion must be classified as one of:

## CONFIRMED

Directly supported by reproducible evidence such as:

- source code
- deterministic tests
- packet capture
- raw protocol artifact
- structured runtime log
- client log
- debugger/instrumentation output
- repeatable visible client behavior

## LIKELY

Strongly supported, but not yet directly demonstrated.

## SPECULATIVE

A hypothesis requiring an experiment.

Never silently promote LIKELY or SPECULATIVE claims to CONFIRMED.

---

# Anti-Hallucination Rules

You must follow these throughout the session.

1. Never claim code exists without opening it.
2. Never claim a test passes without running it.
3. Never claim a service is running without verifying it.
4. Never claim a packet/message was sent or received without evidence.
5. Never claim Git state without checking Git.
6. Never assume a previous agent's summary is correct when primary evidence is available.
7. Never fabricate protocol fields, service IDs, routes, message structures, or semantics.
8. Unknown values must remain neutrally named until evidenced.
9. Never invent client-side behavior because it would make an implementation convenient.
10. Never keep pursuing a hypothesis solely because substantial code has already been written for it.
11. When new evidence contradicts previous documentation, correct the documentation.
12. Prefer:

```text
UNKNOWN — requires evidence
```

over an unsupported explanation.

---

# Session Scope Rule

There must be exactly **one primary CURRENT TODO**.

Do not broaden the session into unrelated cleanup, architecture work, or downstream protocol implementation unless that work is directly necessary to complete the TODO.

When the TODO succeeds and exposes a new protocol boundary:

- document the new boundary
- write the next TODO
- stop development for this session

Do **not** automatically continue into the newly discovered TODO.

One session should ordinarily move the project forward by one logical research/development boundary.

---

# SESSION STARTUP

Perform this procedure at the beginning of every session.

## 1. Read the repository state

Read completely:

```text
session-prompt.md
docs/PROJECT_STATE.md
docs/EXPERIMENTS.md
README.md
```

Read `.hermes/HANDOFF.local.md` if it exists.

Then inspect any experiment/protocol/source documents referenced by the CURRENT TODO.

Do not begin implementation before this reconstruction is complete.

---

## 2. Inspect Git

Run at minimum:

```bash
pwd
git status --short --branch
git log --oneline --decorate -20
git remote -v
git diff
git diff --staged
```

Determine:

```text
CURRENT BRANCH:
HEAD:
WORKTREE STATE:
REMOTE STATE:
```

Preserve unrelated existing work.

Never silently discard:

- staged changes
- unstaged changes
- untracked research artifacts
- existing patches
- local `.hermes/` state

---

## 3. Start from current `main`

Development sessions should ordinarily begin from current `origin/main`.

Fetch remote state:

```bash
git fetch origin
```

Verify local `main` can be safely synchronized.

Prefer:

```bash
git checkout main
git pull --ff-only origin main
```

Do not perform destructive resets.

If local state prevents safe synchronization, preserve it and resolve the situation without losing work.

---

## 4. Check for unfinished session work

Before creating a new branch, determine whether an earlier session branch or pull request is still active.

Do not unknowingly redo the same TODO on a second branch.

If an existing unmerged PR contains the authoritative continuation of this exact TODO, inspect it first.

Do not merge PRs automatically unless explicitly allowed by the repository workflow.

---

## 5. Create a session branch

Create a dedicated branch for this session.

Use a descriptive format similar to:

```text
session/YYYYMMDD-short-task-name
```

Example:

```text
session/20260816-post-auth-oracle
```

All intentional tracked work for the session should occur on this branch.

Never perform ordinary development directly on `main`.

---

## 6. Baseline validation

Before modifying behavior:

- run the relevant existing tests
- verify the current documented behavior where practical
- inspect the implementation relevant to the TODO
- inspect recent history touching that implementation

Record any baseline failure before making changes.

A pre-existing failure must not later be presented as caused by the session.

---

# RESEARCH / DEVELOPMENT PROCEDURE

## 1. Define the frontier

Before editing code, establish:

```text
LAST CONFIRMED WORKING EVENT:
FIRST MISSING / FAILING EVENT:
EVIDENCE:
QUESTION THIS TODO MUST ANSWER:
```

If these cannot be determined, the first task is to gather the evidence needed to determine them.

---

## 2. Prefer known-good oracles

Where default/internal Sunrise performs behavior that the external replacement server does not yet reproduce, use the known-good Sunrise behavior as the primary oracle.

Preferred methodology:

```text
known-good internal/default path
              ↓
instrument
              ↓
capture ordered behavior
              ↓
external path
              ↓
compare
              ↓
FIRST semantic divergence
              ↓
implement that one missing behavior
```

Do not guess later behavior when an observable working implementation exists.

---

## 3. Keep experiments narrow

A controlled experiment should answer one clear question.

Examples:

```text
Does the client accept this exact server response?
```

```text
What is the first authenticated server-originated event?
```

```text
Does this publication cause the client to enter another state?
```

Do not change several independent variables in one experiment unless unavoidable.

---

## 4. Instrument before guessing

When behavior is unclear, improve observability first.

Use where appropriate:

- structured JSONL logs
- client logs
- server logs
- PCAPs
- sanitized fixtures
- payload hashes
- raw local artifacts
- source instrumentation
- screenshots / visual state
- timestamped state transitions

Do not commit sensitive/private/raw artifacts when repository policy excludes them.

Record their local paths and hashes where useful.

---

## 5. Preserve cryptographic/protocol invariants

Known-good encryption, framing, sequencing, and nonce behavior are fragile.

Do not casually refactor proven BAP cryptographic state while investigating an unrelated downstream protocol.

Nonce ownership must remain singular and deterministic.

Any change affecting:

- framing
- AES-GCM
- nonces
- connection sequencing
- confirmed service replies

requires direct justification and regression tests.

---

# GAME TEST PROCEDURE

Do not ask for a live Destiny test until the experiment is actually ready.

Before a live test verify all applicable items:

- relevant implementation complete
- tests passing
- listener/server started
- required ports listening
- logs rotated/prepared
- capture started if needed
- correct client configuration
- Windows SSH available
- client Internet isolation still verified
- no stale listener/process conflicts
- exact experiment question documented

Only then report:

```text
READY FOR GAME TEST

Action:
<minimum human action required>
```

If visual/client automation is available and authorized, use it instead of requiring unnecessary manual input.

After the run, inspect the evidence yourself.

Do not ask the user to interpret logs that the agent can retrieve.

---

# SUCCESS / FAILURE RULES

## If the TODO succeeds

Before declaring completion:

1. prove the success with client/server evidence
2. identify the newly exposed frontier
3. update tests
4. update technical documentation
5. update experiment records
6. update README.md if public project progress materially changed
7. replace CURRENT TODO in this file with the **single next logical task**

Do not begin that next task.

---

## If the TODO partially succeeds

Document exactly:

```text
WHAT PASSED:
WHAT DID NOT:
NEW EVIDENCE:
CURRENT FRONTIER:
```

Rewrite CURRENT TODO to target the remaining first divergence more precisely.

Do not falsely advance the project frontier.

---

## If the TODO fails

Record the failed hypothesis and evidence.

Do not leave the next session with instructions to blindly repeat the same attempt.

Update CURRENT TODO to the next falsifiable diagnostic/research step.

---

# DOCUMENTATION UPDATE RULES

At meaningful milestones update:

```text
docs/PROJECT_STATE.md
```

so that it accurately reflects:

- confirmed progress
- current frontier
- frozen behavior
- new unknowns
- superseded hypotheses
- important source/evidence locations

Update:

```text
docs/EXPERIMENTS.md
```

and create/update a detailed experiment document when a controlled experiment produced meaningful evidence.

Technical protocol discoveries should be documented under an appropriate location such as:

```text
docs/protocols/
docs/client-analysis/
docs/architecture/
docs/experiments/
```

Do not make documentation duplicate the same current-state paragraph in many different files.

`PROJECT_STATE.md` should be the detailed canonical technical state.

---

# README RULES

README.md is public-facing.

Update it when the session changes things such as:

- a major protocol boundary now works
- architecture materially changes
- installation/run instructions change
- dependencies change
- project capabilities change
- a major previous limitation is removed
- a major new limitation is discovered

Do not update README merely because an internal experiment occurred.

Keep raw protocol implementation details in `docs/`.

---

# CURRENT TODO MANAGEMENT

The CURRENT TODO section at the end of this file is deliberately mutable.

When completing a TODO:

1. determine whether its completion criteria were actually satisfied
2. preserve the result in project documentation
3. identify the first new unresolved boundary
4. replace the previous TODO with exactly one next task
5. include:
   - objective
   - known starting state
   - completion criteria
   - explicit non-goals where useful

The next TODO must be understandable to a completely fresh agent.

Do not embed large historical summaries in the TODO.

Reference repository evidence instead.

---

# SESSION END / CHECKPOINT PROCEDURE

Before ending every session, perform ALL applicable cleanup.

## 1. Stop experiment processes

Stop only project/lab processes started for the session.

Verify that temporary:

- Destiny processes if appropriate
- packet captures
- test HTTPS listeners
- UDP discovery listeners
- BAP listeners
- instrumentation processes
- temporary observers

are stopped.

Do not kill unrelated system services.

Preserve normal SSH access and client network isolation.

---

## 2. Preserve evidence

Ensure important evidence is either:

- represented in tracked sanitized documentation/fixtures, or
- retained locally and referenced by path/hash where appropriate

Never commit prohibited:

- Destiny binaries/assets
- credentials
- keys
- private LAN details
- raw sensitive captures
- copyrighted dumps
- session secrets

---

## 3. Run validation

Run the repository's complete relevant validation, ordinarily including:

```bash
scripts/run-tests.sh
python3 -m compileall -q src
```

plus any relevant static/lint/shell checks.

Report exact results.

---

## 4. Review the entire diff

Inspect:

```bash
git status --short
git diff
git diff --staged
```

Confirm:

- no unrelated modifications
- no secrets
- no private lab data
- no large accidental artifacts
- documentation agrees with implementation
- CURRENT TODO matches the actual new frontier

---

## 5. Update repository memory

Before committing, ensure:

```text
session-prompt.md
docs/PROJECT_STATE.md
docs/EXPERIMENTS.md
```

accurately describe the finished session.

Update README.md if warranted.

A fresh agent must be able to understand the next task without this conversation.

---

## 6. Commit

Create one or more focused commits.

Commit messages should explain the actual project advancement.

Avoid vague messages such as:

```text
updates
more work
fix stuff
```

---

## 7. Push the session branch

Push the session branch to `origin`.

Do not force-push over unrelated remote work.

---

## 8. Create a pull request

Create a PR from the session branch into `main`.

The PR description should contain:

```text
## Session objective

## Result
PASS / PARTIAL / FAIL

## What changed

## Evidence

## Tests

## New verified frontier

## Next TODO

## Safety / repository-hygiene notes
```

The PR should represent the complete checkpoint needed for the next session.

Do not begin the next TODO after opening the PR.

---

## 9. Final consistency check

Pretend all conversational context disappears.

Using only the PR plus:

```text
README.md
session-prompt.md
docs/PROJECT_STATE.md
docs/EXPERIMENTS.md
repository source/tests
```

verify that a fresh agent can determine:

1. what the project does
2. what is confirmed working
3. what changed this session
4. what remains unknown
5. exactly what the next TODO is
6. how the result was validated

If not, fix the repository before finishing.

---

# FINAL SESSION RESPONSE

When the session is fully checkpointed and the PR is created, return:

```text
SESSION COMPLETE

TODO result:
PASS / PARTIAL / FAIL

Branch:
...

HEAD:
...

Tests:
...

Verified advancement:
...

New frontier:
...

Next TODO:
...

Documentation updated:
...

README updated:
YES / NO — reason

Lab cleanup:
...

Pull request:
...

Anything requiring human attention:
...
```

Do not claim the session is complete until the Git branch, documentation, CURRENT TODO, validation, cleanup, and PR are all complete.

---

# PROJECT SAFETY / SCOPE

This is an isolated clean-room interoperability and preservation research project.

Maintain these constraints:

- the research client remains isolated from Bungie/public production infrastructure
- never forward, NAT, proxy, or tunnel client traffic to Bungie
- do not develop live-service cheats
- do not use leaked/proprietary server code, keys, credentials, or private infrastructure
- do not commit Destiny binaries or proprietary game assets
- keep machine-specific/private values out of tracked files
- independently implement only behavior established through controlled evidence and permissible reference material

---

# CURRENT TODO

## Objective

Produce one controlled, metadata-only **authenticated BAP** trace from the dedicated known-good internal/default Sunrise oracle runtime, so the previously instrumented outbound-send seam can identify the actual first post-auth event (or a deterministic earlier launch/authentication failure).

## Known Starting State

`docs/PROJECT_STATE.md` contains the detailed authoritative state.

The current external client is confirmed to reach a stable authenticated encrypted BAP connection.

Confirmed working behavior includes the currently documented request/reply sequence through recurring keepalive traffic.

The external client remains connected but does not advance to character selection, and no later client-originated route has been observed.

`docs/experiments/2026-08-16-internal-post-auth-oracle.md` records that the dedicated oracle runtime and trace DLL started its local transport but the attempted direct executable invocation did not reach BAP authentication. It is not an oracle trace.

`docs/client-analysis/post-auth-oracle.md` confirms from source that Queuez service 123 is not automatically emitted solely on authentication.

Do not modify already-confirmed protocol boundaries without contradictory evidence.

## Required Work

1. Reconstruct state from the documents above and inspect the dedicated oracle’s local ignored handoff/evidence before changing it.
2. Identify the full launcher/invocation used by the existing known-good internal/default client path; do not infer it from a direct `destiny2.exe` invocation.
3. Preserve the original external-validation runtime; use the existing dedicated oracle copy only.
4. Before launch, verify the trace DLL/settings and client Internet isolation, and confirm no Old-School-D2 external listener is running.
5. Run exactly one bounded internal/default oracle experiment with `external_server.enabled=false` and the existing metadata-only instrumentation.
6. Stop the game and retrieve only sanitized metadata/log evidence.
7. Determine whether authenticated BAP was reached. If it was, record the ordered `post_auth_send` trace and stop; if not, record the first deterministic launch/authentication divergence and replace this TODO with that more precise diagnostic.
8. Restore any changed oracle files and verify the original external-validation DLL/settings were unchanged.
9. Update documentation, validation, commit, push, and PR according to the result.

## Completion Criteria

This TODO is PASS only if:

- the controlled internal/default oracle reaches authenticated BAP
- the metadata-only trace records the ordered first post-auth outbound-send event, or records a deterministic authenticated state with no such event in the bounded window
- the launcher/configuration and evidence classification are documented without private values or raw payloads
- the original external-validation runtime is verified unchanged
- tests pass
- the next CURRENT TODO is written
- the session branch is committed, pushed, and represented by a PR into `main`

## Explicit Non-Goals

Do not:

- change the external replacement listener or its proven BAP crypto
- implement Queuez, account/character state, activity, or a notification
- alter client Internet isolation or contact public/Bungie services
- modify the existing external-validation installation in place
- send speculative notifications
- continue automatically into the next newly discovered boundary
