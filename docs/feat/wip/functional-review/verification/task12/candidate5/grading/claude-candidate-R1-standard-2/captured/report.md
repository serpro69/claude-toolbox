Now the review report (Step 9).

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (+1 / −3)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Staged "cleanup simplification" of `cleanup_setup` in `cleanup.py`. Requirement source is the repo `README.md` (the component contract). Selected diff = staged changes only (no unstaged changes present); candidate = git index blob of `cleanup.py`.
**Baselines**: Review base = commit `a7ab15e` ("Review base"); candidate = staged version. No separate release baseline applies.
**Profile**: `python` (active via `.py` extension). Checklists applied: security, SOLID, code-quality, removal-plan. Capy KB empty (cold start) — standard guidance used.

## Behavior and Compatibility

The change removes the ownership guard before evicting a workspace's active association:

```python
# before                                        # after
association = store.active.get(workspace_id)
if association and association["setup_id"] == setup_id:
    store.active.pop(workspace_id, None)        store.active.pop(workspace_id, None)
```

The README states the contract precisely: *"A workspace has one active setup association. Another setup can complete before the failed job's queued cleanup runs… Cleanup removes the failed setup's pending record **and any association it owns**."* The deleted `if association["setup_id"] == setup_id` check **is** the "association it owns" semantics. The simplification makes the pop unconditional, so a stale cleanup now evicts an active association owned by a *different* setup.

**Scenario traced** (by inspection; ad-hoc reproduction was denied by sandbox, project `unittest` suite was run and passes):

| contract/source | initial state | operation | expected | candidate result | evidence |
|---|---|---|---|---|---|
| README L4–7 | setup A pending (job failed, cleanup queued); setup B then completes → `active["w"]={setup_id:"B"}` | `cleanup_setup(store,"w","A")` | `active["w"]` keeps B; `active_connection="connection-B"` | `active["w"]` popped → `active_connection=None` | trace of `cleanup.py:3` + `setup.py:6,11` |

- **Correctness (in-scope):** **Blocked** — the change breaks the documented "removes any association it owns" invariant for the exact race the README calls out.
- **Concurrency:** **Not applicable** — README explicitly scopes the store to serialized operations, so the guard's non-atomic get-then-pop is out of scope.
- **Test coverage:** `test_cleanup_removes_its_own_association` cleans up a setup's *own* association, so it passes under both versions and cannot detect this regression.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[cleanup.py:3]** Unconditional `active.pop` evicts another setup's live association
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / None-vs-missing; also general correctness)
  - Triggered by: content — `.py` extension; contract from `README.md:4–7`
  - Trigger/path: `begin_setup(w,A)` (A fails, cleanup queued) → `complete_setup(w,B,conn-B)` → `cleanup_setup(w,A)`. Expected: B's association preserved (`active_connection=="connection-B"`). Actual: `active["w"]` is popped unconditionally → `active_connection` returns `None`, silently orphaning a workspace that has a completed, live setup. Consequence: data/availability loss for the workspace; the live connection disappears with no error.
  - Confidence: 97% — plain dict operations, deterministic; the removed guard maps one-to-one onto the README's "any association it owns" wording; execution of the exact scenario was blocked but the trace is unambiguous.
  - Suggested fix: restore the ownership guard:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 - Medium

- **[tests/test_setup.py:14]** Missing regression test for the documented cross-setup scenario
  - Profile: generic · Checklist: —
  - The suite never exercises "setup B completes before setup A's stale cleanup," which is the one scenario the README highlights and the only one that distinguishes correct from incorrect behavior. Without it, this exact regression ships green.
  - Confidence: 90% — verified by reading the two tests; both pass against the buggy version.
  - Suggested fix: add a test asserting that after `complete_setup(w,"B",…)`, calling `cleanup_setup(w,"A")` leaves `active_connection(store,"w") == "connection-B"` and clears `pending["A"]`.

### P3 - Low

(none)

---

## Removal/Iteration Plan

The deleted guard is **not** a safe removal candidate: it encodes the required "association it owns" invariant, not redundant verbosity. The correct iteration is to *restore* it (P1) and add the discriminating test (P2).

---

## Coverage and limits

- **Checked:** full staged diff and complete current `cleanup.py`; the contract (`README.md`); all consumers/producers of `store.active`/`store.pending` (`setup.py`, `store.py`); both existing tests; security, SOLID, and code-quality checklists.
- **Ran:** project `unittest` suite (2 tests, pass) — confirms tests don't catch the bug.
- **Not covered / limits:** an ad-hoc scenario-reproduction script was denied by the sandbox, so the P1 scenario is established by code trace + the contract rather than live execution (confidence remains high — deterministic dict logic). No concurrency assessment (explicitly out of scope per README). No other callers of `cleanup_setup` exist in the repo.

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P1** — Restore the ownership guard in `cleanup_setup` so cleanup only evicts the association it owns.
2. **P2** — Add a regression test for "another setup completes before the stale cleanup runs."

Items I recommend keeping as is:
- The `pending.pop(setup_id, None)` line is correct and unchanged.
- No concurrency hardening needed — README scopes the store to serialized operations.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

I recommend **option 1**. This "simplification" is a correctness regression: it deletes the invariant the README explicitly specifies, and the existing tests pass anyway — so it would ship silently. Please choose an option or give specific instructions.
