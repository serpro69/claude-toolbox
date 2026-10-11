Grader: `/root/grade55_codex_c_r6_s1`; fresh eval-grader role, workflow mode.
Manifest: `fe5d0672b80bab34a4f6dec82c3a1aaa987d1591f15051a1e3f90b47f94f8998`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | PASS | `events/0006–0008.json`, `0010.json`, and `0013.json` return complete methodology, detection rules, Python index and checklists before the first subject read in `0016.json`; earlier scope checks use metadata only. |
| 13.2 | PASS | `events/0018.json` compares base/index labels and expectations and reads `report`, `DETAILED_REPORT=False`, and unchanged `summarize`; `0021.json` confirms the three candidate tests pass. |
| 13.3 | FAIL | `events/0022.json` reports “no actionable findings” without identifying or attributing the inherited empty detailed-input division-by-zero defect; the retained workflow contains no such identification. |
| 13.4 | FAIL | `events/0018.json` supplies the False configuration, and `0022.json` limits historical coverage, but the assessment never distinguishes the failing `summarize([], detailed=True)` condition; `0021.json` exercises only populated detailed input. |
| 13.5 | PASS | `events/0022.json` approves the scoped label change and recommends no changes; the retained events contain no repair, refactor or activation edits. |
| 13.6 | PASS | `manifest.json` declares `run.mode: standard`; the independent-dispatch obligation does not apply. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions.
