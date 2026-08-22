# In-process character-sign-in probe design

Status: IMPLEMENTED / NOT BUILT OR DEPLOYED — source and regression tests only

## Purpose

Resolve the mismatch between Sunrise's successful in-process character-select hook installation and the zero exact matches seen by external static and process-memory readers. The proposed probe would report only bounded target/caller metadata from the same image view Sunrise already uses.

## Existing source primitives

- `executable::inspect_main_module` reads the current process main image and exposes executable PE ranges only.
- `patterns::collect_matches` can collect a fixed, bounded number of matching addresses without retaining image bytes.
- `patterns::resolve_all` already defines unique/missing/ambiguous semantics.
- `core::log::write` emits bounded structured events with a 1 KiB line cap.

## Proposed narrow implementation

In `character_select_hold.cpp`, during `install_character_select_hold` and immediately before the existing target resolution/attach:

1. Reuse the existing character-sign-in signature exactly; introduce no new signature and no guessed predecessor.
2. Call `inspect_main_module` and `collect_matches` with fixed storage for two addresses. Serialize only `match_count=0|1|2plus`.
3. If and only if there is exactly one target, locally inspect executable ranges for direct `E8 rel32` instructions whose destination equals that target. Retain at most four caller RVAs relative to the current main-module base, and serialize `direct_callers=0|1|2|3|4plus` plus only the collected RVAs.
4. Emit once, before attaching the existing detour. Do not retain bytes, disassembly text, target address, module base, arguments, native strings, package data, identities, payloads, or account data.
5. Continue to call the existing `scan_main_image_unique` and detour installation unmodified. The probe must not change its success/failure, the handler, bootflow state, package handling, services, or network behavior.

## Implementation result

The approved source-only implementation is in `Sunrise/src/client/hooks/bootflow/character_select_hold.cpp` with `tests/test_inprocess_character_signin_metadata.py`. It runs once before the existing resolver/attach, uses the existing signature, scans only Sunrise's in-process executable ranges, and preserves resolver/detour control flow. The source test suite passed 10 tests. No Windows build, deployment, or game run was performed for this implementation.

## Explicit exclusions

- No `ReadProcessMemory`, process handle, external scanner, debugger, thread suspension, or memory write.
- No additional game launch in this design phase.
- No source change or CI build yet.
- No game input, protocol/service behavior change, Queuez publication, account/world-state change, or package change.

## Review criteria before implementation

Implementation is justified only if the event has the stated fixed bounds, exact source-signature reuse, no raw bytes/string serialization, and a regression test that rejects payload/byte logging and behavior changes. Deployment/run needs a separate approval after source tests and Windows CI pass.
