Grader: `/root/grade55_codex_b_r7_s1`; fresh eval-grader role, workflow mode.
Manifest: `fa82dee33a5499c6bad114d5cc408f9fe2d71956b467bee5a5ca27676eb239fc`.

| id | verdict | evidence |
|----|---------|----------|
| 14.1 | PASS | Successful methodology/profile reads in events/0002.json, 0004.json, and 0007–0020 precede diff/source investigation in events/0023.json and 0024.json; earlier scope reads contain filenames only. |
| 14.2 | FAIL | Events/0026.json and 0028.json cover `save` and transport behavior; events/0030.json omits inferred-intent labeling, before/after explanation, and preserved payload shape. |
| 14.3 | FAIL | Events/0030.json acknowledges unverified external contracts but never distinguishes the local Git base and `MemoryTransport` from a released/deployed provider baseline. |
| 14.4 | FAIL | Events/0030.json reports “APPROVE”; it supplies neither an Unknown deployment conclusion nor a bounded action to obtain missing baseline evidence. |
| 14.5 | FAIL | Events/0030.json returns “APPROVE — no code-level deployment blockers found” despite acknowledging unverified external caller contracts and API behavior. |
| 14.6 | FAIL | Events/0030.json makes no credentials/access demands, but identifies no useful locally obtainable contract or revision evidence; its only next action is review closure. |
| 14.7 | PASS | Manifest `run.mode` is `standard`; independent-reviewer dispatch obligations do not apply. |

**Summary**: 2 PASS / 5 FAIL / 0 PARTIAL of 7 assertions; no grading-material access was observed in retained actor events.
