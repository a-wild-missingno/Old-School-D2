# Character-sign-in static call-site scan

Status: COMPLETE — no static target recovered from the on-disk executable

## Authorized scope

The user explicitly authorized offline/static analysis of the locally installed game executable only. The game was not launched, patched, or inspected in memory. The scanner reads executable bytes, reports only bounded counts/RVAs and the executable SHA-256, and deletes its temporary remote script after execution.

## Method

`scripts/windows/static-character-signin-callers.sh external-trace` copies a read-only PowerShell scanner to a temporary remote path, scans every PE section of the configured on-disk executable for the exact wildcarded `character_signin_enter` signature already defined in Sunrise source, and, only when unique, scans for direct `E8 rel32` call sites to that RVA. It retains no code bytes, payloads, package data, account data, text, or user data.

## Observation

```text
STATIC_ANALYSIS=READ_ONLY
IMAGE_SHA256=81964380664e7fcee3c620085a157fdeaf91fefacf7214907820f188bbeb4ced
TARGET_SIGNATURE_MATCHES=0
```

The signature was absent from all on-disk PE sections, so no target RVA or direct caller can be derived statically.

## Result

**CONFIRMED:** this offline image does not contain the source-defined signature in its file representation. The source hook's prior successful runtime installation identifies a target only in the loaded main image; this static scan cannot establish whether the difference is load-time transformation, a version/build mismatch, or another runtime-image distinction.

**NOT justified:** no caller marker, no guessed signature, and no direct-call conclusion. A static direct-call scan cannot progress without a unique on-disk target.

## Next boundary

Further progress would require separately authorized, bounded observation of the loaded process image after it starts, or independently authorized symbols/disassembly matching this executable. Neither is part of the completed offline-only scope.
