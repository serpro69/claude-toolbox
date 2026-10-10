Finding indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file (`cleanup.py`), 4 lines changed (1 insertion, 3 deletions)
**Overall assessment**: **REQUEST_CHANGES**

The "simplification" removes a load-bearing guard, introducing a silent correctness/data-loss bug. I verified this against the full `store` contract (`store.py`, `setup.py`) and the existing test.

---

## Findings

### P0 - Critical

- **[cleanup.py:3]** Unconditional `store.active.pop` clobbers a superseded-but-valid active association
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / correctness)
  - Triggered by: content — `.py` extension (python profile)
  - **What changed**: the guarded removal
    ```python
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
    ```
    became an unconditional `store.active.pop(workspace_id, None)`.
  - **Why it's a bug**: `store.active` is keyed by `workspace_id`, but `complete_setup` (`setup.py:6`) *overwrites* `store.active[workspace_id]` whenever a new setup completes. So a workspace's active entry can belong to a **different** `setup_id` than the one being cleaned up. The original guard made cleanup *setup-scoped and idempotent*: it only removed the active entry if that entry actually belonged to the setup being torn down. The new code removes it regardless.
  - **Failure scenario**:
    1. `begin_setup(store, "w", "one")`; `complete_setup(store, "w", "one", "conn-one")` → `active["w"] = {setup_id: "one", ...}`
    2. Workspace re-setup: `begin_setup(store, "w", "two")`; `complete_setup(store, "w", "two", "conn-two")` → `active["w"] = {setup_id: "two", ...}` (setup "one" is now superseded)
    3. A late/out-of-order cleanup for the *old* setup fires: `cleanup_setup(store, "w", "one")`
    - **Old behavior**: `active["w"].setup_id == "two" != "one"` → active entry preserved. `active_connection(store, "w")` still returns `"conn-two"`. ✅
    - **New behavior**: `active["w"]` is popped unconditionally → the live `"conn-two"` connection is silently dropped. `active_connection(store, "w")` returns `None`. ❌
  - **Confidence**: 95% — the store semantics confirm re-setup overwrites the active entry, and the guard exists precisely to scope the delete to its own setup. The only way removal would be safe is if `cleanup_setup` were *guaranteed* to be called only for the currently-active setup, which the overwrite-on-complete flow does not guarantee. Residual uncertainty is only around whether out-of-order/stale cleanups actually occur in the calling code (not in this repo).
  - **Suggested fix**: restore the guard.
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P1 - High

*(none)*

### P2 - Medium

- **[tests/test_setup.py:14]** Test coverage masks the regression
  - Profile: python · Checklist: code-quality-checklist.md (test hygiene)
  - Triggered by: content — `.py` extension (python profile)
  - `test_cleanup_removes_its_own_association` only exercises the *matching* case (cleanup of the currently-active setup), which passes under both the old and new code. There is no test for the **mismatch** case, so the bug ships green. This absent case is exactly what let the "simplification" look safe.
  - **Confidence**: 90%
  - **Suggested fix**: add a regression test, e.g. `test_cleanup_of_superseded_setup_preserves_active`:
    ```python
    def test_cleanup_of_superseded_setup_preserves_active(self):
        store = Store()
        begin_setup(store, "w", "one")
        complete_setup(store, "w", "one", "connection-one")
        begin_setup(store, "w", "two")
        complete_setup(store, "w", "two", "connection-two")
        cleanup_setup(store, "w", "one")  # stale cleanup of superseded setup
        self.assertEqual(active_connection(store, "w"), "connection-two")
    ```

### P3 - Low

*(none)*

---

## Removal/Iteration Plan

The deleted guard is **not** a safe-delete candidate — it encodes a correctness invariant (setup-scoped, idempotent cleanup). Per the removal checklist, a guard whose mismatch branch is reachable (it is, via `complete_setup` overwrites) must be kept. Recommend reverting the deletion and adding the P2 test alongside.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P0** — Restore the `setup_id` guard in `cleanup_setup` (reverts the staged simplification).
2. **P2** — Add a regression test for cleanup of a superseded setup.

Items I recommend keeping as is:
- The `store.pending.pop(setup_id, None)` line — unchanged and correct.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P0 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Note: I'd push back on the simplification's premise — the two-line version is tidier but incorrect. Please choose an option or give specific instructions.
