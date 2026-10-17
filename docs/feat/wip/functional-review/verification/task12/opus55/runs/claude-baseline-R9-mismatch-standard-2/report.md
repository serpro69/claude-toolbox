## Code Review Summary

**Files reviewed**: 2 files (`reader.py`, `tests/test_reads.py`), 10 insertions, 4 deletions (staged)
**Profiles**: `python` (matched on `.py` extension). Loaded its security, SOLID, code-quality and removal-plan checklists.
**Overall assessment**: **REQUEST_CHANGES**

The trimming works, but the same line also swaps `read_resilient` for `read_once`. That removes the retry behaviour the README says to keep, and the updated test now checks for the broken behaviour.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[reader.py:2]** Trimming change also removes retries on transient errors
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling)
  - Triggered by: content — `.py` extension
  - Before, the call was `repository.read_resilient(key)`. Now it's `repository.read_once(key.strip())`. `read_resilient` (`repository.py:29-35`) makes up to 3 attempts on `TransientRead`. `read_once` makes one. The README says: *"Trim the ID before looking it up; preserve the existing resilient-read contract. A logical read may make up to three attempts on `TransientRead`…"* After this change, every `Preferences.read` call fails on the first transient backend error, which used to be absorbed.
  - Confidence: 97%. The only path is `Preferences.read` → `read_preferences` → `read_once` → `backend.read`, with no retry anywhere along it. The README states the contract outright.
  - Fix: `return repository.read_resilient(key.strip())`

- **[tests/test_reads.py:13-17]** `test_transient_error` checks for the broken behaviour
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling)
  - Triggered by: content — `.py` extension
  - The backend is set up to fail once (`TransientRead("busy")`) and then return `{"color": "blue"}`. The test expects `TransientRead` to be raised with one backend call. Under the contract, the retry should succeed. So the test passes only because of the P1 above, and it would fail once that's fixed.
  - Confidence: 95%. Under `read_resilient`, the second outcome is returned and `backend.keys == ["w", "w"]`.
  - Fix:
    ```python
    def test_transient_error_is_retried(self):
        backend = ScriptedBackend([TransientRead("busy"), {"color": "blue"}])
        self.assertEqual(Preferences(Repository(backend)).read(" w "), {"color": "blue"})
        self.assertEqual(backend.keys, ["w", "w"])
    ```

### P2 - Medium

- **[tests/test_reads.py]** Two rules in the retry contract have no tests
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The README defines two more rules that no test checks: (a) after 3 transient failures, `TransientRead` is raised to the caller; (b) `MissingPreference` is raised on the first attempt, with no retry. If those tests had existed, the P1 regression would have been caught, or at least made more visible.
  - Confidence: 85%. These are missing tests, not a bug in the change itself.
  - Fix: add `test_transient_exhausted` (3× `TransientRead` → `assertRaises`, `keys == ["w"]*3`) and `test_missing_is_not_retried` (`MissingPreference` then a success value → `assertRaises(MissingPreference)`, `keys == ["w"]`). Both should use a padded key so they also check that trimming happens before each attempt.

### P3 - Low

- **[reader.py:2]** Unusual keys after `strip()`
  - Profile: python · Checklist: code-quality-checklist.md (String Boundaries / None Handling)
  - Triggered by: content — `.py` extension
  - A key that is only whitespace becomes `""` and is still sent to the backend. A non-string key (e.g. `None`) now raises `AttributeError`, where before it was passed through unchanged. The README only talks about preference IDs with whitespace around them, so this may be fine.
  - Confidence: 50%. It depends on what callers pass, and that isn't in the repo.
  - Fix (optional): reject empty keys after trimming, or document that IDs must be non-empty strings.

---

## Additional Suggestions

- The rename from `test_existing_key` to `test_trim_key` is fine, because the padded-key case also covers the plain lookup.
- Security and SOLID checklists turned up nothing: there's no untrusted input reaching anything dangerous, and the trimming sits at the right layer.

**Not covered**: I didn't run the test suite. I expect it passes as staged, because the test was changed to match the regression.

**Indexed**: the main finding is saved to capy as `kk:review-findings` (a trimming change that also dropped the retry, with tests changed to match).

---

## Next Steps

I found 4 issues (P0: 0, P1: 2, P2: 1, P3: 1).

What I recommend fixing:
1. P1: restore `read_resilient` in `reader.py:2` and keep the `.strip()`.
2. P1: change `test_transient_error` to expect the retry to succeed.
3. P2: add tests for "exhausted retries raise" and "`MissingPreference` is not retried".
4. P3: optional, decide how empty or non-string keys should be handled.

**How would you like to proceed?**

1. **Fix all**: I'll make all the suggested fixes
2. **Fix P0/P1 only**: just the two high-priority issues
3. **Fix specific items**: tell me which ones
4. **No changes**: review complete, nothing to implement
