## Code Review Summary

**Files reviewed**: 2 files, 25 lines changed (`reader.py`, `tests/test_reads.py`, staged)
**Overall assessment**: APPROVE. I found no P0, P1 or P2 issues, only minor suggestions.

**What I did**: Only the `python` profile applied. I loaded its four checklists (security, SOLID, code quality, removal) before reading the diff. I also read `preferences.py` and `repository.py` to follow the full call path: `Preferences.read` → `read_preferences` → `Repository.read_resilient` → `backend.read`. The knowledge base had no earlier review findings or Python idioms stored.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low

- **[reader.py:2]** Keys that are empty or only whitespace still reach the backend
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `read(" ")` now becomes `read_resilient("")`. Before this change the backend got `" "`; now it gets an empty key. That is almost certainly not a real preference ID, and the backend will report it as missing (or worse, as a valid lookup).
  - Confidence: 70%. The behavior is certain. Whether it matters depends on how the real backend handles `""`, which isn't in this repo.
  - Suggested fix: after stripping, raise `ValueError` if the key is empty. Add a test for that case.

- **[reader.py:2]** Normalization only happens in the `read_preferences` helper
  - Profile: python · Checklist: solid-checklist.md
  - Triggered by: content — `.py` extension
  - Anything that calls `Repository.read_resilient` or `read_once` directly skips the trim, so preference IDs are normalized on one path and not the other. Right now `read_preferences` is the only caller and there's no write path, so nothing is broken today.
  - Confidence: 55%. This is a forward-looking design risk, not a current bug.
  - Suggested fix: when a write path or a second reader appears, move normalization into `Repository` (or a small `normalize_key` helper) so reads and writes always produce the same ID.

- **[reader.py:2]** `.strip()` assumes the key is a string
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - A `None` or non-string key now raises `AttributeError` here, where before it was passed through to the backend. This is arguably better (it fails early), but the error message is unclear.
  - Confidence: 40%. No caller in the repo passes a non-string key.
  - Suggested fix: leave it as is, or add a type hint (`key: str`) to make the contract explicit.

- **[tests/test_reads.py:8]** No test covers a key that is already trimmed
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `test_existing_key` (`read("w")`) was renamed into `test_trim_key`, so every test now passes `" w "`. Plain keys are almost certainly fine, but that basic case is no longer checked directly.
  - Confidence: 60%. This is a coverage gap, not a defect.
  - Suggested fix: keep a `read("w")` assertion. You could also cover tab and newline padding (`"\tw\n"`), since `strip()` handles all whitespace.

---

## Additional Suggestions

- The new `test_transient_error`, `test_retry_limit` and `test_permanent_error` tests are good: they check exact attempt counts and that a missing preference isn't retried. They test the existing retry behavior rather than the trimming change, so you might mention that in the commit message.
- `ScriptedBackend` is a test double, but it lives in the production module `repository.py` (this predates your change). Moving it to `tests/` would keep test code out of production.

**Not covered**: I couldn't run the test suite because shell commands were blocked partway through the review. I checked the tests by reading the code, and against `repository.py` they should pass.

**Indexing**: No P0/P1 findings, so there was nothing to save to the knowledge base.

---

## Next Steps

I found 4 issues (P0: 0, P1: 0, P2: 0, P3: 4).

The actionable items I recommend fixing:
1. Reject keys that are empty after trimming, and add a test (`reader.py:2`)
2. Add an already-trimmed key and tab/newline cases to the tests (`tests/test_reads.py:8`)

Items I recommend keeping as is:
- Where normalization lives: only one call path exists today, so moving it isn't needed yet.
- `.strip()` on a non-string key: failing early with `AttributeError` is acceptable when every caller passes strings.

**How would you like to proceed?**

1. **Fix all**: I'll implement all suggested fixes
2. **Fix P0/P1 only**: Address critical and high priority issues (none here)
3. **Fix specific items**: Tell me which issues to fix
4. **No changes**: Review complete, no implementation needed
