Now presenting the review.

## Code Review Summary

**Files reviewed**: 1 file (`service.py`), 8 insertions / 8 deletions (staged)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: "Save recovery update" — rework of `save()` in `service.py`. Requirement source: `README.md` (workspace-preferences save/recovery contract). Selected diff: **staged changes only** (no unstaged changes exist). Candidate = git index blob of `service.py`.
**Baselines**: Review base = `HEAD` (`feeb199 Review base`); candidate = staged `service.py`. No separate release baseline (in-memory store, single-process; README explicitly disclaims threads/restart/network).
**Profile**: `python` (always-load checklists applied). Task scope: shape 3 (no `docs/feat/wip/`) — reviewed on its own merits against README.

## Behavior and Compatibility

The README is an explicit contract. I traced each clause against the candidate through `store.py` (the provider) and `client.py`/`tests/test_save.py` (consumers):

| Contract clause | Candidate behavior | Result |
|---|---|---|
| Repeating a **completed ID** returns its receipt | Works for same workspace (test passes), but re-invokes `store.receipt` on the completed record rather than returning early | **Supported** (minor extra side-effect, see P2) |
| Failed save retried with **same ID and edited values** → latest values active | Apply is gated on `status == "pending"`; after the first attempt the record is `"applied"`, so a retry **never re-applies the edited values** | **Blocked** (P1-A) |
| A **fresh operation ID** must perform a fresh save, even for the same workspace | Lookup is by `workspace`, so a fresh ID finds the prior record and does nothing — new values dropped | **Blocked** (P1-B) |
| Provider replaces preferences idempotently; receipt may fail after apply | Apply happens before receipt; idempotent at provider level | Supported |
| Concurrency / threads | README disclaims threads | **Not applicable** |

**Root insight:** the function keys the recovery dict by `operation_id` on *write* (`store.recovery[operation_id] = record`) but *reads* by scanning for a matching `workspace`. Combined with gating apply on `status == "pending"` and only storing `values` at record-creation time, the **`values` argument is effectively ignored on every call after the first save for a given workspace.** The existing tests pass only because they never exercise edited values or a second operation ID — they give false confidence.

---

## Findings

### P0 - Critical

(none — impact is scoped, recoverable, in-memory data loss, not catastrophic/irreversible)

### P1 - High

- **[service.py:2-3, 8]** Fresh operation ID on an existing workspace silently performs no save
  - Profile: python · Checklist: security-checklist.md (Data Integrity — lost updates / missing idempotency), functional-review (contract violation)
  - Triggered by: content — `.py` extension
  - **Trigger/path**: `save(store,"w","op-1",{"color":"blue"})` completes → `save(store,"w","op-2",{"color":"red"})`. The lookup `next(item for item in store.recovery.values() if item["workspace"]==workspace)` returns the **op-1** record (status `completed`). `record is not None` → no new record; `status != "pending"` → `apply` skipped. Returns `{"ok": True, "operation_id": "op-2"}`.
  - **Expected vs actual**: README — "A fresh operation ID must perform a fresh save, even for the same workspace" and "success means the latest submitted values are active." Actual — `preferences["w"]` stays `{"blue"}`, no `recovery["op-2"]` record is created, yet the caller is told `ok: True`. Silent lost update.
  - **Consequence**: Every subsequent operation on a workspace is a no-op that reports success. Data loss masquerading as success.
  - Confidence: 95% — traced directly against `store.py`; contract clause is explicit. The only residual uncertainty is whether "fresh ID same workspace" was intended to be dropped, but the README forbids that reading.
  - **Suggested fix**: Look up the record by the key it is stored under — `record = store.recovery.get(operation_id)` — not by workspace.

