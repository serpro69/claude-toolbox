1. The issue exists because replaying a completed job reportedly produced duplicate receipts, leaving operators unsure whether the job was handled twice.

2. On QueueKit 1.4.2, Linux x86_64, the reporter seeded completed `job-42`, ran `queuectl replay job-42 --retry 1 --timeout-ms 250`, and let the first receipt time out at 250 ms. Two receipts appeared in 2 of 5 attempts; one was expected.

3. The reporter’s environment is captured. Duplicate receipts are reported; the retry loop is only a suspected cause, and `seen_receipts` is mentioned tentatively. Reproduction with receipt logging remains pending. Version 1.5.0 was not tested. The artifact does not establish whether the job was actually handled twice.

4. UI work is explicitly outside this issue. The artifact describes a report, not a delivered fix.

5. Bea owns repeating the reproduction on version 1.4.2 with receipt logging. No subsequent steps or fix owner are specified.
