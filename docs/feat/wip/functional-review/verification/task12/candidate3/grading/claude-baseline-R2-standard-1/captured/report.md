## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 16 lines changed (8 insertions, 8 deletions)
**Overall assessment**: **REQUEST_CHANGES**

The change makes one legitimate improvement (persist `values` into the recovery record *before* `apply`, guarded by `status == "pending"`, so a crash between apply and receipt can be recovered on retry). But it also changed the record lookup from the operation_id key to a workspace scan, which introduces a critical silent-data-loss bug.

---

## Findings

### P0 - Critical

- **[service.py:2-3]** Recovery lookup scans by `workspace` instead of the `operation_id` key → every operation after the first per workspace is silently dropped
  - Profile: python · Checklist: security-checklist.md (Data Integrity / Race Conditions), code-quality-checklist.md (Boundary Conditions)
  - Triggered by: content — `.py` extension
  - Records are *written* keyed by `operation_id` (`store.recovery[operation_id] = record`, line 7) but *read* by scanning `.values()` for the first matching `workspace` (lines 2-3). Trace with two distinct operations on the same workspace:
    1. `save(store, "W", "A", V1)` → no record → create `pending`, `apply("W", V1)`, mark `applied`, `receipt` marks `completed`. `preferences["W"] == V1`.
    2. `save(store, "W", "B", V2)` → the scan finds record **A** (status `completed`), so `record is None` is false (B is never stored), `status != "pending"` so **`apply` is skipped**, and the function returns `{"ok": True, "operation_id": "B"}`.
  - **Result:** `V2` is never applied (`preferences["W"]` stays `V1`), operation `B` is never recorded, yet the caller is told it succeeded. The `values` and `operation_id` arguments are effectively ignored for any workspace that already has a record. The old code keyed on `operation_id` via `store.recovery.get(operation_id)`, so each operation was independent and applied correctly.
  - `store.py` confirms the intent: `apply` writes per-workspace prefs and `fail_receipt_once` simulates a `receipt` failure — i.e. recovery is about **retrying the same `operation_id`** after a receipt failure, not about one-record-per-workspace.
  - Confidence: 95% — Verified against `store.py`. The write-key/read-field mismatch is internally contradictory; the only reading under which it's "correct" is a one-op-per-workspace guarantee, which contradicts the function accepting per-call `operation_id` + `values` and keying storage by `operation_id`.
  - Suggested fix: revert the lookup to the key, keeping the recovery reorder:
    ```python
    def save(store, workspace, operation_id, values):
        record = store.recovery.get(operation_id)
        if record is None:
            record = {"operation_id": operation_id, "workspace": workspace,
                      "status": "pending", "values": dict(values)}
            store.recovery[operation_id] = record
        if record["status"] == "pending":
            store.apply(workspace, record["values"])
            record["status"] = "applied"
        return store.receipt(record)
    ```

::code-comment{file="service.py" line="2" severity="P0"}
Lookup scans `store.recovery.values()` by `workspace`, but records are keyed by `operation_id`. Once any record exists for a workspace, a later `save` with a different `operation_id`/`values` matches the stale record, skips `store.apply` (status != "pending"), and returns `{"ok": True}` — silently dropping the operation and its values. Use `store.recovery.get(operation_id)` instead.
::

### P1 - High

- **[service.py:11-12]** `store.receipt(record)` return value discarded; hardcoded response built from the parameter `operation_id`
  - Profile: generic · Checklist: —
  - The old code did `return store.receipt(record)`. `receipt` returns `{"ok": True, "operation_id": record["operation_id"]}` and marks the record `completed`. The new code discards that return and rebuilds a dict from the *parameter* `operation_id`. In the happy path these match, but combined with the P0 bug this actively **masks** the mismatch: in the scenario above it returns `operation_id "B"` while the record/receipt that actually ran belongs to operation `"A"`. It also discards any future enrichment of the receipt contract.
  - Confidence: 80% — Behavioral change is certain; impact is partly contingent on the P0 bug. Fixing the P0 lookup and restoring `return store.receipt(record)` resolves both.
  - Suggested fix: `return store.receipt(record)` (as in the P0 fix block).

### P2 - Medium

- **[service.py:2-3]** O(n) linear scan replaces O(1) dict lookup on every call
  - Profile: python · Checklist: code-quality-checklist.md (Performance)
  - `next(item for item in store.recovery.values() if ...)` is O(n) over all recovery records per call; `store.recovery` is never pruned, so this degrades as recovery history grows. Same root cause and same fix as the P0 (`.get(operation_id)` restores O(1)).
  - Confidence: 90%.

### P3 - Low

- **[service.py:9]** `record["values"]` / `item["workspace"]` assume keys exist
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions)
  - Records created by this code always carry both keys, so this is safe in the current fixture. But any record written in a different shape (older format, external writer) would raise `KeyError` in the scan or at apply. Low priority given the isolated fixture; noted for robustness.
  - Confidence: 55%.

- **[service.py:2-10]** Check-then-act (TOCTOU) under concurrency
  - Profile: python · Checklist: security-checklist.md (Race Conditions)
  - Two concurrent `save` calls for the same workspace can both see "no record" and both create records / double-apply. No locking anywhere and the fixture is single-threaded, and the old code had an equivalent get-then-set window, so this is pre-existing rather than a regression. Flagging only for awareness.
  - Confidence: 45%.

---

## Additional Suggestions

- The recovery reorder itself is a good change — keep it. The clean version is exactly the P0 fix block above: it preserves crash recovery (values persisted before `apply`; `pending` guard prevents double-apply on retry) *and* restores per-operation idempotency.
- Consider a test matrix against `store.py`: (a) two distinct operations on one workspace both apply; (b) retry after `fail_receipt_once` applies once and completes on retry; (c) same `operation_id` retried does not double-apply.

---

## Next Steps

I found 5 issues (P0: 1, P1: 1, P2: 1, P3: 2).

The actionable items I recommend fixing — all resolved by the single P0 fix block:
1. **P0** — look up by `operation_id` (`store.recovery.get(operation_id)`) instead of scanning by `workspace`; stops silent data loss.
2. **P1** — `return store.receipt(record)` instead of the hardcoded dict; restores the receipt contract and removes the op_id mismatch.
3. **P2** — same change restores O(1) lookup.

Items I recommend keeping as-is:
- The recovery reorder (store `values` before `apply`, `pending`-guarded apply): correct behavior — it's the legitimate improvement this change was for.
- **P3 KeyError / TOCTOU**: low priority — safe in the current fixture; TOCTOU is pre-existing, not introduced here.

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes
2. **Fix P0/P1 only** — Address critical and high priority issues (single edit covers both)
3. **Fix specific items** — Tell me which issues to fix
4. **No changes** — Review complete, no implementation needed

Please choose an option or provide specific instructions. (Note: the P0 pattern — store written by key, read by scanning a non-key field — has been indexed to `kk:review-findings` for future reviews.)
