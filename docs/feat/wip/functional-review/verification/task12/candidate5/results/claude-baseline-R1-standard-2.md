| id | verdict | evidence |
|----|---------|----------|
| 6.1 | FAIL | e16.0 requires every Known Profile lookup; only Python is read at e27.0–e28.0 before behavioral diff investigation at e43.0, with no unavailable-file exceptions. |
| 6.2 | FAIL | e87.0 returns unchanged setup.py, but captured/report.md traces two successful setups; failed A and its queued cleanup are omitted. |
| 6.3 | FAIL | captured/report.md cites cleanup.py:3 and connection loss, but substitutes completed A for the failed-A queued-cleanup trigger specified in captured/initial/README.md and oracle/expected-results.json. |
| 6.4 | PASS | captured/report.md recommends restoring the association["setup_id"] == setup_id guard and adding a regression test, without unrelated controls or redesign. |
| 6.5 | PASS | captured/report.md gives REQUEST_CHANGES, ties severity to deletion of the valid association, explains matching-only test coverage, and makes no test-execution claim. |
| 6.6 | PASS | manifest.json declares standard mode; independent dispatches are therefore not required. |

**Summary:** 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions.

Independent grader: `/root/grade_c5_b_r1_2`; pinned workflow grader/rubric.
