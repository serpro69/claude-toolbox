# Auth Refactor — Design

## Overview

Replace the legacy session-based auth middleware with JWT-based authentication. The current middleware stores session tokens in a way that does not meet the stated token-storage policy.

## Problem Statement

The existing auth middleware persists session tokens in plaintext cookies. Legal flagged this as non-compliant with the updated data handling policy. The intended replacement uses JWT access and refresh tokens. The exact storage-policy interpretation still needs validation: using JWTs and an httpOnly refresh cookie does not itself establish that tokens are kept out of persistent storage.

## Goals

1. Replace session-based auth with JWT tokens (access + refresh).
2. Preserve access throughout the dual-auth transition: existing legacy clients use their current sessions unchanged, and new clients use JWT Authorization headers.
3. Retire legacy-session support after the transition window. Compatibility with unchanged legacy clients is guaranteed only during that window; clients must adopt JWT authentication to retain protected access afterward.

## Non-Goals

1. OAuth/social login integration — separate feature.
2. API rate limiting — outside this auth migration.

## Architecture

### Token Flow

Login issues a short-lived access token (15 minutes) and a longer-lived refresh token (7 days). New clients send the access token in the Authorization header. The refresh token is sent as an httpOnly cookie. On access-token expiry, the client calls the refresh endpoint. Refresh tokens rotate on use; expired or reused refresh tokens are rejected.

The existing rotation implementation is recorded as complete in the task list. Its storage and reuse-detection mechanism must be inspected before tests are added; the plan does not assume a new token store or dependency.

### Migration Strategy

During the dual-auth phase, either a valid legacy session or a valid JWT provides access to an existing protected endpoint. A legacy client does not need to add an Authorization header during this phase. A JWT client does not need a legacy session. Applying both middleware components must not require both credentials to succeed.

Old sessions remain valid until their normal expiry, with a maximum lifetime of 24 hours. Transition compatibility does not extend an expired session. At the end of the stated 24-hour window, retire session middleware; protected requests must then authenticate with JWTs. Unchanged legacy clients lose protected access after this cutoff.

Before scheduling removal, establish the transition start time and verify that legacy-session issuance or renewal cannot create sessions whose expected validity extends beyond the cutoff. The supplied design does not specify how issuance is stopped. Record that mechanism and the observable retirement condition during implementation.

## Assumptions

- Clients that need access after the transition will adopt Authorization headers before legacy support is retired. Legacy clients may remain unchanged during the transition while their sessions remain valid.
- Legacy sessions have a maximum lifetime of 24 hours; verify expiry and renewal behavior before setting the retirement deadline.
- One-time refresh-token rotation is acceptable for expected session concurrency; verify that a token cannot be successfully consumed twice.
- The existing refresh implementation can detect reuse. Its mechanism and compatibility with the storage policy remain to be checked.

## Not Doing

- **OAuth/social login** — separate feature.
- **API rate limiting** — outside this auth migration.
- **Token revocation list** — excluded from this design. Do not promise immediate access-token invalidation on logout; logout behavior still needs definition.
- **Multi-device session management** — out of scope; each device gets independent tokens.

## Rejected Alternatives

No prior alternative evaluation was supplied. The recorded direction is a dual-auth migration followed by retirement of legacy sessions; no additional architecture choice is introduced by this refinement.

## Open Decisions and Verification Gates

- **Storage policy:** Confirm what persistent storage the policy prohibits and whether the 7-day refresh token, cookie persistence settings, and existing reuse-detection state comply. Resolve before approving the migration for release.
- **Mixed credentials:** Define behavior when a request presents both credentials, particularly conflicting identities or an invalid credential alongside a valid one. Resolve before completing the route migration.
- **Transition timing:** Identify the control that stops legacy issuance/renewal, define the 24-hour window's start, and verify that retirement does not truncate promised session validity.
- **Logout:** Define client token removal and refresh-token behavior after logout. The end-to-end test must use that agreed contract without assuming an access-token revocation list.

## Delivery Plan

See [implementation.md](./implementation.md) for component-level steps and verification, and [tasks.md](./tasks.md) for recorded progress. Runtime source is unavailable in this planning workspace; completed statuses are preserved from the existing task list and have not been independently verified.
