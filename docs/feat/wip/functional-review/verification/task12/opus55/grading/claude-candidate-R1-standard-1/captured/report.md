## Code review: staged `cleanup.py` simplification

**Overall assessment: REQUEST_CHANGES.** The change makes `cleanup_setup` delete a different setup's active association.

**Files reviewed:** 1 file (`cleanup.py`), 1 line added and 3 removed.

**Intent and scope:** The requirement comes from `README.md`: "Cleanup removes the failed setup's pending record and any association it owns." The README also notes that "another setup can complete before the failed job's queued cleanup runs." There is no `docs/feat/wip` task scope, so I reviewed the diff on its own merits against the README.

**Baselines:** I compared the staged index blob of `cleanup.py` against `HEAD` (`a7ab15e`). There's no release baseline to compare.

**How the review was set up:** The `python` profile matched on the `.py` extension, so I applied its security, SOLID, code-quality and removal-plan checklists. No other profile matched.

## Behaviour and compatibility

| Scenario | Expected (README) | Before | After the staged change |
| --- | --- | --- | --- |
| Setup A completes, then cleanup(A) | A's association is removed | Removed ✔ | Removed ✔ |
| A fails while pending, no active association | Only the pending record is removed | ✔ | ✔ (`pop` with a default is a no-op) |
| A begins, B begins and completes, then A's queued cleanup runs | B's association survives | Survives ✔ (setup_id doesn't match) | **B's association is deleted ✘** |

- **Unchanged consumer:** `active_connection` (`setup.py:10`) returns `None` for the workspace after the third scenario, so a successfully completed setup disappears.
- **Persisted data / rollout:** Not applicable. The store is in-memory and the README excludes concurrency and external services from this change.

## Findings

### P1 (high)

- **[cleanup.py:3] Cleanup deletes an association it doesn't own**
  - Profile: python · Checklist: security-checklist.md (Data Integrity / check-then-act) · Triggered by: content, `.py` extension. Also covered by the generic functional method.
  - **Trigger:** `begin_setup(w, "A")`, then `begin_setup(w, "B")`, then `complete_setup(w, "B", conn)`, then A fails and `cleanup_setup(store, w, "A")` runs.
  - **Expected:** `active[w]` still belongs to B and `active_connection(w) == conn`.
  - **Actual:** `store.active.pop(workspace_id, None)` runs unconditionally. B's connection is lost and `active_connection` returns `None`.
  - **Consequence:** A setup that completed successfully is silently undone. This is exactly the ordering the README documents.
  - **Why the tests miss it:** `tests/test_setup.py` only covers cleanup of the setup's own association, so both tests still pass with this change.
  - **Confidence: 95%.** I traced it by hand through `setup.py` and `cleanup.py`, and the README states the contract explicitly. The remaining uncertainty is only that I couldn't run the tests.
  - **Suggested fix:** Keep the ownership check, which is the code in `HEAD`. If you still want it shorter, use something like:
    ```python
    if store.active.get(workspace_id, {}).get("setup_id") == setup_id:
        store.active.pop(workspace_id)
    ```
    Also add a test where another setup completes before the failed setup's cleanup runs, and assert that `active_connection` still returns the other setup's connection.

### P0, P2, P3

None.

## Coverage and limits

- **Checked:** the staged diff, the staged and `HEAD` versions of `cleanup.py`, `store.py`, `setup.py`, `tests/test_setup.py` and `README.md`. The Python checklists had nothing else to flag: no injection or secrets risk, no broad exception handling, and nothing to remove.
- **Not executed:** the tests. Running shell commands was denied in this session, so the evidence is from reading the source only.
- **Knowledge base:** The `kk:review-findings` and `kk:lang-idioms` searches found nothing because the knowledge base is empty. I indexed this P1 finding under `kk:review-findings` as a recurring pattern (a cleanup that deletes a shared slot without checking ownership).

## Next step

Restore the ownership check (or use the shorter form above) and add the test where another setup completes first. I haven't changed any files. If you want me to apply the fix and the test, let me know.
