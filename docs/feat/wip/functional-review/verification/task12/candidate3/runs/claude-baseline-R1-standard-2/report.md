## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (+1 / −3), staged
**Overall assessment**: **REQUEST_CHANGES**

The "simplification" removes a load-bearing identity guard. What looks like dead-code cleanup actually changes runtime behavior under setup supersession.

---

## Findings

### P0 - Critical

- **[cleanup.py:3]** Unconditional `active.pop` evicts a *different* workspace's active setup
  - Profile: python · Checklist: security-checklist.md (Check-Then-Act / Data Integrity)
  - Triggered by: content — `.py` extension
  - **Description:** The original code only cleared the workspace's active association when it belonged to the setup being cleaned up:
    ```python
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
    ```
    The new code pops unconditionally. The `setup_id == setup_id` check was not redundant — it is an **ownership/identity guard**. Failure scenario:
    1. Setup `A` becomes active for workspace `W` → `active[W] = {"setup_id": A}`
    2. Setup `A` is superseded by setup `B` → `active[W] = {"setup_id": B}`
    3. A delayed/stale `cleanup_setup(store, W, A)` fires (cleaning up the *old* setup `A`)
       - **Before:** `association["setup_id"]` is `B ≠ A` → active association for `B` is preserved. ✅
       - **After:** `active[W]` is popped unconditionally → workspace `W` silently loses its **current, valid** active setup `B`. ❌

    This is a correctness/data-integrity regression (loss of valid in-memory state), reachable whenever a cleanup can arrive after supersession — exactly the case the guard was written to handle.
  - **Confidence: 85%** — The diff unambiguously removes an identity check, converting a conditional pop into an unconditional one. The guard's very existence implies the mismatch case is reachable. Residual uncertainty: if every caller guarantees `setup_id` is always the currently-active setup (never a stale/superseded id), the removal would be behavior-preserving — but that invariant isn't visible here and the guard asserts the opposite. I did not see the callers of `cleanup_setup`.
  - **Suggested fix:** Restore the identity guard:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If the simplification *is* intended (callers truly never pass a stale `setup_id`), encode that invariant with a comment and, ideally, a test covering the supersession case so the guard isn't silently re-removed.

### P1 - High

(none)

### P2 - Medium

(none)

### P3 - Low

(none)

---

## Additional Suggestions

- Add a regression test for the supersession path: active setup `B`, then `cleanup_setup(store, W, A)` for the superseded `A`, asserting `active[W]` still points at `B`. This is the behavior the diff breaks and the cheapest guard against it recurring.

*(Checked: SOLID, security/reliability, code-quality, and removal checklists for the Python profile. Not covered: callers of `cleanup_setup` and the `store` type definition — not in the diff; the P0 confidence hinges on whether a stale `setup_id` can reach this function.)*

Indexed the systemic pattern ("removing an identity guard before a destructive map eviction") as `kk:review-findings`.

---

## Next Steps

I found 1 issue (P0: 1, P1: 0, P2: 0, P3: 0).

The actionable item I recommend fixing:
1. **P0 — cleanup.py:3** Restore the `setup_id` identity guard before popping `store.active[workspace_id]` (or prove the invariant and add a test).

Items I recommend keeping as is:
- Removing `store.pending.pop(setup_id, None)` was never touched — the pending cleanup is fine; only the active-eviction guard is the problem.

**How would you like to proceed?**

1. **Fix all** — restore the guard
2. **Fix P0/P1 only** — same as above (only P0 exists)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions. I won't change anything until you confirm.
