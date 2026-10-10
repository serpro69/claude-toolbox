Finding indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (1 insertion, 3 deletions)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The user described this as a "cleanup simplification" of `cleanup_setup`. Selected diff = **staged** changes only (no unstaged changes present); candidate state = index blob `:cleanup.py`. No `docs/feat/wip/` feature dir relates to this diff → **no task scope available**; reviewed on its own merits.
**Baselines**: Review base = `HEAD` (`a7ab15e`), candidate = staged index. No separate release baseline inspected.
**Active profile**: `python` (checklists: security, SOLID, code-quality, removal — all applied).

## Behavior and Compatibility

`cleanup_setup` is called to clean up after a setup job. Per `README.md`, the domain contract is explicit:

> "A workspace has one active setup association. Setup jobs can fail after creating a pending record. **Another setup can complete before the failed job's queued cleanup runs.** … Cleanup removes the failed setup's pending record **and any association it owns.**"

The removed code was the ownership guard that enforced "an association **it owns**":

```python
association = store.active.get(workspace_id)
if association and association["setup_id"] == setup_id:
    store.active.pop(workspace_id, None)
```

The simplification replaces this with an **unconditional** `store.active.pop(workspace_id, None)`.

**Traced scenario — the exact interleaving the README calls out:**

1. `begin_setup(store, "w", "one")` → `pending["one"]` created.
2. Setup `"one"` fails; its `cleanup_setup(store, "w", "one")` is **queued**.
3. Before cleanup runs: `begin_setup(store, "w", "two")` + `complete_setup(store, "w", "two", "conn-two")` → `active["w"] = {setup_id: "two", connection: "conn-two"}`.
4. Queued `cleanup_setup(store, "w", "one")` now runs → **unconditionally deletes `active["w"]`**, which belongs to setup `"two"`.
5. `active_connection(store, "w")` returns `None` — a valid, completed connection is silently lost.

The old guard prevented step 4 (it checked `association["setup_id"] == setup_id`, i.e. `"two" == "one"` → False → no delete). The "simplification" removes a **load-bearing** guard, not redundant code. For the empty/own-association cases the behavior is unchanged (both are no-ops / correct deletes); the regression is strictly in the cross-setup interleaving.

- **Compatibility — concurrent/interleaved cleanup**: **Blocked** — the change breaks the documented "another setup completes before queued cleanup" flow against the `HEAD` baseline. (The README notes the store models *serialized* operations, but the interleaving is logical ordering of queued cleanup vs. new setup, not thread concurrency — it applies even single-threaded.)
- **Existing happy-path test**: `test_cleanup_removes_its_own_association` stays **green** — it only exercises cleanup of a setup's *own* association and does not cover the interleaving, so CI will not catch this.

---

## Findings

### P0 — Critical

- **[cleanup.py:3]** Unconditional `store.active.pop` drops an association owned by a different setup (data loss)
  - Profile: python · Checklist: code-quality-checklist.md (Data Integrity / lost updates) + generic correctness
  - Triggered by: content — `.py` extension activated the python profile; finding from functional trace against `README.md` contract
  - Trigger/path: queued cleanup for a failed setup runs after a newer setup completed on the same `workspace_id` → the newer setup's active association is deleted → `active_connection` returns `None` for a live connection.
  - Expected vs actual: expected cleanup to remove *only the association it owns* (guard on `setup_id`); actual removes any association for the workspace unconditionally.
  - Consequence: silent loss of a valid completed connection; the workspace appears to have no active setup.
  - Confidence: **97%** — the README documents this exact interleaving, and the removed guard directly implemented the ownership semantics. Verified store/setup/cleanup source; only residual uncertainty is whether an out-of-repo caller guarantees no interleaving, which the README explicitly contradicts.
  - Suggested fix: restore the ownership guard.
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 — Medium

- **[tests/test_setup.py:14]** Missing test coverage for the cross-setup interleaving
  - Profile: python · Checklist: code-quality-checklist.md (error/boundary coverage)
  - The only cleanup test exercises the happy path (cleanup of own association). There is no test where a second setup completes before the first's cleanup runs — exactly the case this bug breaks. A green implementation-shaped test does not prove the ownership contract.
  - Confidence: 95%.
  - Suggested fix (add alongside the restored guard):
    ```python
    def test_cleanup_ignores_association_owned_by_later_setup(self):
        store = Store()
        begin_setup(store, "w", "one")          # setup "one" begins, then fails
        begin_setup(store, "w", "two")
        complete_setup(store, "w", "two", "conn-two")  # "two" completes first
        cleanup_setup(store, "w", "one")        # queued cleanup for failed "one"
        self.assertEqual(active_connection(store, "w"), "conn-two")
    ```

---

## Coverage and Limits

- **Checked**: full staged diff, `cleanup.py` at the index revision, `store.py`, `setup.py`, `tests/test_setup.py`, `README.md` contract; traced the documented failure/interleave scenario through the unchanged consumer `active_connection`.
- **Not covered**: did not execute the test suite (static trace only); no out-of-repo callers of `cleanup_setup` exist in the tracked tree, so external invocation patterns are assumed per the README.
- **Security/SOLID/removal checklists**: no additional issues — the diff introduces no injection/deserialization/secret/crypto surface and no SOLID structural change beyond the correctness defect above.
- Indexed as `kk:review-findings`: the "dropped ownership guard before destructive pop" pattern.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P0** — Restore the `setup_id` ownership guard in `cleanup_setup` before popping `store.active`.
2. **P2** — Add the interleaving regression test.

Items I recommend keeping as is:
- The `store.pending.pop(setup_id, None)` line and the empty-association no-op behavior are correct and unchanged.

**How would you like to proceed?**

1. **Fix all** — restore the guard + add the regression test
2. **Fix P0 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

This is a review-first workflow — I won't change anything until you confirm.
