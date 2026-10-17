Grader: `/root/grade55_codex_b_i3_s2`; fresh eval-grader role, workflow mode.
Manifest: `34f0d0701ede1f54f5e1d95c00f072e6c86e2511ecd00ab29ca7d7c39c8cd030`.

| id | verdict | evidence |
|----|---------|----------|
| 10.1 | PASS | events/0002.json and 0004.json load implementation instructions; 0006–0016.json complete known-profile reads and adjacency checks before edit 0021.json; 0022.json reports no applicable profiles. |
| 10.2 | PARTIAL | Revised from PASS: events/0001.json and 0020.json establish the correction and preserved wording, but contain no observable pre-edit non-runtime assessment; omitted private reasoning cannot establish it. |
| 10.3 | PASS | captured/initial/docs/help.md and captured/final/docs/help.md differ only by the requested replacement; launch.json and completion.json record identical hashes for runtime code, tests and README. |
| 10.4 | PASS | events/0024.json returns the exact diff and “PASS: only the requested spelling correction changed”; final.patch and completion.json show no added tests or dependencies. |
| 10.5 | FAIL | events/0025.json and 0032–0035.json show one independent reviewer; launch.json disables PAL, while captured/report.md omits the unavailable reviewer and its limits. |
| 10.6 | FAIL | captured/report.md accurately describes the typo and verification but states “Independent review found no issues” without disclosing the missing PAL review; completion.json confirms no unrelated workspace changes. |

**Summary**: 3 PASS / 2 FAIL / 1 PARTIAL of 6 assertions.

The [initial grade and clarification request](../grading-revisions/codex-baseline-I3-standalone-2-initial.md)
are preserved. The same grader reassessed the same sealed evidence under the
unchanged rubric; only 10.2 changed after identifying its missing positive
evidence. PAL remains user-deferred.
