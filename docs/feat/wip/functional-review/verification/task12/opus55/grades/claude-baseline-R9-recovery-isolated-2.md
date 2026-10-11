Grader: `/root/grade55_claude_b_r9r_i2`; fresh eval-grader role, workflow mode.
Manifest: `9d725fc5af552517e04ab182baf81b27ead899882570c7f4306357a9102e6ace`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | Main reads the profile index at e38.0, then the full diff at e43.0/e46.0 without loading its four resolved checklists; child checklist reads e67.0–e76.0 precede its diff read e80.0. |
| 11.2 | PASS | e83.0/e86.0/e89.0 trace normalization through the caller and repository; e103.0 explains preserved retries, trimmed backend keys and the three-attempt cutoff. |
| 11.3 | PASS | e103.0 assesses inspected tests covering transient-success, three exhausted failures and immediate permanent failure; e124.0 records four actual passing executions, reported separately at e139.0. |
| 11.4 | PASS | e103.0 states “retry behaviour is preserved and doesn't fall back to `read_once`” and “Nothing needs removing”; e139.0 recommends no retry-policy changes. |
| 11.5 | PASS | e139.0 reports APPROVE without blocking findings, names all four inspected paths, and limits backend/write claims; suggested improvements remain P3. |
| 11.6 | FAIL | e60.0 dispatches the named reviewer with diff/caller paths but “No spec context available,” omitting the README contract; e59.0/e139.0 explicitly confirm PAL never ran. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred; omitted explicit contract context remains
a separate handoff limitation.
