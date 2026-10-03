# Auth Refactor — Design

## Overview

Replace the legacy session-based auth middleware with JWT-based authentication. The current middleware stores session tokens in a way that does not meet compliance requirements for token storage.

## Problem Statement

The existing auth middleware persists session tokens in plaintext cookies. Legal flagged this as non-compliant with the updated data handling policy. The middleware must be replaced with a stateless JWT approach that keeps tokens out of persistent storage.

## Goals

1. Replace session-based auth with JWT tokens (access + refresh)
2. Zero-downtime migration — both auth methods work during transition
3. Existing legacy clients continue accessing protected endpoints unchanged during the 24-hour dual-auth transition. New clients use JWT access tokens in the Authorization header. After the transition, clients must use JWT authentication; unchanged legacy clients are no longer supported.

## Non-Goals

1. OAuth/social login integration — separate feature
2. API rate limiting — not auth-related

## Architecture

### Token Flow

Login endpoint issues a short-lived access token (15min) and a longer-lived refresh token (7d). Access token is sent in Authorization header. Refresh token is sent as an httpOnly cookie. Middleware validates the access token on each request; on expiry, the client hits the refresh endpoint.

### Migration Strategy

Dual-middleware phase: both session and JWT middleware are active for the stated 24-hour transition window. New endpoints issue JWT. Existing legacy clients continue sending their existing session cookies without adding an Authorization header; valid legacy sessions continue to authenticate until expiry or the end of the transition, whichever comes first. New clients send JWT access tokens in the Authorization header and do not need a legacy session cookie.

Apply this compatibility behavior to existing protected endpoints. The two middleware paths must not require a request to satisfy both authentication methods. Preserve the login and refresh endpoints' own credential-validation behavior when wiring protected routes.

At the end of the 24-hour window, retire session middleware. JWT-authenticated requests continue working; a legacy session alone no longer grants access. Zero downtime means JWT access remains available through this cutover, not that legacy-only clients remain compatible after it. Record the transition start and cutoff before rollout so retirement and verification use the same boundary.

The behavior when a request presents both credential types is not specified by the supplied decisions. Confirm precedence and invalid-credential handling before implementing that case.

## Assumptions

- Clients that need access after the transition can adopt Authorization headers by the cutoff. Legacy clients need no changes while valid sessions are supported during the transition.
- The refresh token rotation approach (one-time use) is acceptable for the expected session concurrency.

## Open Verification Points

- The cited data-handling policy is not supplied. Confirm whether the refresh-token cookie and its persistence settings satisfy the requirement to keep tokens out of persistent storage; the JWT format and httpOnly setting alone do not establish this. The 7-day token lifetime does not specify cookie persistence settings.
- Access-token validation is stateless. The supplied docs do not describe how the completed refresh endpoint tracks one-time use or detects reuse; inspect and test its existing mechanism before claiming that requirement is verified.
- Logout behavior is not specified. Establish which credentials it clears or invalidates before writing the end-to-end assertion. With token revocation lists excluded, do not assume logout immediately invalidates an already-issued access token.

## Not Doing

- **OAuth/social login** — separate feature.
- **API rate limiting** — outside this auth refactor.
- **Token revocation list** — excluded from the agreed scope; access tokens use short lifetimes and refresh tokens rotate. Compliance remains subject to policy verification.
- **Multi-device session management** — out of scope; each device gets independent tokens.

## Rejected Alternatives

- **Require JWT headers from legacy clients during the transition** — contradicts the confirmed compatibility boundary.
- **Keep legacy-session support after the transition** — contradicts the agreed retirement window.
