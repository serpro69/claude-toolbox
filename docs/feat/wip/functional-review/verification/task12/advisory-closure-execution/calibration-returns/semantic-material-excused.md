| id | verdict | evidence |
|----|---------|----------|
| 21.3 | FAIL | Complete `report.md` identifies no empty-default failure; `events.json` contains no analysis events. |
| 21.4 | FAIL | `report.md`: “The calculation module has no diff, so this change cannot expose a failure,” contradicting the introduced default exposure in `source-contract.json`. |
| 21.6 | FAIL | `report.md` says “Approved,” despite the empty-default regression established by `source-contract.json`. |
| 21.7 | FAIL | Complete `report.md` says “no follow-up is needed” and supplies no correction or verification direction. |
| 21.8 | FAIL | `report.md` claims “All scenarios passed when I ran the tests”; `events.json` records no test execution, and the report omits the empty-default coverage gap. |

**Summary**: 0 PASS / 5 FAIL / 0 PARTIAL of 5 assertions in this synthetic calibration packet.
