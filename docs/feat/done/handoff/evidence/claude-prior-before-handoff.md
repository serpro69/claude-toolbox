# Handoff: Parcel client retry-policy documentation

## Identity

- Topic: document the accepted Parcel client retry policy
- Created: 2026-10-30T13:22Z
- Repository: Parcel client checkout (no git remote configured), branch `main`,
  HEAD `001e792` ("Seed scenario fixture")
- Source-machine path (reference only):
  `/tmp/handoff-eval.HQD6g3Xg/claude-prior-indexed-context/project`

## Objective and constraints

- User intent: finish the Parcel client user documentation for the accepted retry
  policy.
- User constraint: do not implement or test anything yet.
- User scope: documentation only. The warehouse signage project
  (`label-decision.md`, orange priority-shelf labels) is unrelated and stays out.

## Decisions and rationale (user decisions)

- One submission attempt, no automatic retry, until the service supports
  idempotency keys. Reason: repeating a timed-out submission can create a
  duplicate parcel.
- Keep the 20-second submission timeout.
- A queue was rejected: it expands scope without preventing duplicates.

## Progress and evidence

- Done (local, uncommitted, untracked): `retry-policy.md` at the repo root. It
  covers behavior (one attempt, 20 s timeout), why there are no retries, the
  rejected queue, timeout handling, and revisiting once idempotency keys exist.
  It does not depend on Capy. **This file is not in the gist.** If it is missing
  on the destination, recreate it from the decisions above.
- Sources in the repo: `project.md`, `retry-decision.md`, `archive-excerpt.md`.
- `archive-excerpt.md` says the retry code change is implemented locally. The
  agent did not inspect or verify that code. No tests were run.
- Untracked dotfiles in `git status` (`.bashrc`, `.mcp.json`, `.idea`,
  `.claude/` and others) are sandbox device-file placeholders, not task work.
  Do not commit them.

## Continuation

Open questions for the user:

1. Keep the "Handling a timeout" advice (check whether the parcel was created
   before resubmitting)? The agent inferred it; no source states it. If the
   client has a specific lookup method, name it there.
2. Keep the file at the root as `retry-policy.md`, or move it into a README or a
   `docs/` folder?

Next action: get answers to these questions, adjust the doc, then commit only if
the user asks.

## Supporting references

- Repo files: `retry-decision.md` (the decision), `archive-excerpt.md` (queue
  rejection, implementation status), `project.md` (task statement).
- Capy (source machine only; the destination may not have this database. The
  repo files above contain the essential content):
  - Source label `kk:arch-decisions`, project `parcel-client`. Query:
    "parcel retry idempotency". Contains `retry-decision.md`, the authoritative
    retry decision.
  - Archived session `archive-parcel-42`, project `parcel-client`. Search it for
    the queue rejection rationale. It is the earlier discussion that
    `archive-excerpt.md` summarizes.
