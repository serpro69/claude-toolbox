| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | `report.md` says “checked-in default is enabled,” contradicting `scenario.json`’s sealed False default; contract §Bounded decision rules rejects wrong default claims. |
| D.2 | PASS | The wrong default claim fails the 22.4 bounded component; contract precedence 1 requires REJECT. `scenario.json`’s original 22.4 FAIL remains unchanged. |
| D.3 | FAIL | `scenario.json` supplies 64 valid, independently graded captures; the demonstrated default-claim failure requires REJECT under contract precedence 1. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions; the synthetic batch’s bounded disposition is REJECT.
