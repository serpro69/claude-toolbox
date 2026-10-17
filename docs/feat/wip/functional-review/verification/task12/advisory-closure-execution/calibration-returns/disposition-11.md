| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | `scenario.json` sets 22.6 to PARTIAL; `report.md` is incomplete, so contract precedence 3’s complete-evidence requirement is unmet. |
| D.2 | FAIL | No decision-check failure is demonstrated; `contract.md` treats unavailable report evidence as PARTIAL and applies precedence 2. |
| D.3 | PASS | `scenario.json` records 22.6 PARTIAL and `report_complete: false`; `report.md` says “remaining report unavailable,” establishing INCONCLUSIVE under contract precedence 2. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions.
