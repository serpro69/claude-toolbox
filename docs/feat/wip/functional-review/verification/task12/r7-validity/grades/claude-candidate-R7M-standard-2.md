| id | verdict | evidence |
|----|---------|----------|
| 19.1 | PASS | Instructions return in captured sequence 6, e15.0–e25.0, e59.0 and e65.0/e67.0 before investigation at e82.0; earlier subject operations inspect metadata and filename adjacency only. |
| 19.2 | PASS | captured/report.md traces preserved string/empty-string saves and `clear_name` sending `PUT /settings` with null to restore the account default. |
| 19.3 | PASS | captured/report.md distinguishes v1’s 422 without mutation from v2 clearing; explicitly limits MemoryTransport evidence and separates the Git review base from deployment state. |
| 19.4 | PASS | captured/report.md says deployment readiness is “Unknown,” explains v1 failure, and requires confirmation that target environments run v2 before deployment. |
| 19.5 | PASS | captured/report.md gives COMMENT, reports no code defects, and closes with the unresolved provider-version check rather than deployment approval. |
| 19.6 | PASS | captured/report.md requests a version check and dependency note without demanding live access or speculative code changes; e110.0 confirms its three-test execution claim. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions.
