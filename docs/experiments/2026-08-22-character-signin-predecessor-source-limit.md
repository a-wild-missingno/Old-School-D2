# Character-sign-in predecessor source-limit review

Status: COMPLETE — no unique predecessor exists in the authorized Sunrise source

## Question

Can a unique, metadata-safe predecessor of the character-sign-in enter handler be identified from authorized Sunrise source alone?

## Review

The shared character-select hook resolves the target only by a unique byte signature named `character_signin_enter`, then attaches a detour. The source contains no caller/call-site signature, no target table entry, no symbolic call graph, and no state-machine predecessor for that game-native handler. Repository history shows the handler hook was introduced with the same signature-only implementation; no later source records a predecessor.

Searches across the external trace and reference source find the target label only in the hook itself. The bootflow lifecycle only installs the hook; callback dispatch calls the worker after activation but does not call the game-native boot-step handler. Thus the source can establish that the external route has not entered the target, but cannot establish which native branch/caller would reach it.

## Result

**CONFIRMED:** no concrete predecessor target is source-backed. Adding a marker at any guessed nearby signature or generic callback would not distinguish the native branch and would violate the one-variable evidence requirement.

**No code change:** no new probe, no game launch, and no replacement-service/protocol/package/account behavior changed.

## Scope boundary

Finding an actual caller now requires a separately scoped static call-site analysis of the locally installed game executable or other authorized symbol/disassembly evidence. That is outside this source-only task and must be explicitly authorized before proceeding.
