# Destiny 2 / Sunrise Reverse-Engineering Session Prompt

You are continuing an existing reverse-engineering project whose goal is to get an older Shadowkeep-era build of Destiny 2 running against a custom replacement server using Project Sunrise as the client-side foundation.

This is a continuing engineering project. **Do not treat this as a new project and do not assume prior conversational context is accurate or complete. Reconstruct the current project state from the code, Git history, logs, captures, documentation, and running processes before making changes.**

## Ultimate Goal

The long-term goal is:

```text
Historical Destiny 2 client
        ↓
Project Sunrise compatibility layer
        ↓
our external replacement services
        ↓
OptiPlex
```

Eventually the client should be able to progress through:

```text
startup
→ sign-on
→ character select
→ character/profile loading
→ destination/activity loading
→ playable PvE content
```

The immediate objective is always to advance the client **one observable state farther** while documenting what server/client behavior caused that advancement.

Do not attempt to rebuild the entire Destiny backend at once.

---

# Hardware / Network Environment

## MacBook

- Runs Hermes.
- This is the control/development workstation.

## OptiPlex

- Ubuntu Linux.
- Hermes executes commands on this machine.
- Hosts the reverse-engineered Destiny replacement services.
- Hosts traffic capture, listeners, logs, server code, and analysis tooling.
- Has Internet access for development.

## Legion Cube

- Windows 10.
- Runs Destiny 2 / Sunrise.
- IP:

```text
192.168.0.225
```

- Completely isolated from the Internet.
- Communicates directly with the OptiPlex.
- Must NEVER be allowed to contact Bungie or the public Internet.

SSH access from the OptiPlex already works:

```bash
ssh -i ~/.ssh/hermes_legion missingno@192.168.0.225
```

Do not alter this SSH configuration unless necessary.

Do not make networking changes that could break this SSH path without first creating and documenting a rollback method.

---

# Project Repository

Primary project:

```text
a-wild-missingno/Old-School-D2
```

There is also a local working copy on the OptiPlex.

The **local repository is the authoritative development state**.

The GitHub repository is useful for:

- checking remote history
- comparing committed changes
- reviewing branches
- identifying whether local work has been pushed

Do not assume GitHub contains the newest local work.

At the beginning of every session inspect at minimum:

```bash
pwd
git status --short --branch
git log --oneline --decorate -15
git diff
git diff --staged
git remote -v
```

Also inspect relevant recent server/client logs and currently running project processes.

If there are uncommitted changes, understand them before modifying the same code.

Do not overwrite, revert, discard, or replace existing work simply because you do not understand it yet.

---

# Sunrise

Project Sunrise is being used as the client-side compatibility layer.

Sunrise has an external-server mode capable of redirecting its expected network behavior to the OptiPlex.

Important architectural principle:

```text
Sunrise internal implementation
        ↓
evidence of expected client/server behavior
        ↓
understand that behavior
        ↓
implement equivalent functionality externally
        ↓
Sunrise external-server mode
        ↓
OptiPlex replacement service
```

Where Sunrise already has an in-process implementation of something the client expects, use that implementation as a reference for understanding the protocol/state transition.

Do not blindly copy implementation details without understanding their purpose.

We ultimately want the external server to provide the required behavior.

---

# Current Known Client State

The current reproducible client behavior is:

1. Destiny 2 launches.
2. The Shadowkeep title/start screen appears.
3. Enter is pressed.
4. A white loading screen appears for several seconds.
5. The display becomes black.
6. No visible error appears.
7. Character select is never reached.

This is the current blocker.

Do not assume the black screen itself is the root cause.

It may represent:

- a missing server response
- an incorrect response
- incomplete state initialization
- a protocol transition failure
- a missing callback/event
- bad runtime state
- an unexpected client-side value
- a transport failure
- another service the client expects next

Determine the cause experimentally.

---

# Session Startup Procedure

At the beginning of EACH new Hermes session, do this before proposing code changes.

## 1. Reconstruct repository state

Inspect:

- current branch
- staged changes
- unstaged changes
- recent commits
- recent files modified
- existing tests
- server architecture
- Sunrise modifications
- listener implementation

## 2. Find project documentation/state files

Search the repository for files such as:

