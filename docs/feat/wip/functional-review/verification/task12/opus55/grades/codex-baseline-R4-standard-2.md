Grader: `/root/grade55_codex_b_r4_s2`; fresh eval-grader role, workflow mode.
Manifest: `4369af1e0d682b7f1dcb86978fb64546594de2b0a551bc1386ebe2d9e346163f`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | Successful instruction reads in events/0002.json, 0007.json, 0008.json and 0010.json precede behavioral investigation in 0012.json. |
| 9.2 | PASS | events/0015.json returns the persisted records and unchanged callers; 0020.json identifies the removed fallback and legacy-row incompatibility. |
| 9.3 | FAIL | events/0020.json reports both failures, but omits fully migrated readability despite the successful control in 0017.json. |
| 9.4 | FAIL | events/0020.json ties REQUEST_CHANGES to the supplied snapshot and README contract, but never marks the affected required combination Blocked. |
| 9.5 | PASS | events/0020.json recommends restoring the fallback until migration completion and requests changes despite passing new-write tests. |
| 9.6 | PASS | manifest.json declares standard mode; independent dispatch obligations do not apply. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.
