# Account and session design

## Current status

The laboratory SignOn response is intentionally a single-user, clean-room transport fixture. It creates fresh in-memory BAP session material for each run and does **not** inspect a username or password. The current PostgreSQL schema contains experiment and event metadata only; it does not contain account, credential, entitlement, or character records.

This is appropriate for protocol research, but it is not a multi-user sign-in system.

## Decision: do not place user passwords in configuration

A server configuration file must never contain player usernames or passwords. Configuration may identify the database through a deployment-secret reference or environment variable, but it must not act as an account store. Passwords must never be logged, included in packet captures, copied to experiment events, or committed to the repository.

The currently observed game SignOn flow has not supplied an application username/password field. Consequently, a future account-login experience must use a separate trusted enrolment/authentication boundary rather than inventing credentials inside the game protocol.

## Target separation

1. **Operator configuration**
   - Database connection settings and service-wide signing/encryption secrets are deployment secrets, supplied outside Git.
   - The database role has only the permissions required by the service.

2. **Account service**
   - Owns account creation, password verification, reset/revocation, and rate limiting.
   - Stores only a modern password verifier (Argon2id), a per-password random salt, and optional verifier metadata—never plaintext or reversible passwords.
   - Exposes a local administrative CLI first; a public registration UI comes later with email verification, abuse controls, and recovery design.

3. **Game-session bridge**
   - Accepts only an already-authenticated account identity from the trusted account boundary.
   - Creates short-lived SignOn/BAP session material in memory.
   - Resolves account, character, entitlement, and Queuez snapshot state from PostgreSQL.
   - Never persists BAP nonces, AES keys, HMAC keys, or session tokens.

4. **Protocol runtime**
   - Uses account/character state to construct documented server-initiated Queuez snapshots and later activity state.
   - Keeps decrypted request bodies in memory only for documented codecs and logs metadata only.

## Planned PostgreSQL model

The model should be introduced through additive migrations once the Queuez bootstrap contract is understood:

- `accounts`: internal UUID, normalized display name, account status, created/disabled timestamps.
- `account_password_credentials`: account UUID, Argon2id encoded verifier, verifier version, changed timestamp. Keep credentials separate from profile data.
- `characters`: internal UUID/SOID mapping, owning account, name, selection state, lifecycle timestamps.
- `account_entitlements`: account-to-entitlement records required by documented response/snapshot builders.
- `auth_sessions` (optional): opaque, revocable, short-lived account-bound session references. No BAP cryptographic material.
- Existing `experiments` and `events`: remain protocol-observation records and must not gain credential or plaintext-payload columns.

Use UUID primary keys for account/character identities and store any protocol-specific numeric SOID separately with uniqueness constraints.

## Sequencing

1. Finish evidence-backed Queuez/bootstrap research using a deterministic local fixture account.
2. Define the minimal account/character state required to produce a Sunrise-compatible initial snapshot.
3. Add migrations plus fixture-only account/character records.
4. Add local operator account creation with Argon2id verification and tests.
5. Bind authenticated account identity to SignOn/BAP sessions.
6. Only then design external user registration and login UX.

No user-password configuration file is needed—or safe—at the current stage.
