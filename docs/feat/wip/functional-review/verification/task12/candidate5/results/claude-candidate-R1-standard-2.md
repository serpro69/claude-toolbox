| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PASS | Completed bootstrap reads e16.0–e26.0, index e44.0 and all checklist parts e52.0/e54.0 precede source investigation e61.0; e31.0 reads scope metadata only. |
| 6.2 | PASS | e86.0 reads unchanged setup.py; e142.0 traces A beginning, failing with cleanup queued, B completing in workspace w, then cleanup A causing active_connection to return None. |
| 6.3 | PASS | e147.0 cites cleanup.py:3, identifies unconditional deletion of B's live association and describes the queued-cleanup trigger and lost connection. |
| 6.4 | PASS | e147.0 proposes restoring the setup_id ownership guard and states no concurrency hardening is needed. |
| 6.5 | PASS | e147.0 gives P1 and REQUEST_CHANGES, explains passing tests miss the scenario, and discloses denied reproduction; e133.0 confirms two passing tests and e122.0 confirms denial. |
| 6.6 | PASS | manifest.json records mode standard; independent dispatch requirements do not apply. |

**Summary:** 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.

Independent grader: `/root/grade_c5_r1_2`; pinned workflow grader/rubric.
