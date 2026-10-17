I’m using `$kk:implement` to update `patch_settings`, test the omission and explicit-value behavior, and run an independent review.


`patch_settings` uses `or`, so it discards explicitly supplied falsey values. I’ll assign each supplied value directly and keep the existing copy of `current`. I’m using `$kk:test` for regression coverage and `$kk:document` to clarify the contract in the README.


The fix passes all five tests, including the new cases that failed against the original code. Both inputs remain unchanged, and the CLI can now clear the note. I’m running `$kk:review-code:isolated`; the external PAL reviewer is unavailable, so the skill’s fallback will use the independent code-reviewer agent.


Updated `patch_settings`: omitted keys retain their values; explicit values—including `None`, `""`, and `False`—replace them. Caller inputs and existing exports are preserved. No dependencies added.

Added regression tests and README documentation. All 5 tests pass; `git diff --check` passes. Independent review found no issues; PAL was unavailable.
