## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (1 insertion, 3 deletions) — `cleanup.py`
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The user staged a "cleanup simplification" of `cleanup_setup`. Authoritative intent comes from `README.md` (unchanged, part of the review base): *"Cleanup removes the failed setup's pending record and any association **it owns**."* Scope is the staged diff to `cleanup.py` only; `store.py`, `setup.py`, `tests/`, `README.md` are unchanged context.
**Baselines**: Review base = `HEAD` (a7ab15e "Review base"); candidate = staged index. Note: git content commands (`diff`/`show`/`log -p`) were blocked by the harness permission mode, so I could not inspect the exact deleted lines — but the diff stat (1 insertion, 3 deletions, candidate = 3 lines) and the README contract are sufficient to judge the change. The finding does not depend on the removed source.

## Behavior and Compatibility

Candidate:
```python
def cleanup_setup(store, workspace_id, setup_id):
    store.pending.pop(setup_id, None)
    store.active.pop(workspace_id, None)   # unconditional
```

Data model (`setup.py`/`store.py`): `store.active[workspace_id] = {"setup_id": ..., "connection": ...}` — the active record **records which setup_id owns it**. That `setup_id` field exists precisely so cleanup can check ownership.

Tracing the **documented** scenario (README: *"Another setup can complete before the failed job's queued cleanup runs"*), in purely serialized order:

1. `begin_setup(store, "w", "one")` → setup "one" pending; then it fails, cleanup queued.
2. `begin_setup(store, "w", "two")` → pending "two".
3. `complete_setup(store, "w", "two", "conn-two")` → `active["w"] = {setup_id:"two", connection:"conn-two"}`.
4. Queued `cleanup_setup(store, "w", "one")` runs → pops `pending["one"]` ✓, then pops `active["w"]` ✗ — **destroying setup "two"'s valid, completed association**.
5. `active_connection(store, "w")` → `None` (should be `"conn-two"`).

This is a silent correctness/data-loss regression on the exact scenario the README says cleanup exists to handle. This is **not** a concurrency issue (README explicitly scopes concurrency out, and the bug reproduces in serialized order) — so no race-condition finding is raised.

- **Supported**: single-setup happy path (begin → complete → cleanup) — baseline review base, covered by `test_cleanup_removes_its_own_association`.
- **Blocked**: the documented interleaving (failed setup's cleanup after another setup completes for the same workspace) — the change violates the "any association **it owns**" contract.

---

## Findings

### P0 - Critical

- **[cleanup.py:3]** `cleanup_setup` unconditionally pops `store.active[workspace_id]`, clobbering an association owned by a *different* setup
  - Profile: python · Checklist: code-quality-checklist.md (boundary/correctness) + functional-review (documented-scenario trace)
  - Triggered by: content — `.py` extension (python profile active)
  - **Trigger/path**: failed setup's queued cleanup runs after another setup has completed for the same workspace (README's documented scenario). **Expected**: cleanup removes `active[workspace_id]` only if that record's `setup_id` matches the one being cleaned up. **Actual**: it removes it unconditionally. **Consequence**: a valid, completed workspace connection silently disappears; `active_connection` returns `None`. Silent data loss on a documented flow.
  - Confidence: 88% — the README contract ("any association it owns") is unchanged and authoritative; the data model carries `setup_id` in the active record specifically to enable this check; the candidate ignores it. The diff stat (3 deletions → 1 insertion) is consistent with an ownership guard (`get` + `if`) having been collapsed into one unconditional `pop`. Residual uncertainty: I could not read the exact removed lines (git content blocked), and it's conceivable the contract change was intended — but then `README.md` should have been updated in the same change, and it was not.
  - **Suggested fix**:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P1 - High

- **[tests/test_setup.py:14]** Test coverage masks the regression — only the single-setup happy path is exercised
  - Profile: python · Checklist: functional-review (tests must exercise the documented failure/recovery path)
  - Triggered by: content — `.py` extension
  - `test_cleanup_removes_its_own_association` does begin-one → complete-one → cleanup-one, so the unconditional pop looks correct. The README's interleaving scenario (the reason the ownership qualifier exists) is untested, so the suite stays green over the bug. A green, implementation-shaped test does not prove the documented recovery path.
  - Confidence: 92% — directly verified against the test file.
  - **Suggested fix**: add a test — begin "one"; begin "two"; complete "two"; `cleanup_setup(store, "w", "one")`; assert `active_connection(store, "w") == "connection-two"` and `"one" not in store.pending`. This fails on the current candidate and passes with the guarded fix.

### P2 / P3

None. `store.pending.pop(setup_id, None)` is correct and idempotent; no security, SOLID, or other quality issues in this small diff.

---

## Coverage and limits

- **Checked**: the full staged diff, the candidate function against the live data model (`store.py`, `setup.py`), the authoritative contract in `README.md`, and the existing tests. Applied the python security / SOLID / code-quality / removal checklists and the common functional method.
- **Not covered**: I could not read the exact removed lines (harness blocked `git diff`/`show`/`log -p`); the finding stands on the unchanged README contract + data model, not on the removed source. No concurrency analysis (explicitly out of scope per README).
- **Residual risk**: if the contract was *deliberately* changed to "cleanup always clears the active slot," then `README.md` and the ownership-bearing `setup_id` field are now stale and should be updated too — but that reading contradicts the current docs.

**Indexed**: the P0 pattern ("simplification drops an ownership/identity guard before deleting shared state; happy-path test masks it") → `kk:review-findings`.

---

## Next Steps

I found 2 issues (P0: 1, P1: 1, P2: 0, P3: 0).

Recommended fixes:
1. **P0** — restore the ownership guard in `cleanup_setup` before popping `store.active[workspace_id]`.
2. **P1** — add the interleaved-setup test that reproduces the regression.

Items to keep as-is:
- `store.pending.pop(setup_id, None)` — correct and idempotent.

**How would you like to proceed?**

1. **Fix all** — implement both fixes (guard + test)
2. **Fix P0/P1 only** — same as above here
3. **Fix specific items** — tell me which
4. **No changes** — review only

If you'd prefer I confirm against the exact removed lines, re-run me with `git` read access (or paste the original `cleanup_setup`) and I'll verify the reconstruction — though it doesn't change the verdict.
