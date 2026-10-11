Grader: `/root/grade55_codex_b_r9r_i2`; fresh eval-grader role, workflow mode.
Manifest: `de804977ca30b5422a54cc229d8d656f7a56e54de8e50b2ae7863b1f35d72af8`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | `events/0004.json` references the shared PAL protocol, but no completed load precedes investigation in `0025`; child checklists complete in `0036`–`0039` before source reads. |
| 11.2 | PASS | `events/0041.json`–`0042.json` trace the public caller, trimming and resilient repository path; `0045` explains that trimming preserves the existing contract. |
| 11.3 | PASS | `events/0028.json` records four passing tests; `0041` supplies exact outcomes and attempt counts, while `0045` distinguishes the child’s static inspection from parent execution. |
| 11.4 | PASS | `events/0034.json` recommends retaining the change; `0045` preserves the resilient-read contract and proposes no retry removal or permanent-error retries. |
| 11.5 | FAIL | `captured/report.md` approves without invented blockers and discloses PAL absence, but omits inspected source paths; `events/0045.json` also omits those paths. |
| 11.6 | FAIL | Manifest mode is isolated; `events/0027.json` links one child, while `0034` explicitly confirms PAL was unavailable and only one reviewer ran; exact handoff plaintext remains unverified. |

**Summary**: 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred; instruction loading and missing path
coverage are retained as separate failures.
