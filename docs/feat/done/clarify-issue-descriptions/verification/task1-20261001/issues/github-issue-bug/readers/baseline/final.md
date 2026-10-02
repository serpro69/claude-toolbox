1. The issue exists because replaying a completed job after a receipt timeout reportedly produced duplicate receipts on QueueKit 1.4.2, leaving operators unsure whether the job was processed twice.

2. On Linux x86_64, replaying completed `job-42` with `--retry 1 --timeout-ms 250` produced two receipts in 2 of 5 attempts. The expected behavior was one receipt despite delivery retries, under a requirement predating 1.4.2.

3. The environment is captured. Duplicate receipts are reported; duplicate processing is unproven. The supplied 1.5.0 source suppresses receipts for IDs already in the supplied `seen_receipts` collection. It does not establish 1.4.2 behavior or prove a fix in 1.5.0, which the reporter did not test. The root cause remains unknown; the retry loop and `seen_receipts` are investigation leads. No 1.4.2 source revision or additional runtime evidence is available.

4. The status UI is outside scope. This remains a bug report, with no delivered fix, accepted implementation choice, or new acceptance threshold.

5. Bea owns repeating the report on 1.4.2 with receipt logging to gather evidence about the cause. That task remains open.
