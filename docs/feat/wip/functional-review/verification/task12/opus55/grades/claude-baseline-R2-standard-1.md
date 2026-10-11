Grader: `/root/grade55_claude_b_r2_s1`; fresh eval-grader role, workflow mode.
Manifest: `975c29c57e4bd3e5adc6f621cae3102c70220887beab8eec3da6736639dc3707`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | SKILL bytes appear in `captured/events.jsonl` sequence 6; successful methodology, detection, index, and checklist results (e12.0–e61.0) precede the full diff at e66.0. |
| 8.2 | PASS | e100.0 invokes `client.submit` through receipt failure and an edited retry; e103.0 confirms success with blue still active. e115.0 finding 2 cites `service.py:6,8` and explains skipped application. |
| 8.3 | PASS | e103.0 shows op-2 success with blue unchanged and only op-1 recorded; e115.0 finding 1 attributes this to workspace lookup accepting the completed record at `service.py:2`. |
| 8.4 | PASS | e115.0 quotes both README contracts; its suggested fix restores operation-ID lookup, completed-ID handling, and application of current retry values. |
| 8.5 | FAIL | e115.0 requests changes and explains test gaps, but rates both failures P0; `oracle/expected-results.json` supports P1 or justified P2. |
| 8.6 | PASS | `manifest.json` declares standard mode, so independent dispatch obligations do not apply. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.
