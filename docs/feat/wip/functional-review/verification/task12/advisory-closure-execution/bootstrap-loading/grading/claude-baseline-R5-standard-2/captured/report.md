## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (`preview.py` new, `routes.py` modified)
**Overall assessment**: **APPROVE**

**How I reviewed it:** only the `python` profile matched the diff. I applied its four checklists (security, SOLID, code quality, removal-plan) plus the generic categories. I also checked the change against `tasks.md` Task 1 and the rules in `README.md`. The capy knowledge base is empty, so there were no earlier findings or language idioms to compare against.

---

## Findings

### P0 – Critical
None.

### P1 – High
None.

### P2 – Medium
None.

### P3 – Low
None.

---

## What was checked

- **Existing behaviour is unchanged.** `config.EXPORT_PREVIEW_ENABLED = False`, so `/export-preview` still returns `(404, None)` and `/settings` behaves as before. The test suite already contained `test_preview_route` asserting 404, and it passes. `python3 -B -m unittest discover -s tests` ran 3 tests, all OK.
- **The new route can't be switched on from outside.** The flag is a constant in the source, not read from the request, an environment variable or a config file, which is what the README requires. `and` short-circuits on the flag first, so `render_preview()` can't run in the checked-in build. If it did run, `test_preview_route` would fail with `NotImplementedError`.
- **Security:** no input reaches the new code apart from the path compared against a fixed string. There is no deserialization, file I/O or subprocess. The new endpoint has no auth guard, but neither does `/settings`, and the repo has no auth layer.
- **Import side effects:** `preview.py` only defines a function, so importing it in `routes.py` is harmless.
- **SOLID / quality:** no problems at this size. The `if` chain in `get()` is the existing routing pattern.

## Things I deliberately didn't flag

- **The `NotImplementedError` stub is reachable if the flag is flipped.** Task 1 explicitly asks for a placeholder module and a guarded route. `tasks.md` Task 2 requires `render_preview` and its enabled-path tests before the build setting changes. So this is on purpose, not a defect.
- **The route is dead code while the flag is off.** It's switched-off scaffolding that Task 2 will complete, so it should stay, not be deleted.
- **There are no enabled-path tests.** Task 2 explicitly owns them.

## A note for Task 2

`routes.py` copies the flag into its own namespace when it loads (`from config import EXPORT_PREVIEW_ENABLED`). Enabled-path tests therefore have to patch `routes.EXPORT_PREVIEW_ENABLED`. Patching `config.EXPORT_PREVIEW_ENABLED` would silently do nothing. The alternative is to switch to `import config` and check `config.EXPORT_PREVIEW_ENABLED` inside `get()`. This doesn't block Task 1.

## Not covered

I didn't check deployment or runtime config overrides, because the README says this repo has none.

**Indexing:** nothing indexed, since there were no P0/P1 findings.

---

## Next Steps

I found 0 issues (P0: 0, P1: 0, P2: 0, P3: 0). Task 1 matches its spec and the existing tests pass.

**How would you like to proceed?**

1. **No changes**: review complete, Task 1 is ready to commit
2. **Apply the Task 2 note now**: switch to `import config` so later tests can patch `config` directly
3. **Something else**: tell me what you'd like
