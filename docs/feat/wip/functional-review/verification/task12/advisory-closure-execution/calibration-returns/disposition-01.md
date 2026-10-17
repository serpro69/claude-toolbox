| id | verdict | evidence |
|----|---------|----------|
| D.1 | PASS | scenario.json establishes 64 valid independently graded captures, all bounded checks PASS and all eight advisory triggers present; report.md satisfies every 22.4 component, meeting contract.md precedence 3. |
| D.2 | FAIL | scenario.json stipulates passing checks; report.md identifies empty detailed input, limits conclusions to inspected behavior and requests separate follow-up, so contract.md precedence 1 is unmet. |
| D.3 | FAIL | scenario.json establishes complete valid captures, passing checks and present triggers; contract.md precedence 2 has no qualifying condition. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions; the synthetic batch supports KEEP FOR THIS BOUNDED SLICE, with original 22.4 PASS retained.
