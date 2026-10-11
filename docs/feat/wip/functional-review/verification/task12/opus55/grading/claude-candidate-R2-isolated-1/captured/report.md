## Review Summary (Isolated Mode)

**Overall assessment: REQUEST_CHANGES.** The staged change breaks two explicit README rules: a new operation ID must do a new save, and a retry may change the values. In both cases it reports success without applying the new values.

**Reviewers**: one of the two ran.
- The `kk:code-reviewer` subagent completed. It read the diff, `service.py`, `store.py`, `client.py`, the tests and `README.md`.
- **PAL didn't run.** Its server failed to connect this session. So nothing here is confirmed by two reviewers; reconnect PAL and re-run if you want the second opinion.

**Files reviewed**: `service.py`, staged (+8/−8), plus the unchanged `store.py`, `client.py` and `tests/test_save.py`.
**Intent and scope**: The rules come from `README.md`. There are no design or task docs, so I took the purpose ("save recovery update") from your description and the diff. Reviewed: staged changes only (there were no unstaged ones).
**Baselines**: Compared against HEAD `feeb199`. The whole old version of `service.py` (12 lines) is in the diff. Compatibility with older data doesn't apply because the store is in-memory and nothing survives a restart.

### Behavior and Compatibility

| README rule / scenario | Before | Staged | Conclusion |
|---|---|---|---|
| First save | correct | correct | Supported |
| New ID on the same workspace (op-1 blue done, then op-2 red) | red | **stays blue, success returned for op-2** | Blocked |
| Retry the same ID with edited values after the receipt failed | red | **stays blue, success returned** | Blocked |
| Retry the same ID with the same values | correct | correct | Supported |
| Repeat a completed ID | returns its receipt | correct, unless the receipt store is down, then it raises | Blocked during a receipt outage |
| Records kept for audit | kept | op-2 never gets a record; reusing an ID on another workspace overwrites the old record | Blocked |
| Concurrency, older data | — | — | Not applicable (no threads, in-memory) |

**Tests weren't run.** Shell commands were denied in this session, so every conclusion comes from reading the code. By that reading, all three existing tests still pass on the staged code. None of them covers a new ID on the same workspace, a retry with edited values, or a receipt outage.

### Code Reviewer Findings

**P1. `service.py:2-3` looks up the record by workspace instead of operation ID** (confidence 97%)
- **What happens:** once a workspace has any record, every later save to it reuses that record. The apply step is skipped because the record is already completed, yet the caller gets `{"ok": True, "operation_id": "op-2"}`. That workspace's preferences can never change again.
- **Side effects of the same cause:**
  - The receipt is written for op-1 while the response names op-2.
  - Reusing an operation ID for a different workspace overwrites the old record (line 7), which loses audit history.
  - Every save scans all records, and that set only grows.
- **Fix:** go back to `store.recovery.get(operation_id)` and return what `store.receipt(record)` returns.

**P1. `service.py:5-10` ignores edited values on retry** (confidence 95%)
- **What happens:** when the receipt fails, the record is left as `applied`. On retry the apply step is skipped and the new `values` are never read, so the old values stay active and the success response is wrong.
- This is a separate bug: it remains even after the lookup is fixed.
- **Fix:** on every attempt that hasn't completed, store `dict(values)` on the record and apply it before writing the receipt. The provider is idempotent, so re-applying is safe.

**P2. `service.py:11` repeating a completed ID writes the receipt again** (confidence 80%)
- **What happens:** the old code returned early for a completed ID. Now, if the receipt store is unavailable, repeating an operation that already succeeded raises `ReceiptUnavailable`.
- **Fix:** restore the early return for completed records.

The reviewer's simplest fix is to revert to the old version and keep one improvement: store the values on the record before applying them. By its trace, that passes every row in the table. The security, SOLID and dead-code checks found nothing.

### Outstanding Evidence
- **Run the tests:** `python3 -B -m unittest discover -s tests` once a fix is in.
- **Missing tests:** a new ID on the same workspace, a retry with edited values, a completed repeat during a receipt outage, and records kept per operation.

### Housekeeping
- Both P1 patterns are saved in the knowledge base as `kk:review-findings`. This repo's `.capy.toml` points that store at `.runner/knowledge.db`.
- **Temp files weren't deleted:** the delete command was denied. Remove them with `rm -r /tmp/kk-review-code-save-recovery-20261011 /tmp/kk-review-instructions-9ic79q2h /tmp/kk-review-instructions-usrp1u17 /tmp/kk-review-instructions-760_e1z8`.

This was a review only; I haven't edited anything. Should I apply the fix and add the four tests?
