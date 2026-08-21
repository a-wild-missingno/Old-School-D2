# Windows lab control

## Purpose

`scripts/windows/` supplies deterministic, process-level control of the
isolated Windows Legion from the repository. It replaces per-session ad-hoc
SSH/PowerShell snippets and does not alter protocol behavior or network
isolation.

## Install the Hermes skill

The checked-in `.hermes/skills/windows-lab/SKILL.md` is source-controlled project
documentation; Hermes does **not** auto-discover repository-local skills by name.
Install it once on the machine running Hermes (the MacBook, not the Ubuntu SSH
backend), then begin a fresh Hermes session:

```bash
hermes skills install https://raw.githubusercontent.com/a-wild-missingno/Old-School-D2/main/.hermes/skills/windows-lab/SKILL.md --name windows-lab
```

Verify with `hermes skills list` or `/skill windows-lab`. Updating the repository
does not automatically update an installed profile skill; explicitly run the same
installation command again after a skill update.

## Private configuration

Copy `.hermes/windows-lab.local.env.example` to the ignored
`.hermes/windows-lab.local.env`. The private file contains the SSH target and
maps aliases to local Windows runtime directories. Never commit it, a key,
address, binary, DLL, log, capture, or runtime path.

The accepted aliases are `oracle`, `external-validation`, and `external-trace`.
An unknown alias is rejected. `external-validation` is the protected known-good
baseline: trace deployment refuses it unconditionally. Instrumentation belongs
on a dedicated `external-trace` (or privately authorized oracle) copy.

## Commands

```text
scripts/windows/status.sh
scripts/windows/preflight.sh <runtime>
scripts/windows/start-destiny.sh <runtime>
scripts/windows/stop-destiny.sh
scripts/windows/hash-runtime.sh <runtime>
scripts/windows/create-trace-runtime.sh external-validation external-trace
scripts/windows/deploy-trace.sh <runtime> <prepared-artifact>
scripts/windows/restore-runtime.sh <runtime>
scripts/windows/tail-sunrise-log.sh <runtime> [1..500]
scripts/windows/screenshot.sh <runtime> [local-png-path]
scripts/windows/verify-isolation.sh
scripts/windows/probe-transport-baseline.sh
scripts/windows/cleanup-test.sh [--destiny]
```

`create-trace-runtime.sh external-validation external-trace` makes a fresh dedicated copy only when the trace target is absent and no Destiny process is running. It hashes the source/target DLL and settings and removes the target on a mismatch; it never changes the protected source.

`deploy-trace` hashes the local artifact, backs up the managed target DLL,
deploys, requires remote SHA-256 equality, and records a restore manifest under
the dedicated runtime. `restore-runtime` restores only a file managed by that
manifest. Cleanup touches only exact project process names privately configured
for the lab; it does not alter isolation.

## Preflight and isolation

`preflight` is the normal first command. It reports SSH, runtime existence,
process status, runtime hashes, forwarding state, listener conflicts, Legion
public-HTTPS isolation, and separate process/UI readiness values. Isolation
verification is read-only: gateway IPv4/IPv6 forwarding must be disabled and
configured public HTTPS probes must fail from Legion. It reports `ISOLATION=PASS`
or `ISOLATION=FAIL`.

A representative successful preflight has this shape:

```text
WINDOWS_SSH=PASS
RUNTIME=external-trace
RUNTIME_EXISTS=PASS
DESTINY_RUNNING=NO
DLL_SHA256=<sha256>
SETTINGS_SHA256=<sha256>
INTERNET_ISOLATION=PASS
IPV4_FORWARDING=DISABLED
IPV6_FORWARDING=DISABLED
CONFLICTING_LISTENERS=NONE
INTERACTIVE_CONTROL_VERIFIED=NO
READY_FOR_PROCESS_LAUNCH=YES
READY_FOR_AUTOMATED_UI_TEST=NO
```

## Interactive-session launch

`start-destiny.sh` does not use SSH's Session 0 process context. It discovers the
currently logged-in Windows Explorer session, resolves its owner dynamically, and
creates a uniquely named one-shot Scheduled Task with the Windows `Interactive`
logon type. The script waits for a `destiny2.exe` process whose Session ID and
executable path match that target, then reports the PID and interactive-session ID.
If no interactive Explorer session exists, task registration fails, or the process
exits before verification, it returns failure rather than claiming success.

The temporary task and launch-state record are owned by the project and removed by
`cleanup-test.sh`; task cleanup does not stop a still-running Destiny process.

## Screenshots

`screenshot.sh` runs a short-lived Windows Scheduled Task in the currently
logged-in Explorer session, captures the virtual desktop, verifies the downloaded
file has a PNG signature, and removes both the temporary task and remote image.
By default it writes a timestamped PNG under `artifacts/screenshots/`, which is
ignored by Git. It requires an active interactive Explorer session and supplies
visual evidence only; it does not provide keyboard or mouse control.

Example:

```bash
scripts/windows/screenshot.sh external-validation
```

## Process control versus desktop control

A running `destiny2.exe` proves only that a process exists. It does not prove a
title screen, menu, button action, or any protocol boundary. `status` and
`preflight` deliberately report `INTERACTIVE_CONTROL_VERIFIED=NO` and
`UI_STATE=unknown` unless actual Windows desktop visual/input automation has
been independently verified. SSH-launched processes are explicitly marked as
noninteractive launch context.

When UI interaction is required and interactive control is unverified, the
agent must remain in the session and request the minimum exact user action with
the `READY FOR GAME TEST` gate in the Windows-lab skill.

## Failure modes

- Missing private configuration or aliases: populate the ignored local file;
  do not put substitutions in Git.
- Duplicate process: stop the approved process or use the explicit duplicate
  override only when the experiment authorizes it.
- Missing backup/restore manifest: do not manually delete unrelated runtime
  files; investigate the dedicated runtime.
- Isolation failure: do not launch the client. Repair the lab outside these
  scripts, then re-run the read-only verification.

## No-game transport baseline probe

Start the session-owned local listeners and filtered capture, then run `scripts/windows/probe-transport-baseline.sh`. It sends recognized NatProbe requests from Legion and makes one bounded HTTPS TCP connection. Pair its PASS output with capture metadata showing UDP request/reply and TCP SYN/SYN-ACK before a game observation. Stop the capture and listeners afterward. This probe is transport-only; it does not launch Destiny or make an HTTP request.
