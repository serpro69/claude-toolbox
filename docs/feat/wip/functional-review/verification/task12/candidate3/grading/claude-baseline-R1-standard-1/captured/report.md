## Code Review Summary

**Files reviewed**: 1 file (`cleanup.py`), 4 lines changed (1 insertion, 3 deletions, staged)
**Overall assessment**: REQUEST_CHANGES

The "simplification" deletes an ownership guard. What looks like redundant code was actually load-bearing: it ensured the active slot for a workspace is only cleared by the setup that currently owns it.

```python
# Before
def cleanup_setup(store, workspace_id, setup_id):
    store.pending.pop(setup_id, None)
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:   # ← ownership check
        store.active.pop(workspace_id, None)

# After
def cleanup_setup(store, workspace_id, setup_id):
    store.pending.pop(setup_id, None)
    store.active.pop(workspace_id, None)                       # ← unconditional
```

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[cleanup.py:3]** Unconditional `store.active.pop` evicts the active association of a *different* setup
  - Profile: python · Checklist: security-checklist.md (Data Integrity / Check-Then-Act ownership) — also code-quality (Boundary Conditions)
  - Triggered by: content — extension `.py`
  - **Description**: The removed guard only cleared `store.active[workspace_id]` when the currently-active association's `setup_id` matched the one being cleaned up. The new code clears it unconditionally. When a workspace's active setup has already been superseded by a newer one, a late, retried, or out-of-order `cleanup_setup` for the *old* setup now wipes the *current* active association.
  - **Failure scenario**: Workspace `W` has setup `A` active → setup `B` replaces it (`store.active[W] = {"setup_id": B}`). A delayed/retried cleanup for the cancelled setup `A` runs: `cleanup_setup(store, W, A)`.
    - Old behavior: `association["setup_id"] == A`? No (it's `B`) → active slot for `B` preserved. ✅
    - New behavior: `store.active.pop(W, None)` → `B`'s active association silently removed. ❌ Workspace loses its live setup.
  - **Confidence**: 85% — Verified against the full file and diff; behavior differs precisely in the superseded/retried-cleanup case. The guard's existence is strong evidence that `store.active[workspace_id]` is not guaranteed to belong to `setup_id` at cleanup time. Residual uncertainty: if callers guarantee cleanup only ever fires for the currently-active setup (never superseded, never retried), the two are equivalent — but nothing in this file establishes that, and the guard implies the opposite.
  - **Suggested fix**: Restore the ownership check:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If the goal was genuinely to simplify, first prove (with a test or caller audit) that `store.active[workspace_id]` always belongs to `setup_id` at this call site; absent that proof, keep the guard.

### P2 - Medium

(none)

### P3 - Low

(none)

---

## Notes on what was checked

- **Security checklist**: The relevant hit is the Check-Then-Act / Data Integrity section — the deleted code was an identity-before-mutate guard; its removal is a lost-update / wrong-eviction bug. No injection/secrets/crypto surface in this diff. Note there is still a mild TOCTOU shape even in the *original* (get-then-pop is non-atomic), but that's pre-existing and not introduced here.
- **SOLID checklist**: No new SOLID violations.
- **Code quality**: Boundary handling actually *regressed* — the removed `association and ...` check also guarded against `workspace_id` absent / `None` association.
- **Removal plan**: N/A — this isn't retiring dead code; the deleted lines were live correctness logic.
- Capy knowledge base was empty (cold start); the pattern has now been indexed as `kk:review-findings`.

**Not covered**: I could not verify callers of `cleanup_setup` or the `store` structure (not in the diff). The whole finding hinges on whether a cleanup can ever fire for a non-current setup — worth confirming with a test.

---

## Next Steps

I found 1 issue (P0: 0, P1: 1, P2: 0, P3: 0).

The actionable item I recommend fixing:
1. **P1** — Restore the ownership guard in `cleanup.py` before the unconditional `store.active.pop`, OR prove the key always belongs to the caller and add a test documenting that invariant.

Items I recommend keeping as is:
- None — this diff is a single change, and it's the one flagged.

**How would you like to proceed?**

1. **Fix all** — I'll restore the guard
2. **Fix P0/P1 only** — same as above (the one P1)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions. (I won't change anything until you confirm.)
