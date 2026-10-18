I’m using `kk:review-code` to review the staged change. I’ll load the required review checklists before reading the diff.

The staged change touches two Python files. All four Python review checklists are loaded; I’ll now check the label change, its callers, and the tests.

**APPROVE** — no findings introduced by the staged change.

Reviewed 2 files, with 5 additions and 5 deletions. The label changes consistently to `Records`; counts, mode selection, and mean formatting remain intact. All 4 tests pass. No findings to index.

Existing limitation: `report([], detailed=True)` raises `ZeroDivisionError`, confirmed in both HEAD and the working tree. It is outside this patch; the checked-in default remains `False`.

The [kk:review-code skill](/home/sergio/.codex/plugins/cache/fr-advisory-c2d28c9e/kk/0.23.0/skills/review-code/SKILL.md) requires “Next steps confirmation from user.” Leave this review-only with no changes?
