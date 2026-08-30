# Package-trust comparator audit

Date: 2026-08-30
Status: COMPLETE — source-backed local prerequisite identified; no runtime behavior changed

## Question

Does the current working/offline Sunrise comparator contain a client-local pre-character-select prerequisite that is absent from the external trace lineage, without inferring a server response or modifying client package verification?

## Sources compared

- External trace lineage: `jules-the-ai/sunrise-external-lab`, commit `3671dcd`, based on the older `b12a9da` Sunrise baseline plus the approved external SignOn handoff and trace-only diagnostics.
- Official Sunrise master: `stanuwu/Sunrise`, commit `01888412edd6aba5071b78fef83917c9e6ef21f4`.
- Existing external observations: authenticated BAP, nine one-way service-29 notifications, recurring keepalives, local patchable-bootstrap and investment-globals assertions, no client service 10, and no character-signin entry.

## Confirmed source differential

Current official Sunrise installs its `package_trust` component during Steam initialization, explicitly before base-package registration. The same component is also checked during main-image activation.

The official source describes the component as accepting three local package-authentication outcomes:

1. package-header RSA trust;
2. patchable extended-header authentication; and
3. cached-data hash authentication.

The external trace lineage predates that component and does not install it. This is an exact client-local differential that is upstream of both base-package registration and the missing character-signin entry.

The order is material: official Sunrise installs it at Steam initialization because base generation packages register before the ordinary callback-driven main-image hook sweep. The external trace's observed package assertions are later than external BAP/service 29, but that temporal observation does not remove the earlier local registration path as a candidate condition.

## What this does and does not establish

This audit establishes an independently sourced local difference between the working/offline comparator and the external trace. It does not prove that this is the sole cause of the black screen, that either recorded assertion is causal, or that the external listener needs any additional message.

In particular, the component changes client package-integrity acceptance. It is not a metadata-only observer. Therefore this project will not port, deploy, or activate it merely on the basis of this audit. It will not copy package data, change ContentConfig identity, or alter SignOn, BAP, service 29, Queuez, account state, or web-service handling.

## Safe next step

The next permissible experiment is a read-only compatibility probe only:

- resolve the three official component target classes against the isolated historical client;
- emit only a three-boolean/aggregate compatibility result, with no addresses, raw bytes, package names, headers, hashes, identities, or payloads;
- make no detour, memory-protection change, code write, return-value override, listener change, or server behavior change.

Success criterion: one unambiguous `compatible` or `incompatible` result before the existing external BAP path. A compatible result only validates that the official comparator's local prerequisite has applicable targets in this client; it does not authorize an integrity-bypass change. An incompatible result rules out directly reusing that comparator mechanism on this historical binary.

No Windows launch is warranted until the read-only probe is independently source-tested, Windows-built, and staged only to `external-trace`.
