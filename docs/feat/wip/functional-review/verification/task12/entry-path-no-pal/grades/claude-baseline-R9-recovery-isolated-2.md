Grader: `/root/grade_entry_b_r9_2`; fresh eval-grader role, workflow mode.
Manifest: `747c2f0aa7b7a98386ae988783b2da3c6592c1e90247999dd5a968e86cf111f3`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | e37.0 loads Python detection, but the trace ends at e47.0 without loading its review index/checklists; e18.0 contains scope metadata only, and e31.0 was denied. |
| 11.2 | FAIL | captured/report.md stops at setup and contains no trace through `Preferences.read`, normalization or `Repository.read_resilient`. |
| 11.3 | FAIL | captured/report.md contains no assessment of transient success, exhausted retries or `MissingPreference`; the complete retained trace contains no source investigation or test execution. |
| 11.4 | PASS | e47.0 and captured/report.md recommend only ways to resume the review; neither recommends changing normalization or retry behavior. |
| 11.5 | FAIL | captured/report.md says “I've stopped before running any reviewers” and requests permission to proceed; it provides no scoped approval. |
| 11.6 | FAIL | manifest.json declares isolated mode, but event-index.json contains no named-reviewer or PAL dispatch; captured/events.jsonl sequence 48 records zero spawned subagents and no reviewer results. |

**Summary**: 1 PASS / 5 FAIL / 0 PARTIAL of 6 assertions; no grader-material access appears in the retained tool requests, while the final access audit remains pending.
