## Code Review Summary

**Files reviewed:** 2 staged files (`preview.py` new, `routes.py` modified), 6 lines added
**Overall assessment:** APPROVE. I found no issues.

**How I reviewed it:** Only the `python` profile applied. I checked the diff against its four checklists: security, SOLID, code quality and removal. Tests pass (`Ran 3 tests … OK`). The project's stored review notes and Python idioms (capy) are empty, so there was no prior history to compare against.

---

## Findings

None at any level, P0 through P3.

### What I checked

- **Unchanged behavior with the preview off:** `config.EXPORT_PREVIEW_ENABLED` is a fixed `False` in the code. Nothing in a request, environment variable or outside config can change it, as `README.md` requires. `/settings`, unknown routes and `/export-preview` all respond exactly as before. The existing `test_preview_route` test, which expects `(404, None)`, already covers the disabled case.
- **The stub that raises an error:** `render_preview()` can't be reached while the preview is off. `tasks.md` says Task 2 implements it and adds tests for the enabled case before turning the setting on. So this is planned groundwork, not dead code or a crash waiting to happen.
- **Security:** the new route takes no user input, and there's no injection, path, deserialization or auth surface. The setting can't be controlled by a client.
- **Imports and structure:** `preview.py` imports nothing, so there's no circular import. Two routes in an `if` chain don't justify a router abstraction yet.
- **Removal:** nothing to remove. The gated code has a named follow-up in Task 2.

### Not covered

- No deployment inventory exists, per the README, so I couldn't check whether any deployed build changes the setting. The README says none does.

## Additional Suggestions (for Task 2, not this diff)

- `routes.py:1` uses `from config import EXPORT_PREVIEW_ENABLED`, which copies the value into `routes` when the module loads. A Task 2 test that patches `config.EXPORT_PREVIEW_ENABLED` will have no effect; it has to patch `routes.EXPORT_PREVIEW_ENABLED`. Alternatively, `routes` could read `config.EXPORT_PREVIEW_ENABLED` each time a request comes in.

**Saved review notes:** none. Nothing serious (P0/P1) or recurring came up.

---

## Next Steps

I found 0 issues (P0: 0, P1: 0, P2: 0, P3: 0). Nothing needs fixing before Task 1 is merged.

**How would you like to proceed?**

1. **No changes:** the review is done and Task 1 is ready to commit.
2. **Apply the Task 2 suggestion now:** switch `routes.py` to read `config.EXPORT_PREVIEW_ENABLED` at request time.
3. **Something else:** tell me what you'd like.