```text
STATE.md
PROJECT_STATE.md
STATUS.md
NOTES.md
TODO.md
EXPERIMENTS.md
README.md
docs/
captures/
logs/
reports/
```

Read relevant ones.

If no persistent session-state document exists, create:

```text
docs/PROJECT_STATE.md
```

and use it from now on.

## 3. Inspect running processes

Determine whether:

- replacement listeners are running
- packet captures are running
- delegated/background agents left anything running
- stale server processes exist
- ports required by the client are already occupied

Do not assume a previously mentioned process still exists.

Verify it.

## 4. Inspect recent evidence

Review the most recent:

- server logs
- Sunrise logs
- PCAPs
- HTTP requests
- BAP traffic
- UDP discovery
- TCP connection attempts
- errors/exceptions
- client-side debug output

Prefer the most recent successful/reproducible experiment.

## 5. Identify the exact frontier

Before coding, state internally:

```text
LAST CONFIRMED WORKING STATE:
FIRST CONFIRMED FAILING STATE:
EVIDENCE:
CURRENT BEST HYPOTHESIS:
NEXT EXPERIMENT:
```

The next change should target that boundary.

---

# Evidence Rules

You must distinguish facts from hypotheses.

Use these categories internally and in documentation:

### CONFIRMED

Directly demonstrated by:

- source code
- packet capture
- logs
- reproducible client behavior
- debugger output
- test results

### LIKELY

Strongly supported by evidence but not proven.

### SPECULATIVE

A hypothesis needing an experiment.

Never convert a prior hypothesis into a "known fact" merely because it appeared earlier in the conversation.

If you cannot find evidence for a remembered claim, treat it as unverified.

---

# Anti-Hallucination Rules

This project has previously suffered from context compression, forgotten state, and invented assumptions.

Therefore:

1. **Never claim code exists without opening the file.**
2. **Never claim a test passes without running it.**
3. **Never claim a server/listener is running without checking the process/port.**
4. **Never claim a packet was sent or received without logs/capture evidence.**
5. **Never claim a Git change is committed without checking Git.**
6. **Never assume the contents of a file based on a previous conversation summary.**
7. **Never fabricate protocol fields, message IDs, endpoints, ports, responses, or structures.**
8. If a value is unknown, name it neutrally, such as:

```text
unknown_field_3
message_0x17
service_unknown_A
```

until evidence establishes its meaning.

9. If you realize an earlier conclusion was wrong, explicitly correct the project documentation.
10. Prefer saying:

```text
Unknown — next experiment will determine this.
```

over inventing an answer.

---

# Persistent Project Memory

Do not rely on the chat session as project memory.

Maintain:

```text
docs/PROJECT_STATE.md
```

It should contain at minimum:

```text
CURRENT CLIENT FRONTIER

LAST SUCCESSFUL TEST

CURRENT BLOCKER

CONFIRMED FINDINGS

ACTIVE HYPOTHESES

FAILED HYPOTHESES / DEAD ENDS

CURRENT SERVER ARCHITECTURE

KNOWN SERVICES / PORTS

RECENT IMPORTANT COMMITS

NEXT EXPERIMENT

HOW TO START THE LAB

HOW TO STOP THE LAB

HOW TO CAPTURE TRAFFIC

IMPORTANT PATHS

WINDOWS SSH COMMAND
```

Update this file whenever a meaningful discovery or architectural change occurs.

Keep it concise enough that a new agent can read it quickly.

Do not dump raw logs into it.

Reference log/capture filenames instead.

---

# Experiment Log

Maintain a separate chronological experiment log, for example:

```text
docs/EXPERIMENTS.md
```

Each significant game launch should record:

```text
EXPERIMENT ID:
DATE/TIME:

QUESTION:
What are we trying to determine?

CLIENT CONFIG:
Relevant Sunrise settings/build.

SERVER CONFIG:
Relevant server commit/config.

CHANGE:
What changed since the previous launch?

OBSERVATION:
What visibly happened?

NETWORK EVIDENCE:
Important connections/messages.

SERVER EVIDENCE:
Important logs/responses.

RESULT:
Did the client advance?

CONCLUSION:
What did we learn?

CONFIDENCE:
Confirmed / High / Medium / Low

NEXT TEST:
```

Do not repeat experiments unless there is a specific reason.

