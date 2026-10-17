| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | scenario.json records 22.6 FAIL; report.md says “No changes recommended.” contract.md precedence 1 bars KEEP. |
| D.2 | PASS | scenario.json establishes a present final advisory and 22.6 FAIL; report.md supplies no follow-up action. contract.md requires REJECT; original 22.4 remains PASS. |
| D.3 | FAIL | scenario.json records one missing baseline capture, but contract.md precedence 1 states that a known failure remains REJECT despite missing evidence. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions; the synthetic batch disposition is REJECT.
