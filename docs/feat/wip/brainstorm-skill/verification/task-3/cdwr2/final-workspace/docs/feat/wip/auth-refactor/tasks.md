# Tasks: Auth Refactor

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: in-progress
> Created: 2026-05-15
> Not Doing: OAuth/social login, API rate limiting, token revocation list, multi-device session management

Recorded completion is preserved from the existing task list; no runtime code or test results were available during this refinement. Next unchecked item: **2.2**. Runtime file locations must be identified as described in [the implementation starting point](./implementation.md#starting-point-and-scope).

## Task 1: User login end-to-end
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2
- **Docs:** [User login](./implementation.md#user-login)

### Subtasks
- [x] 1.1 Create JWT token generation and validation module
- [x] 1.2 Create login endpoint with credential validation and token issuance
- [x] 1.3 Create auth middleware that validates access tokens
- [x] 1.4 Integration test for the login flow

## Task 2: Token refresh end-to-end
- **Status:** in-progress
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1
- **Docs:** [Token refresh](./implementation.md#token-refresh)

### Subtasks
- [x] 2.1 Create refresh endpoint with token rotation
- [ ] 2.2 Extend the existing refresh integration test suite using the current handler, rotation state, and expiry fixtures → verify: successful refresh returns usable replacement credentials; expired tokens and already-consumed tokens produce no replacement credentials; the replacement token supports a subsequent refresh. Run these cases with the existing login tests and record the actual command and results.

## Task 3: Protected routes migration
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Protected routes migration](./implementation.md#protected-routes-migration)

### Subtasks
- [ ] 3.1 Integrate JWT and existing session authentication in protected `/api/v1/*` route registration, preserving public authentication entry points → verify: a valid legacy session alone and a valid JWT alone each grant appropriate access during the transition; neither path requires both credentials.
- [ ] 3.2 Extend protected-route integration tests → verify: absent credentials, expired/malformed JWTs, and expired legacy sessions are rejected when no other accepted credential is present; valid credentials preserve identity and authorization behavior. Resolve and test the mixed-credential contract before completing this subtask.
- [ ] 3.3 Identify the legacy issuance/renewal control, establish the 24-hour transition start and retirement condition, and remove session middleware only after that condition is met → verify: unchanged legacy clients retain access with valid sessions during the window, no session is promised validity beyond the cutoff, legacy-only access is rejected afterward, and JWT access continues.

## Task 4: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](./implementation.md#final-verification)

### Subtasks
- [ ] 4.1 Resolve the logout contract and run the end-to-end flow: login → access → refresh → access → logout → verify: credential removal and post-logout refresh behavior match the agreed contract, without assuming an access-token revocation list.
- [ ] 4.2 Verify zero-downtime migration → verify: both auth methods work independently during transition, JWT access works after retirement, and legacy-only access ends at the cutoff. Confirm the storage-policy, mixed-credential, transition-timing, and logout gates in [the design](./design.md#open-decisions-and-verification-gates) are resolved before release.
- [ ] 4.3 Run `/kk:test` in the runtime repository → verify: the full relevant suite passes, including refresh rejection and migration boundary cases; record commands and results.
- [ ] 4.4 Run `/kk:document` → verify: client and operational documentation describes the compatibility boundary, cutoff controls, and confirmed storage/logout behavior.
- [ ] 4.5 Run `/kk:review-code` with the actual project language → verify: findings are addressed or explicitly dispositioned.
- [ ] 4.6 Run `/kk:review-spec` → verify: implementation matches the design and implementation plan, including resolved open decisions.

## Dependency Graph

```
Task 1 ──→ Task 3 ──→ Task 4
Task 2 ─────────────→ Task 4
```