- **[service.py:8-10]** Retry with edited values after a receipt failure drops the edited values
  - Profile: python · Checklist: security-checklist.md (Data Integrity — idempotency for retryable ops), functional-review (contract violation)
  - Triggered by: content — `.py` extension
  - **Trigger/path**: `store.fail_receipt_once = True`; `save(store,"w","op-1",{"color":"blue"})` → record created `pending`, `apply` runs, `status="applied"`, then `store.receipt` raises `ReceiptUnavailable` (record persisted as `applied`). Retry `save(store,"w","op-1",{"color":"red"})` → record found, `status == "applied"` so `apply` is **skipped**; `values` arg ignored (apply uses the stored `record["values"]` from creation anyway). Receipt now succeeds.
  - **Expected vs actual**: README — "A failed save can be retried with the same ID and edited values; success means the latest submitted values are active." Actual — `preferences["w"]` stays `{"blue"}`; the edited `{"red"}` never applies.
  - **Consequence**: The documented failure-recovery path (receipt fails after apply) silently discards corrected values on retry — the exact scenario this "save recovery" change exists to handle. `test_retry_same_values` masks it by retrying with identical values.
  - Confidence: 92% — independent of P1-A's lookup bug; caused by the `status == "pending"` gate plus storing `values` only at creation. Verified against `store.receipt`'s mutation order.
  - **Suggested fix**: Re-apply the freshly supplied `values` on each attempt until the operation is **completed** (not merely `applied`), and update `record["values"] = dict(values)` on every call. E.g. early-return only when `status == "completed"`; otherwise `store.apply(workspace, values)` then `record["values"]=dict(values)` and return `store.receipt(record)` — close to the original structure.

### P2 - Medium

- **[service.py:11-12]** Return value of `store.receipt(record)` is discarded; a hardcoded dict is returned instead
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The original returned `store.receipt(record)`. The candidate ignores it and returns `{"ok": True, "operation_id": operation_id}`. In the happy path these match, but it couples `save` to receipt's current shape and, under the P1-A collision, returns the *requested* `operation_id` while the receipt/record belong to a *different* op — a misleading response. Also, repeating a completed ID now calls `store.receipt` again on an already-completed record (an extra re-issue / side effect) rather than returning early.
  - Confidence: 70% — behaviorally minor today; flagged as fragility and a symptom of the lookup bug.
  - **Suggested fix**: Return `store.receipt(record)` and short-circuit completed IDs before re-invoking receipt.

### P3 - Low

- **[tests/test_save.py]** Test coverage does not exercise the contract's two hardest clauses — "fresh ID, same workspace" and "retry with *edited* values." Both P1s live in those gaps. (Not a defect in the staged file, but the reason the regression is invisible.) Recommend adding both cases alongside any fix.

---

## Removal/Iteration Plan

Not applicable — no dead/retired code introduced.

## Coverage and limits

- **Checked**: full `service.py` candidate; the provider contract (`store.py`), the consumer (`client.py`), the test suite, and the README contract clause-by-clause; concrete traces for first-save, completed-repeat, receipt-failure retry (same + edited values), and fresh-ID-same-workspace.
- **Not covered**: did not execute the test suite (static trace only; `store.receipt` mutation order verified by reading). No concurrency analysis — README disclaims threads (Not applicable).
- **Residual risk**: if there are consumers beyond `client.py` passing operation IDs with a different semantics, the P1 severity could shift — none found in-repo.
- **No findings to index**: the two P1s *were* indexed as `kk:review-findings` (idempotency lookup-by-wrong-key; idempotent-apply gated on one-shot status).

---

## Next Steps

I found 4 issues (**P0: 0, P1: 2, P2: 1, P3: 1**). Both P1s trace to the same rewrite: looking up recovery records by `workspace` instead of `operation_id`, and gating `apply` on a one-shot `"pending"` status. Together they make `save()` ignore its `values` argument on every call after the first for a workspace — silent data loss with `ok: True`.

The actionable items I recommend fixing:
1. **P1-A** — look up by `operation_id` (`store.recovery.get(operation_id)`).
2. **P1-B** — re-apply supplied `values` until status is `completed`; early-return only on `completed`.
3. **P2** — return `store.receipt(record)`; don't re-issue receipt for completed IDs.
4. **P3** — add tests for fresh-ID-same-workspace and edited-values retry.

Fixes 1–3 essentially restore the original `service.py` structure, which satisfied all four README clauses; the staged version regresses them.

Items I recommend keeping as is:
- None — the "completed ID returns receipt" path still works, but is entangled with the P2 re-issue fix.

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes (incl. tests)
2. **Fix P0/P1 only** — address the two data-loss regressions
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions. (Review-only so far — I won't change anything until you confirm.)