---

# Development Method

Follow this loop:

```text
observe failure
      ↓
identify last successful transition
      ↓
inspect client/Sunrise/server behavior
      ↓
form smallest useful hypothesis
      ↓
implement minimal change
      ↓
compile/test
      ↓
prepare logging/capture
      ↓
ask me to launch Destiny
      ↓
observe result
      ↓
document finding
      ↓
repeat
```

Prefer small, falsifiable experiments over large speculative implementations.

Do not make five unrelated protocol changes before a game test.

We need to know **which change caused which behavior**.

---

# Traffic / Server Monitoring

When preparing a live client test:

- start required server/listener processes
- verify expected ports are listening
- start packet capture if useful
- clear or rotate old logs
- record the server commit/hash
- record relevant Sunrise configuration
- verify SSH to Windows still works
- verify the Legion remains Internet-isolated

Use timestamps wherever practical so network activity, server logs, and visual game state can be correlated.

---

# Visual Client State

The visible game state is important evidence.

When possible, use the existing/available screenshot or visual-monitoring system to distinguish states such as:

```text
title screen
white loading screen
black screen
character select
loading spinner
error dialog
destination loading
destination loaded
```

Do not infer visual state solely from networking if screenshots or direct observation are available.

---

# Code Changes

Before editing:

1. Read the relevant implementation.
2. Understand current behavior.
3. Check recent Git history for that area.
4. Determine whether another unfinished change already addresses it.

After editing:

1. Build/compile as appropriate.
2. Run relevant automated tests.
3. Run static checks/linting if configured.
4. Inspect `git diff`.
5. Verify no unrelated files were accidentally changed.
6. Add or update tests when practical.
7. Update project documentation if the discovery matters.

Do not commit broken experimental code unless there is a deliberate reason.

Prefer focused commits with useful messages.

---

# Current Session Task

The immediate blocker is:

```text
Shadowkeep start screen
→ Enter
→ white loading screen
→ black screen
→ never reaches character select
```

Your task for this session is:

1. Reconstruct the current state of the local repository and running lab.
2. Read `docs/PROJECT_STATE.md` and recent experiment records if they exist.
3. Inspect recent commits, staged/uncommitted changes, logs, captures, and server processes.
4. Determine what has already been implemented toward passing the current blocker.
5. Identify the last confirmed successful client/server transition.
6. Identify the next expected client request or state transition.
7. Compare our external implementation with the relevant Sunrise internal implementation where useful.
8. Form the smallest evidence-backed hypothesis for why the client ends at the black screen.
9. Implement the smallest useful change needed to test that hypothesis.
10. Build and run all relevant checks/tests.
11. Prepare the OptiPlex listener/logging/capture environment.
12. Verify the system is actually ready for another game launch.

Then tell me explicitly:

```text
READY FOR GAME TEST
```

and provide only the short action you need me to perform on the Legion.

If the system is NOT ready, continue working autonomously.

Do not stop merely to tell me what you intend to code next.

Do not say:

```text
"I'll implement..."
"I'm going to work on..."
"The next change will be..."
```

and then return control to me.

Actually perform the implementation first.

Only stop before readiness if there is a genuine blocker requiring information or physical interaction from me.

---

# Definition of Ready for Game Test

Do not ask me to launch Destiny until all applicable items are true:

- required code change is implemented
- relevant code builds
- relevant tests pass
- listener is running
- expected ports are listening
- logs are ready
- capture is ready if needed
- previous stale processes will not interfere
- Sunrise/client configuration matches the experiment
- Legion SSH works
- Legion remains isolated from the Internet
- the exact experiment question is known

Then say:

```text
READY FOR GAME TEST

Action:
<very short instruction for what I should do>
```

Example:

```text
READY FOR GAME TEST

Action:
Launch Sunrise, press Enter once at the Shadowkeep screen, and do nothing else until I tell you the capture is complete.
```

After I perform the action, immediately inspect the resulting evidence rather than asking me to interpret technical logs that you can access yourself.

---

# Primary Engineering Principle

The goal of every session is not "write more server code."

The goal is:

**Move the historical Destiny 2 client one verified step closer to functioning against our custom server, while leaving enough evidence and documentation that the next session can continue accurately without relying on chat memory.**
