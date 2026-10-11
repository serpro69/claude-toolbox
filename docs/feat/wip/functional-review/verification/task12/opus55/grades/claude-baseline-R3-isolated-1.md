Grader: `/root/grade55_claude_b_r3_i1`; fresh eval-grader role, workflow mode.
Manifest: `fe1b55f0ac63ce2f0a9c9441df8d35c9947a00f59978da8c4be86b22176ff818`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main reads design at e43.0 and the full diff at e69.0 without loading resolved checklists; the child correctly loads all four before e117.0. |
| 7.2 | PASS | e81.0 identifies the repository's release contract; e86.0/e89.0 retrieve `eval-release:provider/settings.py`, distinct from the staged client and undeployed candidate. |
| 7.3 | PASS | e160.0 traces values stored, `{"ok": True}` without `applied`, and the unconditional acknowledgement check raising regardless of `enhanced_settings`. |
| 7.4 | PASS | e160.0 identifies the current compatibility break and says pending Task 2 cannot change the baseline; Task 2 is excluded from missing-implementation findings. |
| 7.5 | FAIL | e94.0 confirms external materialization and e123.0 confirms named-reviewer receipt; e96.0 lacks full revision/hash/span provenance, and e95.0 explicitly skips PAL. |
| 7.6 | FAIL | e123.0 and e145.0 link named-reviewer receipt and comparison; e95.0/e160.0 confirm PAL never ran, leaving no second independent result. |
| 7.7 | FAIL | e145.0 states `REQUEST_CHANGES`, but e160.0 and `captured/report.md` omit the required `Blocked` compatibility status. |
| 7.8 | PASS | e160.0 proposes accepting missing legacy receipts or gating strictness on provider capabilities and retaining released-provider tests; receipt-only mocks are identified as hiding the break. |

**Summary**: 4 PASS / 4 FAIL / 0 PARTIAL of 8 assertions; no actor access to grading material was observed.

Controller note: PAL was user-deferred. Assertions 7.5/7.6 retain that missing
component; 7.5 also fails named-reviewer provenance requirements independently.
