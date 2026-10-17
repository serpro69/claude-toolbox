Capy knowledge base is empty, so there are no earlier findings or idioms to compare against. Writing up the review now.

## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (`preview.py` new, `routes.py` modified, both staged)
**Overall assessment**: **APPROVE**

**What I checked:**
- **Profiles:** only `python` matched. Both files are `.py`, and the other seven profiles had no matching signals. I applied all four Python checklists: security, SOLID, code-quality and removal-plan.
- **Spec:** I compared the change with `tasks.md` Task 1 ("preserve existing routes with preview disabled", "add the preview module and guarded route") and the contract in `README.md`. The change matches both.
- **Tests:** `python3 -B -m unittest discover -s tests` ran 3 tests and all passed, including `test_preview_route`, which expects `/export-preview` to return `(404, None)`.

## Findings

### P0 – Critical
None.

### P1 – High
None.

### P2 – Medium
None.

### P3 – Low

- **[routes.py:1]** Importing the flag by name makes it awkward to override in Task 2's tests
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `from config import EXPORT_PREVIEW_ENABLED` copies the value into `routes` when the module is imported. When Task 2 writes its enabled-path tests, `patch("config.EXPORT_PREVIEW_ENABLED", True)` will have no effect on `get()`. Only `patch("routes.EXPORT_PREVIEW_ENABLED", True)` will work, and that is easy to get wrong.
  - Confidence: 70%. The import behaviour is certain. Whether it causes trouble depends on how Task 2 writes its tests.
  - Suggested fix (optional): `import config` and check `config.EXPORT_PREVIEW_ENABLED` inside `get()`, or just note the correct patch target in Task 2.

::code-comment{file="routes.py" line="1" severity="P3"}
Importing the flag by name copies it into `routes`, so Task 2 tests must patch `routes.EXPORT_PREVIEW_ENABLED`, not `config.EXPORT_PREVIEW_ENABLED`. Consider `import config` and reading `config.EXPORT_PREVIEW_ENABLED` inside `get()`.
::

### Checked and not flagged
- **Stub that raises `NotImplementedError` behind the route** (`preview.py:2`, `routes.py:9-10`): turning the flag on today would make `get("/export-preview")` raise instead of returning a response. That isn't a defect here:
  - The flag is hard-coded to `False` in `config.py`. Per the README, nothing outside the source (no request, environment variable or external config) can change it.
  - `tasks.md` requires Task 2 to implement `render_preview` and its tests before the setting changes.
  - Because the flag is checked first, the stub is never called in this build.
- **Security:** the new route uses no user input. A disabled route returns the same 404 as an unknown path, so nothing leaks. Importing `preview` has no side effects.
- **Removal:** the stub can't be reached while the flag is off, but it's planned scaffolding for Task 2, not dead code, so there's nothing to remove.
- **SOLID:** an `if` chain for routing is fine at this size.

**Not covered:** there are no tests for the enabled path yet; Task 2 owns those.

## Indexing
Nothing to index: there are no P0/P1 findings.

---

## Next Steps

I found 1 issue (P0: 0, P1: 0, P2: 0, P3: 1).

Optional fix:
1. P3: read the flag through the `config` module (`config.EXPORT_PREVIEW_ENABLED`) so Task 2's tests can override it at its source.

What I'd leave as is:
- The stub that raises `NotImplementedError`: it can't be reached while the flag is fixed at `False`, and `tasks.md` requires Task 2 to implement it before the flag changes.

**How would you like to proceed?**

1. **Fix all**: I'll apply the P3 change.
2. **Fix P0/P1 only**: there are none, so nothing changes.
3. **Fix specific items**: tell me which to fix.
4. **No changes**: the review is complete and Task 1 is ready to commit as staged.
