Finding indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 16 lines changed (8 insertions, 8 deletions)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: "Save recovery update" — an idempotent `save(store, workspace, operation_id, values)` that persists a workspace's preferences, records the operation for crash/retry recovery, and issues a receipt. Inferred intent (no design doc present): capture the operation's `values` in the recovery record so a retry after a receipt failure can resume. No `docs/feat/wip/` directory relates to this diff → **no task scope available**; reviewed on its own merits.
**Baselines**: Review base = `HEAD` (feeb199 `service.py`); candidate = staged (index) blob. No separate deployed baseline inspected or claimed.

## Behavior and Compatibility

I traced both revisions against the actual `store.py` contract (`recovery` dict keyed by `operation_id`; `apply` writes `preferences[workspace]`; `receipt` flips status to `completed`, can raise `ReceiptUnavailable` once) and the `client.submit` caller / `tests/test_save.py`.

- **Tests**: all three pass under the staged code — but every test reuses the **same** `workspace` + `operation_id` + `values`. The behavioral change (lookup by `workspace` instead of `operation_id`) is **not exercised by any test**. Green tests here do not demonstrate a correct save. (Verified by tracing each test by hand.)
- **Single operation / same-id retry** (what tests cover): Supported.
- **Second distinct operation on the same workspace** (new `operation_id` and/or new `values`): **Blocked** — silent data loss (P0 below).
- **Idempotent retry of an already-completed op during a transient receipt outage**: **Blocked/regressed** (P1 below).

---

## Findings

### P0 - Critical

- **[service.py:2-3]** Existing-record lookup changed from the idempotency key to `workspace` → silent data loss
  - Profile: python · Checklist: code-quality-checklist.md (Data Integrity / boundary), functional-review.md
  - Triggered by: content — `.py` extension (python profile)
  - **Trigger/path**: The lookup became `next((item for item in store.recovery.values() if item["workspace"] == workspace), None)` instead of `store.recovery.get(operation_id)`. `store.recovery` is keyed by `operation_id`, so any *new* operation on a workspace that already has a record resolves to the **first** stored record.
  - **Scenario**: `save(store,"w","op-1",{"color":"blue"})` then `save(store,"w","op-2",{"color":"red"})`.
    - Expected: `preferences["w"] == {"color":"red"}`, `recovery` tracks `op-2`.
    - Actual: lookup finds the completed `op-1` record → `record` is not `None` so `op-2` is **never inserted** into `recovery`; `record["status"]` is `completed` (not `pending`) so `store.apply` is **skipped** → `preferences["w"]` stays `{"color":"blue"}`. The new values are dropped and the function still returns `{"ok": True, "operation_id": "op-2"}`.
  - **Consequence**: Caller is told `op-2` succeeded while the write was silently discarded and untracked. The function cannot update a workspace more than once. This defeats the primary purpose of `save`.
  - Confidence: 97% — direct code trace against the real `store.py`; the only uncertainty is whether per-workspace single-record semantics were somehow intended, but even then silently returning `ok:True` for a dropped write is a defect, and keying `recovery` by `operation_id` contradicts that interpretation.
  - **Suggested fix**: Restore key-based lookup: `record = store.recovery.get(operation_id)`. If values must be refreshed on an existing pending record, apply the incoming `values` (see related note below) rather than only `record["values"]`.

### P1 - High

- **[service.py:10]** Removing the `completed` short-circuit re-invokes `receipt` on already-completed operations
  - Profile: python · Checklist: security-checklist.md (Data Integrity / idempotency), functional-review.md
  - Triggered by: content — `.py` extension (python profile)
  - **Trigger/path**: The base returned early when `record["status"] == "completed"`, never calling `apply`/`receipt` again. The candidate drops that guard and always calls `store.receipt(record)`.
  - **Scenario**: op-1 completes; later `store.fail_receipt_once` is set (a transient receipt outage) and the client retries the already-durable op-1. New code calls `receipt` again → raises `ReceiptUnavailable`; base code returned `{"ok": True, ...}` without touching the receipt store.
  - **Consequence**: A benign idempotent retry of a fully-completed operation can now surface a transient downstream error — exactly the robustness the recovery record was meant to provide. Not covered by tests (`fail_receipt_once` is false in `test_completed_id_returns_receipt`).
  - Confidence: 80% — code trace is certain; severity assumes the transient-failure-on-retry path is reachable in this recovery-oriented domain, which is plausible but not proven from a doc.
  - **Suggested fix**: Re-add an early return when `record["status"] == "completed"` (keyed by `operation_id`), before calling `receipt`.

### P2 - Medium

- **[service.py:11]** Response hardcodes `operation_id` and discards `store.receipt(record)`'s return
  - Profile: generic · Checklist: —
  - Triggered by: —
  - **Trigger/path**: Base returned `store.receipt(record)` (whose `operation_id` is `record["operation_id"]`); candidate ignores that return and builds `{"ok": True, "operation_id": operation_id}` from the passed argument.
  - **Consequence**: When the acted-on record differs from the passed id (the P0 scenario), the response claims `op-2` while `receipt` actually completed `op-1`'s record — an internally inconsistent receipt. Independently, it duplicates `store.receipt`'s response contract (coupling/DIP smell): a future change to receipt's shape won't be reflected here.
  - Confidence: 70% — correct as a consistency/coupling observation; its user-visible impact is mostly a symptom of the P0.
  - **Suggested fix**: Return the value from `store.receipt(record)`; once lookup is key-correct, `record["operation_id"]` and `operation_id` coincide.

### P3 - Low

- **[service.py:8-9]** The `values` parameter is now dead on every existing-record path — `apply` uses `record["values"]`, and new `values` are only captured at first creation. Even with the P0 fixed, decide explicitly whether a retry should re-apply the originally-stored values (recovery semantics) or the caller's latest `values`; the current code silently chooses the former for pending records and neither for applied/completed ones.

---

## Removal/Iteration Plan

Not applicable — no code being retired.

## Areas Not Covered / Residual Risk

- **Test gap**: no test exercises two distinct `operation_id`s, differing `values` on the same workspace, or a transient receipt failure on an already-completed op. I recommend adding those before merge — they fail with the current code and would have caught the P0/P1.
- I did not execute the tests (source-trace only) and there are no migrations, concurrency primitives, or external I/O beyond the in-memory `Store` to assess. Thread-safety of `store.recovery` is out of scope for this diff (pre-existing, single-threaded test usage).

**Indexed**: the P0 (wrong-field idempotency lookup → silent data loss) as a systemic pattern under `kk:review-findings`.

---

## Next Steps

I found 4 issues (P0: 1, P1: 1, P2: 1, P3: 1).

Actionable items I recommend fixing:
1. **P0** — restore `store.recovery.get(operation_id)` lookup (fixes the silent data loss).
2. **P1** — re-add the `status == "completed"` early return before `receipt`.
3. **P2** — return `store.receipt(record)` rather than a hardcoded dict.
4. **P3** — decide and document retry value semantics (stored vs. incoming `values`).

Plus: add regression tests for distinct operation_ids / changed values / transient failure on a completed op.

Items I recommend keeping: none — the diff's recovery-record `values` capture is a reasonable idea, but the lookup change undermines it.

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes (+ tests)
2. **Fix P0/P1 only** — critical/high priority
3. **Fix specific items** — tell me which
4. **No changes** — review complete

Please choose an option or provide specific instructions.
