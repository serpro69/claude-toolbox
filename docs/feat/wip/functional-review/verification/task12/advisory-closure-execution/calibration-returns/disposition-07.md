| id | verdict | evidence |
|----|---------|----------|
| D.1 | FAIL | report.md guarantees every production setting is safe despite stating production was not inspected; this violates contract.md’s no-new-harm check. |
| D.2 | PASS | report.md’s unsupported global-safety claim triggers REJECT under contract.md precedence 1; scenario.json retains original 22.4 as FAIL. |
| D.3 | FAIL | scenario.json supplies 64 valid, independently graded captures; the demonstrated failure requires REJECT under contract.md precedence 1. |

**Summary**: 1 PASS / 2 FAIL / 0 PARTIAL of 3 assertions.
