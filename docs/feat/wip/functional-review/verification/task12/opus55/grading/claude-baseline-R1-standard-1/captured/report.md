## Code review summary

**Files reviewed:** 1 file (`cleanup.py`), 4 lines changed (+1/−3)
**Overall assessment:** REQUEST_CHANGES. This change is a bug fix in disguise as a simplification; it breaks behaviour. Don't merge it as is.

**Profiles:** `cleanup.py` activates the `python` profile (`.py` extension), so its security, SOLID, code-quality and removal-plan checklists were applied. No other profile matched, and none of them had content-dependent checklists to resolve.

---

## Findings

### P0 – Critical

- **`cleanup.py:3`: Cleanup now deletes another setup's active connection**
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions) / security-checklist.md (Data Integrity)
  - Triggered by: content, `.py` extension
  - The old code was a compare-and-delete. It removed `store.active[workspace_id]` only if that association belonged to the `setup_id` being cleaned up. The new code always removes the workspace's association, whichever setup owns it. Because `store.active` is keyed by workspace and `cleanup_setup` is meant to clean up one setup, the check was doing real work.
  - I ran both scenarios against the staged code and both lose a working connection:
    1. **Cancelling a re-setup:** complete setup `one` (`conn-one`), start setup `two`, then cancel it with `cleanup_setup(s, 'w', 'two')`. `active_connection` returns `None`. Before the change it returned `conn-one`.
    2. **Cleaning up a replaced setup:** complete `one`, then complete `two`, then `cleanup_setup(s, 'w', 'one')`. `active_connection` returns `None`. Before the change it returned `conn-two`.
  - Confidence: 92%. I reproduced both cases. The remaining doubt is whether callers outside this repo only ever pass the current active `setup_id`. The function takes `setup_id` and is named per-setup, which says they don't.
  - Suggested fix: revert to the guarded version.
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 – Medium

- **`tests/test_setup.py:14`: Tests can't catch this regression**
  - Profile: generic · Checklist: —
  - Triggered by: —
  - `test_cleanup_removes_its_own_association` only covers a setup cleaning up its own association. That path behaves the same with or without the check, so this change passes the existing tests unnoticed.
  - Confidence: 95%. Checked by reading the code. I couldn't run the test suite because the second Bash call was denied.
  - Suggested fix: add tests for both scenarios above, asserting that `active_connection` still returns the other setup's connection.

### P1 / P3
None.

---

## Notes
- No security, SOLID, or performance problems in the change itself.
- The original get-then-pop isn't atomic. It would race under concurrent access, but nothing in the repo is concurrent, so that's a note rather than a finding.
- I saved the "simplification dropped the ownership check" pattern to the review-findings knowledge base so future reviews can recognise it. The knowledge base was empty before this, so there were no earlier findings to compare against.

---

## Next steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

Recommended fixes:
1. **P0:** restore the ownership check in `cleanup_setup`.
2. **P2:** add regression tests for cancelling a re-setup and cleaning up a replaced setup.

**How would you like to proceed?**
1. **Fix all:** I'll make both fixes.
2. **Fix P0/P1 only:** I'll restore the check only.
3. **Fix specific items:** tell me which.
4. **No changes:** the review is complete.
