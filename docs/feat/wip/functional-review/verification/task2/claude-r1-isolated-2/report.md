Temp-file cleanup was blocked by sandbox (harmless `/tmp` leftover). Here's the report.

---

## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent), pal codereview (gemini-3.1-pro-preview)
**Files reviewed**: 1 changed file (`cleanup.py`), 3 read for cross-file context, 2 lines removed → 1 added
**Active profile**: `python` (triggered by `.py` extension — authoritative)

> Both reviewers ran and agreed. No reviewer failures.

---

### Corroborated Findings

**[cleanup.py:3]** Unconditional `store.active.pop` destroys a newer setup's live connection ⟨corroborated⟩
- Profile: python · Checklist: security-checklist.md (Race Conditions — Check-Then-Act / Data Integrity) + code-quality-checklist.md (Boundary Conditions)
- Triggered by: content — `.py` extension (authoritative)
- **code-reviewer: P0 (Critical), 97%** — The guard `if association and association["setup_id"] == setup_id:` was load-bearing. `complete_setup` overwrites `store.active[workspace_id]` for the newest setup (`setup.py:6`), so the slot may be owned by a *different* setup than the one being cleaned up. The unconditional pop makes the `setup_id` argument irrelevant for the active map.
- **pal: [CRITICAL]** — "Cleaning up an older, superseded setup will delete the live connection belonging to a newer setup." Recommends restoring the ownership guard.
- **Failure sequence** (both reviewers independently derived it):
  1. `complete_setup(store, "w", "one", conn1)` → `active["w"]` owned by `"one"`
  2. `complete_setup(store, "w", "two", conn2)` → `active["w"]` now owned by `"two"` (conn2 live)
  3. `cleanup_setup(store, "w", "one")` → blindly pops `active["w"]`, discarding `"two"`'s live `conn2`; `active_connection(store, "w")` now returns `None` while conn2 is still open (dropped service + resource leak).
- **Suggested fix** — restore the check:
  ```python
  def cleanup_setup(store, workspace_id, setup_id):
      store.pending.pop(setup_id, None)
      association = store.active.get(workspace_id)
      if association and association["setup_id"] == setup_id:
          store.active.pop(workspace_id, None)
  ```
- **Author context:** The change was staged as a "simplification." It is behavior-changing, not a safe cleanup — the removed lines were load-bearing. `store.pending.pop(setup_id, None)` is correctly keyed by `setup_id` and is unaffected; only the `active`-map removal regressed.

**[tests/test_setup.py:14]** No regression test for the superseded-setup case ⟨corroborated⟩
- Profile: python · Checklist: code-quality-checklist.md (Boundary coverage)
- Triggered by: content — `.py` extension (authoritative)
- **code-reviewer: P2, 90%** / **pal: [MEDIUM]** — `test_cleanup_removes_its_own_association` only exercises one setup per workspace, where the guarded and unguarded pop behave identically. The suite therefore passes green against the buggy diff.
- **Suggested fix:**
  ```python
  def test_cleanup_superseded_setup_preserves_new_connection(self):
      store = Store()
      complete_setup(store, "w", "one", "conn-1")
      complete_setup(store, "w", "two", "conn-2")
      cleanup_setup(store, "w", "one")
      self.assertEqual(active_connection(store, "w"), "conn-2")
  ```

### Code Reviewer Findings

**[cleanup.py:1-3]** Shared mutable state mutated without synchronization (pre-existing, aggravated)
- Profile: python · Checklist: security-checklist.md (Race Conditions — Shared State / TOCTOU)
- Triggered by: content — `.py` extension (authoritative)
- Severity: P3 | Confidence: 55%
- `store.pending` / `store.active` are plain dicts mutated without a lock. The correct fix reintroduces a get-then-pop (check-then-act) window. Only a risk if `cleanup_setup` / `complete_setup` run concurrently — concurrency model isn't visible in the provided files.
- **Author context:** Pre-existing; not introduced by this diff. Only worth acting on if these functions are called from multiple threads/async tasks.

### Areas Not Covered
- **Callers of `cleanup_setup`**: No call site exists in the repo yet — the P0 scenario is reachable *by contract* (the `active` map's last-writer-wins semantics), confirmed by both reviewers, but no production invocation ordering was observed.
- **Connection lifecycle**: Whether dropping the `active` entry also closes the underlying connection (resource-leak severity) isn't determinable from these files.

**Indexed:** The P0 was indexed as `kk:review-findings` ("ownership guard removed before destructive pop on keyed shared state").

---

## Next Steps

I found 3 issues (corroborated: 2 — one P0, one P2; code-reviewer-only: 1 P3).

The actionable items I recommend fixing:

1. **P0 (corroborated)** — Restore the `setup_id` ownership guard in `cleanup_setup` before popping `store.active`. This is the headline bug; the staged "simplification" silently breaks teardown of superseded setups.
2. **P2 (corroborated)** — Add the superseded-setup regression test so this can't ship green again.

Items I recommend keeping as-is:

- **P3 (locking)** — Pre-existing and context-dependent; defer unless you know this store is accessed concurrently.

**How would you like to proceed?**

1. **Fix all** — restore the guard + add the regression test
2. **Fix corroborated + high severity** — same as above (the P3 is out)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Note: given the P0, the simplest correct resolution is to **revert the staged change** (or unstage it). Let me know which option you'd like.
