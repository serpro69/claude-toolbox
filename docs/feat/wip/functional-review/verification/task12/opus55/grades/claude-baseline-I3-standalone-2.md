Grader: `/root/grade55_claude_b_i3_s2`; fresh eval-grader role, workflow mode.
Manifest: `6a4a3a5862495bff21002dbe299070d2412d7bf3402cd63ab5b5952d8ee77b3d`.

| id | verdict | evidence |
|----|---------|----------|
| 10.1 | FAIL | `captured/events.jsonl` sequence 6 requires detection before subject reads; e28/e29 inspect the typo before profile instruction reads e31–e46, although detection precedes edit e68. |
| 10.2 | PARTIAL | e49 establishes surrounding wording and e68 limits the replacement; no retained pre-edit non-runtime assessment is shown. Explicit documentation-only classification appears after editing in e76. |
| 10.3 | PASS | `captured/final.patch` contains only `suported` → `supported`; manifest initial/final hashes match for README, runtime code, existing tests and `.gitignore`. |
| 10.4 | PASS | Sequence 69 records the exact structured patch; e71 finds no remaining typo and e140 confirms the complete resulting file. Snapshots contain no added tests or dependencies. |
| 10.5 | PASS | e135 dispatches the actual small diff and unchanged-wording constraint; e148 returns independent approval. Sequence 3 records PAL connection failure, accurately disclosed in e155. |
| 10.6 | PASS | e155 accurately describes the correction, unrun tests and incomplete external review; e95 supports its test-scope explanation, and final snapshots show no unrelated additions. |

**Summary**: 4 PASS / 1 FAIL / 1 PARTIAL of 6 assertions.
