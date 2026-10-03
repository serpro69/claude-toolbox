# Auth Refactor — Design

## Overview

Replace the legacy session-based auth middleware with JWT-based authentication. Preserve existing protected endpoints through a dual-authentication migration window.

## Problem Statement

The existing auth middleware persists session tokens in plaintext cookies. The approved storage constraint prohibits persistent cookies and localStorage. It permits an HttpOnly, Secure **session cookie** for the refresh token. Browser-session storage and token validity are separate constraints: a refresh token remains valid for at most 7 days, but its cookie ends with the browser session and must not set `Expires` or `Max-Age`.

## Goals

1. Replace session-based auth with JWT tokens (access + refresh).
2. Zero-downtime migration — both auth methods work during transition.
3. Preserve existing protected endpoints and legacy-session access during the migration window. JWT clients must send Authorization headers and handle refresh; the refactor does require that client update before legacy-session support ends.
4. Keep tokens out of persistent cookies and localStorage while permitting the approved refresh session cookie.

## Non-Goals

1. OAuth/social login integration — separate feature.
2. API rate limiting — not part of this auth refactor.

## Architecture

### Token Flow

Login issues a short-lived access token (15 minutes) and a longer-lived refresh token (7 days). The client keeps the access token in memory and sends it in the Authorization header. The refresh token is sent as an HttpOnly, Secure session cookie with neither `Expires` nor `Max-Age`. Apply the same cookie attributes when refresh rotation replaces the cookie.

Middleware validates the access token on each request. On access-token expiry, the client calls the refresh endpoint. Each successful refresh rotates the refresh token and consumes the previous token; expired or reused refresh tokens must be rejected.

The refresh token's 7-day validity does not authorize a persistent cookie. The browser-session cookie may end before the token expires, and a still-present session cookie does not extend an expired token's validity. HttpOnly restricts script access; it does not itself make a cookie non-persistent. Browser session restoration can retain session cookies, so this design does not promise token invalidation on every browser-process exit.

Access-token validation is stateless. One-time refresh use and reuse detection require a way to recognize consumed tokens; the existing rotation implementation must be inspected before choosing or documenting its backing mechanism. The browser-storage restriction does not establish an additional server-side storage policy.

### Migration Strategy

During the dual-middleware phase, protected endpoints accept both existing sessions and JWT authentication. Login and refresh remain reachable without a valid access token. Existing sessions remain valid until they expire, for a maximum of 24 hours. JWT clients use the Authorization header and refresh flow during this same window.

Retire legacy-session middleware after the 24-hour migration window. Confirm when that window starts and when legacy-session issuance stops before scheduling removal; otherwise, newly issued sessions could outlive the intended cutoff. Validate both auth methods during coexistence and JWT access after retirement.

The compatibility promise covers existing endpoints and legacy-session clients during the window. It does not imply that unchanged legacy clients can authenticate after session support is removed.

## Assumptions

- All clients can be updated to send Authorization headers and use refresh within the migration window. Confirm client readiness before removing session support.
- Refresh token rotation uses one-time tokens and is acceptable for expected session concurrency.
- The completed login work and refresh endpoint recorded in tasks.md exist in the runtime repository. No runtime code was available for this planning pass, so their implementation has not been verified.
- Existing sessions have a maximum lifetime of 24 hours; verify this and the issuance cutoff before migration.

## Not Doing

- **OAuth/social login** — separate feature.
- **API rate limiting** — outside this auth refactor.
- **Token revocation list** — excluded by the existing scope decision. This does not remove the need to enforce one-time refresh rotation. Immediate invalidation of issued access tokens is not promised; they retain the 15-minute expiry limit.
- **Multi-device session management** — out of scope; each device gets independent tokens.

## Rejected Alternatives

- **Persistent refresh cookies or localStorage** — rejected by the approved storage constraint. The 7-day token lifetime must not become a cookie persistence setting.
- No additional architecture alternatives were supplied for this continuation; the existing JWT and rotation decisions are retained.

## Implementation Questions

Resolve these against the runtime implementation when it becomes available; they are not new approved design decisions:

- Which components and tests own login, refresh, cookie configuration, JWT validation, session validation, route registration, and logout?
- How does the existing refresh endpoint enforce one-time use, including concurrent attempts, and does rotation preserve the current 7-day expiry policy?
- What is the established behavior when a request supplies both a JWT and a legacy session, especially when one credential is invalid?
- What event starts the 24-hour window, and when does legacy-session issuance stop?
- What does the existing logout flow clear or invalidate? Preserve its documented scope without implying immediate access-token revocation.

## Related Documents

- [Implementation plan](./implementation.md)
- [Task progress](./tasks.md)
