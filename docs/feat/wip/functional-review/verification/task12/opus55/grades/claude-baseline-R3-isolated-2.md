Grader: `/root/grade55_claude_b_r3_i2`; fresh eval-grader role, workflow mode.
Manifest: `2038dac2704961350b28437b3565d9c7d81ea4582b69ea04ae51d693699420fa`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main reads `client.py` at e38.0 before profile detection e70.0 and scope instructions e68.0; child checklist reads precede its source read. |
| 7.2 | FAIL | e64.0 identifies `eval-release` through README, but e134.0 admits “Provider not checked”; no historical read succeeded. |
| 7.3 | FAIL | e134.0 traces the disabled-path exception but explicitly assumes the provider response instead of citing historical source evidence. |
| 7.4 | PASS | e119.0 and e134.0 flag the current increment's delivery-contract violation; pending Task 2 neither excuses it nor receives a missing-implementation finding. |
| 7.5 | FAIL | e75.0 tells the named reviewer historical source cannot be read; no materialization/provenance appears, and e134.0 confirms PAL never ran. |
| 7.6 | FAIL | e119.0 bases the comparison on an “unverified assumption”; e134.0 confirms no PAL result or historical-source receipt. |
| 7.7 | FAIL | e119.0 gives REQUEST_CHANGES, but neither that result nor e134.0 marks the required combination Blocked; historical source remains uninspected. |
| 7.8 | PASS | e134.0 proposes accepting `ok: True` without `applied` and testing disabled saves against the released response; green receipt-only mocks are identified as inadequate. |

**Summary**: 2 PASS / 6 FAIL / 0 PARTIAL of 8 assertions; no grader-material access was observed.

Controller note: PAL is user-deferred. The historical-source and named-reviewer
failures remain separate observed limitations; no assertion is waived.
