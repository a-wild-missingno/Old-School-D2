# Internal/default post-auth BAP oracle

Date: 2026-08-16

Status: complete — diagnostic result; no external server behavior changed.

## Question

What is the first server-originated encrypted BAP event in a known-good internal/default Sunrise run after authentication, and is Queuez involved?

## Safety pre-check

- **CONFIRMED:** the existing external-validation client process was stopped only after its DLL/settings hashes and timestamps were recorded locally.
- **CONFIRMED:** independent checks to two public HTTPS endpoints failed from the client before the oracle launch; no network-isolation rule was changed.
- **CONFIRMED:** no Old-School-D2 HTTPS, BAP, discovery listener, or packet capture was started for this internal/default oracle.
- **CONFIRMED:** the oracle used a separate local runtime copy. The original external-validation DLL and settings hashes were unchanged after setup and cleanup.

## Setup

A dedicated local Oracle runtime used the Windows-CI-built metadata-only Sunrise trace DLL. Its copy alone had `external_server.enabled` set to false and the server log threshold set to `info`; the file sink was already enabled. The original runtime was not edited. The artifact, preflight metadata, and resulting raw local log remain ignored local evidence.

## Observation

The instrumented DLL loaded successfully and its internal BAP transport listener reported startup. During the bounded 100-second run, the client process remained alive but did not progress to BAP authentication. The oracle log contained no `post_auth_send` record and no authenticated BAP route record.

**Procedural limitation (CONFIRMED):** no visual-state record was captured, no keyboard/controller input event was recorded, and no action equivalent to pressing Enter at the Shadowkeep title/start screen was performed. The run therefore did not test whether the dedicated runtime could reach authenticated BAP after normal title-screen start input. It must not be interpreted as a launcher/invocation mismatch.

The sanitized log facts were:

```text
server transport listener started on the configured local BAP port
client Steam initialization succeeded
egress hook installation completed
```

No payload, account, character, token, key, private address, or packet content is committed.

## Evidence

- Public source call chains: `docs/client-analysis/post-auth-oracle.md`.
- Local metadata-only oracle log SHA-256: `01f82d6aab1bf8bad7adac0790401b14eea8a777b6d5e93cc426e51e5395ad4e`.
- The separate Sunrise instrumentation build passed Windows CI before the run.
- The original runtime DLL SHA-256 before and after the oracle was `2f447c4ec10bbfdd20baa10170e9eed7bb8e97292223bec7fb56eace076cb5fc`.
- The original runtime settings SHA-256 before and after the oracle was `f46370633b3ef00af8abda27fcf5b51bcab84b44db6becb2eaf3a58325574eae`.

## Result

**PARTIAL / procedural diagnostic.** The instrumentation build and dedicated internal/default runtime were validated through transport startup, but the required title/start-screen input did not occur. This invocation did not reach the required authenticated BAP state, cannot establish an ordered post-auth outbound oracle, and provides no authority to emit a Queuez frame externally.

## Follow-up

Run the already-prepared dedicated internal/default runtime, perform exactly one Enter-equivalent action at the title/start screen, and leave it running for the bounded observation. Only if that controlled input run fails before authentication should launcher/invocation behavior be investigated. Capture exactly one authenticated oracle trace and compare it to the external stable wait before changing the external listener.