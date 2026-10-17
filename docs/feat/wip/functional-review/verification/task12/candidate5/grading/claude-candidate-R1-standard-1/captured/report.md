Finding indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (+1/−3)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Stated intent — simplify `cleanup_setup` in `cleanup.py`. Requirement source — `README.md` ("Workspace associations" contract). Selected diff — **staged** changes only (nothing unstaged); candidate state = git index blob of `cleanup.py`.
**Baselines**: Review base `a7ab15e` (HEAD) → staged candidate. No separate release baseline involved.

## Behavior and Compatibility

Traced the full module set: `store.py` (`pending`/`active` are plain dicts), `setup.py` (`begin_setup`/`complete_setup`/`active_connection`), `cleanup.py`, and `tests/test_setup.py`.

The change removes the ownership guard:

```python
# before
association = store.active.get(workspace_id)
if association and association["setup_id"] == setup_id:
    store.active.pop(workspace_id, None)
# after
store.active.pop(workspace_id, None)
```

The README states the contract precisely: *"Cleanup removes the failed setup's pending record and **any association it owns**"* — and explicitly describes the decisive interleaving: *"Another setup can complete before the failed job's queued cleanup runs."* This is a **serialized** sequence (the README scopes concurrency out, but this ordering is plain sequential, so it is in scope).

**Scenario trace** (contract → state → op → expected vs candidate):
1. `begin_setup(w, "one")` → `"one"` pending; setup "one" fails.
2. Before its queued cleanup runs: `complete_setup(w, "two", "conn-two")` → `active["w"] = {setup_id:"two", connection:"conn-two"}`.
3. `cleanup_setup(w, "one")` runs (the failed job's queued cleanup).
   - **Expected** (owns-only): `"two" != "one"` → `active["w"]` untouched → `active_connection(w) == "conn-two"`.
   - **Candidate**: unconditional `active.pop("w")` → `active_connection(w) == None`. The newer, valid setup's live connection is destroyed.

- **Correctness (sequential ownership)**: **Blocked** — candidate violates the documented "association it owns" invariant; deterministic from dict semantics (runtime confirmation not needed; an ad-hoc repro was sandbox-denied but the trace is airtight).
- **Same-setup cleanup path**: **Supported** — when the active association belongs to `setup_id`, both versions pop it; `test_cleanup_removes_its_own_association` covers this.
- **Pending removal (`store.pending.pop`)**: **Not applicable** — unchanged.
- **Concurrency / external services**: **Not applicable** — README scopes these out; the finding is a serialized-ordering bug, not a race.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[cleanup.py:3]** Dropping the ownership guard lets a stale setup's cleanup wipe a newer setup's active association
  - Profile: python · Checklist: solid-checklist.md (check-then-act / dead-code misjudgment), code-quality-checklist.md (boundary/ownership)
  - Triggered by: content — `.py` file; removed `association["setup_id"] == setup_id` guard before `active.pop`
  - Trigger/path: failed setup "one" → setup "two" completes for the same workspace → queued `cleanup_setup(store, "w", "one")` runs. Expected: `active_connection("w") == "conn-two"`. Actual: `None` — "two"'s live connection is lost.
  - Consequence: data loss of a valid active workspace connection; violates the README contract "removes … any association **it owns**." Recoverable only by re-running setup.
  - Confidence: **95%** — Verified by reading all four modules and tracing dict operations; the README documents both the invariant and the exact interleaving, so the path is reachable by design. Residual 5%: whether the real caller ever schedules "one"'s cleanup after "two" completes — but the README asserts it does.
  - Suggested fix: restore the guard (keep the simplification of `pending.pop`, which is safe):
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 - Medium

- **[tests/test_setup.py:14]** Test coverage gap masks the regression
  - Profile: python · Checklist: code-quality-checklist.md (boundary conditions)
  - Triggered by: — (generic, tied to the P1)
  - The suite only exercises the same-setup cleanup path, so it stays green against the buggy code. There is no test for "cleanup of setup A must not remove setup B's active association."
  - Confidence: 90% — confirmed by reading the full test file (2 tests).
  - Suggested fix: add a test reproducing the step-2/step-3 interleaving above and asserting `active_connection(store, "w") == "conn-two"` after `cleanup_setup(store, "w", "one")`. This test fails on the candidate and passes once the guard is restored.

### P3 - Low

(none)

---

## Coverage and limits

- **Checked**: full behavior trace across `cleanup.py`, `setup.py`, `store.py`, `tests/test_setup.py`, and the README contract; existing suite runs green (2 passed); all four Python checklists (security, SOLID, code-quality, removal) applied.
- **Security**: no concerns — plain in-memory dict ops, no user input, injection, deserialization, or secret surface.
- **Not covered / residual risk**: could not execute an ad-hoc repro script (sandbox denied non-test execution); relied on deterministic code tracing. Did not inspect any caller that enqueues cleanup jobs (none exists in this repo — `cleanup_setup` is only referenced by the test), so the ordering guarantee rests on the README's stated behavior.

**Indexed**: the P1 pattern (load-bearing ownership guard dropped during "simplification") was indexed to `kk:review-findings`.

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P1** — Restore the `setup_id` ownership guard in `cleanup.py` before the `active.pop`.
2. **P2** — Add a regression test for the cross-setup interleaving.

Items I recommend keeping as is:
- The `store.pending.pop(setup_id, None)` simplification is unaffected and correct — keep it.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions.
