# 2026-08-21 external trace provenance comparison

## Question

What trace-vs-baseline startup or external-transport difference is directly evidenced before the Marionberry observation could have reached the isolated listener?

## Method

No Destiny process, listener, capture, trace deployment, protocol response, or game observation was started for this comparison. The current Windows-lab scripts queried only runtime metadata and isolation/process state.

## Evidence

- The known-good `external-validation` runtime exists, has no running Destiny process, and its current DLL SHA-256 is `9f2fd0ef85b818eeb74e92a4dc33d151e242499cfccef08fa2e96fa45dc5c9ae`. Its current settings SHA-256 is `8a7f49fefa1e41d4f51021078db6ec1241c31101a5ac5b81d7c6790bfe4bc95c`.
- The prior trace-preflight record identifies the deployed trace artifact as SHA-256 `3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e`. That digest differs from the current baseline DLL digest.
- The `external-trace` runtime is absent now, as required by the prior observation cleanup. It therefore cannot provide a present installed-DLL or settings comparison.
- The documented source commit `d025f3d` is not an object in this repository. The documented Actions run `32069461540` was not retrievable through either recorded repository remote during this session. This establishes an evidence-access limitation, not that the source commit or run never existed.
- The current external-validation preflight reports IPv4/IPv6 forwarding disabled and Internet isolation passing. It also reports that interactive UI control is unverified; no launch was attempted.

## Result

**PASS for the provenance boundary; no protocol conclusion.** The first directly evidenced trace-vs-baseline startup difference is binary identity: the dedicated trace observation used a DLL artifact whose documented SHA-256 differs from the known-good external-validation DLL. This difference exists before any configuration lookup, outbound transport attempt, or listener application event.

This is sufficient to prevent attributing Marionberry to the replacement listener or to a missing BAP/HTTP response: the client-visible failure occurred with a different injected DLL, while the listener saw no application event. It does **not** prove that the trace instrumentation caused Marionberry, and it does not identify a particular hook, configuration value, or transport call as causal.

## First falsifiable diagnostic

Before any further client observation, recover the authorized trace-source/build provenance for the artifact documented above and perform a no-game-run reproducibility check:

1. obtain the exact source revision and build workflow record for the trace artifact through an authorized source repository or retained local build evidence;
2. rebuild it in Windows CI and require the emitted DLL SHA-256 to equal `3b72bbe0c18b466c8e39743fbb1ed7caa053acaf7ad041d5cc4b94b26380b65e`;
3. if the digest does not match, record a build-provenance break and do not deploy it; if it matches, inspect only the trace-only startup/transport hooks and add a payload-free, value-free stage marker for module initialization, external-config lookup outcome class, and first outbound transport result class; and
4. validate that metadata-only change in Windows CI without deploying or starting Destiny.

A matching rebuild plus stage markers makes the next startup divergence falsifiable without retaining retail text, BAP bodies, identities, endpoints, raw client data, or adding protocol behavior.
