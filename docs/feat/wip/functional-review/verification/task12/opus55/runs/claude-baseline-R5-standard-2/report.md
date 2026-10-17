I've finished the review of the staged Task 1 changes. Only the `python` profile applied, and I used all four of its checklists (security, SOLID, code quality, removal). The knowledge base had no earlier findings or Python idioms to draw on.

## Code Review Summary

**Files reviewed**: 2 files (`preview.py`, `routes.py`), 6 lines added
**Overall assessment**: **APPROVE**
**Tests**: `python3 -B -m unittest discover -s tests` passes (3 tests, including `test_preview_route` → `(404, None)`)

---

## Findings

### P0 - Critical
None.

### P1 - High
None.

### P2 - Medium
None.

### P3 - Low

- **[routes.py:1]** The flag is copied into `routes` at import time, which matters for Task 2's tests
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `from config import EXPORT_PREVIEW_ENABLED` copies the value into `routes`' own namespace when the module loads. Task 2 says to write the enabled-path tests before changing the build setting, so those tests will have to switch the flag on. Patching `config.EXPORT_PREVIEW_ENABLED` would do nothing; only `routes.EXPORT_PREVIEW_ENABLED` works. Production behaviour is unaffected.
  - Confidence: 85%. This is how Python imports work, so the behaviour itself is certain. The impact is only a possible confusing moment when writing Task 2's tests.
  - Suggested fix (optional): use `import config` and check `config.EXPORT_PREVIEW_ENABLED`, or leave the import as is and note that tests should patch `routes.EXPORT_PREVIEW_ENABLED`.

---

## Things I checked and am not flagging

- **`render_preview()` raises `NotImplementedError` (`preview.py:2`) behind a route that returns 200.** That code can't run in the checked-in build. `config.EXPORT_PREVIEW_ENABLED` is hardcoded to `False`, and the README says it doesn't come from a request, environment variable or external config. The flag is checked before the path, so `/export-preview` falls through to the existing `404, None`, and `test_preview_route` covers that. Task 2 explicitly says to implement `render_preview` before turning the flag on. The stub is a deliberate placeholder, not dead code to remove.
- **No auth on the new route.** No route in this module has auth (`/settings` has none either), and this one is unreachable for now. Task 2 should check this when it enables the route.
- **SOLID / security:** The feature-flag check keeps the new route separate from existing behaviour. There's no user input and no I/O, and nothing touches shared state.
- **Task 1 scope:** "Preserve existing routes with preview disabled" and "Add the preview module and guarded route" are both met. `/settings` and the 404 for unknown paths behave as before.

**Not covered:** I didn't check how Task 2 will render the preview. No deployment inventory exists, per the README.

## Index findings
Nothing to index: there are no P0/P1 findings.

---

## Next Steps

I found 1 issue (P0: 0, P1: 0, P2: 0, P3: 1).

The one optional fix I'd make:
1. P3: switch `routes.py` to `import config` so Task 2's tests can patch the flag in the obvious place.

Things I'd leave as they are:
- The `NotImplementedError` stub behind the route: it can't run while the flag is fixed at `False`, and Task 2 implements it before enabling.

**How would you like to proceed?**

1. **Fix all**: I'll apply the P3 change
2. **Fix P0/P1 only**: nothing to do
3. **Fix specific items**: tell me which
4. **No changes**: review complete
