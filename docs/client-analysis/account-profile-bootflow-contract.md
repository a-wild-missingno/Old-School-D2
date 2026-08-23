# Account/profile bootflow contract audit

Date: 2026-08-23
Status: COMPLETE — no source-backed external adapter identified; no runtime behavior changed

## Question

Can the external replacement safely model a minimal account/profile completion field before the client’s missing service-10 boundary, based on current public Sunrise source and the upstream profile-setup work?

## Sources reviewed

- Official `stanuwu/Sunrise` `master` at `01888412edd6aba5071b78fef83917c9e6ef21f4`.
- Official default configuration at `Sunrise/resources/default_settings.json` (schema version 8).
- Current-master state parser: `Sunrise/src/core/settings/state_settings.cpp`.
- Current-master account state: `Sunrise/src/state/account/account_state.h`.
- Current-master family-4 account encoder: `Sunrise/src/middleware/datagen/family4/account/account_encoder.cpp`.
- Current-master BAP routing and web-service runtime.
- Open, unmerged upstream PR #75, `replaces profile_setup_skip's hook with the server side equivalent`, head `d2e7f08d7181ec62351466c63d1af77f6c4072ea`.

## Field-level result

| Candidate | Current master | Open PR #75 | Earliest observed external relevance | Result |
| --- | --- | --- | --- | --- |
| `state.account.primary_soid` | Parsed and used as account identity | unchanged | Account state/Family-4 source only | No standalone external wire contract established |
| Complete account settings | Parsed in master | unchanged | Family-4 account encoding | No client request for this state is observed before service 10 |
| Account/character/inventory state | Parsed and encoded in master | expanded indirectly | Family-4/Queuez publication path | Downstream of the missing service-10 request |
| `profile_setup_completed` | Not present in master parser, state, or encoder | adds settings field, account byte at native offset `0xB90`, WS opcode 701 parsing, and monotonic update | WS-701 is processed by the server web-service runtime | Not a valid pre-service-10 adapter candidate |

## Why PR #75 does not unblock the current external route

PR #75 handles the profile marker inside the server web-service runtime after a web-service request is received. The public BAP router maps web service to a correlated request/reply route. The external trace has not emitted client service 10, which is the source-backed predecessor for the observed internal service-11 response and later Queuez publication.

Therefore the external listener has no observed service-10/web-service request through which it could receive WS-701. Pre-populating or inventing a profile-completion field in SignOn, BAP bootstrap, service 29, or an unsolicited Queuez frame would not follow the reviewed source path.

The open PR is valuable evidence that profile setup is represented in account state in newer Sunrise work. It does not establish that the field is the missing earlier transition in the historical external route.

## Consequence

**DISPROVEN for the current evidence:** implementing an external profile-setup/WS-701 adapter is the fastest source-backed way to produce client service 10.

No account/profile adapter, test fixture, endpoint, Web Service handler, Queuez notification, or BAP behavior was added. Existing client/server behavior remains frozen.

## Current source-backed frontier

The client has completed the transport and authenticated BAP prefix and now reaches one-way service 29, but it does not enter the existing character-sign-in handler or emit service 10. The remaining frontier is client-local/native control flow before that handler, not a server account field whose only demonstrated handling occurs after the missing request.

## Next action

Select one separately scoped, source-backed metadata-only hypothesis for a non-canonical use of the existing read-only character-signin target reference, or locate a different unique predecessor from current public Sunrise source. Do not run a Windows test until that hypothesis has a single unambiguous success criterion.
