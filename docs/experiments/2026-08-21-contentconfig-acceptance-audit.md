# ContentConfig acceptance audit

Date: 2026-08-21
Status: complete — first structural mismatch identified; no game launch

## Scope

This was an evidence-only comparison of the clean-room Python listener's ContentConfig input path against the authorized local Sunrise reference source. It did not start Destiny, modify the protected baseline, start listeners, or retain cache bytes, identifiers, GUID text, payloads, certificates, or credentials.

## Reference contract

The Sunrise cache reader accepts a version-2 cache only after it verifies the exact cache layout, the stored build fingerprint against the complete canonical row set, and derives the ContentConfig UUID from that verified fingerprint. The reference encoder then writes that derived UUID as top-level protobuf field 5.

The client-side ContentConfig path records that it compares the returned 36-character UUID with the fetch token before it can proceed.

## Sanitized local audit results

| Invariant | Result |
| --- | --- |
| Manifest cache is nonempty and rows are ordered | PASS |
| Cache build fingerprint corresponds to its rows | PASS |
| Locally configured external ContentConfig UUID equals the cache-derived UUID | **FAIL** |

The Python listener was serving the configured `OLD_SCHOOL_D2_CONFIG_GUID` instead of deriving the response UUID from the verified manifest cache. The two public identifiers were not equal in the local lab configuration. No identifier values are recorded here.

## Interpretation

This is the first source-backed structural mismatch that can explain the observed `turkey` failure at the ContentConfig acceptance boundary. It is not proof of sole causality: no post-fix game observation has been run, and no inference is made about BAP or later services.

The manifest itself is not the first mismatch: its stored build fingerprint matched the rows under Sunrise's published fingerprint/UUID derivation. The mismatch lies specifically between that derived identity and the listener's separately configured response identity.

## Safe next step

Before any new game observation, reconcile the external runtime's ContentConfig fetch token and its response field-5 UUID to the same cache-derived public identity, preserving the cache and protected baseline. Add a preflight identity guard so a mismatch fails before a listener can serve a structurally inconsistent response. This audit intentionally does not alter ignored runtime settings or protocol behavior.
