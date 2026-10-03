# Auth Refactor — Implementation Plan

> Design: [design.md](./design.md)
> Progress: [tasks.md](./tasks.md)
> Status: in-progress

## Starting Point and Scope

Task 1 (login, token module, access-token middleware, and login integration test) is recorded as done. Task 2.1 (refresh endpoint with rotation) is also recorded as done. Preserve that work. The next unchecked item is Task 2.2, refresh integration tests; route migration and final verification follow.

Runtime code is unavailable in this workspace. Component names below identify implementation targets, not verified filenames or function names. At implementation handoff, locate the existing token module, login/refresh handlers, legacy-session middleware, JWT middleware, route registration, client logout flow, and integration-test fixtures. Record their actual locations before editing them. Use existing libraries and test conventions; this plan introduces no dependency.

The migration guarantees unchanged legacy-client access only during the dual-auth window and only while the client's session remains valid. JWT clients use Authorization headers. After the 24-hour transition, legacy authentication is retired.

## Assumptions and Open Decisions

Carry forward the [design assumptions](./design.md#assumptions). Before release, resolve the [verification gates](./design.md#open-decisions-and-verification-gates): storage-policy interpretation, mixed-credential behavior, session issuance/renewal and cutoff timing, and logout semantics. Do not infer these contracts from the word “stateless” or from cookie flags.

## Not Doing

OAuth/social login, API rate limiting, token revocation lists, and multi-device session management remain excluded, for the reasons in the [design](./design.md#not-doing).

## User Login

Task 1 remains complete in the progress record; this planning pass does not reopen its checked subtasks.

- Locate the existing token module, login endpoint, JWT middleware, and login integration test → verify: confirm the recorded implementation and identify the existing test command and fixtures before extending refresh coverage.
- Establish a baseline using the existing login integration test → verify: valid credentials still issue tokens and the existing failure cases retain their recorded behavior. Report discrepancies instead of silently treating recorded completion as new verification.

## Token Refresh

Task 2 completes the existing refresh path without rebuilding Task 2.1.

- Inspect the refresh handler, rotation state, and integration fixtures; locate the expiry control or test clock → verify: identify how the implementation distinguishes a usable, expired, and previously consumed refresh token. Record the exact targeted test command from the repository's test setup.
- Add a login → refresh → protected-access integration case → verify: refresh returns a usable access token and a replacement refresh cookie; the replacement refresh token can be used for the next refresh. The access and refresh lifetimes remain 15 minutes and 7 days respectively.
- Add an expired-refresh case using the existing clock/fixture mechanism → verify: the expired credential is rejected and no replacement access or refresh credential is issued.
- Add a reuse case by submitting the original refresh token after a successful rotation → verify: the original token is rejected and no replacement credentials are issued. Include simultaneous use if the existing harness can deterministically exercise it; at most one refresh may succeed for the same token.
- Run the targeted refresh cases and existing login tests → verify: happy-path rotation, expiry rejection, and reuse rejection pass together without regressing login. Mark Task 2.2 done only with actual execution evidence.

## Protected Routes Migration

Task 3 depends on Task 1. Resolve mixed-credential behavior and transition timing before considering this task complete.

- Inventory the existing protected routes and public authentication entry points in route registration → verify: record which routes require authentication and preserve access to login and refresh under their existing contracts. The `/api/v1/*` shorthand must not accidentally require an access token to log in or refresh.
- Integrate the existing legacy and JWT authenticators at the protected-route boundary → verify: a valid legacy session without an Authorization header reaches each protected route; a valid JWT without a legacy session also reaches it. Both paths preserve the authenticated identity and existing authorization checks.
- Add rejection and compatibility cases → verify: missing credentials, expired JWTs, malformed JWTs, and expired legacy sessions fail before the protected handler when no other accepted credential is present. Add separate mixed-credential cases once that contract is agreed.
- Establish the transition start and retirement control using the existing issuance/renewal and middleware configuration components → verify: no legacy session is promised validity beyond the retirement deadline, and the agreed maximum session lifetime is 24 hours. Record the actual control and start time before scheduling removal.
- Retire legacy middleware after the transition window → verify: JWT-authenticated requests still succeed, legacy-only requests are rejected, and public authentication entry points remain usable. Exercise before/after behavior with the existing time/configuration test mechanism instead of waiting 24 hours in tests.

Session support is removed only after the agreed transition condition is met. “Zero downtime” here means protected access remains available through the accepted authentication path in each phase; it does not promise indefinite access to unchanged legacy clients after retirement.

## Final Verification

Task 4 depends on Tasks 1, 2, and 3.

- Resolve and document the logout contract in the existing logout component and its tests → verify: the contract specifies client credential removal and whether the refresh token remains usable. Do not claim previously issued access tokens are immediately invalidated without a supporting mechanism; their stated lifetime is 15 minutes.
- Run login → protected access → refresh → protected access → logout → verify: each step matches the agreed contract, including post-logout client behavior and refresh behavior.
- Exercise representative existing protected endpoints through the transition → verify: unchanged legacy clients work with valid sessions during dual auth, JWT clients work during and after it, and legacy-only access ends at retirement. Check identity/authorization behavior as well as successful response status.
- Invoke `/kk:test` in the runtime repository → verify: the full relevant suite passes, including refresh rejection and migration boundary cases; record commands and outcomes.
- Invoke `/kk:document` → verify: relevant client and operational documentation explains the compatibility window, Authorization-header requirement after retirement, cutoff control, and confirmed storage/logout decisions.
- Invoke `/kk:review-code` with the actual project language → verify: findings are addressed or explicitly dispositioned.
- Invoke `/kk:review-spec` → verify: runtime behavior matches this plan and the design, including resolved open decisions. Update task status only after the associated checks complete.

## Handoff

Start with **Task 2.2: refresh-flow integration tests** using `/kk:implement` in the runtime repository. Source discovery and baseline checks precede edits. This planning pass ran no runtime tests, changed no runtime code, and performed no independent review.
