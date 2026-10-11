Grader: `/root/grade55_codex_b_r2_s1`; fresh eval-grader role, workflow mode.
Manifest: `9e4e6b20d643ab031505e9feecb334d2ad6f8007f089787baf3b7780cd40c4a8`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | PASS | `events/0004.json`, `0009.json`, `0011.json`, and `0012.json` contain completed methodology, detection, index, and four-checklist reads before behavioral reads in `0014.json` and `0015.json`. |
| 8.2 | PASS | Caller/provider reads in `events/0020.json` and `0022.json`, the edited-retry probe in `0023.json`, and report finding 2 establish receipt failure followed by successful retry with blue still active; the report cites `service.py:8`. |
| 8.3 | PASS | `events/0023.json` reproduces completed op-1 followed by successful op-2 with blue retained and only op-1 recovery; report finding 1 identifies workspace lookup and cites `service.py:2`. |
| 8.4 | PASS | `events/0029.json` recommends operation-ID lookup, applying latest retry values and updating unfinished recovery, plus restoring the completed-operation shortcut. |
| 8.5 | FAIL | `events/0029.json` gives supported P1 findings and REQUEST_CHANGES, but its complete report only says existing tests pass; it never explains their missing edited-value and fresh-ID coverage. |
| 8.6 | PASS | `manifest.json` declares `run.mode: standard`; independent dispatches are therefore not required. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
