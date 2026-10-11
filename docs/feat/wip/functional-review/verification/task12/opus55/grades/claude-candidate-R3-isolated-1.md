Grader: `/root/grade55_claude_c_r3_i1`; fresh eval-grader role, workflow mode.
Manifest: `e2a43e0d69781a0c4ced4ac0ccfe32f9e8d188c5a35847665925da32ce07e727`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Main completes instruction/checklist reads through e105.0 before e130.0; child completes its required reads through e214.0 before e218.0. |
| 7.2 | FAIL | e131.0 identifies the repository contract and e162.0 resolves `eval-release`; e186.0 explicitly states the historical provider source was not obtained. |
| 7.3 | FAIL | e309.0 cites the unconditional acknowledgement check but says provider behavior is inferred from documentation, without historical source evidence. |
| 7.4 | FAIL | e275.0 explicitly marks “Introduced vs inherited: Unknown at source level,” although it correctly excludes Task 2 and rejects it as an excuse. |
| 7.5 | FAIL | In manifest-declared isolated mode, e186.0 states “Historical source: none materialized”; event-index.json records no PAL invocation, confirmed by e309.0. |
| 7.6 | FAIL | e275.0 admits the named reviewer never read the historical provider; e309.0 confirms the second independent review never ran. |
| 7.7 | FAIL | e309.0 gives REQUEST_CHANGES and Blocked but explicitly says the provider source could not be read; the required inspected-release basis is absent. |
| 7.8 | PASS | e309.0 proposes accepting legacy `ok: True` responses without `applied`, gating the new request key, and testing disabled-feature saves; it rejects the receipt-only mock as compatibility proof. |

**Summary**: 2 PASS / 6 FAIL / 0 PARTIAL of 8 assertions; no actor access to grading material was observed.

Controller note: PAL is user-deferred. The missing historical source and named
reviewer receipt are independently unmet obligations, not waived by that exception.
