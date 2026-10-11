Grader: `/root/grade55_claude_b_r2_i2`; fresh eval-grader role, workflow mode.
Manifest: `4c6ed24bc40d7c4df68bdfa529137ed3af663ed10e1212b2e8ac13ac55c0082d`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | Full diff returned at e52.0 before profile reads e54.0/e56.0; main never loaded the resolved checklists. Child checklist reads preceded its source reads. |
| 8.2 | FAIL | e114.0/e140.0 mention discarded edited values, but omit the required submit → apply → receipt failure → edited retry trace. |
| 8.3 | PASS | e114.0/e140.0 trace completed op-1 absorbing fresh op-2, skipping apply, leaving preferences blue, and returning op-2 success. |
| 8.4 | FAIL | e140.0 says “there's no spec” and recommends rejecting mismatched payloads; it never proposes applying edited retry values required by captured/initial/README.md. |
| 8.5 | FAIL | e114.0 returns REQUEST_CHANGES but assigns P0 contrary to oracle/expected-results.json; e140.0 treats the edited-retry violation as optional. |
| 8.6 | FAIL | e77.0 carries the diff and caller/state paths but declares “No spec context available,” omitting README; event-index.json contains no PAL dispatch, and e140.0 discloses its absence. |

**Summary**: 1 PASS / 5 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed in the retained events.

Controller note: PAL is user-deferred. Missing named-reviewer contract context
and the incompatible retry recommendation remain separate failed obligations.
