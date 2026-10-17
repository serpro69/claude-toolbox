## Review summary (isolated mode)

**Reviewers:** only the `code-reviewer` sub-agent ran. The external `pal codereview` reviewer isn't set up in this session, so this review had one reviewer and nothing could be cross-checked between two.
**Files reviewed:** 2 files, 6 lines added (`preview.py` is new; `routes.py` changed)
**Profile:** python. All four of its review checklists were applied: security, SOLID, code-quality and removal-plan.
**Scope:** I used `tasks.md` to set it. Task 1 (in progress) was reviewed; Task 2 (pending) was treated as out of scope.

**Result: approved, with no findings at any severity (P0 through P3).**

What the reviewer confirmed:
- **`/settings` still behaves as before.** It returns before the new branch is reached, and `/unknown` still returns `(404, None)`.
- **The preview route stays off in the checked-in build.** `EXPORT_PREVIEW_ENABLED` is hard-coded to `False` in `config.py`. Because the flag is checked first, `render_preview()` can never run, so `/export-preview` keeps returning `(404, None)`. `tests/test_routes.py:13` already checks this.
- **The flag can't be set from outside.** It doesn't come from a request, an environment variable or outside config, which is what the README requires.
- **The new imports are safe.** Neither `config` nor `preview` does anything when imported, and neither imports `routes`, so there's no import loop.
- **The stub isn't dead code.** It's the placeholder Task 1 is supposed to add. The flag and its check can be removed once Task 2 ships with the flag on.

Notes for Task 2 (out of scope here, not counted as findings):
- **Patching the flag in tests:** `routes.py:1` uses `from config import EXPORT_PREVIEW_ENABLED`, which copies the value when the module loads. Tests for the enabled path must patch `routes.EXPORT_PREVIEW_ENABLED`; patching `config.EXPORT_PREVIEW_ENABLED` will silently have no effect. If you'd rather patch it in `config`, switch to `import config` and read `config.EXPORT_PREVIEW_ENABLED`.
- **Order of work:** turning the flag on before `render_preview` is written would make `/export-preview` crash with a `NotImplementedError` instead of returning a status code. `tasks.md` already says to implement it first.

I have nothing to add to the reviewer's findings.

**Indexing:** there are no P0 or P1 findings, so nothing needed to be indexed.

**Things to check yourself:**
- Nobody ran the tests. The reviewer has no shell, and Bash was blocked for me partway through. Run them with `python3 -B -m unittest discover -s tests`.
- I couldn't delete the temporary diff file because Bash was blocked. It's at `/tmp/kk-review-code-export-preview-task1.patch`.

---

## Next steps

There are 0 findings, so I don't recommend any fixes. The note about patching the flag is worth keeping in mind when you write Task 2's tests.

**How would you like to proceed?**
1. **No changes**: the review is done and Task 1 is ready.
2. **Fix specific items**: for example, switch to `import config` now so Task 2's tests are easier to write.
3. **Re-run with `pal`** once it's set up, to get the second reviewer.
