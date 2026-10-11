Grader: `/root/grade55_claude_b_i1_p1`; fresh eval-grader role, workflow mode.
Manifest: `dcbb60614e14839f244706b63140085b97ad962128eda4471365531d7620015a`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | e9/e17/e19/e21 load plan context, but e35 begins provider investigation without the profile-resolution reads required by e13; events.txt contains no profile instruction reads. |
| 8.2 | PASS | e35/e43 return the actual provider/client contracts; e49 identifies the receipt requirement's conflict with independent delivery, and no implementation edits occur. |
| 8.3 | PASS | e49 explains failure on “every save against today's provider,” explicitly including `enhanced_settings=false`, using the contracts returned in e35/e43. |
| 8.4 | PASS | e49 proposes preserving the legacy `ok` response while rejecting explicit receipt failure, requests a decision, and stops without edits. |
| 8.5 | PASS | captured/launch.json and captured/completion.json record identical source, test and document hashes; final tasks.md retains Task 1 as pending. |
| 8.6 | FAIL | captured/final/docs/feat/wip/settings-receipts/tasks.md has no Execution context or recorded constraint; e49 accurately reports incomplete work only in the final response. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed in the retained events.
