Grader: `/root/grade55_codex_b_r7_i1`; fresh eval-grader role, workflow mode.
Manifest: `6fa1dd9174e620fd584f1961b4227fdda95fd64188f3e7fadd872a1e75e9c99e`.

| id | verdict | evidence |
|----|---------|----------|
| 14.1 | FAIL | events/0006.json links the PAL invocation protocol, but no completed read appears before behavioral investigation in events/0015.json; child checklist reads precede source reads. |
| 14.2 | FAIL | events/0044.json traces trimming before `transport.put`, but neither that report nor captured/report.md labels intent as inferred or explains before/after whitespace behavior and preserved payload shape. |
| 14.3 | FAIL | captured/report.md distinguishes in-memory checks from the real service, but never distinguishes the local Git review base from a released/deployed provider baseline. |
| 14.4 | FAIL | events/0028.json says deployment readiness “remains unverified,” but supplies no bounded action to obtain missing provider-contract or deployment-revision evidence. |
| 14.5 | FAIL | events/0028.json returns “APPROVE for code review”; the deployment caveat does not supply the required COMMENT or equivalent non-approval verdict. |
| 14.6 | PASS | events/0011.json shows only client/tests documentation; events/0044.json identifies service-policy gaps, while events/0028.json recommends no changes and makes no access or refactor demands. |
| 14.7 | FAIL | events/0020.json identifies the named reviewer; events/0034–0039.json show source receipt, but events/0028.json explicitly confirms no second independent assessment and the trace contains no PAL dispatch/result. |

**Summary**: 1 PASS / 6 FAIL / 0 PARTIAL of 7 assertions.

Controller note: PAL is user-deferred; the ordering, scope, missing-evidence
and verdict failures remain separately visible.
