Indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file, +1/−3 lines (`cleanup.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: User-described "cleanup simplification" — collapse the guarded active-association removal in `cleanup_setup` into a single unconditional `pop`. Selected diff: **staged** changes only (no unstaged changes). Candidate = index blob of `cleanup.py`.
**Baselines**: Review base `a7ab15e` ("Review base"); candidate = staged index. No release/deployment baseline in play (in-memory store, local module). No `docs/feat/wip/` feature — shape 3, review on its own merits.

## Behavior and Compatibility

The change removes an **ownership guard**, not just dead code:

```python
# before
store.pending.pop(setup_id, None)
association = store.active.get(workspace_id)
if association and association["setup_id"] == setup_id:   # guard: only clear OUR association
    store.active.pop(workspace_id, None)
# after
store.pending.pop(setup_id, None)
store.active.pop(workspace_id, None)                       # clears whatever is active, unconditionally
```

Tracing against the collaborating module (`setup.py`):
- `complete_setup` does `store.active[workspace_id] = {"setup_id": ..., "connection": ...}` — it **overwrites** per workspace, so a later setup supersedes an earlier one.
- `begin_setup` places multiple setups in `pending` for the same workspace.
- `active_connection(store, w)` reads `store.active[w]["connection"]`.

**Reachable regression** (source-traced; execution was denied by sandbox, so this is source-only evidence, not an executed repro):

1. Supersession: `begin/complete "one"` → active[w]=one. `begin/complete "two"` → active[w]=two. Then `cleanup_setup(store, w, "one")` (old setup times out).
   - *Before*: active["setup_id"]=="two" ≠ "one" → active preserved (conn **two** still live). ✅
   - *After*: `active.pop(w)` unconditionally → **live "two" association evicted**, `active_connection` returns `None`. ❌
2. Cancelled pending: `begin/complete "one"` → active[w]=one. `begin "two"` (pending, never completed). Then `cleanup_setup(store, w, "two")` (cancel pending two).
   - *Before*: "one" ≠ "two" → active **one** preserved. ✅
   - *After*: `active.pop(w)` → **unrelated live "one" evicted**. ❌

- **Compatibility — single-setup-per-workspace flow:** Supported. Matches existing behavior and the one green test.
- **Compatibility — concurrent/superseded/cancelled setups per workspace:** **Blocked** — the change silently drops a live connection association.

The existing test `test_cleanup_removes_its_own_association` stays green because it only cleans up the *same* setup that is active; it never exercises the cross-setup case the guard protected. Green test ≠ preserved contract.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[cleanup.py:3]** Unconditional `store.active.pop` evicts another setup's live association
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / state ownership) + functional-review (contract preservation)
  - Triggered by: content — `.py` extension activates the python profile
  - **Trigger/path**: `cleanup_setup(store, w, old_or_cancelled_setup_id)` when `store.active[w]` belongs to a *different* (current) setup. **Expected**: only the active association owned by `setup_id` is cleared (the removed guard). **Actual**: the workspace's current active association is removed regardless of owner → `active_connection(store, w)` returns `None`, dropping a live connection. **Consequence**: silent state loss / spurious disconnect; a stale or cancelled setup's cleanup corrupts the live one.
  - Confidence: 90% — behavior change is unambiguous from the diff; reachability confirmed by tracing `complete_setup`/`begin_setup`. Residual 10%: possibility the author *intends* cleanup to always clear the workspace — but the retained `setup_id` parameter, the original guard, and the setup_id-tagged active record all indicate the guard was the correct contract.
  - **Suggested fix**: restore the ownership guard.
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```
    If a genuinely simpler form is desired while preserving behavior:
    ```python
        if store.active.get(workspace_id, {}).get("setup_id") == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 - Medium

- **[tests/test_setup.py:14]** Test coverage gap masks the regression
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions)
  - The suite only covers cleanup of the *currently active* setup. There is no test for cleaning up a superseded or cancelled setup while another is active — exactly the case the guard protected. This is why the removal looks safe.
  - Confidence: 95%.
  - **Suggested fix**: add a test asserting that `cleanup_setup(store, "w", "one")` after `"two"` became active leaves `active_connection(store, "w") == "connection-two"`.

### P3 - Low

(none)

---

## Removal/Iteration Plan

The deleted lines were **not** dead/redundant code — they encoded a required ownership check. This is not a safe removal; recommend reverting the guard removal (see P1) rather than staging it for deletion.

## Coverage & Limits

- **Checked**: full `cleanup.py` diff and staged blob; collaborators `setup.py`, `store.py`; existing test. Applied python security, SOLID, code-quality, and removal checklists plus the common functional method.
- **Security checklist**: no injection/secret/crypto/authz surface in this diff — Not applicable.
- **Not executed**: Bash/pytest was denied in this session, so findings are source-trace only (not a live repro). The logic is simple enough that the trace is conclusive; running the two scenarios above would confirm.
- **Residual risk**: product intent for `cleanup_setup` (owner-scoped vs. workspace-wide clear) is inferred, not documented — see P1 confidence note.

**Indexed**: 1 P1 systemic pattern to `kk:review-findings` ("simplification drops ownership guard before a mutation → evicts unrelated state").

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

Actionable items I recommend fixing:
1. **P1** — Restore the ownership guard in `cleanup.py` (or the preserving one-liner variant).
2. **P2** — Add the superseded-setup regression test in `tests/test_setup.py`.

Items to keep as-is:
- Removing `store.pending.pop(setup_id, None)`'s surrounding structure is fine — that line is unchanged and correct.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

If you believe `cleanup_setup` is *meant* to clear the workspace unconditionally, tell me — then the `setup_id` parameter and the test name both become misleading and I'd flag those instead.
