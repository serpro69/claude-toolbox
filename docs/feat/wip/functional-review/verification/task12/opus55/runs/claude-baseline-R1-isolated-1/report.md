## Review Summary (Isolated Mode, reduced)

**Reviewers**: code-reviewer (Claude sub-agent) only. The `pal` MCP server failed to connect, so there was no second-model review and nothing could be corroborated.
**Files reviewed**: 1 file (`cleanup.py`, 3 lines)

Bash is denied in this session, so I couldn't run `git diff --cached` to see the old `cleanup.py`. The reviewer judged the staged version against `store.py`, `setup.py`, the tests and the contract in `README.md`. Active profile: python (security, SOLID, code-quality and removal-plan checklists).

---

### Code Reviewer Findings

- **`cleanup.py:3`** Cleanup deletes the workspace's active association even when another setup owns it
  - Profile: python · Checklist: security-checklist.md (data integrity / event ordering)
  - Triggered by: file_extension — cleanup.py
  - Severity: **P0** | Confidence: 95%
  - The README says another setup can complete before a failed job's queued cleanup runs, and that cleanup removes only an association the failed setup *owns*. `store.active.pop(workspace_id, None)` doesn't check the owner. Sequence: setups A and B both start → A fails → B completes and sets `active["w"]` → A's cleanup runs and removes B's association → `active_connection("w")` returns `None`. B's successful setup is silently lost.
  - Fix: the owner is already stored in `active[workspace_id]["setup_id"]` (`setup.py:6`), so check it before deleting:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association is not None and association.get("setup_id") == setup_id:
            del store.active[workspace_id]
    ```

- **`tests/test_setup.py:14`** No test covers the out-of-order cleanup case, so the P0 passes the suite
  - Profile: python · Checklist: code-quality-checklist.md
  - Severity: **P1** | Confidence: 95%
  - The only cleanup test runs cleanup for the setup that owns the association. The old guarded code and this simplified version both pass it.
  - Fix: add a regression test:
    ```python
    def test_stale_cleanup_does_not_remove_newer_association(self):
        store = Store()
        begin_setup(store, "w", "one")
        begin_setup(store, "w", "two")
        complete_setup(store, "w", "two", "connection-two")
        cleanup_setup(store, "w", "one")
        self.assertEqual(active_connection(store, "w"), "connection-two")
        self.assertNotIn("one", store.pending)
    ```
    Also worth adding: a setup that fails before any association exists, where cleanup should only remove the pending record.

### Author-Sourced Findings

I didn't write this change, so I have no author context to add. One observation from reading the code:

- **`setup.py:10`** README and code disagree on "consumed" ⟨author-sourced⟩
  - Profile: generic · Checklist: —
  - The README says completed associations are "consumed by `active_connection`", but `active_connection` only reads them and never removes them. This is outside this diff, and the owner-check fix is correct either way. Still, either the docs or `setup.py` should be brought into line.

**Indexing**: the P0 is a reusable pattern (cleanup deleting by a shared key without checking the owner). I saved it to the capy knowledge base under `kk:review-findings`.

---

## Next Steps

There are 3 issues: 2 from code-reviewer (one P0, one P1) and 1 I noticed myself (P3). None are corroborated because pal didn't run.

I recommend fixing:
1. **P0** (code-reviewer): restore the owner check in `cleanup_setup`. As staged, the simplification breaks the documented contract.
2. **P1** (code-reviewer): add the out-of-order cleanup regression test, so the guard can't be removed again without a test failing.
3. **P3** (author-sourced): make the README and `setup.py` agree on what "consumed" means.

To get a real two-reviewer run, reconnect the `pal` server and allow `git` in Bash, then run this command again.

**How would you like to proceed?**
1. **Fix all**
2. **Fix corroborated + high severity**: the P0 and P1
3. **Fix specific items**
4. **No changes**
