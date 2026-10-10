| id | verdict | evidence |
|----|---------|----------|
| 12.1 | FAIL | e17 requires detection reads for eight Known profiles; only Python is read (e33–e34), with no unavailable exceptions recorded, before investigation at e59. |
| 12.2 | PARTIAL | e119 confirms import safety, short-circuiting, and preview 404; e62/e87 provide source, but settings 200 and unknown-route 404 are not observably traced. |
| 12.3 | FAIL | The only subject reads are e59, e61, e84, and e86; README.md and tasks.md are never read, although e119 correctly calls the stub intentional Task 1 scaffolding. |
| 12.4 | FAIL | e119 proposes premature-enablement safeguards and future auth work while acknowledging it is not a live bug; these changes lack a demonstrated current issue. |
| 12.5 | PASS | e119 names the inspected modules, gives APPROVE for this Task 1 commit, and bounds reachability to while the flag is off, without deployment demands or production guarantees. |
| 12.6 | PASS | manifest.json records run.mode: standard; independent-dispatch obligations do not apply. |

**Summary:** 2 PASS / 3 FAIL / 1 PARTIAL of 6 assertions.

Independent grader: `/root/grade_c5_b_r5_2`; pinned workflow grader/rubric.
