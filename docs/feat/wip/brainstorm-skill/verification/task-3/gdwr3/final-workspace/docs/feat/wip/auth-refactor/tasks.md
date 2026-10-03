# Tasks: Auth Refactor

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: in-progress
> Created: 2026-05-15
> Not Doing: OAuth/social login, API rate limiting, token revocation list, multi-device session management

## Task 1: User login end-to-end
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2
- **Docs:** [implementation.md#task-1-completed-login-path](./implementation.md#task-1-completed-login-path)

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
- **Docs:** [implementation.md#task-2-refresh-integration-tests](./implementation.md#task-2-refresh-integration-tests)

### Subtasks
- [x] 2.1 Create refresh endpoint with token rotation
- [ ] 2.2 In the existing refresh endpoint's integration tests, cover successful rotation, expired refresh tokens, and reuse of a consumed token → verify: a successful refresh provides usable replacement credentials, while expiry and reuse cannot issue new credentials. Identify the existing rotation mechanism and resolve any missing reuse/concurrency contract before marking this complete.

## Task 3: Protected routes migration
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#task-3-protected-route-migration](./implementation.md#task-3-protected-route-migration)

### Subtasks
- [ ] 3.1 In the protected-route registration and auth middleware composition, accept legacy sessions and JWTs during transition, preserving login/refresh access → verify: an unchanged legacy request with a valid session and a new-client request with a valid Authorization header each reach the same protected endpoint independently. Resolve mixed-credential precedence before implementation.
- [ ] 3.2 Extend protected-route integration tests for missing, expired, and malformed credentials → verify: each is rejected without another valid credential; requests carrying both credential types follow the documented policy.
- [ ] 3.3 Remove session middleware after the recorded 24-hour transition window → verify before deployment: transition start/cutoff and renewal behavior are known, and dual-auth checks pass; verify after retirement: legacy-session-only requests are rejected and valid JWT requests still succeed.

## Task 4: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#task-4-final-verification](./implementation.md#task-4-final-verification)

### Subtasks
- [ ] 4.1 In the auth end-to-end suite, exercise login → access → refresh → access → logout → verify: access succeeds at each valid stage and logout has the agreed credential-clearing/invalidation behavior. Resolve the logout contract first.
- [ ] 4.2 Verify zero-downtime migration in both phases → verify: unchanged legacy-session requests and JWT requests work during transition; after cutoff, only the JWT path continues. Retain both phase configurations in the test coverage.
- [ ] 4.3 Run `$kk:test` over the full available suite, including refresh edge cases and both migration phases → verify: relevant tests pass and any untestable deployment assumptions are recorded.
- [ ] 4.4 Run `$kk:document` to update authentication and migration documentation → verify: client guidance states the compatibility cutoff and the resolved storage/logout contracts.
- [ ] 4.5 Run `$kk:review-code` with the actual project language → verify: implementation findings are resolved or explicitly tracked.
- [ ] 4.6 Run `$kk:review-spec` against all three feature documents → verify: implementation matches the documented decisions and completed task states have evidence.

## Dependency Graph

```
Task 1 ──→ Task 3 ──→ Task 4
Task 2 ─────────────→ Task 4
```
