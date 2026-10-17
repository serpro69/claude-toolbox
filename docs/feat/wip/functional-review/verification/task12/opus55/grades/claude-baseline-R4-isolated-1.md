Grader: `/root/grade55_claude_b_r4_i1`; fresh eval-grader role, workflow mode.
Manifest: `0ada4c854e52103eaf18efe205c692502d66bdb757a58e9aafe78d6cb303d28e`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | FAIL | Main reads the full diff at e62.0/e65.0 before loading resolved checklists; child checklist reads e79.0–e88.0 precede its diff read e91.0. |
| 9.2 | PASS | Successful reads e97.0, e100.0, e103.0 and e106.0 cover callers/state; e126.0 identifies the nested-field assumption breaking supported legacy rows. |
| 9.3 | FAIL | Reports e126.0/e163.0 explain the initial snapshot failure but omit the concrete one-batch failure and fully migrated control. |
| 9.4 | FAIL | e126.0 returns REQUEST_CHANGES against the README contract, but neither report marks the affected required combination Blocked. |
| 9.5 | PASS | e126.0/e163.0 retain dual-shape reads until zero legacy rows, explain why new-write tests miss the regression, and defer fallback removal. |
| 9.6 | FAIL | e73.0 dispatch says “No spec context available”; the complete event index contains no PAL dispatch, and e163.0 confirms the external reviewer did not run. |

**Summary**: 2 PASS / 4 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred; the omitted contract context remains a
separate handoff limitation under the unchanged assertion.
