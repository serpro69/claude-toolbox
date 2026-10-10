## Code Review Summary

**Files reviewed**: 1 file, 1 insertion / 3 deletions (`cleanup.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Profiles active**: `python` (triggered by extension `.py`)
**Capy KB**: empty (cold-start) — standard guidelines applied.

---

## Findings

### P0 - Critical

- **[cleanup.py:3]** Deleted guard makes stale cleanup clobber the workspace's *active* setup
  - Profile: python · Checklist: security-checklist.md (Race Conditions → Check-Then-Act) + code-quality-checklist.md (Boundary Conditions)
  - Triggered by: content — extension `.py`
  - **What changed:** The guard was removed:
    ```python
    # before
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
    # after
    store.active.pop(workspace_id, None)
    ```
  - **Why it's a bug:** The removed condition was not dead code — it enforced a correctness invariant: *only clear a workspace's active association if that association belongs to the setup being cleaned up*. Note the asymmetry in the data model: `store.pending` is keyed per **setup_id**, while `store.active` is keyed per **workspace_id**. That strongly implies a workspace can have multiple setups over its lifetime (one pending per setup, at most one active), so `cleanup_setup` can legitimately be called for a *superseded/stale* setup. With the guard gone, cleaning up an old setup unconditionally evicts whatever setup is *currently active* for that workspace.
  - **Failure scenario:** Workspace W has setup A active. Setup B is created, promoted to active (`active[W] = {"setup_id": B}`). A late/duplicate cleanup for A fires → `cleanup_setup(store, W, A)`. Old code: `active[W]["setup_id"]` is B ≠ A → left intact. New code: `active[W]` is popped → B's active association silently lost (data-loss / incorrect state). This is also classic check-then-act territory, now turned into an unconditional write.
  - **Confidence: 88%** — The behavioral divergence is certain from the diff. The only path where the simplification is safe is if `cleanup_setup` is *guaranteed* to be invoked only for the currently-active setup; nothing in this file establishes that invariant, and the pending/active key asymmetry argues against it. Residual uncertainty is only about caller guarantees I can't see from this single file.
  - **Suggested fix:** Restore the identity check:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If the simplification is genuinely desired, first prove (via callers/tests) that cleanup is never called for a non-active setup, and encode that assumption explicitly.

### P1 / P2 / P3

(none)

---

## Removal/Iteration Plan

Not applicable — this is a regression, not a removal opportunity. Before accepting any simplification here, add a test for the stale-cleanup case (active = setup B, cleanup called for setup A → active must remain B).

## Additional Suggestions

- `pending.pop(setup_id, None)` is correctly per-setup and unaffected — keep as is.
- Consider a brief docstring documenting the active-association invariant so future "simplifications" don't re-trip this.

---

## Next Steps

I found **1 issue** (P0: 1, P1: 0, P2: 0, P3: 0). Indexed to `kk:review-findings` as a systemic pattern (guard-deletion during "simplification").

The actionable item I recommend fixing:
1. **P0** — Restore the `setup_id` match guard before `store.active.pop(...)` in `cleanup.py`.

Items I recommend keeping as is:
- `store.pending.pop(setup_id, None)` — correct, per-setup, unchanged.

**How would you like to proceed?**

1. **Fix all** — restore the guard
2. **Fix P0/P1 only** — same as above (only the P0 exists)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions. (I won't change anything until you confirm.)
