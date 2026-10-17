Grader: `/root/grade55_claude_b_r9r_i1`; fresh eval-grader role, workflow mode.
Manifest: `81435dd952534db6e2d91090b95487656b82d5a0292fc6388182b3a246c31a87`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | Main reads the full diff at e45.0/e48.0 after loading only the Python index (e40.0); checklist reads occur in the child at e79.0–e88.0. |
| 11.2 | PASS | e121.0 traces `Preferences.read` → `read_preferences` → `Repository.read_resilient`, explaining trimming once and unchanged bounded recovery. |
| 11.3 | PASS | e121.0 assesses success after a transient failure, three exhausted failures, and immediate permanent failure, explicitly stating source-only inspection; e141.0 records four passing tests, attributed to the main actor in e152.0. |
| 11.4 | PASS | e121.0 preserves retry semantics; e152.0 identifies the stale `read_once` alternative as skipping the required retry policy and recommends no retry removal. |
| 11.5 | PASS | e121.0 names all five inspected paths and source limits; captured/report.md approves with optional P3 suggestions and discloses absent PAL corroboration. |
| 11.6 | FAIL | e71.0 dispatches `kk:code-reviewer` with the diff and source paths but says “No spec context available”; e70.0/e152.0 confirm PAL never ran, leaving no PAL dispatch or result. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL is user-deferred; omitted explicit contract context remains
a separate handoff limitation.
