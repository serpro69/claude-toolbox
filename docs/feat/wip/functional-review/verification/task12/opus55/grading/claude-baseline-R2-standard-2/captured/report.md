## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 16 lines changed (staged)
**Profiles**: `python` (activated by the `.py` extension). Checklists used: security, SOLID, code-quality and removal-plan.
**Overall assessment**: **REQUEST_CHANGES**

The existing tests still pass (3/3), but they don't cover the two cases that break. I reproduced both bugs against the real `Store`. The change conflicts with the save contract in `README.md` on three points: retries must apply the latest values, a new operation ID must do a fresh save, and recovery records must stay available for audit.

---

## Findings

### P0 - Critical

- **[service.py:2-3]** Recovery record is looked up by workspace instead of operation ID, so a new save on the same workspace silently does nothing
  - Profile: python · Checklist: security-checklist.md (Data Integrity) · Triggered by: content — `.py` extension
  - `next(... if item["workspace"] == workspace)` matches any earlier record for that workspace. Once a workspace has one completed save, every later save with a new operation ID finds that old record. It skips `apply`, never stores the new operation ID, and still returns `{"ok": True, "operation_id": <new id>}`. When a workspace has several records, `next()` picks the oldest. It also breaks the audit trail, because new operation IDs never reach `store.recovery`.
  - Repro: `submit(s,"w","op-1",{"color":"blue"})`, then `submit(s,"w","op-2",{"color":"red"})` returns `ok: True`, but preferences stay `{'color': 'blue'}` and `recovery` holds only `['op-1']`.
  - Confidence: 98%. Confirmed by running it; the README says "A fresh operation ID must perform a fresh save, even for the same workspace."
  - Fix: key the lookup on `store.recovery.get(operation_id)`, as before.

- **[service.py:6-10]** A retry applies the first values it was given, not the edited ones
  - Profile: python · Checklist: security-checklist.md (Data Integrity) · Triggered by: content — `.py` extension
  - `values` is only stored when the record is created, and `apply` only runs while the status is `"pending"`. After a receipt failure the status is `"applied"`, so a retry with edited values skips `apply` completely. Even a `"pending"` retry would replay `record["values"]` from the first attempt. Either way the call reports success while the old values are live.
  - Repro: the first submit with `{"color":"blue"}` raises `ReceiptUnavailable`; the retry with `{"color":"green"}` returns `ok`, but preferences are still `{'color': 'blue'}`.
  - Confidence: 97%. Confirmed by running it; the README says "can be retried with the same ID and edited values; success means the latest submitted values are active." The provider is documented as idempotent, so re-applying on retry is safe and is what the contract expects.
  - Fix: on any non-completed record, set `record["values"] = dict(values)` and always call `store.apply`.

### P2 - Medium

- **[service.py:11-12]** A repeated completed ID now calls `store.receipt` again, and the receipt's return value is dropped
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling) · Triggered by: content — `.py` extension
  - The short-circuit for completed records was removed. Repeating an operation that already finished now writes the receipt again, so it can raise `ReceiptUnavailable` even though nothing is left to do. The function also ignores what `store.receipt` returns and builds its own response. After the P0 above, that response can carry an operation ID that doesn't match the record that was used.
  - Confidence: 80%. The behaviour is clear from the code; how much it matters depends on how expensive or fallible real receipt writes are.
  - Fix: bring back the early return for `status == "completed"` and `return store.receipt(record)`.

- **[tests/test_save.py]** Missing tests for the two broken cases
  - Profile: generic · Checklist: — · Triggered by: —
  - Add (a) a new operation ID on the same workspace with different values, which should apply them and create a second recovery record, and (b) a receipt failure followed by a retry with edited values, which should leave the edited values active.
  - Confidence: 95%.

### P3 - Low

- **[service.py:2-3]** Every save scans all recovery records (O(n)), and records are kept forever for audit. This goes away once the lookup uses the operation ID as the dict key.

---

## Suggested shape

```python
def save(store, workspace, operation_id, values):
    record = store.recovery.get(operation_id)
    if record is not None and record["status"] == "completed":
        return {"ok": True, "operation_id": operation_id}
    if record is None:
        record = {"operation_id": operation_id, "workspace": workspace,
                  "status": "pending"}
        store.recovery[operation_id] = record
    record["values"] = dict(values)
    store.apply(workspace, record["values"])
    record["status"] = "applied"
    return store.receipt(record)
```

This is essentially the pre-change code, which already met the README contract. If the update was meant to fix a specific recovery problem, tell me what it was and I'll check that the fix covers it without these regressions.

**Indexing:** the "lookup by natural key instead of operation ID" pattern is now indexed as `kk:review-findings`. The knowledge base was empty, so there were no earlier findings to compare against.

---

## Next Steps

I found 5 issues (P0: 2, P1: 0, P2: 2, P3: 1).

What I recommend fixing:
1. P0: look up the recovery record by `operation_id`
2. P0: store and apply the latest `values` on every retry that hasn't completed
3. P2: bring back the early return for completed records and return the receipt from `store.receipt`
4. P2: add the two regression tests

The P3 goes away with fix 1.

**How would you like to proceed?**

1. **Fix all**: I'll implement all the fixes above
2. **Fix P0/P1 only**: only the critical and high-priority issues
3. **Fix specific items**: tell me which ones
4. **No changes**: the review is done and nothing needs implementing
