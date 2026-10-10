Finding indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 1 file (`cleanup.py`), 3 lines changed (−3 / +1 net)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Staged "cleanup simplification" — collapse `cleanup_setup` so it unconditionally removes the workspace's active association instead of first checking the association belongs to the setup being cleaned up. Selected diff = staged `cleanup.py` (no unstaged changes). No `docs/feat/wip/` relates to this diff → **no task scope available; reviewed on its own merits.**
**Baselines**: Review base `a7ab15e` ("Review base") → staged candidate. No separate release baseline inspected.
**Profile**: `python` (always-load checklists: security, solid, code-quality, removal). Capy KB empty (cold start).

## Behavior and Compatibility

The change:
```python
-    association = store.active.get(workspace_id)
-    if association and association["setup_id"] == setup_id:
-        store.active.pop(workspace_id, None)
+    store.active.pop(workspace_id, None)
```

Tracing the contract (`setup.py`, `store.py`): `store.active` is keyed by **`workspace_id`** and each entry records the **`setup_id`** that owns it (`{"setup_id":..., "connection":...}`). `complete_setup` **overwrites** `active[workspace_id]` — so a workspace's active entry can belong to a *newer* setup than the one a given `cleanup_setup` call is tearing down. The removed guard existed precisely to only delete the active entry when it still belongs to *this* `setup_id`.

- **Data integrity — Supported? No (Blocked).** Scenario: setup `one` completes (`active[w]={one, conn-1}`), then setup `two` completes for the same workspace (`active[w]={two, conn-2}`), then a late/duplicate `cleanup_setup(store, "w", "one")` fires. Base code preserves `conn-2` (guard fails: `"two" != "one"`). Candidate unconditionally pops `active[w]`, **silently discarding the valid `conn-2`** → `active_connection(store,"w")` returns `None`.
- **Same-setup cleanup — Supported.** When the active entry belongs to the setup being cleaned up, both versions behave identically. Both `pop(..., None)` calls remain idempotent.
- **Evidence limit**: no in-repo caller of `cleanup_setup` beyond the test, so the superseding-setup ordering is inferred from the data model, not observed from a live call site. The guard's existence is strong evidence the author intended to handle it.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[cleanup.py:3]** Dropped ownership guard lets a stale cleanup wipe a newer workspace's live connection
  - Profile: python · Checklist: security-checklist.md (Data Integrity / TOCTOU check-then-act) + generic SOLID/correctness
  - Triggered by: content — `.py` activation; behavioral trace of `store.active` ownership
  - Trigger/path: `cleanup_setup(store, w, old_setup_id)` after a newer `complete_setup(store, w, new_setup_id, ...)` → unconditional `store.active.pop(w)` removes the entry owned by `new_setup_id`. Expected: only the old setup's own state is removed and the current connection is preserved; actual: current connection silently dropped (`active_connection` → `None`).
  - Consequence: silent loss of a valid, in-use connection for the workspace; recoverable only by re-running setup. The delete is keyed by `workspace_id` while the caller's intent is scoped to `setup_id` — those are not the same, so ownership must be verified.
  - Confidence: **88%** — the behavioral divergence is certain from the data model; the only uncertainty is real-world reachability of the superseding-setup ordering, which no in-repo caller confirms, but the removed guard indicates it was a handled case.
  - Suggested fix: restore the ownership check, keeping it as a single guarded pop:
    ```python
    def cleanup_setup(store, workspace_id, setup_id):
        store.pending.pop(setup_id, None)
        association = store.active.get(workspace_id)
        if association and association["setup_id"] == setup_id:
            store.active.pop(workspace_id, None)
    ```

### P2 - Medium

- **[tests/test_setup.py:14]** Test coverage does not discriminate the regression
  - Profile: python · Checklist: code-quality-checklist.md (boundary/coverage)
  - `test_cleanup_removes_its_own_association` only exercises the same-setup path, so it stays green under both versions and gave false confidence to the "simplification." There is no test asserting that cleanup of a *superseded* setup leaves the newer active connection intact.
  - Confidence: 95% — directly verifiable from the test file.
  - Suggested fix: add a test — begin/complete `one`, begin/complete `two` on the same workspace, `cleanup_setup(store,"w","one")`, then assert `active_connection(store,"w") == "connection-two"`. This test fails on the candidate and passes once the guard is restored.

### P3 - Low
(none)

---

## Coverage and limits

- **Checked**: the full 3-line diff and every symbol it touches (`store.active`/`store.pending` model in `store.py`, producers in `setup.py`, the one test). Security checklist — no injection/secret/crypto/auth surface in a pure in-memory dict function; the only applicable lens is Data Integrity (flagged). SOLID — no structural concern in a 3-line function.
- **Not covered**: no external/production caller of `cleanup_setup` exists in the repo, so I could not observe the real call ordering (timeouts, cancellation, retries) that produces a stale cleanup — reachability is inferred, not executed. No tests were run (environment is read-only; Bash disabled).
- **Residual risk**: if the real system guarantees `cleanup_setup` is only ever called for the currently-active setup before any superseding `complete_setup`, the impact is latent rather than live — but that invariant is undocumented and not enforced anywhere, which is itself the risk.

**Indexed**: the P1 pattern recorded to `kk:review-findings` (ownership-guard removal before an unconditional delete keyed by a different identifier).

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

Actionable items I recommend fixing:
1. **P1** — Restore the `setup_id` ownership guard in `cleanup.py` before popping `store.active`.
2. **P2** — Add the superseding-setup regression test in `tests/test_setup.py`.

Items I recommend keeping as is:
- The `store.pending.pop(setup_id, None)` line and idempotent `pop(..., None)` usage — correct and unchanged in effect.

**How would you like to proceed?**

1. **Fix all** — restore the guard and add the regression test
2. **Fix P1 only** — restore the guard
3. **Fix specific items** — tell me which
4. **No changes** — review complete

My recommendation: this "simplification" changes behavior rather than preserving it, so I'd restore the guard (option 1). Let me know how you'd like to proceed — I won't change anything until you confirm.
