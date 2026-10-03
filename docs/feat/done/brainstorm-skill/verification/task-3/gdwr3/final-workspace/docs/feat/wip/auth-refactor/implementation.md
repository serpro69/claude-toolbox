# Auth Refactor — Implementation Plan

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)
> Status: ready for implementation handoff with explicit open decisions

## Scope and Current State

Replace legacy session authentication with JWT access and refresh tokens. Keep unchanged legacy clients working with valid sessions during the 24-hour dual-auth transition. New clients send access tokens in Authorization headers. Retire legacy authentication at the cutoff; compatibility after that point requires the JWT flow.

The task log reports Task 1 complete and the refresh endpoint in Task 2.1 complete. Preserve those states. Task 2.2 is the next unfinished subtask. This plan is based on the supplied documents; no runtime source or tests were available to verify the recorded implementation.

Access tokens last 15 minutes. Refresh tokens last 7 days, travel in an httpOnly cookie, and rotate on use. These are existing design decisions, not newly verified implementation behavior.

## Implementation Entry and Component Mapping

When runtime source becomes available, identify the existing login endpoint, token generation/validation module, auth middleware, refresh endpoint and rotation mechanism, protected-route registration, legacy session configuration, logout handler, and auth test suites. Record the actual file paths alongside the affected task before editing. No filenames, endpoint paths for login/refresh, test commands, or dependencies can be inferred reliably from the supplied documents.

Map each component to its existing tests → verify: the implementer can identify where each task's behavior is exercised and how to run those specific tests. Preserve the completed work rather than recreating it.

## Decisions Required Before Affected Work

| Decision | Why it matters | Resolve before |
| --- | --- | --- |
| Permitted client/server token storage, refresh-cookie persistence, and temporary legacy-policy acceptance | The current storage requirement and refresh-cookie design are not reconciled | Finalizing storage behavior or claiming policy compliance |
| Existing one-time refresh mechanism and concurrent refresh behavior | The reuse test needs a defined acceptance rule and observable outcome | Completing Task 2.2 |
| Precedence and errors when both credential types are supplied | Dual-auth composition must not accidentally require both credentials or choose an undocumented fallback | Task 3.1 |
| Recorded transition start/cutoff and legacy login/renewal behavior | Session authentication must end after 24 hours even if renewal is possible | Deploying Task 3 |
| Logout's credential clearing/invalidation contract | The end-to-end test needs a specified terminal state | Task 4.1 |

Inspect existing behavior and use the supplied decisions to resolve implementation details. Escalate a requirement choice if inspection cannot settle it; do not silently introduce a token revocation list or a new storage architecture.

## Task 1: Completed Login Path

The task log records token generation/validation, login credential validation and issuance, access-token middleware, and a login integration test as complete. Keep these checkboxes complete. Locate their implementations and reuse their established contracts → verify: the existing login integration test remains passing when subsequent auth changes are introduced.

## Task 2: Refresh Integration Tests

The refresh endpoint with rotation is recorded as implemented. Extend its integration tests rather than adding a replacement endpoint.

1. Identify how the endpoint validates expiry, consumes a refresh token, and issues replacement credentials → verify: the implementation exposes enough behavior to assert one-time use. If it does not, document the gap before claiming completion.
2. Exercise a valid refresh and use the resulting access token against a protected endpoint → verify: replacement credentials are usable and the consumed refresh token is no longer accepted.
3. Exercise an expired refresh token and reuse a previously consumed token → verify: neither attempt yields usable replacement credentials; expected error responses follow the existing endpoint contract.
4. Resolve how simultaneous use of the same refresh token is handled → verify: coverage reflects the agreed one-time-use behavior, using the project's existing concurrency/test facilities if relevant.

Do not claim that stateless access-token validation itself provides refresh reuse detection. Document the existing mechanism and reconcile any storage requirements with the open policy question.

## Task 3: Protected-Route Migration

### Dual-Auth Phase

1. Locate registration of protected `/api/v1/*` routes and the existing session/JWT middleware. Identify the login and refresh routes that must remain reachable under their own credential rules → verify: obtaining or refreshing credentials does not require an already-valid access token.
2. Compose authentication so either a valid legacy session alone or a valid JWT alone can authenticate a protected request during transition → verify: representative unchanged legacy requests and JWT requests independently reach the same protected endpoint and retain its existing authorization behavior.
3. Implement the agreed mixed-credential policy and cover missing, expired, and malformed credentials → verify: requests with no valid credentials are rejected; mixed requests follow the documented precedence/error rules.

### Retirement After 24 Hours

1. Record the transition start and cutoff using the actual deployment/configuration mechanism. Check legacy session expiry, login, and renewal behavior → verify: the retirement procedure cannot extend acceptance beyond the cutoff.
2. Verify dual-auth behavior before retiring sessions → verify: legacy clients require no request changes during the transition and JWT clients remain operational.
3. Remove legacy-session authentication at the cutoff → verify: legacy-session-only requests fail, valid JWT requests still pass, and login/refresh remain usable.

The supplied design does not select an automatic timer, feature flag, or deployment system for retirement. Choose the concrete mechanism after examining the project. Keep tests for both phases; retirement must not erase the evidence for transition compatibility.

## Task 4: Final Verification

1. Resolve logout semantics and exercise login → protected access → refresh → protected access → logout → verify: each stage matches its documented credential contract. Do not assume immediate access-token revocation, which is not an approved requirement.
2. Run the compatibility acceptance criteria in [design.md](./design.md#compatibility-acceptance-criteria) against both migration phases → verify: unchanged legacy requests work within the window and fail after retirement while JWT requests continue working.
3. Run `$kk:test` with the real repository's test tooling → verify: the full available suite passes, including expiry, reuse, rejection, and transition coverage. Record any checks requiring a deployed environment separately from automated results.
4. Run `$kk:document` → verify: authentication usage, migration timing, and the resolved storage/logout rules match the implementation.
5. Run `$kk:review-code` with the detected project language and `$kk:review-spec` against design, implementation, and tasks → verify: findings are resolved or explicitly tracked and task completion is supported by evidence.

## Assumptions and Scope Boundaries

The documented 24-hour maximum legacy-session lifetime and suitability of one-time refresh rotation remain assumptions to check against the implementation. An unchanged legacy request is the compatibility reference during transition; updating every legacy client during that window is not a prerequisite.

OAuth/social login, API rate limiting, a token revocation list, and multi-device session management remain excluded. Token-storage compliance is unresolved; neither the chosen JWT format nor the completed task log establishes it.

## Handoff

Next pending work: **Task 2.2, refresh integration tests**. Invoke `$kk:implement` to continue auth-refactor from Task 2.2 when runtime source and test tooling are available. Map the actual components first and resolve the refresh behavior needed by those tests. This document does not mark implementation or independent review as performed.
