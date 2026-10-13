## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (`preview.py` is new, `routes.py` is modified)
**Overall assessment**: **APPROVE**
**Intent and scope**:
- **Requirements:** `README.md` and `tasks.md`.
- **What's in scope:** Task 1, "Prepare preview module". Existing routes must behave the same while the checked-in setting keeps preview off, and the preview module and its guarded route are added for the next task.
- **What's out of scope:** Task 2 (implement and enable preview) is pending, so I didn't flag the missing preview implementation.
- **Diff reviewed:** the staged changes only (`git diff --cached`). There were no unstaged changes.

**Baselines**: Review base is `HEAD` (`f1a16b5 Review base`); the candidate is the staged index. There's no separate release baseline, and the README says the repo keeps no deployment inventory.

## Behavior and Compatibility

What I read: `README.md`, `tasks.md`, the staged diff, `routes.py`, `preview.py`, `config.py`, `settings.py` and `tests/test_routes.py`. There are no unstaged changes, so the worktree copies of the two staged files match the index. The other files are unchanged since `HEAD`.

| Scenario | Before | After | Conclusion |
| --- | --- | --- | --- |
| `GET /settings` | `200, {"theme": "light"}` | Same; this check still runs first | **Supported** (source + `test_current_settings`) |
| Unknown route | `404, None` | Same | **Supported** (source + `test_unknown_route`) |
| `/export-preview` with the checked-in setting `False` | `404, None` | `404, None`: the guard short-circuits before `render_preview()` | **Supported** (source + `test_preview_route`) |
| Loading `routes.py` | Imports `settings` | Also imports `config` (already in the repo) and `preview` (added in this same change). Neither does anything on import | **Supported**: the tests import it successfully |
| Preview turned on | n/a | `render_preview()` raises `NotImplementedError` | **Not applicable to this increment.** `EXPORT_PREVIEW_ENABLED` is a checked-in `False`, not set by a request, environment variable or external config (README). It can't be reached until Task 2 changes the setting, and Task 2 also owns the implementation and its tests. |
| Deployed environment | — | — | **Not assessed.** There's no deployment inventory, and this doesn't affect the code verdict. |

**Tests:** I ran `python3 -B -m unittest discover -s tests` and all 3 tests passed. The guarded-off route already has a regression test, so the change stands on its own, as the README requires.

**Checklists applied:**
- python security: the new route is not reachable and takes no input, so there's no injection or auth exposure.
- python solid: the route guard is small and the stub lives in its own module.
- python code-quality: the `NotImplementedError` stub can't be reached, so it isn't swallowed-error or dead-code debt; it's planned scaffolding for Task 2.
- python removal-plan: nothing to remove. A pending task's unreachable scaffold isn't a removal candidate.

**Knowledge base:** I searched `kk:review-findings` and `kk:lang-idioms`, but nothing has been indexed yet, so there was no prior guidance to apply.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
(none)

**Indexing:** there are no P0/P1 findings, so nothing was added to the knowledge base.

---

## Coverage and limits

- **Checked:** the whole staged diff, the modules that `routes.py` imports, the existing tests, and the task and README requirements. I also ran the test suite.
- **Not covered:**
  - Any deployed environment, because no inventory exists.
  - The path with preview turned on, which belongs to Task 2 (pending) and can't be reached in this build.

Task 1 meets its requirements: existing routes behave the same, and the preview route is added but switched off. I don't recommend any changes.
