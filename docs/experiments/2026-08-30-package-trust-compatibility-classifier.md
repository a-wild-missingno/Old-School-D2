# 2026-08-30 package-trust compatibility classification

## Question

Does the historical external client expose all three target classes used by the current package-trust comparator, without changing integrity behavior?

## Scope and safeguards

The diagnostic was limited to an in-process read-only image classifier. It emitted only three aggregate booleans and an aggregate compatibility result. It installed no detour, made no memory or code write, made no return-value override, and did not change packages, content, account state, listener behavior, BAP, or server responses. The official package-integrity component was not ported or activated.

A controlled Windows CI artifact was built and staged only in the dedicated `external-trace` runtime. The protected validation runtime was not modified. The lab preflight confirmed ContentConfig identity, forwarding-disabled isolation, and public-HTTPS blocking before launch.

## Evidence

- The source-level regression suite passed: 94 tests.
- The Windows CI build completed successfully for the scoped classifier artifact.
- The client emitted one aggregate classifier event: all three target classes were present and the aggregate result was compatible.
- The ordinary local bootstrap then reached the previously confirmed authenticated BAP path and emitted service-29 notifications with no reply. It did not emit client service 10 during the bounded observation.
- The client log reported local patchable-bootstrap and investment-globals package-load assertions after the normal bootstrap path. These are observations only; no package data was copied or altered.
- The operator reported the same black screen and no visible error.

## Result

**COMPLETE / NEGATIVE FOR THE COMPATIBILITY-ONLY HYPOTHESIS.** The current comparator target classes apply to the historical binary. That establishes applicability, not that the comparator is the cause of the black screen. Because the diagnostic did not change comparator behavior and the visible result/protocol frontier were unchanged, it does not support porting, bypassing, disabling, or otherwise changing package-integrity behavior.

## Cleanup and verification

The Destiny process, capture, HTTPS/BAP listener, and discovery listeners were stopped. The temporary external-trace DLL was restored from its pre-test backup after its initial in-use lock cleared. Runtime hashes were re-recorded, and the lab isolation check passed with IPv4 forwarding disabled, IPv6 forwarding disabled, and public HTTPS blocked.

## New frontier

The current package-trust comparator's target classes are present in the historical client, but a read-only applicability check does not explain the missing client service 10/character-select transition. Do not repeat this same classifier. The next investigation must identify a source-backed semantic prerequisite for the post-service-29 transition without inventing a service response, account state, Queuez publication, package data, or integrity override.
