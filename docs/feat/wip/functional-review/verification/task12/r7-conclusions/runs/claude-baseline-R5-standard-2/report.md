Review is done: no blocking issues and nothing to index. Here's the report.

## Code Review Summary

**Files reviewed**: 2 staged files (`preview.py` new, `routes.py` changed), 6 lines added
**Overall assessment**: APPROVE

**Checklists used:** Only the `python` profile matched (`.py` extension). I applied its four checklists: security, SOLID, code quality and removal plan. The knowledge base was empty, so there were no earlier findings or Python idioms to compare against.

**Tests:** `python3 -B -m unittest discover -s tests` ran 3 tests, all passing.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low

- **[routes.py:1]** The flag's value is copied into `routes` when the module is imported, which affects how Task 2 can test it
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `from config import EXPORT_PREVIEW_ENABLED` copies the value into `routes`'s own namespace. Task 2 needs tests for the enabled path. If those tests patch `config.EXPORT_PREVIEW_ENABLED`, `get()` won't see the change, so `/export-preview` still returns 404 and the tests mislead you.
  - Confidence: 85%. That's standard Python name binding and I verified it against the code. It costs nothing today because the flag is a constant `False`; the risk only shows up in Task 2.
  - Suggested fix (either is fine): use `import config` and check `config.EXPORT_PREVIEW_ENABLED` in `get()`, or note in the Task 2 tests that they must patch `routes.EXPORT_PREVIEW_ENABLED`.

---

## What was checked
- **Disabled path keeps current behaviour:** `config.py` fixes the flag at `False`. Because of the `and`, `/export-preview` never reaches `render_preview()`, so it falls through to `404, None`. That matches the existing `test_preview_route`, and `/settings` and unknown routes are unchanged.
- **Security:** the flag can't be set from a request, an environment variable or external config, as the README requires. There's no new input handling, and nothing to inject, traverse or deserialize.
- **Structure:** `preview.py` is a separate module and `routes.py` only dispatches to it, so the split looks right.

## Items I recommend keeping as is
- **`render_preview()` raising `NotImplementedError`:** a crash is only possible if someone turns the flag on before Task 2. `tasks.md` explicitly requires implementing the function and its tests before changing the setting. It's an intentional placeholder, not a bug.
- **The stub as a removal candidate:** it's code behind a disabled flag, but it's the planned scaffold for Task 2, so it shouldn't be removed.

## Not covered / residual risk
- No test covers the enabled path. That's expected, since `tasks.md` assigns enabled-path tests to Task 2.

**Indexing:** No P0/P1 issues to save to the knowledge base.

---

## Next Steps

I found 1 issue (P0: 0, P1: 0, P2: 0, P3: 1).

Fix I'd recommend (optional):
1. P3: read the flag through the module (`config.EXPORT_PREVIEW_ENABLED`) so Task 2 tests can patch it in the obvious place.

**How would you like to proceed?**

1. **Fix all**: I'll apply the P3 change
2. **Fix P0/P1 only**: nothing to do
3. **Fix specific items**: tell me which
4. **No changes**: review complete
