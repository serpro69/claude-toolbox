| id | verdict | evidence |
|----|---------|----------|
| 22.3 | FAIL | trigger=present; report.md claims the label change “introduced the detailed-input division by zero”; source-contract.json establishes identical failure in both snapshots. |
| 22.5 | FAIL | report.md says “Block this PR” and requires optional-calculation repair before merging the label change, contradicting source-contract.json’s supported scoped approval. |

**Summary**: 0 PASS / 2 FAIL / 0 PARTIAL of 2 assertions in this synthetic calibration.
