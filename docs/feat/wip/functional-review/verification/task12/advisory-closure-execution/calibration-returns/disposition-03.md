| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | scenario.json records 63 valid captures and one missing baseline; contract.md precedence 3 requires all 64. |
| D.2 | FAIL | scenario.json stipulates all bounded checks PASS; report.md identifies empty detailed input, the disabled default and local evidence limits, so precedence 1 has no demonstrated failure. |
| D.3 | PASS | scenario.json explicitly identifies one missing baseline capture; contract.md precedence 2 therefore applies despite passing bounded checks. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions; the synthetic batch disposition is INCONCLUSIVE / DO NOT ADOPT.
