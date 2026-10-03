# Auth Refactor — Implementation Plan

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)
> Status: planning; runtime implementation is not available in this workspace

## Existing State and Target Mapping

Task 1 is recorded as complete: JWT generation/validation, login token issuance, auth middleware, and login integration coverage. Task 2.1's rotating refresh endpoint is also complete. Preserve those completion records; the remaining work starts with Task 2.2.

The supplied workspace contains design documents only. Exact source filenames, function names, test commands, and runtime behavior cannot be verified here. The component names below identify intended targets, not invented file paths. At implementation handoff, locate the existing token module, login and refresh handlers, JWT and session middleware, protected-route registration, logout handler, and auth integration suite. Record their actual paths and the relevant test command here before making runtime changes → verify: every planned edit and test maps to an existing component or an explicitly justified new test file.

## Token Refresh

Task 2.2 completes the existing refresh path rather than rebuilding Task 2.1.

1. Inspect the refresh handler, token validation, and the mechanism supporting one-time refresh use → verify: identify how expiry, rotation, and reuse are represented, and report any gap against the design before treating the endpoint as complete.
2. Extend the refresh integration suite using the project's existing test setup → verify: a valid refresh token produces usable replacement credentials; an expired refresh token is rejected; after rotation, the previous refresh token is rejected and the replacement remains usable.
3. Check the configured 15-minute access-token and 7-day refresh-token lifetimes with the existing time-control facilities, if available → verify: expiry cases run deterministically without waiting for real token lifetimes.

Use the actual endpoint contract for response assertions; the supplied docs do not establish exact payload fields or error bodies. Mark Task 2.2 complete only after executing the relevant integration tests.

## Protected Routes Migration

Task 3 depends on the completed login/authentication foundation in Task 1.

1. Locate the protected-route registration and both middleware implementations; record the transition start and 24-hour cutoff. Confirm the rule for requests carrying both credential types → verify: the route inventory distinguishes existing protected endpoints from login/refresh handlers, and the credential-selection rule has an explicit expected result.
2. Wire the dual-auth path for existing protected routes → verify: a legacy client with a valid session and no Authorization header retains access; a new client with a valid JWT and no session cookie retains access. Neither client must satisfy both middleware paths.
3. Extend protected-route integration coverage → verify: requests with no usable credential, expired credentials, or malformed credentials are rejected; valid credentials preserve the endpoint's existing behavior. Include the agreed behavior for requests carrying both credential types.
4. Retire session middleware at the cutoff using the project's existing rollout/configuration mechanism → verify: legacy-only requests fail after retirement, while valid JWT requests continue succeeding. Cover the transition and retired states separately; simultaneous acceptance is a transition-only assertion.

Do not claim zero-downtime migration solely from configuration inspection. Exercise protected requests before and after the cutover and check that JWT access remains available. Existing sessions may expire before the cutoff; compatibility does not extend their lifetime or require acceptance of expired sessions.

## Final Verification

Task 4 follows all implementation tasks.

1. Resolve the design's policy/storage and logout verification points using the actual implementation and the applicable policy → verify: record the refresh-cookie settings, the supporting policy requirement, and the expected logout behavior. Do not assert compliance or immediate access-token invalidation without evidence.
2. Run the complete login → protected access → refresh → protected access → logout flow → verify: each step satisfies the documented endpoint contract and the established logout expectations.
3. Verify the migration lifecycle → verify: unchanged legacy and JWT clients both work during the transition, and only JWT authentication remains supported after retirement.
4. Invoke `/kk:test` for the full relevant test suite, `/kk:document` for the affected documentation, `/kk:review-code` with the actual project language, and `/kk:review-spec` against this feature's documents → verify: record executed checks and resolve findings before marking the feature complete.

These checks are planned work. No runtime tests or independent reviews have been executed as part of this document refinement.

## Assumptions and Scope

Clients needing access after the cutoff can adopt JWT authentication by then. Refresh rotation is assumed to fit expected session concurrency, but its reuse behavior still needs the Task 2.2 tests. The storage-policy and logout questions remain explicit verification points rather than inferred guarantees.

OAuth/social login, API rate limiting, token revocation lists, and multi-device session management remain outside scope. The compatibility decision and rejected alternatives are recorded in [design.md](./design.md).
