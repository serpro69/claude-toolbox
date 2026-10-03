# Tasks: Auth Refactor

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: in-progress
> Created: 2026-05-15
> Not Doing: OAuth/social login, API rate limiting, token revocation list, multi-device session management

## Task 1: User login end-to-end
- **Docs:** [Design token flow](./design.md#token-flow), [Implementation starting point](./implementation.md#starting-point)
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2

### Subtasks
- [x] 1.1 Create JWT token generation and validation module
- [x] 1.2 Create login endpoint with credential validation and token issuance
- [x] 1.3 Create auth middleware that validates access tokens
- [x] 1.4 Integration test for the login flow

## Task 2: Token refresh end-to-end
- **Docs:** [Implementation: token refresh](./implementation.md#token-refresh)
- **Status:** in-progress
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1

### Subtasks
- [x] 2.1 Create refresh endpoint with token rotation
- [ ] 2.2 Extend the existing auth integration tests for valid refresh, expired refresh, and consumed-token reuse; verify 15-minute access validity and the existing 7-day refresh expiry policy. Assert HttpOnly + Secure session cookies with no Expires/Max-Age on login and rotation; verify one-time refresh under competing requests and the client storage contract. Run the focused auth integration suite and record its command/result.

### Notes
- Next pending subtask: **2.2**. Locate the runtime components and test command first; no runtime code was supplied for this planning pass.
- Subtask 2.1 remains complete. Preserve existing rotation behavior; resolve its implementation questions using the runtime code before changing it.

## Task 3: Protected routes migration
- **Docs:** [Implementation: protected routes migration](./implementation.md#protected-routes-migration)
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —

### Subtasks
- [ ] 3.1 Apply JWT middleware to protected `/api/v1/*` routes alongside existing session middleware, keeping login and refresh reachable; verify the same endpoint accepts a valid JWT or existing session during coexistence.
- [ ] 3.2 Add missing, expired, and malformed credential rejection tests; verify unauthenticated requests are rejected and resolve mixed-credential precedence from the existing implementation before asserting it.
- [ ] 3.3 Confirm the migration start, legacy-session issuance cutoff, and client readiness, then remove session middleware after the 24-hour window; verify JWT access succeeds, legacy-session-only access fails, and protected-endpoint tests pass.

## Task 4: Final verification
- **Docs:** [Implementation: final verification](./implementation.md#final-verification)
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 4.1 Run login → access → refresh → access → logout end-to-end; verify the approved token/cookie contract and existing logout semantics without assuming immediate access-token revocation.
- [ ] 4.2 Verify zero-downtime migration using coexistence coverage: both auth methods work during the window, and JWT access continues after retirement.
- [ ] 4.3 Invoke `$kk:test` for the full relevant suite and auth edge cases; record actual commands and results.
- [ ] 4.4 Invoke `$kk:document` to update endpoint, client, and migration guidance; verify session-cookie lifetime and client changes are explicit.
- [ ] 4.5 Invoke `$kk:review-code` with the actual runtime language; address findings or record remaining blockers.
- [ ] 4.6 Invoke `$kk:review-spec`; reconcile implementation against design and implementation docs before marking the feature complete.

## Dependency Graph

```
Task 1 ──→ Task 3 ──→ Task 4
Task 2 ─────────────→ Task 4
```
