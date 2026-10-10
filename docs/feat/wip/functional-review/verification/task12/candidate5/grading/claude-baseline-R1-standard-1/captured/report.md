Finding indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file (`cleanup.py`), 4 lines changed (1 insertion, 3 deletions)
**Overall assessment**: **REQUEST_CHANGES**

The staged change is presented as a simplification, but it is a **behavior change** that removes a correctness-critical ownership guard.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[cleanup.py:3]** Unconditional `active` eviction removes the ownership guard — wrong setup can evict a live association
  - Profile: python · Checklist: security-checklist.md (Race Conditions → Check-Then-Act / Data Integrity) + code-quality-checklist.md (Boundary Conditions)
  - Triggered by: content — `.py` extension
  - **What changed:** The original code only popped `store.active[workspace_id]` *when the currently-active association belonged to the setup being cleaned up*:
    ```python
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
    ```
    The new code pops it unconditionally:
    ```python
    store.active.pop(workspace_id, None)
    ```
  - **Failure scenario:** Workspace `W` has setup `A` active. Setup `B` is started for `W` (added to `pending`) but never becomes active, or `B` is an older/superseded setup. Calling `cleanup_setup(store, W, B)` now removes `W`'s active association for `A` — a setup it was never supposed to touch. The workspace silently loses its live active setup. This is exactly the kind of stale/concurrent/superseded-cleanup path such a guard exists to defend against.
  - **Confidence: 95%** — The diff unambiguously drops an identity comparison (`association["setup_id"] == setup_id`) that gated the mutation. The guard's only purpose was to scope *which* active entry may be evicted; removing it broadens the deletion to "whatever is active, regardless of owner." The remaining 5% is uncertainty about whether a caller contract elsewhere guarantees `setup_id` always equals the active one (which would make the guard dead code) — but I can't see such a guarantee in this file, and if it existed the original author presumably wouldn't have written the check. Worth confirming against the call sites.
  - **Note:** `.pop(..., None)` being null-safe (no `KeyError` on a missing key) is a red herring — the guard protected *which value* gets removed, not *whether the key exists*. The simplification preserves null-safety while discarding ownership correctness.
  - **Suggested fix:** Keep the guard. If the goal was readability, restructure without changing semantics:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association.get("setup_id") == setup_id:
            store.active.pop(workspace_id, None)
    ```
    (Using `.get("setup_id")` also hardens against an association dict missing the key — a latent `KeyError` in the original.)

### P2 - Medium

(none)

### P3 - Low

(none)

---

## Additional Suggestions (non-blocking)

- **Test coverage:** Add a regression test for the cross-setup case — `active[W] = {"setup_id": "A"}`, call `cleanup_setup(store, W, "B")`, assert `active[W]` is **unchanged**. This is the exact case the change breaks and would catch any future re-simplification.

---

## Next Steps

I found 1 issue (P0: 0, P1: 1, P2: 0, P3: 0).

The actionable item I recommend fixing:
1. **P1** — Restore the ownership guard in `cleanup_setup` so only the owning setup can evict the active association (and optionally harden the key access with `.get("setup_id")`).

Items I recommend keeping as is:
- The unconditional `store.pending.pop(setup_id, None)` — correct; pending is keyed by `setup_id`, so no ownership ambiguity exists there.

**How would you like to proceed?**

1. **Fix all** — restore the guard (+ optional test)
2. **Fix P0/P1 only** — same single fix
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

A word of caution before you pick: if this simplification was intentional because callers guarantee `setup_id` always matches the active association, let me know and I'll verify against the call sites rather than restoring the guard — but nothing in `cleanup.py` establishes that guarantee today.
