## Review summary (isolated mode)

**Overall: approve. Neither the independent reviewer nor I found anything to fix in Task 1.**

**Reviewers:** only the independent Claude code reviewer ran. The second reviewer, an external model reached through a tool called `pal`, couldn't run because no `pal` tools are available in this session. The isolated workflow allows going ahead with one reviewer when that happens.
**Files reviewed:** 2 files (`preview.py`, `routes.py`), 6 lines added.
**Checklists applied:** the Python profile's security, SOLID, code-quality and removal-plan checklists.
**Scope:** Task 1 was reviewed. Task 2 (pending) was out of scope, so the reviewer didn't flag anything it will add.

### Code reviewer findings
None at any severity.

- **The existing routes behave the same.** `/settings` and unknown paths return what they did before. `/export-preview` still returns `(404, None)` because `EXPORT_PREVIEW_ENABLED` is `False` in `config.py` and is checked before the path match (`routes.py:9`).
- **Security:** no new user input reaches anything, and a request can't change the setting. There are no secrets and no shared mutable state.
- **Imports:** importing `preview.py` has no side effects, and there's no circular import.

**Leave the setting in place for now:** Task 2 is what turns preview on. Once preview stays on for good, decide whether to remove `EXPORT_PREVIEW_ENABLED` and the test that expects a 404 for `/export-preview`.

### Notes for Task 2 (not findings)
- **Turning the setting on early would crash the route.** `render_preview()` raises `NotImplementedError`, so `/export-preview` would throw instead of returning a response. Task 2 already says to implement the function first.
- **Tests will need to patch the setting in `routes`, not `config`.** `routes.py` uses `from config import EXPORT_PREVIEW_ENABLED`, which copies the value when the module loads. Patching `config.EXPORT_PREVIEW_ENABLED` will have no effect. Changing it to `import config` and reading `config.EXPORT_PREVIEW_ENABLED` would make either one patchable. This only matters once Task 2 starts.

### Checks
- I read `tests/test_routes.py` to confirm the reviewer's claim. The suite covers `/settings`, an unknown route, and `/export-preview` returning 404.
- I ran `python3 -B -m unittest discover -s tests`, and all 3 tests passed.
- There were no high-severity findings to save to the knowledge base.

---

## Next steps

I recommend leaving the code as it is. Raise the `import config` change when Task 2 begins.

**How would you like to proceed?**
1. **Fix all:** nothing to fix.
2. **Fix specific items:** for example, switch to `import config` now to get ahead of Task 2.
3. **No changes:** the review is complete.
