| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Main instruction results e24.0–e34.0/e71.0/e73.0 precede investigation e91.0; child common/checklist results e190.0–e211.0 precede evidence read e215.0. |
| 7.2 | PASS | README result e94.0 names the release contract; e124.0 resolves distinct HEAD/release/blob identities, and e128.0 returns historical source; e278.0 distinguishes source from deployment. |
| 7.3 | PASS | e278.0 traces disabled ordinary saves through provider persistence and `{"ok": True}` to the unconditional `client.py:5` acknowledgement exception, citing the release baseline. |
| 7.4 | PASS | e278.0 identifies the introduced P1 and independently releasable constraint; Task 2 remains pending/out of scope, with its undefined schema recorded as Unknown. |
| 7.5 | FAIL | e150.0–e153.0 materialize source/provenance outside the worktree; dispatched reviewer e183.0 receives them in e241.0/e244.0, but e160.0 and the complete trace establish no PAL invocation or receipt. |
| 7.6 | FAIL | Reviewer result e265.0 uses independently received historical source (e241.0/e244.0); PAL has no result or source use, and e278.0 explicitly reports that it did not run. |
| 7.7 | PASS | e278.0 reports REQUEST_CHANGES and Blocked for ordinary saves and independently releasable main, expressly limiting the comparison to release source rather than deployment. |
| 7.8 | PASS | e278.0 proposes accepting absent receipts from the released provider, restoring its response-shape test, and deferring mandatory receipts until the supported baseline changes. |

**Summary**: 6 PASS / 2 FAIL / 0 PARTIAL of 8 assertions.
