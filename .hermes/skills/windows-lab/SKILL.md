---
name: windows-lab
description: Deterministic process-level control of the isolated Windows Destiny lab.
version: 1.0.0
---

# Windows lab control

Use the repository scripts in `scripts/windows/`; do not regenerate ad-hoc SSH or PowerShell commands.

## Private setup

Copy `.hermes/windows-lab.local.env.example` to the ignored
`.hermes/windows-lab.local.env`, then fill it locally. It maps the only accepted
runtime aliases: `oracle`, `external-validation`, and `external-trace`.

`external-validation` is the known-good baseline. `deploy-trace.sh
external-validation ...` always refuses. Deploy instrumentation only to a
dedicated trace/oracle runtime explicitly authorized by private configuration.

## Command interface

- `status.sh` — SSH/process/listener status. It reports `process_running` facts
  independently from desktop facts.
- `preflight.sh <runtime>` — ordinary experiment readiness. Run this first.
- `start-destiny.sh <runtime>` — launches through a one-shot Windows Task Scheduler task bound to the current interactive Explorer session. It verifies the process persists in that session; it does not start a game test.
- `stop-destiny.sh` — stops only `destiny2.exe`; idempotent when none exists.
- `hash-runtime.sh <runtime>` — comparable SHA-256 values for DLL/settings and
  optional movement state.
- `deploy-trace.sh <runtime> <artifact>` — backs up, deploys, verifies exact
  SHA-256 equality, and records a managed restore manifest.
- `restore-runtime.sh <runtime>` — restores only a DLL backup made by deploy.
- `tail-sunrise-log.sh <runtime> [lines]` — bounded tail (1–500 lines).
- `verify-isolation.sh` — confirms gateway forwarding is disabled and public
  HTTPS probes are blocked from Legion; it never changes isolation.
- `cleanup-test.sh [--destiny]` — cleans only configured project processes and,
  with explicit `--destiny`, approved Destiny processes. It never changes
  persistent isolation.

## Process control is not UI control

Launching `destiny2.exe` is process control, not interactive game control. A
running process never proves that the title/menu/UI boundary was crossed.

When `INTERACTIVE_CONTROL_VERIFIED=NO`, prepare the experiment but pause in the
same agent session and ask exactly:

```text
READY FOR GAME TEST

Action:
<minimum exact user interaction>
```

This is a required human gate, not a PARTIAL result and not a reason to end the
session. SSH, PowerShell, and a Task Scheduler launch into the interactive session do not verify visual
or input access to the actual Windows interactive desktop.

## Standard workflow

1. `scripts/windows/preflight.sh external-trace`
2. Hash the baseline and target as appropriate.
3. Start the requested alias. Do not interpret it as a game observation.
4. If UI interaction is required and unverified, use the human gate above.
5. After the bounded work: stop only approved test processes, run cleanup,
   restore a modified trace runtime, then re-hash the protected baseline.
