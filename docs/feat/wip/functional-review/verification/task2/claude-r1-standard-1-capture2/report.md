## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (1 insertion, 3 deletions)
**Overall assessment**: REQUEST_CHANGES

The "simplification" removes a load-bearing ownership guard, changing behavior rather than preserving it.

---

## Findings

### P0 — Critical

(none — see P1; this borders on P0 depending on what `active` governs)

### P1 — High

- **[cleanup.py:3]** Unconditional `active.pop` evicts another setup's live association
  - Profile: python · Checklist: security-checklist.md (Race Conditions / Data Integrity) + solid-checklist.md (Dead code / behavior-preservation)
  - Triggered by: content — `.py` extension (Python profile active)
  - **What changed:** The old code only cleared the workspace's active association when it actually belonged to the setup being cleaned up:
    ```python
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
    ```
    The new code pops `store.active[workspace_id]` unconditionally.
  - **Why it's a bug:** This is a compare-and-delete *ownership* guard, not redundant ceremony. The existence of separate `store.pending` and `store.active` maps proves multiple setups can coexist for one workspace (several pending, at most one active). Failure sequence:
    1. Setup **A** becomes active → `store.active[W] = {"setup_id": A, ...}`.
    2. Setup **B** is started for the same workspace **W** → lives in `store.pending[B]`.
    3. **B** is cancelled/failed → `cleanup_setup(store, W, B)`.
    - **Old behavior:** `active[W].setup_id == A != B` → A's active association is kept. ✅
    - **New behavior:** `active[W]` is popped → **A's legitimate active association is destroyed**, leaving the workspace with no active setup. ❌
  - So cleaning up a *non-active* setup now silently evicts the *active* one. If `active` gates routing/access/session state, this is a correctness + data-integrity regression (hence arguably P0).
  - Confidence: 85% — The guard's structure (`get` + `setup_id` equality) exists precisely to prevent clobbering a different owner, and the pending/active split confirms cross-setup coexistence is expected. Residual uncertainty: if an external invariant guarantees `cleanup_setup` is *only ever* called for the currently-active setup and no other setup can be active, the guard would be redundant — but nothing in scope establishes that, and the pending path (a setup cleaned up before ever becoming active) breaks it.
  - **Suggested fix:** Restore the guard. If the goal was only to reduce lines, keep the semantics:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        active = store.active.get(workspace_id)
        if active and active["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If you genuinely intend unconditional removal, document the invariant (e.g., "only the active setup is ever cleaned up") that makes it safe — ideally with a test asserting a non-active setup's cleanup leaves the active one intact.

### P2 — Medium

(none)

### P3 — Low

(none)

---

## Additional Suggestions

- Add a regression test for the exact sequence above: active A + pending B, call `cleanup_setup(..., B)`, assert `store.active[W]["setup_id"] == A`. This both documents the contract and prevents a future re-simplification.

**Not covered:** I could not see the definition of `store`, `pending`, or `active` (not in scope/diff), so the severity hinges on what the `active` association controls. If you point me at the store model I can tighten the confidence and the P0-vs-P1 call.

---

## Next Steps

I found 1 issue (P0: 0, **P1: 1**, P2: 0, P3: 0), plus 1 test suggestion.

The actionable items I recommend fixing:
1. **P1** — Restore the `setup_id` ownership guard before `store.active.pop` (cleanup.py:3).
2. Add a regression test covering active-A / cleanup-B.

Items I recommend keeping as is:
- Removing `association = store.active.get(...)` *would* be fine **only** if the ownership check is preserved — so there's nothing here to keep from the current diff.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation needed

Choose an option or share the `store` model if you'd like me to re-confirm the severity before deciding.
