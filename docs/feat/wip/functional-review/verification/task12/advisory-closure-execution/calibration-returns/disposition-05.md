| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | scenario.json records an absent final advisory trigger; contract.md requires all eight candidate R6D triggers present for KEEP. |
| D.2 | FAIL | scenario.json stipulates passing bounded checks; report.md limits conclusions to inspected local behavior. No decision-check failure establishes REJECT under contract.md precedence 1. |
| D.3 | PASS | scenario.json records child-only discovery and an absent final advisory trigger; contract.md precedence 2 requires INCONCLUSIVE / DO NOT ADOPT. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions.
