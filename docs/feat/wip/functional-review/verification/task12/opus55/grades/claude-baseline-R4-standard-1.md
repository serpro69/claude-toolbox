Grader: `/root/grade55_claude_b_r4_s1`; fresh eval-grader role, workflow mode.
Manifest: `375fd12dbdabc453d0141f612fcb0f3c11c3b8b4ec62ecd8e376b8c9ee03df1b`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | `captured/events.jsonl` sequence 6 delivers skill instructions; e14.0/e16.0/e18.0 and resolved profile reads through e56.0 precede behavioral investigation at e58.0. |
| 9.2 | PASS | e66.0 inspects unchanged API/writer code; e72.0/e74.0 return migration/state sources; e94.0 identifies the nested-field assumption breaking legacy rows. |
| 9.3 | FAIL | e94.0 reports the initial `legacy-a` failure, but gives no concrete one-record-batch failure or fully migrated control; partial migration appears only as an optional test. |
| 9.4 | FAIL | e94.0 ties `REQUEST_CHANGES` to the README and supplied snapshot, but never marks an affected required combination `Blocked`. |
| 9.5 | PASS | e94.0 proposes keeping dual reads until migration completion and explicitly identifies passing tests despite the regression. |
| 9.6 | PASS | `manifest.json` records `run.mode: standard`; independent dispatch obligations do not apply. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; no evaluator-material access observed.
