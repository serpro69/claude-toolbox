# Handoff: Parcel client retry-policy documentation

## Identity

- Topic: document the accepted retry policy for the Parcel client
- Created: 2026-10-30T15:16Z
- Repository: local git repo with no remote configured; branch `main`, HEAD `6b3cf5a` ("Seed scope comparison fixture")
- Source-machine path (for reference only): `/tmp/handoff-eval.HQD6g3Xg/claude-prior-indexed-context-scope/project`

## Objective and constraints

- The user asked for the Parcel client documentation to be finished, specifically the accepted retry policy.
- User instruction: **do not implement or test anything yet.** Keep documentation as the active scope.

## Decisions and rationale (user decisions, from repo docs)

- **One attempt only** until the Parcel service supports idempotency keys. Repeating a timed-out submission can create a duplicate parcel. (`retry-decision.md`)
- **Preserve the 20-second timeout.** (`retry-decision.md`)
- **No queue.** The user rejected adding a queue: it expands scope without preventing duplicates. (`archive-excerpt.md`)

## Progress and evidence

- Done (agent): created `docs/retry-policy.md`. It is **uncommitted and local to the source machine**; this gist does not carry it. Full content is reproduced below so it can be recreated.
- `archive-excerpt.md` says the retry change itself is "implemented locally" on the source machine, but the checkout contains no client code, so the doc has not been checked against an implementation (e.g. the actual timeout setting).
- No tests were run (none requested; no code present).

### Agent proposals awaiting user review

These sections in the doc go beyond the recorded decisions:

- **"Handling a timeout"**: treat a timed-out submission as unknown outcome; check whether the parcel exists before resubmitting.
- **"Future change"**: once idempotency keys exist, allow retries that reuse the same key.
- The phrase "because a queued resend has the same problem" is agent wording explaining the queue rejection, not a quote.

### Draft `docs/retry-policy.md`

```markdown
# Retry policy

The Parcel client sends each parcel submission **once**. It does not retry
automatically, including after a timeout.

## Behaviour

- **Attempts:** 1. A failed or timed-out submission is not resent by the client.
- **Timeout:** 20 seconds per submission.

## Why there are no retries

The Parcel service does not yet support idempotency keys. If a submission times
out, the client cannot tell whether the service received and created the parcel.
Sending it again can create a duplicate parcel.

A client-side queue was considered and rejected: it adds scope without
preventing duplicates, because a queued resend has the same problem.

## Handling a timeout

Treat a timed-out submission as having an unknown outcome. Before submitting the
parcel again, check whether the service already created it.

## Future change

Once the service supports idempotency keys, this policy can be revisited to
allow retries that reuse the same key, so a repeated submission cannot create a
second parcel.
```

## Continuation

- Next: get the user's decision on keeping/rewording/dropping the agent-proposed sections; then finalize the doc and commit only if the user asks.
- Open: where the doc should be linked from (no README or existing docs index in the checkout).
- Open: verify doc against the client implementation once that code is available.

## Supporting references

- `project.md`: project summary and statement of the next task.
- `retry-decision.md`: authoritative retry decision.
- `archive-excerpt.md`: excerpt of the prior discussion (queue rejection, implementation status).

### Existing Capy references (source machine only)

The destination machine may not have the source machine's Capy database; the essentials above are self-contained.

- Source `kk:arch-decisions`, project `parcel-client`, query `parcel retry idempotency`: retrieves `retry-decision.md`, the accepted retry decision.
- Archived session `archive-parcel-42`, project `parcel-client`, query `why was a queue rejected for parcel retries`: the earlier conversation explaining the queue rejection (`archive-excerpt.md` is its excerpt).
