The Task 1 change is ready to merge: I found nothing at P0, P1 or P2, and one optional P3 note.

## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (staged: `preview.py`, `routes.py`)
**Overall assessment**: APPROVE
**Profiles active**: `python` (both files have a `.py` extension). I applied all four of its checklists: security, SOLID, code quality and removal.

The change:
- adds `preview.render_preview()` as a stub that raises `NotImplementedError`;
- adds an `/export-preview` branch to `routes.get`, guarded by `config.EXPORT_PREVIEW_ENABLED`.

I ran `python3 -B -m unittest discover -s tests`, and all 3 tests pass, including the existing `test_preview_route`, which expects `(404, None)`.

---

## Findings

### P3 - Low

- **[routes.py:1]** The flag's value is copied into `routes` when the module is imported, which affects how Task 2 tests can switch it on
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `from config import EXPORT_PREVIEW_ENABLED` gives `routes` its own copy of the value. Changing `config.EXPORT_PREVIEW_ENABLED` later (for example with `mock.patch("config.EXPORT_PREVIEW_ENABLED", True)`) won't affect the route. Task 2's enabled-path tests will have to patch `routes.EXPORT_PREVIEW_ENABLED` instead, and patching the wrong one quietly leaves the route returning 404.
  - Confidence: 70%. This is standard Python import behaviour, so the mechanism is certain. It doesn't cause a bug now; it only affects how Task 2's tests are written, so the severity is low.
  - Suggested fix: keep it as is and patch `routes.EXPORT_PREVIEW_ENABLED` in Task 2, or use `import config` and read `config.EXPORT_PREVIEW_ENABLED` at call time.

---

## Checked and not flagged

- **The route calls a stub that raises.** Normally that would be serious, but nothing can reach it here:
  - `config.py:1` sets the flag to the constant `False`.
  - `README.md` says the flag can't be set by a request, an environment variable or external config.
  - `tasks.md` says Task 2 implements `render_preview` before the setting changes.
  - `test_preview_route` locks in the disabled behaviour, so turning the flag on early would make that test fail.

  This matches the Task 1 scope ("guarded route for the next increment").
- **Unused code behind the flag:** it's meant to stay until Task 2, so there's nothing to remove now.
- **Security:** the new route takes no input, so there's no authentication or injection surface.
- **Behaviour:** `/settings` and unknown paths behave exactly as before, which is the acceptance contract in the README.

**Not covered:** the Task 2 tests for the enabled route don't exist yet; `tasks.md` schedules them for Task 2.

**Indexing:** there were no P0/P1 findings, so nothing was added to the review knowledge base. It was empty, so there were no earlier findings to compare against either.

---

## Next Steps

The only item is the optional P3 above; I suggest leaving the code as it is and keeping the note for Task 2.

**How would you like to proceed?**

1. **Fix all**: switch to `import config` so the flag is read on each call
2. **Fix P0/P1 only**: nothing to do
3. **Fix specific items**: tell me which
4. **No changes**: review complete
