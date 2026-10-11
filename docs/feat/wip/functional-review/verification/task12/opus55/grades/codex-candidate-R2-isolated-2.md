Grader: `/root/grade55_codex_c_r2_i2`; fresh eval-grader role, workflow mode.
Manifest: `491ebed2f792c06c9eb21d99cda250df3049b7192c826938f00eb0233b2b0bc5`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | Successful main instruction reads in `events/0003.json`, `0007.json`–`0013.json`, `0018.json`, and `0020.json`–`0021.json` precede source investigation in `0026.json`; child instruction reads `0049.json`–`0059.json` precede source reads in `0060.json`. |
| 8.2 | PASS | `events/0034.json` reproduces receipt failure after blue applies, followed by a green retry returning success with blue active; `0082.json` traces `client.submit`, provider application, and the introduced `service.py:8` branch. |
| 8.3 | PASS | `events/0034.json` records completed blue `op-1`, then successful green `op-2` with blue still active and only `op-1` retained; `0082.json` identifies workspace lookup at `service.py:2`. |
| 8.4 | PASS | `events/0082.json` ties both failures to README requirements and recommends operation-ID lookup, completed-record early return, and applying current retry values before receipt completion; `0047.json` repeats these remedies. |
| 8.5 | PASS | `events/0082.json` supports P1 severity, returns `REQUEST_CHANGES`, and explains that nominal-save, same-value-retry, and ordinary-replay tests omit the failing scenarios; it excludes concurrency, restart, network, and deployment guarantees. |
| 8.6 | FAIL | `event-index.json` retains no PAL invocation or result; `events/0047.json` explicitly states “PAL was unavailable, so there is no second independent review.” Exact submitted handoff plaintext also remains unverified. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL remains explicitly user-deferred; the missing component
is retained as FAIL.
