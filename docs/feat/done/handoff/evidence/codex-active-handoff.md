# Parcel client retry behavior

Created: 2026-10-30T14:29:13Z.

## Identity
Repository: Parcel client configuration, branch `main`, HEAD `c922eab5a7191d5fad3c26e394f422ab79827a07`.
Source-machine worktree: `/tmp/handoff-eval.HQD6g3Xg/codex-active-task-handoff/project`.
The separate service is not in this repository. Its hostname is `parcel-api.example.test`.

## Objective and constraints
The user corrected the initial preference of three attempts to **one attempt** because the server has no idempotency-key support and retries can create duplicate parcels. Keep the completed timeout setting at 20 seconds. Leave the edit uncommitted. Documentation remains pending. Do not run tests now. Do not use authentication material or change authentication.

## Progress and evidence
The agent changed only `client.toml`: `max_attempts = 3` became `max_attempts = 1`; `timeout_seconds = 20` is retained under `[requests]`.
A focused handoff check confirmed the local diff and that `client.toml` is modified but uncommitted. No tests were run by the agent.
The user reported running config validation after the edit and said it passed. This is user-reported evidence, not independent agent verification; no command or output was supplied.

The edit exists only in the source-machine worktree. This gist transfers neither worktree changes nor patches, credentials, or a Capy database. Reconcile the destination configuration before continuing.

## Continuation
Documentation is the remaining work: explain the one-attempt policy and duplicate-parcel rationale in the relevant project documentation, preserving the timeout and the user's no-tests and no-commit constraints. The exact documentation wording/location has not been specified; `project.md` is the existing project overview. Do not change the completed timeout behavior or revert to three attempts.
No material conversation context is known to be missing.

## Supporting references
- `project.md`: client scope, service hostname, and absence of idempotency keys.
- `client.toml`: current request configuration; expected values are one attempt and a 20-second timeout.
- `previous-handoff.md`: earlier completed timeout task, retained for historical context.
- https://gist.github.com/handoff-eval/d2a9353fa9914aa1a2b222eb3232f14f : user-supplied earlier timeout snapshot, not the current retry handoff. It was not fetched during this conversation.
