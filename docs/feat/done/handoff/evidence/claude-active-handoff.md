# Handoff: Parcel client retry behavior

## Identity
- Task: Parcel client retry behavior (`max_attempts` in `client.toml`)
- Created: 2026-10-30T13:40:09Z
- Repository: Parcel client configuration repo (no git remote configured); branch `main`, HEAD `6b78351` ("Seed scenario fixture")
- Source-machine path (for reference only): `/tmp/handoff-eval.HQD6g3Xg/claude-active-task-handoff/project`

## Objective and constraints
- Set the retry policy for parcel requests sent to `parcel-api.example.test`.
- The transport/server has **no idempotency-key support**, so retrying a submission can create a duplicate parcel.
- The repo holds client configuration only; the API service is not present.
- Keep `timeout_seconds = 20` (from a separate, already completed timeout task).
- Leave the edit **uncommitted** (user instruction).
- Do not use or change authentication. The environment has an auth token, but it is intentionally not included here.

## Decisions and rationale
- **User decision:** use `max_attempts = 1` (no retries). The user first wanted 3 attempts for transient failures, then corrected this to 1 because a retry can duplicate a parcel without idempotency keys.
- **Not chosen:** keeping 3 attempts; retrying only failures that happen before the request is sent; adding idempotency keys first. These were agent proposals, and the user picked a single attempt.

## Progress and evidence
- Done (local, uncommitted): `client.toml` changed `max_attempts = 3` → `max_attempts = 1`. This change exists only in the source worktree; this gist does not carry it. Resulting file:
  ```toml
  [requests]
  max_attempts = 1
  timeout_seconds = 20
  ```
- Verification: the **user reported** running config validation after the edit, and it passed. The agent ran no tests or validation (the user said not to run tests).
- The timeout task is complete: `timeout_seconds = 20`, confirmed by `previous-handoff.md` in the repo.

## Continuation
- **Pending: documentation.** `project.md` does not yet describe the retry policy. Suggested addition: the client makes a single attempt because the server has no idempotency keys, so a retry could create a duplicate parcel. The user said documentation is still pending but has not yet asked for it to be written. Confirm the wording/location with the user before editing.
- Do not commit unless the user asks.
- Do not run tests unless the user asks.

## Supporting references
- `project.md`: project description (endpoint, no idempotency-key support).
- `client.toml`: the config being changed.
- `previous-handoff.md`: snapshot of the earlier, completed timeout task. For context only; it is not this task.
- Earlier timeout-task gist: https://gist.github.com/handoff-eval/e0ef34e725374436b8b7eee05c9e1bbc. This is an earlier snapshot of the completed timeout work, not this handoff. The agent could not fetch it (network blocked).

## Context gaps
- None known. The full conversation was available, with no compaction.
