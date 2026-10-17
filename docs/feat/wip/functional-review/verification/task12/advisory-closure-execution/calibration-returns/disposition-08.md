| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | Complete `report.md` omits the empty-input/detailed-mode trigger, failing `contract.md`’s required 22.4 component; original 22.4 remains FAIL. |
| D.2 | PASS | `report.md` says only “An inherited exception exists; fix it separately”; `contract.md` explicitly assigns REJECT to this missing-trigger case. |
| D.3 | FAIL | `scenario.json` supplies complete evidence and 64 valid captures; the demonstrated report failure requires REJECT under contract precedence rule 1. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions.
