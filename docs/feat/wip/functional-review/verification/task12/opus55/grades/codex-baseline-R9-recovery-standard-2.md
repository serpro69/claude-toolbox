Grader: `/root/grade55_codex_b_r9r_s2`; fresh eval-grader role, workflow mode.
Manifest: `66301b6f7671810253d2251285d6835f1ed2610226a791cfaabace0d5ba50add`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | events/0003.json and 0005–0018 show successful methodology, detection, index and checklist reads before behavioral source inspection in events/0020.json. |
| 11.2 | PASS | events/0020.json and 0022.json trace the public caller, trimmed key and bounded retry implementation; events/0023.json explains trimming occurs before the existing retry method, preserving its handling. |
| 11.3 | PASS | events/0020.json contains assertions for transient success, exactly three exhausted attempts and one permanent-error attempt; events/0024.json executes all four tests successfully, distinguished from inspection in events/0023.json. |
| 11.4 | PASS | events/0025.json approves with no findings and confirms preservation of the retry policy; no retry-removal or permanent-error retry recommendation appears. |
| 11.5 | FAIL | events/0025.json approves and limits validation to the scripted backend, but reports only “2 staged files” and never names the inspected subject paths. |
| 11.6 | PASS | manifest.json declares standard mode; independent reviewer and PAL dispatch obligations therefore do not apply. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions.
