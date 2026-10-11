## Code Review Summary

**Verdict: REQUEST_CHANGES.** The trimming works, but the change also drops the retry behavior that `README.md` requires, and the updated test now expects the broken behavior.

**Files reviewed**: 2 files, 10 insertions and 4 deletions (staged)

**What was asked**: `README.md` says preference IDs with surrounding whitespace should be accepted by trimming them before lookup. It also says the existing retry rules must keep working: up to 3 attempts on `TransientRead`, returning the first success; `TransientRead` is raised only after all 3 fail; `MissingPreference` is raised on the first attempt without retrying; reads have no side effects. There is no task or design doc beyond the README.

**What was reviewed**: the staged diff (`git diff --cached`) against `HEAD` 7c0410c. Nothing was unstaged, so the files on disk match what is staged. There is no separate release version to compare against.

## Behavior and Compatibility

Read path: `Preferences.read` (`preferences.py:9`) calls `read_preferences` (`reader.py`), which calls `Repository`.

- **Before**: `repository.read_resilient(key)`, which retries up to 3 times on `TransientRead`.
- **After**: `repository.read_once(key.strip())`, a single attempt with no retries.

I ran these scenarios against the `repository.py` test backend:

| Scenario | Required | Your change | Read calls |
| --- | --- | --- | --- |
| `" w "`, success | `{"color": "blue"}`, key `"w"` | ✅ correct | `["w"]` |
| `TransientRead` then success | returns the success | ❌ raises `TransientRead` | `["w"]` |
| `TransientRead` ×3 | raises after 3 attempts | ❌ raises after 1 | `["w"]` |
| `MissingPreference` | raises on attempt 1 | ✅ correct, but only because nothing retries anymore | `["w"]` |
| Fix (`read_resilient(key.strip())`), `TransientRead` then success | returns the success | ✅ returns the success | `["w","w"]` |
| Fix, `TransientRead` ×3 | raises after 3 attempts | ✅ | `["w","w","w"]` |
| Fix, `MissingPreference` | raises on attempt 1 | ✅ | `["w"]` |

- **Trimming whitespace**: works.
- **Retry behavior**: broken. The change causes it, and it affects every caller of `Preferences.read`.
- **Tests**: `python3 -B -m unittest discover -s tests` passes (2/2), but `test_transient_error` checks for the broken behavior.
- **Not checked**: concurrency, timing and deployment (the README says the test backend models none of these).

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[reader.py:2]** Trimming the key also removed the retry
  - Profile: generic · Checklist: — (also python/code-quality-checklist.md, Error Handling)
  - Triggered by: content — `.py` extension
  - **What happens**: any read where the first attempt hits a `TransientRead` should retry and succeed. Instead the error goes straight to the caller after one attempt. I confirmed this with the scenario run above.
  - **Why it's wrong**: the README requires up to three attempts. `read_resilient` owns retrying, and it is now never called. This breaks the existing behavior for every caller, not just inputs with whitespace.
  - **Test problem**: `tests/test_reads.py:13-17` (`test_transient_error`) feeds in `[TransientRead, success]` and asserts that `TransientRead` is raised after one call. That locks the broken behavior in, and it will fail once the code is fixed.
  - **Confidence**: 97%. The README is explicit, the code path is short, and the scenario run reproduced the failure. The test was clearly rewritten on purpose, but it contradicts the README, and only a change to the README contract could make it correct.
  - **Fix**: `return repository.read_resilient(key.strip())`. Then change `test_transient_error` to expect `{"color": "blue"}` with `backend.keys == ["w", "w"]`.

### P2 - Medium

- **[tests/test_reads.py:13]** Two of the README's retry rules have no tests
  - Profile: generic · Checklist: —
  - Triggered by: —
  - **Gap**: no test covers giving up after 3 transient failures (expect `TransientRead` with `keys == ["w"]*3`). No test covers `MissingPreference` being raised without retrying (expect `keys == ["w"]`). Both are explicit README rules, and the bug above went unnoticed because these tests don't exist.
  - **Confidence**: 90%. I checked the whole test file, and it only has the two tests shown in the diff.
  - **Fix**: add those two tests next to the corrected transient-then-success test.

### P3 - Low

(none)

---

The Python security, SOLID and removal checklists found nothing else in this diff. I saved the P1 pattern (a call-site edit that swaps a retrying method for a single-attempt one) to the review-findings knowledge base so future reviews can catch it. The knowledge base had nothing related before this.

Do you want me to apply the fix to `reader.py` and update the tests (the corrected transient test plus the two new ones)? I haven't edited anything, since this was a review-only run.
