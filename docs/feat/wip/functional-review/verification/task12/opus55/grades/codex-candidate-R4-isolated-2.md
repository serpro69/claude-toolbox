Grader: `/root/grade55_codex_c_r4_i2`; fresh eval-grader role, workflow mode.
Manifest: `caa6191df0a5df8eeb851d62cbc82e46ae767290fc330f6e42f3ba9c4c0ed8bc`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | Completed bootstrap/profile reads in events/0006.json–0018.json precede investigation in events/0020.json; child methodology reads in events/0041.json–0048.json precede events/0050.json. |
| 9.2 | PASS | events/0023.json returns records and unchanged callers; events/0069.json identifies the nested-only reader as incompatible with supported legacy rows. |
| 9.3 | PASS | events/0069.json identifies failures on `legacy-a` initially and `legacy-c` after one batch, with completed migration readable; events/0027.json confirms both `KeyError` results. |
| 9.4 | PASS | events/0069.json marks initial and partial migration “Blocked,” returns REQUEST_CHANGES against the README contract, and explicitly claims no deployed-environment assessment. |
| 9.5 | PASS | events/0069.json requires restoring dual-shape reads and deferring removal until the supported-data contract changes; it explains the existing tests omit mixed data. |
| 9.6 | FAIL | events/0025.json records the named reviewer, but events/0039.json explicitly reports PAL unavailable; captured/protocol.jsonl retains no PAL dispatch or result. Exact named-reviewer handoff plaintext remains unverified. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.

Controller note: PAL remains explicitly user-deferred; the omitted component
is retained as FAIL.
