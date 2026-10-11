Grader: `/root/grade55_codex_b_r9r_i1`; fresh eval-grader role, workflow mode.
Manifest: `ba762e832c62895508629f55e9ba524a517bf7b0e8d267d914565c14c29fbb59`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Parent instruction/profile reads in events/0002.json, 0013.json and 0017–0021.json precede investigation in 0024.json; child checklist reads in 0036–0039.json precede source reads in 0041–0042.json. |
| 11.2 | PASS | events/0042.json and 0048.json inspect the complete delegation chain; 0032.json and 0051.json explain normalization before the existing three-attempt retry policy. |
| 11.3 | PASS | events/0028.json records all four tests passing; 0046.json inspects success, exhaustion and permanent-error assertions; 0051.json attributes execution to the parent and disclaims an independent rerun. |
| 11.4 | PASS | events/0034.json approves keeping the change; 0051.json identifies no removal plan and explicitly preserves the bounded retry policy. |
| 11.5 | FAIL | captured/report.md approves and discloses scripted-backend/PAL limits, but names no inspected subject paths; events/0051.json likewise supplies only file counts. |
| 11.6 | FAIL | events/0027.json links the named reviewer, but no PAL invocation/result exists; captured/command.json records PAL disabled and captured/report.md confirms missing corroboration. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred; the report's missing path coverage is
a separate failure.
