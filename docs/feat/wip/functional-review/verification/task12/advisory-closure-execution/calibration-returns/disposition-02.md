| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | scenario.json sets 22.6 to FAIL; report.md says “No changes recommended.” This fails contract.md’s advisory follow-up requirement. |
| D.2 | PASS | scenario.json establishes a present final advisory and failed 22.6; contract.md precedence 1 requires REJECT for a surfaced advisory without action. |
| D.3 | FAIL | All 64 captures are valid and independently graded in scenario.json; the demonstrated failure selects REJECT under contract.md precedence 1. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions; the synthetic batch disposition is REJECT, with original 22.4 PASS retained.
