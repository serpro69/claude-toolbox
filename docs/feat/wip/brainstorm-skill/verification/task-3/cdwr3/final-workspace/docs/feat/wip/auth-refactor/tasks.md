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
- **Docs:** [implementation.md#existing-state-and-target-mapping](./implementation.md#existing-state-and-target-mapping)

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
- **Docs:** [implementation.md#token-refresh](./implementation.md#token-refresh)

### Subtasks
- [x] 2.1 Create refresh endpoint with token rotation
- [ ] 2.2 Map the existing refresh handler and integration suite to actual source paths, then add and run refresh-flow tests — verify: valid refresh produces usable replacement credentials, expired refresh is rejected, and reuse of the rotated token is rejected while its replacement works

## Task 3: Protected routes migration
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#protected-routes-migration](./implementation.md#protected-routes-migration)

### Subtasks
- [ ] 3.1 Map existing protected `/api/v1/*` routes and wire the dual-auth path; establish handling when both credential types are supplied — verify: valid legacy sessions work without Authorization headers and valid JWTs work without session cookies during the transition
- [ ] 3.2 Add protected-route rejection and compatibility tests — verify: requests with no usable credential, expired credentials, or malformed credentials are rejected, and both supported client paths preserve protected-endpoint behavior
- [ ] 3.3 Remove session middleware at the recorded 24-hour cutoff — verify: legacy-only requests are rejected after retirement and valid JWT requests continue succeeding

## Task 4: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#final-verification](./implementation.md#final-verification)

### Subtasks
- [ ] 4.1 Establish the documented logout expectations and run login → access → refresh → access → logout — verify: each step matches its contract without assuming immediate revocation of issued access tokens
- [ ] 4.2 Verify zero downtime across the compatibility boundary — verify: both auth methods work during the transition; JWT access continues after session support is retired
- [ ] 4.3 Verify refresh-cookie storage against the applicable policy and record the evidence — verify: cookie persistence and token handling satisfy the actual policy, or document the remaining blocker
- [ ] 4.4 Run `/kk:test` for the full relevant suite — verify: record passing results and resolve failures
- [ ] 4.5 Run `/kk:document` — verify: affected docs describe the shipped behavior and transition boundary
- [ ] 4.6 Run `/kk:review-code` with the actual project language — verify: resolve review findings
- [ ] 4.7 Run `/kk:review-spec` — verify: implementation matches design and implementation docs

## Dependency Graph

```
Task 1 ──→ Task 3 ──→ Task 4
Task 2 ─────────────→ Task 4
```
