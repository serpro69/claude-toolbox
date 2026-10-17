## Code review (isolated mode): `cleanup.py`

**Verdict: REQUEST_CHANGES.** The new cleanup can delete a workspace connection that belongs to a different, successful setup.

This was weaker than a full isolated review, for three reasons:
- **Only one reviewer ran.** The external reviewer runs through the PAL server, which failed to connect at session start. The independent code reviewer ran normally. With no second opinion, nothing is "corroborated".
- **I couldn't run shell commands** (Bash is denied in this mode). So I had no staged diff and couldn't see the previous version of `cleanup.py`. I reviewed the file as it is on disk, assuming it matches what you staged. That assumption comes from the `git status` taken at session start, which showed only `cleanup.py` staged.
- **No tests were run.** Everything below comes from reading the code.

**What I checked:** `cleanup.py` against the rules in `README.md`, plus the code that uses it (`setup.py`, `store.py`) and `tests/test_setup.py`. Only the Python profile applied; all four of its checklists were loaded.

### Behavior and compatibility

The README says another setup can finish before a failed setup's queued cleanup runs. It also says cleanup removes the failed setup's pending record and "any association it owns".

| Scenario | Expected | Your version |
|---|---|---|
| Failed setup cleans up, no active connection exists | Pending record cleared | ✅ |
| Setup completes, then cleans up its own connection | Its own connection removed | ✅ (the existing test covers this) |
| `one` fails → `two` completes → cleanup for `one` runs | `two`'s connection is kept | ❌ `two`'s connection is deleted |
| An older successful connection exists → a new setup fails and cleans up | Older connection is kept | ❌ deleted |
| Cleanup is retried after another setup has completed | Nothing of the other setup's is touched | ❌ deleted |

- **Storage:** nothing to migrate; the store is two in-memory dicts.
- **Concurrency:** out of scope per the README. This bug happens even when operations run one at a time.
- **New or pre-existing?** Unknown, because I couldn't see the old file. The name "simplification" and the fact that the stored `setup_id` field is now never read suggest an ownership check was removed.

### Code reviewer findings

**P1, `cleanup.py:3`: a failed setup's cleanup deletes a connection owned by another setup** (95% confidence)
- **How it happens:**
  1. Setup `one` fails.
  2. Setup `two` completes and `complete_setup` stores `{"setup_id": "two", ...}` for workspace `w`.
  3. Cleanup for `one` runs `store.active.pop("w", None)` without checking who owns it.
- **Result:** `active_connection("w")` returns `None` instead of `"connection-two"`. The successful connection is lost and the user has to run setup again.
- **Tests:** they only cover cleaning up your own connection, so they wouldn't catch this.
- **Suggested fix:** delete only when the connection belongs to the failed setup:
  ```python
  def cleanup_setup(store, workspace_id, setup_id):
      store.pending.pop(setup_id, None)
      association = store.active.get(workspace_id)
      if association is not None and association["setup_id"] == setup_id:
          del store.active[workspace_id]
  ```
  Then add tests for two cases: (a) `one` fails, `two` completes, cleanup for `one` leaves `two` in place; (b) an older connection survives a newer setup's failed cleanup.
- **Don't remove** the `setup_id` field that `complete_setup` writes, even though nothing reads it right now. The fix depends on it.

I traced the same scenario myself and got the same result.

### Still open
- **Previous version of `cleanup.py`:** the reviewer asked for it, but I couldn't read it without git. It would only tell us whether this is a new bug or an old one; the verdict stays the same either way.
- **Test run:** run `python3 -B -m unittest discover -s tests` after the fix. Nobody has run it yet.

I saved this "check ownership before deleting" pattern to the knowledge base (`kk:review-findings`) for future reviews. No temporary files were created.

Should I apply the fix and add the two tests?
