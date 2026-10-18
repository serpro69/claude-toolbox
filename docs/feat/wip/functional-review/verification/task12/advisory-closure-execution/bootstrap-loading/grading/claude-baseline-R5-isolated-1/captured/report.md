## Review Summary (Isolated Mode)

**Reviewers:** code-reviewer (Claude sub-agent) only. pal codereview didn't run because the pal tool isn't available in this session.
**Files reviewed:** 2 staged files, about 5 lines changed. `preview.py` is new (+2) and `routes.py` has +3.
**Profile:** python. The sub-agent applied all four of its always-load checklists: security, SOLID, code-quality and removal-plan.

**Limitations:**
- **No literal diff.** Bash was denied, so I couldn't run `git diff --cached` or write the patch file. The reviewer worked from the staged file list (`preview.py` added, `routes.py` modified) and the full current file contents.
- **One reviewer, no corroboration.** With pal missing, nothing could be confirmed by a second reviewer.
- **Tests not run.** The reviewer checked the expected results by reading the code.

---

### Code Reviewer Findings

**Assessment: APPROVE, with no P0–P3 findings.**

The reviewer checked each Task 1 requirement:
- **Existing routes are kept:** `/settings` and the 404 fallback behave as before, and existing tests cover both.
- **The guard holds:** `EXPORT_PREVIEW_ENABLED and path == ...` checks the flag first. The flag is a hard-coded `False` (`config.py:1`), so no request can reach the stub. `test_preview_route` checks that `/export-preview` returns `(404, None)`.
- **Importing the stub is safe:** `NotImplementedError` is only raised when `render_preview` is called, not when the module loads.

The reviewer also raised two notes for Task 2 (not defects in Task 1):
- **Turning the flag on too early:** if `EXPORT_PREVIEW_ENABLED` becomes `True` before `render_preview` is written, `/export-preview` raises an unhandled exception instead of returning a status tuple. `tasks.md` already requires the implementation to come before the flag change.
- **Patching in tests:** `routes.py:1` uses `from config import EXPORT_PREVIEW_ENABLED`, which copies the value when `routes` is imported. A Task 2 test that patches `config.EXPORT_PREVIEW_ENABLED` will have no effect on `routes.get`. It has to patch `routes.EXPORT_PREVIEW_ENABLED` instead.

I have no author context to add, since I didn't write this code, and I have no observations of my own beyond the above.

### Indexing

There's nothing to save to the review-findings index because there are no P0/P1 findings.

---

## Next Steps

There are no actionable findings for Task 1. The only items worth keeping are the two Task 2 notes, which belong to the next increment.

**How would you like to proceed?**
1. **No changes:** Task 1 is ready.
2. **Rerun with full coverage:** enable Bash (for the exact staged diff and a test run) and/or the pal MCP server, then I'll run the review again.
3. **Record the Task 2 notes:** I'll add the two notes to Task 2 in `tasks.md`.
