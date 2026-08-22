# Post-investment bootflow boundary review

Status: PARTIAL — external path has not entered the existing character-select boot-step hook

## Question

After completed investment refresh, what is the first source-backed native transition that still separates the internal/default service-10 path from the external black-screen path?

## Source comparison

The external-trace diff from baseline contains only the external SignOn handoff and metadata-only tracing/readiness/assertion changes. It contains no modification under `client/hooks/bootflow` or `steam/runtime/callbacks`; every bootflow implementation file has the same SHA-256 in external trace and reference.

The shared callback dispatcher runs `server::service(now)` then `client::content::investment::worker::service(now)` after main activation. The completed external observation proved the worker's persistence-complete result. There is no external-trace source change on that next callback/bootflow path.

The earliest existing native bootflow hook that directly represents character-select entry is `character_select_hold.cpp::enter_handler`. It runs the original character-sign-in enter handler first, then logs `ev=bootflow stage=character_select result=held` once. The dedicated internal/default oracle reached character select after title-screen input. In each current external black-screen observation, the trace shows only the install line (`result=ok`), never the entry line (`result=held`). Later bootflow execution markers are absent as well, including profile-setup skip, join-ready predicate evaluation, orbit handoff release, spawn-world phase, and fade release.

## Result

**CONFIRMED:** after fully completed local investment refresh, the external run has not reached the existing native character-sign-in enter handler that the internal/default route reaches on character-select entry. This is a stronger boundary than readiness/persistence but remains an ordered observation, not a demonstrated cause.

**NOT justified:** adding another trace marker at that hook would duplicate the existing once-only `result=held` evidence. No source-backed code change is warranted by this review.

## Next falsifiable step

Use source-only signature/call-site review to locate a predecessor of the character-sign-in enter handler that is observable without capturing arguments, native text, package data, identities, or payloads. Add at most one bounded entry/order marker only if the predecessor has a unique source-backed target. Do not launch the game until that criterion is met.

## Constraints preserved

No package data, replacement-service behavior, service-29 reply, Queuez service 123, account/world state, or protocol message changed.
