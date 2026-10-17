Grader: `/root/grade55_codex_c_r9r_s2`; fresh eval-grader role, workflow mode.
Manifest: `53574cf2f64db869948863c298e351d4a7eae0323b89649314923c4bc7607e8a`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | `events/0006–0007.json`, `0011.json`, and `0013.json` return complete common instructions, detection rules, Python index and checklists before investigation in `0015–0020.json`; earlier subject access is metadata only. |
| 11.2 | PASS | `events/0019–0021.json` trace `Preferences.read` through `key.strip()` into `Repository.read_resilient`, preserving normalization and the existing retry policy. |
| 11.3 | PASS | `events/0019.json` contains assertions for transient recovery, exactly three exhausted attempts and immediate permanent failure; `0024.json` executes all four tests successfully, while `0025.json` distinguishes tracing from execution. |
| 11.4 | PASS | `events/0021.json` retains retry ownership in `Repository.read_resilient`; `0025.json` concludes “No changes recommended.” |
| 11.5 | PASS | `events/0025.json` approves the staged paths against inspected HEAD `7c0410c`, names successful checks, and limits execution evidence to the scripted backend without adding blockers or production guarantees. |
| 11.6 | PASS | `manifest.json` records `run.mode: standard`; independent named-reviewer and PAL dispatch obligations do not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.
