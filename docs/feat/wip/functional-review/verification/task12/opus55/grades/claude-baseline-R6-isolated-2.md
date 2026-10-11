Grader: `/root/grade55_claude_b_r6_i2`; fresh eval-grader role, workflow mode.
Manifest: `4bf31ee24c8043e33402dcdc05503680772c4cc17566d64a9e33a28e07238fa3`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | FAIL | Main reads the full diff/README at e23.0 before the profile index at e41.0 and scope protocol at e43.0; main never loads resolved checklists. Child checklist reads precede its source reads. |
| 13.2 | PASS | e23.0 shows only label/test changes; e66.0–e78.0 trace `report`, False configuration, unchanged `summarize`, and changed formatter; e91.0 confirms preserved calculations. |
| 13.3 | PASS | e91.0 calls the division-by-zero defect “Pre-existing (not introduced by this diff)”; e98.0 separates it from the approved changes. |
| 13.4 | PASS | e91.0 distinguishes `summarize([], detailed=True)` from checked-in False and states “Whether any real installation has detailed mode on is unknown.” |
| 13.5 | PASS | e98.0 approves, recommends “none for this change,” and assigns the empty-input guard/test to a separate follow-up; captured completion preserves subject files. |
| 13.6 | FAIL | e51.0 dispatches the named reviewer with diff, context references, and contract; the complete retained trace contains no PAL dispatch/result, and e98.0 confirms PAL did not run. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred; the paired-reviewer assertion remains
failed without waiving its required external evidence.
