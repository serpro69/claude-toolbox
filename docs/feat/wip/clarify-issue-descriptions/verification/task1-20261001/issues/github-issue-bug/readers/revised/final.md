1. The issue tracks duplicate receipts for completed jobs, which leave operators unsure whether a job was handled twice. The existing requirement is one receipt per completed job, including retried delivery. Duplicate job processing is not established.

2. On QueueKit 1.4.2, Linux x86_64, the reporter seeded completed `job-42`, ran `queuectl replay job-42 --retry 1 --timeout-ms 250`, and let the first receipt time out. Two receipts appeared in 2 of 5 attempts; one was expected.

3. The reproduction result is reported, not independently verified. Inspection of the supplied 1.5.0 source shows that `emit_receipt` suppresses a receipt when the job ID is already in the supplied `seen_receipts` collection. That does not establish 1.4.2 behavior or prove a fix. The root cause remains unknown; the retry loop and `seen_receipts` are suspects. No tests were run for this edit, and the reporter did not test 1.5.0.

4. The status UI is outside scope. Duplicate job processing is not established, and no implementation choice or new acceptance threshold has been accepted. This is a bug report, not a delivered fix.

5. Bea owns repeating the report on 1.4.2 with receipt logging. Capturing the reporter’s environment is complete; the repeat remains outstanding.
