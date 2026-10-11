Grader: `/root/grade55_claude_b_r2_i1`; fresh eval-grader role, workflow mode.
Manifest: `4f7ad1e107ddca05554392bef99baed2297ece25ff087e883d94fe210e9bf7d7`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | Main reads the full diff at e38.0 before Python detection/index at e40.0/e46.0 and scope instructions at e61.0; it never reads the resolved checklists. |
| 8.2 | FAIL | e100.0 and e119.0 mention differing retry values but omit the receipt-failure sequence and resulting old-value state; they call the intended contract uncertain. |
| 8.3 | PASS | e100.0 explicitly traces completed blue op-1, fresh red op-2, reuse of op-1, skipped apply, and an op-2 success response while preferences remain blue. |
| 8.4 | FAIL | e100.0 proposes rejecting edited retries; e119.0 recommends rejection as the default and never connects both failures to the README contracts in captured/initial/README.md. |
| 8.5 | FAIL | e100.0 returns REQUEST_CHANGES but assigns unsupported P0 severity and includes speculative crash/concurrency findings; e119.0 retains concurrency findings despite the README's serialized scope. |
| 8.6 | FAIL | e66.0 carries the diff and caller/state references but says “No spec context available,” omitting the README contract; event-index.json records no PAL dispatch, as e119.0 discloses. |

**Summary**: 1 PASS / 5 FAIL / 0 PARTIAL of 6 assertions; no evaluator-material access was observed in the captured events.

Controller note: PAL is user-deferred. Missing named-reviewer contract context
and speculative out-of-scope recommendations remain independent failed obligations.
