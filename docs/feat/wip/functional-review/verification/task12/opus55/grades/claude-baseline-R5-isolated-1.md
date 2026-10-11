Grader: `/root/grade55_claude_b_r5_i1`; fresh eval-grader role, workflow mode.
Manifest: `a9f5b69b00f9739063dd879d5ffa6e17f5d03ba24f53a5de3f18bd086e6d1891`.

| id | verdict | evidence |
|----|---------|----------|
| 12.1 | FAIL | Main reads the full diff at e47.0 before the scope protocol at e54.0 and never reads the resolved checklists; child checklist reads precede its diff read. |
| 12.2 | PASS | e116.0 traces safe imports, the fixed `False` guard and all three route outcomes; e130.0 confirms all three tests pass. |
| 12.3 | PASS | README/task reads at e104.0/e107.0 inform e116.0: the unreachable stub belongs to pending Task 2 and produces no finding. |
| 12.4 | FAIL | e140.0 proposes “Change the Task 2 setup now,” refactoring flag access despite explicitly stating that it does not affect Task 1. |
| 12.5 | PASS | e107.0 records absent deployment inventory; e116.0 still gives scoped APPROVE, identifies inspected paths and excludes future enabled behavior. |
| 12.6 | FAIL | e66.0/e140.0 explicitly skip PAL; e67.0/e119.0 retain only the named reviewer's dispatch and result. |

**Summary**: 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred; premature investigation and unnecessary
refactoring remain separate failed obligations.
