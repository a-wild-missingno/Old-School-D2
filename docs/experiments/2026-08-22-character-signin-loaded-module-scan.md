# Character-sign-in loaded-module scan

Status: COMPLETE — bounded external read sees no target signature or direct caller

## Authorized scope

The user explicitly authorized a launch with no title-screen input and bounded, read-only loaded-main-module inspection. The scanner reads only PE-section memory from the launched process and returns counts, image size, and RVAs if a unique target exists. It does not write process memory, patch code, retain bytes, capture payload/account/package data, or change service behavior.

## Method

`scan-loaded-character-signin-callers.sh external-trace` uses a temporary PowerShell scanner to read the main module via `ReadProcessMemory`, scan every loaded PE section for the source-defined wildcard signature, and scan direct `E8 rel32` callers only if that target is unique. It then removes the temporary scanner. The trace runtime was launched without title-screen input and stopped immediately after the bounded observation.

## Observation

```text
LOADED_MODULE_ANALYSIS=READ_ONLY
MODULE_IMAGE_SIZE=145091072
SECTIONS_READ=11
BYTES_SCANNED=145070000
PREFIX4_MATCHES=11632
TARGET_SIGNATURE_MATCHES=0
```

The scan covered eleven loaded sections and 145,070,000 bytes; many generic four-byte prefixes were observed, so the zero exact match is not a no-read or empty-image result. It yielded no target RVA and therefore no direct-caller scan result.

## Result

**CONFIRMED:** the bounded external process-memory reader cannot recover the exact source-defined target signature from this loaded main-module representation, even though the injected trace log reports that Sunrise installed the character-select hook during startup.

**UNKNOWN:** whether this discrepancy is caused by process-memory-view restrictions, target transformation visible only in-process, a runtime-version distinction, or another representation difference. The observation does not identify a predecessor or authorize a guessed marker.

## Safety and cleanup

No title input or game test occurred. Destiny was stopped; no listeners remained; IPv4/IPv6 forwarding stayed disabled; public HTTPS remained blocked; protected external-validation DLL/settings hashes stayed unchanged.

## Next boundary

A caller cannot be derived with the approved external read-only view. Any further attempt would require a separately reviewed design for **in-process** bounded self-observation, still read-only and metadata-only, because that is a different scope from external process-memory inspection.
