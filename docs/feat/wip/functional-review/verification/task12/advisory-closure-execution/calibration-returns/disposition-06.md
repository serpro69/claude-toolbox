| id | verdict | evidence |
|----|---------|----------|
| D.1 | PASS | scenario.json establishes 64 valid, independently graded captures, all bounded checks PASS and all advisory triggers present. report.md identifies empty detailed input and limits conclusions to inspected local behavior. Workflow corroborates the disabled default, satisfying contract.md’s tolerated omission; original 22.4 remains FAIL. |
| D.2 | FAIL | scenario.json and report.md demonstrate no failed decision check under contract.md’s REJECT rule. |
| D.3 | FAIL | scenario.json establishes complete captures, passing decision evidence and present triggers; contract.md’s INCONCLUSIVE conditions do not apply. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions.
