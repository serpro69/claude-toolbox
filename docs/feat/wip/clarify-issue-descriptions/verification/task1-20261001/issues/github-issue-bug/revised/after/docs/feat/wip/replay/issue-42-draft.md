# REPLAY broken?? retries????

## Problem

The reporter observed two receipts for a completed job in 2 of 5 replay attempts
on QueueKit 1.4.2, Linux x86_64. Duplicate receipts make operators unsure whether
the completed job was handled twice; the report does not establish duplicate job
processing.

The [requirement](../../../../repository/requirements.md), which predates 1.4.2, is that a
completed job must emit one receipt even when delivery is retried. This issue
concerns duplicate receipts; the status UI is outside its scope.

## Reported reproduction

Environment: QueueKit 1.4.2, Linux x86_64.

1. Seed completed `job-42`.
2. Run `queuectl replay job-42 --retry 1 --timeout-ms 250`.
3. Let the first receipt time out at 250 ms.

Expected: one receipt for the completed job, including when delivery is retried.

Observed: two receipts in 2 of 5 attempts. The reporter did not test 1.5.0.

## Evidence and investigation

The retry loop and `seen_receipts` are suspected areas to investigate, not
established causes. The root cause remains undecided.

The supplied [current source](../../../../repository/replay.py) is from the default branch
`main`, revision `5c814d7` (QueueKit 1.5.0). In that snapshot, `emit_receipt`
returns no receipt when the job ID is already in the supplied `seen_receipts`
collection; otherwise, it records the ID and returns a completed receipt. This
source inspection does not establish behavior on 1.4.2 or demonstrate that the
reported problem is fixed. No 1.4.2 source or runtime evidence beyond the report
is available, and no tests were run for this edit.

Bea owns repeating the report on 1.4.2 with receipt logging. No implementation
choice or new acceptance threshold has been accepted. This remains a bug report,
not a delivered fix.

- [x] Capture reporter environment
- [ ] Bea: repeat on 1.4.2 with receipt logging
