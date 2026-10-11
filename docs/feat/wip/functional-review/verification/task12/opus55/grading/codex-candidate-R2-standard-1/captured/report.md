I’m using `kk:review-code` to review the staged save recovery update and trace its affected save and recovery flows.

The staged scope is one Python file, with 8 additions and 8 deletions. I’ve loaded the common review instructions and all four Python checklists; the other seven profiles do not match. Preparation is complete, and I’m moving on to the save contract and recovery behavior.

The existing three tests pass, but the documented recovery scenarios expose regressions: an edited retry reports success while keeping the old values, and a fresh operation ID reuses the previous save instead of applying new values. I also reproduced a completed-ID replay failing when receipt storage is unavailable. All three behaviors work on `HEAD`; I’m finishing the checks and recording the findings.

**REQUEST_CHANGES** — three regressions in the staged `service.py` update.

Reviewed the index against `HEAD` (`feeb199a`): one changed file, 8 additions and 8 deletions. Requirements come from [README.md](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-1/README.md:5); no separate task scope exists.

1. **P1 — Fresh operation IDs silently skip saving.** [service.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-1/service.py:2) selects recovery records by workspace. After `op-1` completes, submitting changed values as `op-2` reuses that completed record, leaves preferences unchanged, creates no `op-2` audit record, and returns success for `op-2`. Restore lookup by operation ID while retaining completed records for audit.

2. **P1 — Edited retries acknowledge stale values.** [service.py:8](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-1/service.py:8) only applies values while pending. A receipt failure leaves the record `applied`; retrying blue → green with the same ID skips replacement and returns success with blue still active. For incomplete operations, apply and record the latest submitted values before completing. Preserve the completed-ID fast path.

3. **P2 — Completed-ID replay can now fail.** [service.py:11](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-1/service.py:11) calls receipt persistence even for completed records. Completing an operation, setting `fail_receipt_once`, then repeating its ID raises `ReceiptUnavailable` instead of returning its receipt. Restore the early return for completed operations.

Confidence is **100% within the supplied store model**: all three regressions were reproduced through unchanged `client.submit`; the corresponding scenarios succeed on `HEAD`. Findings 1–2 use the Python security/data-integrity checklist; finding 3 uses its error-handling checklist. The profile trigger is `service.py`’s `.py` extension.

Both revisions pass all **3 existing tests**. Additional lifecycle checks show:

| Scenario | Staged result |
|---|---|
| Initial save; receipt failure after applying; unchanged retry | Supported |
| Completed replay with receipt storage available | Supported; values remain unchanged |
| Edited retry after receipt failure | Blocked; stale values become completed |
| Fresh ID after ordinary or recovered completion | Blocked; save skipped |
| Completed replay during receipt failure | Blocked; raises |

Coverage included the full staged file, baseline implementation, caller, store, contract, and tests. Evidence covers the documented serialized, in-memory behavior; concurrency, restart, and external services are outside that contract.

The two systemic P1 findings were indexed as `kk:review-findings`. No repository files were changed.
