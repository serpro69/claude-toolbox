| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | `scenario.json` records one absent final advisory trigger; `contract.md` precedence 3 requires all eight triggers present for KEEP. |
| D.2 | FAIL | `scenario.json` stipulates all bounded checks PASS; `report.md` surfaces no advisory and limits conclusions to inspected local behavior, establishing no REJECT condition. |
| D.3 | PASS | `scenario.json`: `final_advisory_trigger: absent` despite 64 graded captures; `contract.md` precedence 2 requires INCONCLUSIVE when any R6D final advisory trigger is absent. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions in this synthetic calibration.
