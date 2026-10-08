Review complete. Here are the results.

## Code Review Summary

**Files reviewed**: 1 file (`cleanup.py`), 4 lines changed (1 insertion, 3 deletions)
**Overall assessment**: **REQUEST_CHANGES**

The staged change removes a guard and replaces a scoped deletion with an unconditional one. This is not a behavior-preserving simplification — it introduces a correctness regression.

---

## Findings

### P0 - Critical

- **[cleanup.py:3]** Unconditional `active.pop` lets a stale cleanup clobber the current active association
  - Profile: python · Checklist: security-checklist.md (Race Conditions → Check-Then-Act / Data Integrity → Lost updates) + solid-checklist.md (Dead code heuristic misapplied)
  - Triggered by: content — `.py` extension (python profile)
  - **The removed guard was load-bearing.** `store.active` is keyed by `workspace_id` with a single slot (`store.py:4`), and `complete_setup` (`setup.py:6`) *overwrites* that slot — so a newer setup supersedes an older one for the same workspace. The original code only removed the active association **if it still belonged to this `setup_id`**. The new code removes it unconditionally.
  - **Failure scenario:**
    1. `complete_setup(store, "w", "one", conn1)` → `active["w"] = {setup_id: "one", conn1}`
    2. `complete_setup(store, "w", "two", conn2)` → `active["w"] = {setup_id: "two", conn2}` (setup "two" is now the legitimate active connection)
    3. `cleanup_setup(store, "w", "one")` — a late/stale cleanup of the superseded setup
       - *Before:* `active["w"].setup_id == "two" != "one"` → association left intact. ✅
       - *After:* `active["w"]` popped unconditionally → `active_connection("w")` returns `None`, silently dropping the **valid, current** connection for setup "two". ❌
  - This is a lost-update / clobber bug (data loss of live active state); it also widens any TOCTOU window between supersede and cleanup. It also makes the `setup_id` parameter meaningless for the `active` deletion, defeating the purpose of passing it.
  - Confidence: 95% — verified against `store.py`, `setup.py`, and `cleanup.py`; the data model (coarse `workspace_id` key vs. fine `setup_id` identity) and the overwrite in `complete_setup` confirm the superseding path is reachable through the public API. Remaining 5%: I can't see production callers (only the test imports it), so I can't prove the superseding sequence occurs in practice — but the guard existed precisely to handle it.

::code-comment{file="cleanup.py" line="3" severity="P0"}
Unconditional `store.active.pop(workspace_id, None)` drops the active association even when it belongs to a newer, superseding setup. Restore the ownership guard so a stale cleanup only removes its own association:

```python
def cleanup_setup(store, workspace_id, setup_id):
    store.pending.pop(setup_id, None)
    association = store.active.get(workspace_id)
    if association and association["setup_id"] == setup_id:
        store.active.pop(workspace_id, None)
```
::

### P1 - High

(none)

### P2 - Medium

- **[tests/test_setup.py:14]** Test coverage gap masked the regression
  - Profile: python · Checklist: code-quality-checklist.md (boundary/edge cases)
  - Triggered by: content — `.py` extension
  - `test_cleanup_removes_its_own_association` only exercises the case where the active setup *is* the one being cleaned up, so it passes against both the buggy and correct versions. The guard's actual purpose — *ignoring* a stale cleanup when a newer setup is active — is untested. Green tests here do not imply the removed guard was dead code.
  - Confidence: 90%
  - Suggested fix: add a test that completes setup "one", completes "two" for the same workspace, then calls `cleanup_setup(store, "w", "one")` and asserts `active_connection(store, "w") == "connection-two"`. This test fails on the current staged code and passes once the guard is restored.

### P3 - Low

(none)

---

## Findings indexed

Indexed the P0 as a systemic `kk:review-findings` pattern: *ownership-guard removal in keyed-slot cleanup* — scoping a mutation to the owning id is load-bearing when shared state is keyed by a coarser key.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P0** — Restore the `setup_id` ownership guard in `cleanup.py:3` (fix above).
2. **P2** — Add the superseding-setup regression test in `tests/test_setup.py`.

Items I recommend keeping as is:
- The `store.pending.pop(setup_id, None)` line is correct and unaffected — `pending` is keyed by `setup_id`, so unconditional pop there is right.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P0 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Note: this change is staged. I'd recommend not merging it as-is — the "simplification" is a correctness regression. Let me know how you'd like to proceed.
