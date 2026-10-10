## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 16 lines changed (8+/8−)
**Overall assessment**: **REQUEST_CHANGES**

The change rewrites the idempotent `save` recovery path. Its central move — switching the recovery lookup from a keyed read on `operation_id` to a linear scan matching `workspace` — introduces a silent data-loss bug. Capy knowledge base is empty (cold start); findings below are from the Python review checklists + general guidance.

---

## Findings

### P0 - Critical

- **[service.py:2-11]** New `values` are silently dropped once any record exists for the workspace (lost update)
  - Profile: python · Checklist: security-checklist.md (Data Integrity / Lost updates) + code-quality-checklist.md (Boundary Conditions)
  - Triggered by: content — `.py` extension
  - The lookup now scans `store.recovery.values()` for the first record whose `workspace` matches, instead of fetching by `operation_id`. On any call where a record already exists for that workspace:
    - `record` is non-`None`, so the create branch is skipped and the caller's `values` are **never stored**.
    - `record["status"]` is already `"applied"` (or `"completed"`), so `if record["status"] == "pending"` is false and `store.apply` is **never called** — not even with the stale stored values.
    - The function still returns `{"ok": True, ...}`.

    Trace: `save(store,"w","op1",{"a":1})` applies `{a:1}`. A later `save(store,"w","op2",{"a":2})` finds op1's record, applies nothing, and returns success — `{a:2}` is lost with no error. This is silent data loss on a data-write path, the most severe class.
  - Confidence: 90% — the logic is unambiguous from the diff; the only uncertainty is whether "first-write-wins per workspace" is the *intended* recovery semantic. Even if it is, returning success while discarding the caller's input without any signal is unsafe.
  - Suggested fix: Key the lookup on the idempotency key: `record = store.recovery.get(operation_id)`. If recovery must be workspace-scoped by design, detect the new-values case and either reject it or re-apply explicitly, rather than returning `ok` silently.

- **[service.py:2-12]** Idempotency key narrowed to `workspace`; distinct operations collide and the response is inconsistent with persisted state
  - Profile: python · Checklist: security-checklist.md (Data Integrity / idempotency)
  - Triggered by: content — `.py` extension
  - `store.recovery` is keyed by `operation_id`, but lookups now match on `workspace`. Two different `operation_id`s on the same workspace resolve to the *same* record. New records are still stored under `store.recovery[operation_id]`, so the dict key becomes vestigial. The function returns `{"operation_id": operation_id}` (the caller's id) while the persisted record carries a *different* `operation_id` — the returned id does not correspond to any stored record. Callers using the returned id to look up status later will get nothing.
  - Confidence: 85% — depends on the intended contract, but the key/return mismatch is objectively inconsistent.
  - Suggested fix: Decide the idempotency unit. If it is the operation, lookup and return must both use `operation_id`. If it is the workspace, store under `workspace` and return the stored record's id.

### P1 - High

- **[service.py:11-12]** Receipt return value discarded — silent contract change
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling / return contract)
  - Triggered by: content — `.py` extension
  - Old code returned `store.receipt(record)` (the actual receipt). New code calls `store.receipt(record)` for its side effect and returns a hardcoded `{"ok": True, "operation_id": operation_id}`. Any caller that consumed receipt fields now receives a generic stub. If `receipt` is pure (no side effects), this is also a now-useless call.
  - Confidence: 70% — can't see callers; the regression is real if any caller reads receipt data.
  - Suggested fix: `return store.receipt(record)`, or confirm callers no longer need it and drop the call.

### P2 - Medium

- **[service.py:8-10]** Removed terminal `"completed"` short-circuit changes finished-operation behavior
  - Profile: python · Checklist: security-checklist.md (idempotency)
  - Triggered by: content — `.py` extension
  - The old guard returned early for `status == "completed"`. Now a `"completed"` record skips `apply` (good) but still runs `store.receipt(record)` on every call, re-emitting receipts for already-finished operations. If `receipt` has side effects (emits an event, charges, notifies), this is a duplicate-side-effect bug and should be P1.
  - Confidence: 55% — hinges on whether `receipt` is idempotent.
  - Suggested fix: Restore the terminal-state short-circuit, or make `receipt` provably side-effect-free.

- **[service.py:2-3]** O(1) keyed lookup replaced by O(n) scan over an unbounded dict
  - Profile: python · Checklist: code-quality-checklist.md (Performance / Memory — unbounded collections)
  - Triggered by: content — `.py` extension
  - `store.recovery` grows over time (recovery records). Scanning `.values()` on every `save` is linear per call. Combined with no eviction, this degrades as the dict grows.
  - Confidence: 75%.
  - Suggested fix: Keep the keyed `.get(operation_id)` access, or maintain a workspace index if workspace lookup is genuinely required.

- **[service.py:3]** `item["workspace"]` assumes every recovery record has the key (KeyError risk)
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / None & missing keys)
  - Triggered by: content — `.py` extension
  - The generator indexes `item["workspace"]` for every record in the store. A single legacy/partial record lacking `"workspace"` raises `KeyError` and fails the whole `save`.
  - Confidence: 60% — depends on whether all records are guaranteed to have the key.
  - Suggested fix: `item.get("workspace") == workspace`.

- **[service.py:2-7]** Check-then-act race on `store.recovery` widened by the scan
  - Profile: python · Checklist: security-checklist.md (Race Conditions / TOCTOU)
  - Triggered by: content — `.py` extension
  - Scan-for-existing then conditionally insert is non-atomic. Two concurrent calls for the same workspace can both see `None`, both create records, and both call `apply`. The pre-existing code had a similar window, but the workspace scan widens it (any in-flight op for the workspace, not just the same key).
  - Confidence: 55% — concurrency model of `store` is unknown.
  - Suggested fix: Use an atomic upsert / lock around the check-and-insert if concurrent saves are possible.

### P3 - Low

- None beyond the above.

---

## Additional Suggestions

The cleanest reconciliation of P0 findings is likely: `record = store.recovery.get(operation_id)`, keep the `"completed"`/terminal short-circuit, apply the *caller's* `values` for genuinely new/pending operations, and return the real receipt. That preserves idempotency per `operation_id` without the lost-update and response-inconsistency bugs.

---

## Next Steps

I found 6 issues (P0: 2, P1: 1, P2: 3, P3: 0). The P0 lost-update finding was indexed as `kk:review-findings`.

The actionable items I recommend fixing:
1. **P0** — Restore `operation_id`-keyed lookup so new `values` aren't silently dropped (service.py:2-11).
2. **P0** — Align the idempotency key and the returned `operation_id` with the persisted record (service.py:2-12).
3. **P1** — Return the actual `store.receipt(record)` or confirm callers don't need it (service.py:11-12).
4. **P2** — Restore terminal-state handling; avoid O(n) scan; guard `item["workspace"]`; address the TOCTOU window.

Items that may be intentional (need your confirmation):
- If "first-write-wins per workspace" is the deliberate recovery semantic, the workspace scan is by design — but it must not return `ok` while silently discarding new input.

**How would you like to proceed?**

1. **Fix all** — implement all suggested fixes
2. **Fix P0/P1 only** — address critical and high priority issues
3. **Fix specific items** — tell me which issues to fix
4. **No changes** — review complete, no implementation needed

Please choose an option or clarify the intended recovery semantics (operation-keyed vs workspace-keyed), which determines the correct fix.
