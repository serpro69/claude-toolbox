## Code Review Summary

**Files reviewed**: 1 file (`cleanup.py`), 4 lines changed (+1 / −3, staged)
**Overall assessment**: **REQUEST_CHANGES**

The "simplification" removes a compare-before-delete ownership guard, turning a conditional eviction into an unconditional one. This is a correctness/data-loss bug, not an equivalent refactor.

---

## Findings

### P0 - Critical

- **[cleanup.py:3]** Removing the ownership guard wrongly evicts the active setup on stale cleanup
  - Profile: python · Checklist: security-checklist.md (Race Conditions → Check-Then-Act / Data Integrity → Lost updates)
  - Triggered by: content — `.py` extension (python profile)
  - **The guard that was deleted was load-bearing.** Original logic only removed the workspace's active association if *that association still belonged to this `setup_id`*:
    ```python
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
    ```
    The new code pops `store.active[workspace_id]` unconditionally. The `setup_id` stored in the active record is an **ownership token**; comparing it before mutating is the whole reason it's stored.
  - **Failure scenario** (resource reassignment):
    1. Setup `A` becomes active for workspace `W` → `store.active[W] = {"setup_id": A}`
    2. Setup `B` supersedes it → `store.active[W] = {"setup_id": B}`
    3. `cleanup_setup(store, W, A)` runs (A expired / was cancelled / duplicate/delayed cleanup)
       - **Old:** `B != A` → active left pointing at `B` ✓
       - **New:** unconditionally pops → **`B`'s active association is destroyed** ✗
    This is the classic check-then-act / lost-update pattern: a stale or retried cleanup now silently tears down the *current* owner's state.
  - Confidence: 80% — The bug is certain *if* a workspace's active setup can ever be reassigned while an older setup is still subject to cleanup. The existence of the `setup_id` ownership field plus the original guard is strong evidence that this is an expected state. Residual uncertainty: if an external invariant guarantees `cleanup_setup` is only ever called for the currently-active setup, the guard was merely defensive and its removal is "safe but fragile." I could not verify callers (only `cleanup.py` is in scope).
  - **Suggested fix**: Restore the guard. If the goal was to reduce lines, keep the semantics:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        if store.active.get(workspace_id, {}).get("setup_id") == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If you believe the invariant makes the guard unnecessary, don't drop it silently — assert it instead so a violated assumption fails loudly rather than corrupting state (note: not a plain `assert`, which `python -O` strips).

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
- **[cleanup.py:1]** No type hints on `store` / `workspace_id` / `setup_id`. Pre-existing, not introduced by this diff; mentioned only as optional polish. Confidence: 100%.

---

## Additional Suggestions
- A regression test covers the real risk directly: activate `B` over `A` for the same workspace, call `cleanup_setup(..., A)`, assert `store.active[W]["setup_id"] == B`. The current diff would fail it; the fixed version passes.

**Verification note**: I reviewed only the staged change to `cleanup.py`. I did **not** trace callers of `cleanup_setup` or the lifecycle that governs when setups are activated/superseded — that's the key input to confirming the failure scenario occurs in practice.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 0, P3: 1).

The actionable items I recommend fixing:
1. **P0** — Restore the `setup_id` ownership guard before popping `store.active[workspace_id]` (or replace it with a loud assertion if the invariant truly holds).

Items I recommend keeping as is:
- **P3 type hints** — pre-existing, out of scope for this simplification.

**How would you like to proceed?**

1. **Fix all** — I'll implement the suggested fixes
2. **Fix P0/P1 only** — Address the critical guard-removal issue
3. **Fix specific items** — Tell me which issues to fix
4. **No changes** — Review complete, no implementation needed

Before I'd confidently fix, it's worth confirming: **can a workspace's active setup be reassigned to a newer `setup_id` while an older setup still gets cleaned up?** If yes, this is a definite P0. If `cleanup_setup` is guaranteed to run only for the active setup, the guard is defensive-only and the call is yours. Let me know how you'd like to proceed.
