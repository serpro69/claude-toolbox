# Duplicate receipts when replaying a completed job on QueueKit 1.4.2

Replaying a completed job after a receipt timeout produced two receipts in 2 of 5 attempts on QueueKit 1.4.2. Operators cannot tell from the duplicate receipts whether the completed job was handled twice; duplicate job processing has not been established.

## Environment and reproduction

- QueueKit 1.4.2
- Linux x86_64

1. Seed completed job `job-42`.
2. Run `queuectl replay job-42 --retry 1 --timeout-ms 250`.
3. Let the first receipt time out at 250 ms.
4. Observe the receipts emitted for the job.

**Expected:** A completed job emits one receipt even when delivery is retried. This [requirement](https://github.example.invalid/replay/queue/blob/5c814d7/requirements.md) predates 1.4.2.

**Observed:** Two receipts in 2 of 5 attempts. QueueKit 1.5.0 was not tested by the reporter.

## Investigation and limits

The root cause remains undecided. The retry loop and `seen_receipts` are investigation leads, not confirmed causes.

The supplied [current source](https://github.example.invalid/replay/queue/blob/5c814d7/replay.py) is from `main` at revision `5c814d7` (QueueKit 1.5.0). Its `emit_receipt` function returns no receipt when the job ID is already in the supplied `seen_receipts` collection; otherwise it adds the ID and returns a completed receipt. This source snapshot does not establish what happened on 1.4.2 or verify that 1.5.0 resolves the report. No 1.4.2 source revision or additional runtime evidence is available.

Bea owns repeating the report on 1.4.2 with receipt logging to gather evidence about the cause.

- [x] Capture reporter environment
- [ ] Bea: repeat on 1.4.2 with receipt logging

## Scope and status

This issue concerns duplicate receipts; the status UI is outside its scope. It is a bug report, not a delivered fix. No new acceptance threshold or implementation choice has been accepted.
