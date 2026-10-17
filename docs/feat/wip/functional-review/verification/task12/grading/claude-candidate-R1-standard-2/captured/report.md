Now the review report.

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (1 insertion, 3 deletions)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: User-described "cleanup simplification" of `cleanup_setup`. Selected diff = **staged** changes only (no unstaged changes present). Candidate state = `:cleanup.py` (staged blob).
**Baselines**: Review base = `HEAD` (`a7ab15e "Review base"`); candidate = staged index. No release/deployment baseline supplied or relevant.
**Profile**: `python` (triggered by `.py` extension — authoritative content signal). Checklists applied: security, SOLID, code-quality, removal-plan.

## Behavior and Compatibility

Data model (`store.py`): `store.active` is keyed by `workspace_id` — **one active association per workspace** — and each value carries the `setup_id` that owns it. `complete_setup` *overwrites* `store.active[workspace_id]` whenever a new setup completes for that workspace.

The change removes the ownership guard in `cleanup_setup`:

```python
# before
association = store.active.get(workspace_id)
if association and association["setup_id"] == setup_id:
    store.active.pop(workspace_id, None)
# after
store.active.pop(workspace_id, None)
```

- **`store.pending.pop(setup_id, None)`** — unchanged, keyed by `setup_id`; always correct to remove its own pending entry. **Supported.**
- **`store.active.pop(workspace_id, None)`** — now unconditional. Because the slot is keyed by workspace and shared across successive setups, cleaning up a *stale/superseded* `setup_id` now evicts whatever is active — including a *different, newer* setup's live connection. **Blocked (correctness regression).**

Scenario traced (concrete):
1. `complete_setup(store, "w", "one", "conn-one")` → `active["w"] = {setup_id: "one", ...}`
2. Workspace re-runs: `complete_setup(store, "w", "two", "conn-two")` → `active["w"] = {setup_id: "two", ...}`
3. Stale setup "one" is cleaned up late: `cleanup_setup(store, "w", "one")`
   - **Before:** `active["w"].setup_id == "two" != "one"` → does **not** pop → `active_connection("w") == "conn-two"` ✓
   - **After:** pops unconditionally → `active_connection("w") == None` ✗ — the current setup's connection is silently destroyed.

The guard existing in the review base is strong evidence this ordering (late cleanup of a superseded setup) is a real, intended-to-be-handled case — exactly a check-then-act / identity-ownership pattern from the checklists.

**Evidence limit**: `cleanup_setup` has no production caller in-repo (only the test calls it), so I can't confirm from callers how often a late/stale cleanup occurs. The conclusion rests on the data model + the removed guard's intent. This is an *Unknown* on frequency, not on the defect itself.

---

## Findings

### P0 — Critical

(none)

### P1 — High

- **[cleanup.py:3]** Removing the ownership guard makes `cleanup_setup` evict another setup's active association
  - Profile: python · Checklist: security-checklist.md (Race Conditions → Check-Then-Act) + code-quality / functional correctness
  - Triggered by: content — `.py` extension; single-slot `store.active` keyed by `workspace_id`
  - Trigger/path: `cleanup_setup(store, workspace_id, stale_setup_id)` called after a newer setup became active for the same workspace → unconditional `store.active.pop(workspace_id)` deletes the newer setup's live connection. Expected: only the matching setup's association is removed. Actual: any active association for the workspace is removed. Consequence: `active_connection()` returns `None`; the current, valid connection is silently lost.
  - Confidence: **95%** — Verified against `store.py`/`setup.py`: the slot is per-workspace and overwritten on each completion, and the base guard checked `setup_id` ownership specifically. Remaining uncertainty is only whether this call ordering occurs at runtime (no non-test caller in-repo); the guard's prior existence indicates it was intended.
  - Suggested fix: keep the ownership check.
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If the real goal was to shed the local variable, the minimal safe simplification preserves the guard:
    ```python
        if store.active.get(workspace_id, {}).get("setup_id") == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 — Medium

- **[tests/test_setup.py:14]** Test coverage gives false confidence in this change
  - Profile: python · Checklist: code-quality-checklist.md (boundary conditions / test coverage)
  - Triggered by: content — `.py`
  - The only cleanup test, `test_cleanup_removes_its_own_association`, exercises the *matching-id* case, which passes under **both** the old and new code — so it does not catch this regression. The mismatch case (stale cleanup after a re-setup) is untested.
  - Confidence: 90% — directly observable from the test file.
  - Suggested fix: add a test asserting that cleaning up a superseded `setup_id` leaves the newer active connection intact:
    ```python
    def test_cleanup_ignores_superseded_setup(self):
        store = Store()
        complete_setup(store, "w", "one", "conn-one")
        complete_setup(store, "w", "two", "conn-two")
        cleanup_setup(store, "w", "one")
        self.assertEqual(active_connection(store, "w"), "conn-two")
    ```

### P3 — Low

(none)

---

## Coverage and limits

- **Checked**: full staged diff + current `cleanup.py`, data model (`store.py`), all consumers/producers of `store.active`/`store.pending` (`setup.py`), and the test suite. Applied python security, SOLID, code-quality, and removal checklists.
- **Not covered**: runtime call sites of `cleanup_setup` (none exist in-repo beyond the test) — the frequency/exploitability of the bad ordering in production is **Unknown**.
- **Residual risk / recommended follow-up**: add the mismatch-id test above; confirm from the actual caller(s) whether cleanup is ever invoked for a non-active `setup_id` (if it provably never is, the simplification is safe — but that invariant is currently unenforced and undocumented).

**Indexed**: 1 systemic P1 pattern recorded to `kk:review-findings` (ownership-guard removal before a single-slot mutation).

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

Actionable items I recommend fixing:
1. **P1** — Restore the `setup_id` ownership guard in `cleanup_setup` (correctness regression; blocks merge).
2. **P2** — Add the mismatch-id test so the regression can't silently return.

Items I recommend keeping as is:
- The unconditional `store.pending.pop(setup_id, None)` — correct; `pending` is keyed by `setup_id`, so it only ever removes its own entry.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the test
2. **Fix P0/P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

If you believe `cleanup_setup` is *only ever* called for the currently-active setup, tell me — I'll re-examine, but I'd still recommend documenting/asserting that invariant rather than relying on it implicitly.
