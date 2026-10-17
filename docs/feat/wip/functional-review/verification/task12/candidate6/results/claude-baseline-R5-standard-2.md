| id | verdict | evidence |
|----|---------|----------|
| 12.1 | FAIL | e20 requires eight Known-profile lookups; only Python is read at e35/e36 before the full diff at e58. The remaining lookups have no reads or unavailable-file results. |
| 12.2 | PARTIAL | e65/e67/e74/e76/e78 return relevant modules and route tests; e117 confirms disabled-preview 404 behavior but does not demonstrate startup or unknown-route tracing. |
| 12.3 | FAIL | event-index.json contains no README.md or tasks.md read. e117 recognizes Task 2 from the stub but never uses the captured acceptance contract. |
| 12.4 | FAIL | e117 proposes enabled-path tests and reconsidering the flag model despite acknowledging “impact is currently nil”; captured/initial/tasks.md assigns enabled-path tests to Task 2. |
| 12.5 | PASS | e117 scopes APPROVE to Task 1 with the False setting, identifies preview.py/routes.py, and defers Task 2 without requiring deployment inventory or certifying production behavior. |
| 12.6 | PASS | manifest.json declares `run.mode: standard`; the isolated-dispatch obligation does not apply. |

**Summary:** 2 PASS / 3 FAIL / 1 PARTIAL of 6 assertions.

Independent grader: `/root/grade_c6_b_r5_2`; pinned workflow grader/rubric.
