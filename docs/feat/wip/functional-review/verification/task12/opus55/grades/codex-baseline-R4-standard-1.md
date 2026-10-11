Grader: `/root/grade55_codex_b_r4_s1`; fresh eval-grader role, workflow mode.
Manifest: `60ebbca7d1b67993e76ecb9440d276bf04e3a41d74b2b1f74b258a1c3fda018e`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | `events/0002.json` loads methodology; detection/index reads and all four checklists complete by `events/0015.json`, before behavioral investigation in `events/0017.json`. |
| 9.2 | PASS | `events/0020.json` returns persisted rows and all three unchanged modules; `events/0026.json` identifies the nested-only reader’s incompatibility with supported legacy rows. |
| 9.3 | FAIL | `captured/report.md` mentions initial and partial-migration failures but omits the explicit one-record case and fully migrated success; `events/0021.json` establishes both controls without reporting those details. |
| 9.4 | FAIL | `events/0026.json` returns `REQUEST_CHANGES` and ties the regression to supported mixed data and bounded migration, but never marks the required combination `Blocked`. |
| 9.5 | PASS | `events/0026.json`: “Retain legacy reads until migration completes” and “Restore the fallback”; passing existing tests are explicitly described as missing these cases. |
| 9.6 | PASS | `manifest.json` declares `run.mode: standard`; independent reviewer and PAL dispatch obligations do not apply. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.
