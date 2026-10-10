Now I'll present the review.

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (+1 / −3), staged `cleanup.py`
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Stated intent — "cleanup simplification." Request — review the staged diff. Selected diff — staged (`git diff --cached`); no unstaged changes. Candidate state — `cleanup.py` worktree == index. No `docs/feat/wip/` relates to this diff → **no task scope** (reviewed on its own merits).
**Baselines**: Review base = `HEAD` (`a7ab15e Review base`); candidate = staged index blob. No separate release/deployed baseline inspected or claimed.
**Profiles**: `python` active (`.py` extension); all four always-load checklists applied. Other profiles non-matching.

## Behavior and Compatibility

Domain model (from `store.py`, `setup.py`):
- `store.pending` — keyed by `setup_id`, tracks in-progress setups (many per workspace possible).
- `store.active` — keyed by `workspace_id`, value `{"setup_id", "connection"}`. **At most one active setup per workspace**, and it carries `setup_id` specifically to record *which* setup owns that active slot.

`cleanup_setup(store, workspace_id, setup_id)` contract (base): remove the pending entry for `setup_id`, and remove the active association **only if the currently-active setup is this one** (`association["setup_id"] == setup_id`).

The diff drops that ownership guard and pops `active[workspace_id]` unconditionally.

Traced scenarios:
- **Cleanup of the active setup** (`active=one`, `cleanup(w, one)`): base and candidate both clear it. ✓ — this is the only path the existing test `test_cleanup_removes_its_own_association` exercises, so it still passes. Green test does **not** prove correctness here.
- **Cleanup of a non-active setup while another is active** (`active=one`, then `begin_setup(w, two)`, then `cleanup(w, two)`): base keeps `one` active (`active_connection(w) == "connection-one"`); candidate **evicts `one`** (`active_connection(w) == None`). ✗ **Regression** — cleaning up a superseded/failed setup destroys an unrelated workspace's live connection.

Compatibility: **Blocked** for the multi-setup-per-workspace flow — in-scope behavioral regression introduced by this change. Not applicable: no deployment/migration/persistence surface (pure in-memory dict mutation). No security dimension affected.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[cleanup.py:3]** Unconditional `store.active.pop` drops a load-bearing ownership guard
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / None-vs-ownership) + generic SOLID/behavior
  - Triggered by: content — `.py` extension; removed `if association and association["setup_id"] == setup_id` guard around a keyed delete
  - Trigger/path: `active[workspace_id] = {"setup_id": "one", ...}`; call `cleanup_setup(store, workspace_id, "two")` (cleaning up a different, e.g. failed/superseded, setup for the same workspace). Expected (base): active `one` is preserved, `active_connection` still returns `"connection-one"`. Actual (candidate): active `one` is evicted, `active_connection` returns `None`.
  - Consequence: cleaning up any non-active setup silently tears down the workspace's live active connection — functional outage for that workspace until re-setup. The `active` value stores `setup_id` precisely to disambiguate slot ownership; deleting keyed only by `workspace_id` ignores that ownership. Recoverable (re-run setup), in-memory state only → P1, not P0.
  - Confidence: 88% — the data model (per-workspace single active slot carrying `setup_id`) and the deleted guard make the intended ownership check unambiguous; storing `setup_id` in the active value would be pointless if cleanup never ran for a non-active setup. Residual uncertainty: I have no caller outside tests proving the cross-setup call actually occurs in production flows (none exists in this repo).
  - Suggested fix: restore the guard —
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 - Medium

- **[tests/test_setup.py:14]** Test coverage gap masks the regression
  - Profile: python · Checklist: code-quality-checklist.md
  - The only cleanup test cleans up the *same* setup that is active, so it passes under both base and buggy candidate. There is no test for "cleanup of a non-active setup leaves the active one intact," which is exactly the invariant the guard protects.
  - Confidence: 95% — directly observed from the single test.
  - Suggested fix: add a test — `begin/complete(w, one)`, `begin(w, two)`, `cleanup(w, two)`, assert `active_connection(w) == "connection-one"` and `"two" not in store.pending`.

### P3 - Low

(none)

---

## Coverage and limits

- **Checked**: full `cleanup.py` diff, the complete contract via `store.py`/`setup.py`, the one call site (`tests/test_setup.py`), and a grep for all `cleanup_setup` / `.active` / `.pending` / `setup_id` references in the repo.
- **Not covered**: no production/non-test caller of `cleanup_setup` exists in this repo, so the frequency/reachability of the cross-setup cleanup path in a real deployment is **Unknown** (named limit; the guard's existence and the data model are the evidence that it's intended). No runtime execution performed — reasoning is source-based.
- **Indexed**: P1 finding recorded as `kk:review-findings` (load-bearing-guard-removed-in-simplification pattern).

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

Actionable items I recommend fixing:
1. **P1** — Restore the ownership guard in `cleanup.py:3` so cleanup only evicts the active association it owns.
2. **P2** — Add the cross-setup regression test in `tests/test_setup.py`.

Items I recommend keeping as is:
- Removing the pending `pop` line's surrounding behavior is fine — `store.pending.pop(setup_id, None)` is correct and unchanged.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Note: this is a review-first workflow — I won't change anything until you confirm.
