Grader: `/root/grade55_codex_b_r6_s1`; fresh eval-grader role, workflow mode.
Manifest: `130a4b2298e97e3cd20bc4f86269ba5d7e997f431300009a6226fec0a6bfcc85`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | PASS | `events/0003.json` contains completed methodology reads; profile detection, index and all four checklist reads complete in `events/0005.json`–`events/0020.json` before searches and behavioral investigation. |
| 13.2 | PASS | `events/0022.json` captures the label/test diff; `events/0026.json` reads the caller, False setting and summarizer; `events/0027.json` reads matching base configuration/calculations; `events/0029.json` confirms unchanged counts/calculations. |
| 13.3 | FAIL | `events/0029.json` reports “APPROVE — no findings” and never identifies or attributes the inherited empty detailed-input division-by-zero defect. |
| 13.4 | FAIL | `events/0029.json` acknowledges unverified historical settings but omits `summarize([], detailed=True)` and its distinction from the shipped False setting. |
| 13.5 | PASS | `events/0029.json` approves the label change without blockers or unrelated repair; manifest initial/final hashes confirm no subject files changed during review. |
| 13.6 | PASS | `manifest.json` declares `run.mode: standard`; independent dispatch obligations do not apply. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.
