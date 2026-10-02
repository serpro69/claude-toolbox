# REPLAY broken?? retries????

## Reported problem

On QueueKit 1.4.2, replaying a completed job with one retry configured produced two
receipts in 2 of 5 attempts after the first receipt timed out. Operators could not
tell whether the completed job had been handled twice.

The [requirement](../../../../repository/requirements.md), which predates 1.4.2,
is that a completed job must emit one receipt even when delivery is retried.

## Reproduction reported on 1.4.2

Environment: QueueKit 1.4.2 on Linux x86_64.

1. Seed completed `job-42`.
2. Run `queuectl replay job-42 --retry 1 --timeout-ms 250`.
3. Let the first receipt time out at 250 ms.

Expected: one receipt for the completed job, including when delivery is retried.

Observed: two receipts in 2 of 5 attempts.

## Evidence and unresolved cause

The retry loop and `seen_receipts` handling are suspected areas to investigate;
neither is an established cause.

The [supplied source](../../../../repository/replay.py) is from `replay/queue`'s
default branch `main`, revision `5c814d7` (QueueKit 1.5.0). Its `emit_receipt`
function returns no receipt when the job ID is already in the supplied
`seen_receipts` collection; otherwise, it records the ID and returns a completed
receipt. This source does not establish how 1.4.2 behaved or resolve the reported
duplicate receipts. No 1.4.2 source or independent reproduction is available, and
the reporter did not test 1.5.0. No runtime verification is available for 1.5.0.

## Follow-up and scope

- [x] Capture reporter environment
- [ ] Bea: repeat on 1.4.2 with receipt logging

Bea's repeat run is the next step toward establishing the cause. No implementation
choice or new acceptance threshold has been accepted. This issue concerns duplicate
receipts; the status UI is outside its scope. This remains a report, not a delivered
fix.
