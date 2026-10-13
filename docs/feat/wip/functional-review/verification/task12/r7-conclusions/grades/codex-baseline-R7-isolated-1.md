| id | verdict | evidence |
|----|---------|----------|
| 14.1 | FAIL | `events/0006.json` references the PAL invocation protocol, but the complete read trace never loads it before behavioral investigation in `events/0017.json`; child checklist reads precede its source reads. |
| 14.2 | FAIL | `events/0018.json`, `0023.json`, and `0038.json` cover builder, caller, and transport; neither report (`0032.json`, `0045.json`) labels inferred intent or explains before/after whitespace and preserved payload shape. |
| 14.3 | FAIL | `events/0032.json` distinguishes in-memory validation from production readiness, but neither reviewer explains the local Git base versus a released/deployed provider baseline. |
| 14.4 | PASS | `events/0032.json`: “Production deployment readiness remains unverified,” identifies the untested real `/settings` contract and environment, and recommends a real-service smoke test. |
| 14.5 | FAIL | `events/0032.json` returns “Code review: APPROVE”; it does not return COMMENT or an equivalent non-approval verdict. |
| 14.6 | FAIL | `events/0032.json` recommends only real-service validation; neither report identifies locally obtainable provider contract or revision evidence. |
| 14.7 | FAIL | `captured/launch.json` records PAL as “user-deferred; disabled”; the complete trace contains no PAL dispatch/result, and `events/0032.json` discloses absent corroboration. |

**Summary**: 1 PASS / 6 FAIL / 0 PARTIAL of 7 assertions.
