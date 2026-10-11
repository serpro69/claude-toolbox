## Code Review Summary

**Files reviewed**: 2 files, 10 insertions and 4 deletions (staged)
**Overall assessment**: REQUEST_CHANGES

The ID trimming works, but the same change also turns off retries on preference reads. A rewritten test makes that pass. Both staged tests pass, but one of them checks the wrong behavior.

**Profiles**: `python` only (both files are `.py`). I applied all four of its checklists: security, SOLID, code quality and removal.

---

## Findings

### P0 - Critical

- **[reader.py:2]** Reads no longer retry on `TransientRead`
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling: "What happens when this operation fails?")
  - Triggered by: extension `.py`
  - The task was only to trim the key. The diff also changed `repository.read_resilient(key)` to `repository.read_once(key.strip())`. `read_resilient` (`repository.py:29-35`) is the only place the 3-attempt retry lives. `README.md:5-8` says to keep it: "preserve the existing resilient-read contract… up to three attempts on `TransientRead`". Now every short-lived backend error goes straight to the caller of `Preferences.read`.
  - Confidence: 97%. I traced `Preferences.read` → `read_preferences` → `read_once` → `backend.read`, and nothing else on that path retries. The README states the contract outright, so this isn't a matter of taste.
  - Fix: `return repository.read_resilient(key.strip())`

- **[tests/test_reads.py:13-17]** `test_transient_error` checks for the bug
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The backend is set up as `[TransientRead("busy"), {"color": "blue"}]`. The test expects the error to be raised, with only one backend call. The contract says the second attempt should succeed and return `{"color": "blue"}`. So the test makes the regression above look intended, and the suite stays green.
  - Confidence: 95%. It follows directly from the README, and I ran the suite: 2 tests, both pass.
  - Fix: expect `{"color": "blue"}` as the result and `backend.keys == ["w", "w"]`.

### P2 - Medium

- **[tests/test_reads.py]** No tests for the rest of the retry rules
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The README also says that three failed attempts raise `TransientRead`, and that `MissingPreference` is raised on the first attempt with no retry. Neither is tested. Without these, a future edit could break the retry limit or start retrying permanent errors, and no test would fail.
  - Confidence: 85%. These are missing tests, not a broken path, but they're the exact guard that would have caught this change.
  - Fix: add a test with three `TransientRead`s (expects a raise, `keys == ["w"]*3`) and one with `[MissingPreference(), ...]` (expects a raise, `keys == ["w"]`).

### P3 - Low

- **[reader.py:2]** `key.strip()` raises `AttributeError` if the key isn't a string
  - Profile: python · Checklist: code-quality-checklist.md (None Handling)
  - Triggered by: extension `.py`
  - Passing `None` or an integer used to reach the backend. Now it fails earlier with a less helpful error. Leave it unless callers can actually send non-string IDs.
  - Confidence: 40%. Nothing in the repo shows keys being anything but strings.

---

## Removal/Iteration Plan

Nothing to remove. If `read_preferences` goes back to calling `read_resilient`, nothing in the codebase calls `read_once` directly anymore. That's fine, since `read_resilient` uses it internally.

## Other checks

- **Security**: no injection, secrets or deserialization concerns. Stripping the key doesn't create a path or lookup problem with this backend.
- **SOLID**: the layering (`Preferences` → `read_preferences` → `Repository`) is fine. The problem is that the wrong repository method gets called.
- **Knowledge base**: it was empty, so there were no prior findings or idioms to compare against.

**Indexing**: I saved the P0 pattern to `kk:review-findings` as a recurring risk: a normalization change that quietly switches a retrying call to its single-attempt version, with a test edited to match.

---

## Next Steps

I found 4 issues (P0: 2, P1: 0, P2: 1, P3: 1).

What I recommend fixing:
1. P0: go back to `read_resilient` in `reader.py:2`, keeping `.strip()`
2. P0: rewrite `test_transient_error` so the read succeeds on the second attempt
3. P2: add tests for three failed attempts and for `MissingPreference` not being retried

What I'd leave alone:
- P3 non-string key: keys appear to always be strings, and failing fast is acceptable.

**How would you like to proceed?**

1. **Fix all**: I'll make all the fixes above
2. **Fix P0/P1 only**: just the two P0 items
3. **Fix specific items**: tell me which ones
4. **No changes**: stop at the review
