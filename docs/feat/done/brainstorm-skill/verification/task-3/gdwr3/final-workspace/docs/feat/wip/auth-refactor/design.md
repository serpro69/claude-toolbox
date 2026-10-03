# Auth Refactor — Design

## Overview

Replace the legacy session-based auth middleware with JWT-based authentication. The current middleware stores session tokens in a way that does not meet compliance requirements for token storage.

## Problem Statement

The existing auth middleware persists session tokens in plaintext cookies. Legal flagged this as non-compliant with the updated data handling policy. The middleware must be replaced with a stateless JWT approach that keeps tokens out of persistent storage.

## Goals

1. Replace session-based auth with JWT tokens (access + refresh)
2. Zero-downtime migration — both auth methods work during transition
3. During the 24-hour dual-auth transition, existing protected endpoints continue to accept valid legacy sessions without client changes. New clients use JWTs in Authorization headers. Unchanged legacy clients are not supported after session authentication is retired.

## Non-Goals

1. OAuth/social login integration — separate feature
2. API rate limiting — not auth-related

## Architecture

### Token Flow

Login endpoint issues a short-lived access token (15min) and a longer-lived refresh token (7d). Access token is sent in Authorization header. Refresh token is sent as an httpOnly cookie. Middleware validates the access token on each request; on expiry, the client hits the refresh endpoint.

### Migration Strategy

Dual-middleware phase: both session and JWT authentication are accepted on protected routes. A legacy client with a valid session does not need an Authorization header; a new client with a valid JWT does not need a legacy session. Login and refresh retain the access rules needed to obtain credentials.

New endpoints issue JWTs. Existing legacy sessions remain valid until their own expiry, subject to the 24-hour transition cutoff. Supporting legacy clients unchanged means preserving their existing authenticated request format during this window; it does not promise continued legacy authentication after the cutoff.

At the end of the 24-hour transition, remove session middleware. Requests relying only on legacy sessions are then rejected; valid JWT requests continue to work. The implementation plan must identify the recorded transition start and corresponding cutoff before this change is deployed. Requests carrying both credential types need an explicit precedence/error policy before route migration is implemented.

### Compatibility Acceptance Criteria

- During transition, a valid legacy session alone grants access to an existing protected endpoint without changing the client's request.
- During transition, a valid JWT in the Authorization header alone grants access to the same endpoint.
- Missing, expired, or malformed credentials do not grant access when no other valid credential is supplied.
- After the cutoff, a legacy session alone is rejected and a valid JWT still grants access.
- No task may equate temporary legacy compatibility with a requirement that all clients add Authorization headers during the transition.

### Token Storage and Rotation: Unresolved Details

The intended requirement to keep tokens out of persistent storage and the selected 7-day refresh token carried in an httpOnly cookie need reconciliation. The supplied decisions do not define whether the cookie persists across browser restarts or which client/server storage is prohibited. The cookie attribute alone does not establish compliance with the stated policy. Preserve the chosen transport and lifetime in the plan, but confirm the permitted storage and cookie lifecycle before declaring the design compliant.

Refresh tokens rotate on use, and Task 2 requires reuse detection. The mechanism for tracking prior use is not documented. JWT request validation being stateless does not specify how refresh rotation is enforced. The implementer must inspect the existing refresh implementation and record its behavior and storage requirements before treating the reuse test as sufficient.

## Assumptions

- Legacy clients' existing session request format can be preserved throughout the transition; verify this with a representative unchanged request.
- The refresh token rotation approach (one-time use) is acceptable for the expected session concurrency.
- Existing legacy sessions have a maximum lifetime of 24 hours; verify the existing expiry and renewal behavior before scheduling retirement.

## Open Questions

- Which storage is prohibited by the token-handling policy, and what refresh-cookie persistence is permitted? Does the temporary legacy-session window have the required policy acceptance?
- How does the existing refresh endpoint enforce one-time use, including concurrent requests? Resolve any missing behavior before completing Task 2.2.
- What happens when a request supplies both credential types, especially if only one is valid? Resolve before Task 3.1.
- Where is the transition start recorded, how is the cutoff enforced, and can legacy login or renewal extend session use? Resolve before deploying Task 3; no legacy session may grant access beyond the cutoff.
- What does logout invalidate or clear for each auth method? Define the expected result before completing Task 4.1; immediate access-token revocation is not a supplied requirement.

## Not Doing

- **OAuth/social login** — a separate feature.
- **API rate limiting** — outside the authentication refactor.
- **Token revocation list** — excluded from the selected scope to limit complexity. Whether the selected lifetimes and refresh rotation satisfy policy remains subject to the storage clarification above.
- **Multi-device session management** — out of scope; each device gets independent tokens.

## Rejected Alternatives

The supplied documents record the JWT direction but do not record an alternatives evaluation. This resume preserves that decision without inventing prior trade-off analysis.
