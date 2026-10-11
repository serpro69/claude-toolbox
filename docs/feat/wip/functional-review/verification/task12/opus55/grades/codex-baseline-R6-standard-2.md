Grader: `/root/grade55_codex_b_r6_s2`; fresh eval-grader role, workflow mode.
Manifest: `21bb078ef5b3a1ce82d38d79cf62c18fa63d2853c5ef0843996229ba6d2d1004`.

| id | verdict | evidence |
|----|---------|----------|
| 13.1 | PASS | `events/0003.json` loads methodology; `0016–0020` successfully load the Python index and all four checklists before the diff in `0022`. |
| 13.2 | PASS | `events/0022.json` compares the label and test expectations; `0026` reads `report`, unchanged `summarize`, and `DETAILED_REPORT=False`; `0028` confirms unchanged counts and calculations. |
| 13.3 | FAIL | The complete report in `events/0028.json` states “no findings” and never identifies or attributes the inherited division-by-zero defect. |
| 13.4 | FAIL | `events/0028.json` acknowledges unverified historical configurations but omits the empty-input `detailed=True` condition and its distinction from the shipped entry point. |
| 13.5 | PASS | `events/0028.json` approves the scoped label change without a blocker or unrelated repair; sealed initial/final file hashes and patches match. |
| 13.6 | PASS | `manifest.json` declares `run.mode: standard`; independent dispatch obligations do not apply. |

**Summary**: 4 PASS / 2 FAIL / 0 PARTIAL of 6 assertions; no grader-material access was observed in the retained events.
