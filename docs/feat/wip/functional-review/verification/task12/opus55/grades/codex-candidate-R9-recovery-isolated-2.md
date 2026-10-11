Grader: `/root/grade55_codex_c_r9r_i2`; fresh eval-grader role, workflow mode.
Manifest: `959324a29039f695222417e32356940cd6c998a84c39907afb3db6941de913cb`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Main instruction reads precede source investigation at events/0027.json; raw protocol sequences 95/194 confirm complete packet results. Child reads events/0044–0051 precede events/0053.json. |
| 11.2 | PASS | events/0068.json traces `Preferences.read → read_preferences → Repository.read_resilient → read_once → backend`, explaining normalization before unchanged retries. |
| 11.3 | PASS | events/0033–0034 record successful executions; events/0068.json covers recovery, three-error exhaustion and permanent errors, explicitly attributing execution to the parent. |
| 11.4 | PASS | events/0068.json states “preserves repository ownership of retries”; both reports recommend no changes. |
| 11.5 | PASS | captured/report.md and events/0068.json approve the scoped change, identify inspected source paths and baseline, and disclose absent PAL corroboration and production inspection. |
| 11.6 | FAIL | Manifest mode is isolated; events/0030.json records the named reviewer, but the completed workflow invokes no PAL reviewer and events/0042.json explicitly reports a “single-reviewer isolated result.” |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; exact submitted handoff plaintext remains unverified.

Controller note: PAL remains user-deferred. The grader resolved shortened
paginated instruction results using the already-sealed raw protocol before
finalizing 11.1; no final verdict or rubric was revised.
