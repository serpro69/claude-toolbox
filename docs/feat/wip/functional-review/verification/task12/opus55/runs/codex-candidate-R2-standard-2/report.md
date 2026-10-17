I’m using the `kk:review-code` skill to review the staged save recovery update. I’ll load its review guidance, then trace the changes and relevant recovery flows.

Preparation is complete. The staged diff changes only `service.py` (8 additions, 8 deletions). All eight profile rules were checked; only Python applies. I’ve read all six common instruction parts, the Python index, and both checklist parts covering security, SOLID, code quality, and removal guidance.

The three existing tests pass, but comparison with `HEAD` reproduced two false-success cases: an edited retry leaves the old values active, and a fresh operation ID reuses the workspace’s old record without saving. I also reproduced a completed operation raising a receipt-write error when repeated. All three conflict with the README contract.

**REQUEST_CHANGES** — two P1 regressions and one P2 regression.

Reviewed the staged `service.py` change (8 additions, 8 deletions) against `HEAD` (`feeb199`), using the README’s save/recovery contract.

1. **P1 — Fresh operation IDs silently skip saving.** [service.py:2](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-2/service.py:2)  
   Looking up records by workspace reuses an earlier operation’s retained record. After saving blue with `op-1`, saving green with `op-2` returns success but leaves blue active and creates no `op-2` audit record. Restore lookup by operation ID. **Confidence: 100%; reproduced.**

2. **P1 — Edited retries acknowledge values that were never applied.** [service.py:8](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-2/service.py:8)  
   When the receipt fails after applying blue, the record remains `applied`. Retrying that ID with green skips application, completes the receipt, and returns success while blue remains active. Apply the latest submitted values for unfinished operations and update the recovery payload accordingly, preserving the completed-operation shortcut. **Confidence: 100%; reproduced.**

3. **P2 — Completed-operation replay can now fail.** [service.py:11](/tmp/fr-opus55-matrix-20261011/codex-candidate-R2-standard-2/service.py:11)  
   Repeating a completed ID unconditionally calls the fallible receipt writer. With `fail_receipt_once` set, replay raises `ReceiptUnavailable`; `HEAD` returns the completed receipt successfully. Restore the early return for completed IDs. **Confidence: 100%; reproduced.**

All findings apply the Python security/reliability checklist, triggered by `service.py`’s `.py` extension.

**Verification:** All three existing tests pass on both revisions. Additional checks through the unchanged client reproduced these regressions only in the staged candidate. Initial saves, unchanged-value retries, ordinary completed replay, and separate-workspace saves remain supported. Edited retries, fresh IDs for existing workspaces, and completed replay during receipt failure are blocked.

Coverage is limited to the documented serialized, in-memory model; concurrency, restart, and external deployment guarantees are outside that contract. The two P1 patterns were indexed as `kk:review-findings`. No repository files were changed.
