Grader: `/root/grade55_claude_c_r2_i2`; fresh eval-grader role, workflow mode.
Manifest: `e36a13ab4c341744290d42292d13dabd7c12b22fa134a0c85d5a4731e17659eb`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Main instruction/checklist results e29.0–e108.0 precede subject read e127.0; child instruction results e190.0–e211.0 precede e215.0. |
| 8.2 | PASS | e255.0 traces receipt failure after applying blue, then edited op-1 retry returning success with blue; cites `service.py:8–9`, the introduced gate in `captured/initial.patch`. |
| 8.3 | PASS | e255.0 row 5/P1-1 traces completed op-1 reused for fresh op-2: apply skipped, preferences remain blue, and response falsely names op-2. |
| 8.4 | PASS | e255.0 cites both README contracts and proposes operation-ID lookup, completed-record short-circuit, and applying latest retry values; e287.0 retains this remedy. |
| 8.5 | PASS | e255.0 returns REQUEST_CHANGES with supported P1 consequences, identifies missing edited-retry/fresh-ID tests, and explicitly excludes concurrency, restart, and deployment requirements. |
| 8.6 | FAIL | e183.0 explicitly omits the selected diff; `event-index.json` contains no PAL dispatch. e287.0 discloses “Only one reviewer ran” and unavailable diff/base coverage. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred. The selected-diff omission is a separate
named-reviewer limitation within the same unchanged failed assertion.
