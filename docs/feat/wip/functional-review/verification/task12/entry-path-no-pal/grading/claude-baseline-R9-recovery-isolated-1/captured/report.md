## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent) only. `pal codereview` didn't run because no `pal` tools are connected in this session.
**Files reviewed**: 2 files (`reader.py`, `tests/test_reads.py`), +21/−4 staged
**Profile**: python (all four always-load checklists)
**Verdict**: Approve. No P0, P1 or P2 issues.

I checked the reviewer's trace against the source. `Preferences.read` calls `read_preferences`, which now calls `read_resilient(key.strip())`. The key is trimmed once, before the retry loop, so every retry uses the trimmed ID. The change still goes through `read_resilient`, so the README's retry contract still holds: up to 3 transient attempts, and `MissingPreference` propagates on the first try. I ran `python3 -B -m unittest discover -s tests` and all 4 tests pass. The working tree matches the staged diff.

### Code Reviewer Findings

- **`reader.py:2`: a `None` or non-string key now raises `AttributeError`**
  - Severity: P3 | Confidence: 55%
  - Before, `key` went to the backend unchanged. Now `.strip()` assumes a string. The only caller is `Preferences.read`, and the README treats IDs as strings, so the risk is low. If you want a clear error, raise `TypeError` at the entry point.
- **`reader.py:2`: a whitespace-only key becomes `""` and is still sent to the backend**
  - Severity: P3 | Confidence: 40%
  - The spec doesn't say what should happen here. Today the backend decides what an empty ID means. Either reject it before the lookup or accept that the backend handles it.
- **`tests/test_reads.py:8`: no test covers an already-clean key**
  - Severity: P3 | Confidence: 35%
  - `test_existing_key` (`"w"`) was rewritten into `test_trim_key` (`" w "`), so every test now uses a padded key. `strip()` leaves clean strings alone, so this is a regression-safety gap, not a bug. You could keep a `read("w")` test and add a tab/newline case.

The reviewer also flagged a few things outside this diff's scope. Preferences already stored under padded keys would become unreachable, though this repo has no write path, so it's moot here. Code that calls `Repository.read_resilient` directly skips the trimming; only `Preferences.read` does it today.

No author-sourced findings. I didn't write this change, so I have no author context to add. Nothing to index: there are no P0/P1 systemic findings.

---

## Next Steps

There are 3 findings, all P3 and all from the code-reviewer. None blocks merging.

- **Worth doing:** the clean-key regression test. It's cheap and documents that clean IDs pass through unchanged.
- **Could be left as is:** the `None` key and the whitespace-only key. Both are outside the README's string-ID contract. Fix them only if you want stricter input checks.

**How would you like to proceed?**

1. **Fix all**: add the type check, the empty-ID handling and the tests
2. **Fix specific items**: e.g. just the clean-key test
3. **No changes**: the review is complete
