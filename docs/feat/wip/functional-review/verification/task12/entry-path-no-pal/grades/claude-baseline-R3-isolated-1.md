Grader: `/root/grade_entry_b_r3_1`; fresh eval-grader role, workflow mode.
Manifest: `02517f21ca308b8013f320894fc4813c5025881f9e1f85d1f274efc3bab9ab9d`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main reads the full diff at e64 after index-only e52, without loading its four resolved checklists; the child successfully loads them at e107/e110/e113/e116 before its diff read at e119. |
| 7.2 | PASS | Repository contract e76 names the supported release and distinguishes the undeployed candidate; e80/e83 successfully retrieve `eval-release:provider/settings.py`, rather than the PR base. |
| 7.3 | PASS | e166/captured/report.md traces persistence followed by `{"ok": True}`, absent `applied`, and the unconditional client exception with `enhanced_settings=False`, citing historical source. |
| 7.4 | PASS | e166 ties the introduced regression to independently releasable main and states “a pending provider task cannot change the supported baseline”; Task 2 remains outside the findings. |
| 7.5 | FAIL | e95/e96 materialize the external snapshot and e101→e125 establish local reviewer receipt, but full revision/hash/span provenance is absent; e100/e166 confirm PAL never ran. |
| 7.6 | FAIL | e101→e125→e150 link the local code-reviewer’s source receipt and historical comparison; e100/e166 establish that the required PAL invocation and independent result are absent. |
| 7.7 | FAIL | Child e150 says REQUEST_CHANGES, but e166/captured/report.md omits Blocked and a final REQUEST_CHANGES verdict, while asserting “no deployed provider sends” beyond the inspected snapshot. |
| 7.8 | PASS | e150/e166 propose accepting missing receipts for ordinary disabled-feature saves, preserving `eval-release` compatibility, and restoring its response-shape test; receipt-only mocks are identified as hiding the regression. |

**Summary**: 4 PASS / 4 FAIL / 0 PARTIAL of 8 assertions.

Controller note: preliminary evaluator-path scan completed just after dispatch;
all 40 retained tool requests had no evaluator-path flags. The grader received
this timing correction. Original seal/hash validation preceded dispatch.
