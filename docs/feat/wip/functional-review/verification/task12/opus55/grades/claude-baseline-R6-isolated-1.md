Grader: `/root/grade55_claude_b_r6_i1`; fresh eval-grader role, workflow mode.
Manifest: `7fc32c1f3970caa1fc43f310e3bf19469dc2423b53f1c5e7bb6b15ce5f3d0de5`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | FAIL | Main reads source at e60.0–e63.0 after loading only the profile index; its resolved checklists remain unread. Child completes checklist reads at e81.0–e90.0 before source at e93.0. |
| 13.2 | FAIL | e68.0 states the HEAD baseline cannot be read; e126.0 explicitly cannot confirm the change contains only the label and test assertions. |
| 13.3 | PASS | e126.0 separates “Existing crash … (not caused by this change)” from P0–P3 findings, consistent with captured/initial.patch and oracle/expected-results.json. |
| 13.4 | PASS | e126.0 identifies `summarize([], detailed=True)`, the shipped False setting, and unknown deployed settings: “I can't tell whether any deployed installs run with detailed mode on.” |
| 13.5 | PASS | e137.0 approves the change, makes the test suggestion optional, and assigns the crash to a separate issue; initial/final snapshot hashes show no automatic edits. |
| 13.6 | FAIL | In manifest's isolated mode, e68.0 dispatches the named reviewer without a diff; event-index.json contains no PAL dispatch/result, and e137.0 confirms “Only one reviewer ran.” Coverage limitations are disclosed. |

**Summary**: 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred. Missing diff/base evidence remains a
separate limitation in the named-reviewer path.
