# Auth Refactor — Implementation Plan

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)
> Status: planning handoff; runtime code unavailable

## Starting Point

Task 1 (login, token module, auth middleware, and login integration test) is recorded as complete. Task 2.1 (refresh endpoint with rotation) is also complete. Preserve those completion records. The next unchecked subtask is **2.2: refresh-flow integration tests**.

This plan uses the supplied design decisions and task history. It does not claim that runtime code was inspected or tests were run. Exact source paths, function names, test commands, and existing auth conventions must be resolved in the runtime repository at implementation handoff; no paths are invented here.

## Approved Contract

- Access tokens last 15 minutes and are sent in Authorization headers. Client access-token storage is memory only.
- Refresh tokens retain the existing 7-day lifetime and one-time rotation behavior.
- Refresh cookies are HttpOnly, Secure session cookies. Both initial issuance and rotation omit `Expires` and `Max-Age`; neither token may be stored in localStorage or a persistent cookie.
- Token validity and cookie lifetime are independent. A live cookie must not make an expired token acceptable. Cookie session semantics do not guarantee invalidation on every browser-process exit or session restoration.
- Existing sessions and JWT authentication coexist for the 24-hour migration window. Existing endpoint contracts remain available. JWT clients need the header/refresh update before session support ends.
- OAuth/social login, API rate limiting, a token revocation list, and multi-device session management remain out of scope.

## Runtime Mapping

At the beginning of implementation, locate the existing token module, login and refresh handlers, cookie configuration, JWT and session middleware, route registration, client token handling, logout handler, and auth integration-test suite → verify: record their actual paths and the focused test command in the relevant task notes.

Inspect the recorded completed work without resetting its checkboxes → verify: identify which existing tests establish login, access-token validation, refresh issuance, and rotation. Record any discovered discrepancy as follow-up work rather than silently declaring completed tasks unfinished.

Resolve the implementation questions in [design.md](./design.md#implementation-questions) only as needed by the current task → verify: record observed behavior or an explicit unresolved decision, without inventing a storage backend or migration policy.

## Token Refresh

**Task 2; next subtask 2.2.** Touch the existing auth integration tests, refresh handler, cookie configuration, and rotation component only where the tests expose a contract mismatch. The intended slice is one complete refresh request through token validation, rotation, cookie replacement, and subsequent protected access.

1. Add a valid-refresh integration case using the existing login/refresh fixtures → verify: refresh returns a usable access token with the 15-minute lifetime and replaces the refresh token according to the established 7-day expiry policy.
2. Assert cookie attributes on login and successful refresh → verify: each refresh-token cookie has HttpOnly and Secure, and neither `Expires` nor `Max-Age`. Use a secure test transport where the browser client requires one.
3. Add expired-refresh and consumed-token reuse cases → verify: both are rejected with the existing authentication-error contract and neither produces usable replacement credentials. Test token expiry independently of browser cookie presence.
4. Check the existing one-time-use mechanism and exercise competing uses of the same token → verify: no more than one refresh succeeds. Preserve the supplied rotation policy; resolve any unsupported concurrency requirement before changing its mechanism.
5. Verify client token handling against the storage contract → verify: access tokens remain in memory, refresh tokens use the approved cookie, and neither token is written to localStorage or persistent cookies. Inspect browser-session behavior without treating cookie attributes as proof of browser-exit invalidation.
6. Run the focused auth integration suite → verify: refresh cases pass and the existing login integration coverage remains green. Record the actual command and result under Task 2.

Do not choose a new token library, persistence backend, or refresh lifetime in this task. The implementation already recorded as complete supplies the starting point.

## Protected Routes Migration

**Task 3; depends on Task 1.** Touch route registration and the existing JWT/session middleware composition, plus auth integration tests.

1. Identify the protected `/api/v1/*` routes and authentication entry points → verify: login and refresh remain reachable without a valid access token; protected routes still require authentication.
2. Apply JWT authentication alongside legacy-session authentication for the migration window → verify: the same protected endpoint accepts a valid JWT and a valid existing session in separate tests, with the expected identity available downstream.
3. Test missing, expired, and malformed credentials → verify: protected requests with no valid authentication are rejected using the established endpoint contract. Read and resolve existing mixed-credential precedence before asserting behavior for requests carrying both methods.
4. Establish the window start, legacy-session issuance cutoff, and client readiness from runtime configuration and release ownership → verify: no accepted legacy session can outlive the intended removal point, and clients have the required header/refresh support.
5. Remove session middleware when the approved 24-hour window has elapsed → verify: JWT access still succeeds, legacy-session-only requests no longer authenticate, and existing protected-endpoint tests pass.

Keep tests or a reproducible configuration for the coexistence phase so final verification can assess both transition and post-migration behavior.

## Final Verification

**Task 4; depends on Tasks 1, 2, and 3.** Run this after the implementation tasks are complete in the runtime repository.

1. Exercise login → protected access → refresh → protected access → logout → verify: each transition matches the approved token/cookie contract and the existing logout semantics. Do not assert immediate access-token revocation, which is outside scope.
2. Verify coexistence and retirement using the migration coverage → verify: both auth methods work during the window, while JWT access continues after session middleware removal.
3. Invoke `$kk:test` for the relevant full suite and auth edge cases → verify: record commands, results, and any remaining failures in tasks.md.
4. Invoke `$kk:document` for affected endpoint, client, and migration documentation → verify: published guidance distinguishes 7-day refresh validity from session-cookie lifetime and describes client migration requirements.
5. Invoke `$kk:review-code` with the actual runtime language → verify: address actionable findings or record unresolved blockers.
6. Invoke `$kk:review-spec` against these design and implementation documents → verify: reconcile implementation deviations, task completion, cookie behavior, and migration behavior before marking the feature complete.

## Handoff

Planning stops here. Resume with `$kk:implement` on **Task 2, subtask 2.2**, using [tasks.md](./tasks.md) as the progress record. Begin with runtime mapping because source code was unavailable during this continuation.
