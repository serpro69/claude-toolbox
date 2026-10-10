I’ll use `$kk:implement` to check the repo guidance, update `patch_settings`, and verify the behavior with focused tests and an independent review.

`patch_settings` currently uses a truthiness fallback, so it discards `None`, empty text, and `False`. I’ll assign supplied values directly, then use `$kk:test` to check omitted keys, input preservation, and the API/CLI callers. I’ll also document the behavior with `$kk:document`.

The one-line fix is in place. The regression tests reproduced the bug before the change; all six tests now pass, including API and CLI coverage. I’m running the required isolated code review next.

The independent code reviewer found no issues. The external reviewer suggested using dictionary-union syntax as a low-priority style change; I’m retaining the existing copy-and-loop structure to keep this fix focused. There are no findings to index.

Updated [patch_settings](/tmp/functional-review-2b-i2-1-20261010/settings.py:1): omitted keys retain their values; supplied values—including `None`, `""`, and `False`—replace them. Inputs and exports are preserved; no dependencies added.

Added regression tests and documentation. All 6 tests pass; `git diff --check` passes. Independent review found no issues; an external review’s optional style suggestion was left unapplied.
