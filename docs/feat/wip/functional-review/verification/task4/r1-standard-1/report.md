Indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (+1 / −3), staged diff of `cleanup.py`
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Intent (inferred from the commit framing "cleanup simplification") is to simplify `cleanup_setup` by dropping the ownership guard around the active-association removal. Selected diff = staged changes only (no unstaged present). Candidate state = working index.
**Baselines**: Review base = `a7ab15e "Review base"`; candidate = staged `cleanup.py`. No separate release/deployed baseline inspected (none available in repo).
**Profiles**: `python` (extension `.py`, authoritative). Always-load checklists applied: security, SOLID, code-quality, removal-plan.

## Behavior and Compatibility

I traced the full setup lifecycle across `setup.py`, `store.py`, and `tests/test_setup.py`:

- `complete_setup` writes `store.active[workspace_id] = {"setup_id": setup_id, "connection": ...}` — the active association **records which setup currently owns the workspace**.
- The removed guard (`if association and association["setup_id"] == setup_id`) enforced that `cleanup_setup` only clears the active association **if it still belongs to the setup being cleaned up**.
- The new code pops `store.active[workspace_id]` **unconditionally**.

**Discriminating scenario (the one the guard existed for):**

1. `complete_setup(store, "w", "one", "conn-one")` → `active["w"] = {setup_id:"one", ...}`
2. Workspace "w" is re-set-up: `complete_setup(store, "w", "two", "conn-two")` → `active["w"] = {setup_id:"two", ...}`
3. A late/stale cleanup for the **old** setup fires: `cleanup_setup(store, "w", "one")`
   - **Before**: guard sees `active["w"]["setup_id"] == "two" != "one"` → active association preserved. `active_connection("w")` still returns `"conn-two"`. ✅
   - **After**: unconditional pop → the **live, valid** association for setup "two" is destroyed. `active_connection("w")` returns `None`. ❌ The current connection is silently torn down.

- **Blocked**: superseded-setup / re-setup cleanup combination — demonstrated regression caused by this change.
- **Supported**: the single-setup happy path (begin → complete → cleanup of the same setup) — still correct; this is what the existing test covers.
- **Unknown**: production reachability of the superseded-setup path — `cleanup_setup` has **no non-test callers in this repo**, so I can't confirm the call ordering from the call graph. However, the deleted guard plus the test name (`test_cleanup_removes_its_own_association`, "its own") are strong evidence that ownership-scoped cleanup is the intended, relied-upon contract.

---

## Findings

### P0 - Critical

(none — see note; the P1 below is P0-adjacent if the superseded-setup path is confirmed reachable by production callers)

### P1 - High

- **[cleanup.py:3]** Removing the ownership guard lets a stale cleanup clobber a newer workspace association
  - Profile: python · Checklist: code-quality-checklist.md (boundary/correctness) + security-checklist.md (check-then-act / data integrity)
  - Triggered by: content — `.py` extension; diff deletes a conditional comparing `association["setup_id"] == setup_id` before a destructive `pop`
  - Trigger/path: `cleanup_setup(store, "w", "one")` after the workspace has moved on to setup `"two"`. Expected: old association untouched. Actual: `store.active.pop(workspace_id, None)` removes the live association for setup `"two"`, so `active_connection("w")` returns `None` and the valid connection is lost.
  - Consequence: silent loss of a live, valid active connection / incorrect workspace state — a production incident class (workspace loses connectivity due to an unrelated, delayed cleanup).
  - Confidence: 90% — Verified the behavior change directly from source and the lifecycle in `setup.py`; the guard's predicate and the test's name establish the intended ownership contract. Residual uncertainty is only whether out-of-repo callers ever invoke cleanup for a superseded setup; the guard's prior existence strongly implies they can.
  - Suggested fix: restore the ownership check:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 - Medium

- **[tests/test_setup.py:14]** Test name over-claims; it doesn't exercise the discriminating case
  - Profile: generic · Checklist: —
  - Triggered by: —
  - `test_cleanup_removes_its_own_association` only covers the case where the active association **is** its own, so it passes under both the old and new code and gives false-green coverage for the exact contract that just broke. The name ("its own") asserts ownership semantics the test never verifies.
  - Confidence: 95% — the test body plainly lacks a second-setup case.
  - Suggested fix: add a regression test asserting cleanup of an old setup does **not** remove a newer association:
    ```python
    def test_cleanup_ignores_superseded_setup(self):
        store = Store()
        complete_setup(store, "w", "one", "conn-one")
        complete_setup(store, "w", "two", "conn-two")
        cleanup_setup(store, "w", "one")
        self.assertEqual(active_connection(store, "w"), "conn-two")
    ```

---

## Additional Suggestions

- If the simplification's actual goal was to remove the check-then-act window between `.get` and `.pop` (a real, if pre-existing, concern under concurrency), note that this module uses plain unlocked dicts throughout, so no step here is atomic regardless. Dropping the guard trades a rare race for a *guaranteed* logic bug on the common re-setup path — a net regression. Address concurrency with a lock around the store if that's the concern, not by removing correctness.

## Coverage and limits

- Checked: full setup/cleanup lifecycle, the active-association ownership contract, idempotency (`pop(..., None)` keeps double-cleanup safe — unchanged), existing tests.
- Not covered: production callers of `cleanup_setup` (none in repo) and any concurrency model around `Store` (no locking present; pre-existing).
- No security findings (no injection/deserialization/secret/crypto surface in this change).

**Indexed**: the guard-removal pattern recorded under `kk:review-findings`.

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

Recommended fixes:
1. **P1** — Restore the `setup_id` ownership guard in `cleanup_setup` before the `store.active.pop`.
2. **P2** — Add the `test_cleanup_ignores_superseded_setup` regression test.

Items to keep as-is:
- The `store.pending.pop(setup_id, None)` line and the `pop(..., None)` idempotency are correct and unchanged.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete

Note: this is a behavioral regression, so I'd advise against merging the diff as staged. Let me know how you'd like to proceed.
