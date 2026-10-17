## Review summary (isolated mode)

**Request changes.** The trim does what you intended, but the same line also removes retries on transient errors. The rewritten test then treats that loss as expected behavior.

**Reviewers:** only the `code-reviewer` sub-agent ran. The second reviewer, `pal codereview`, couldn't run because the `pal` server failed to connect this session. There are no "both reviewers agreed" findings, so treat everything below as one reviewer's view.

**Files reviewed:** `reader.py` and `tests/test_reads.py`, 10 lines added and 4 removed. Only the Python checklists applied.

I checked the two P1 findings myself against `repository.py` and `README.md`, and both hold. The reviewer's line numbers for the test file were wrong, so I fixed them below.

### Findings

**1. P1 — `reader.py:2`: retries were removed in a change described as trimming the ID** (confidence 97%)
- `read_resilient(key)` became `read_once(key.strip())`. Only the `.strip()` is the trimming you described.
- `read_resilient` is what retries up to 3 times on `TransientRead` (`repository.py:29-35`). `read_once` makes one attempt.
- `README.md:5-8` requires this change to "preserve the existing resilient-read contract".
- `Preferences.read` is the only public entry point, so every caller loses the retry.
- **Fix:** `return repository.read_resilient(key.strip())`

**2. P1 — `tests/test_reads.py:13-17`: `test_transient_error` checks for the bug instead of the documented behavior** (confidence 95%)
- The backend is set up to fail once with `TransientRead` and then succeed. The test expects the error to be raised after one call (`keys == ["w"]`).
- Under the documented behavior, the read should succeed on the second try and return `{"color": "blue"}` with `keys == ["w", "w"]`.
- **Fix:** change the test to expect the second try to succeed. Add a test where three `TransientRead`s in a row raise the error after 3 calls, each using the trimmed key.

**3. P2 — `tests/test_reads.py`: no test for `MissingPreference`** (confidence 75%)
- The README says `MissingPreference` is permanent and must be raised on the first attempt. Nothing tests that, so a later change could start retrying it.
- **Fix:** add a test with `ScriptedBackend([MissingPreference("w"), {...}])` that expects the error to be raised and `keys == ["w"]`.

**4. P3 — `reader.py:2`: `.strip()` changes what happens with bad keys** (confidence 55%)
- A `None` or non-string key now raises `AttributeError` in `reader.py`.
- A key that is only spaces becomes `""` and is looked up as an empty ID.
- **Fix:** decide the behavior and either check for it or document it.

**5. P3 — `tests/test_reads.py:8-11`: no test for a plain key any more** (confidence 50%)
- `test_existing_key` was renamed and now uses `" w "`. The common case with no whitespace no longer has its own test.

### Not covered
- Whether real backends store keys with deliberate surrounding spaces. Trimming would make those entries unreachable, and this repo can't show that.
- Behavior against a real backend, since the scripted one has no timing or concurrency.

### Other notes
- **Saved to the knowledge base:** the pattern behind finding 1 (a resilient call swapped for a single attempt during an unrelated change) is now in capy as `kk:review-findings`.
- **Temp file:** shell commands are blocked in this session, so I couldn't delete `/tmp/kk-review-code-staged-prefid.patch`. You can remove it by hand.

---

## Next steps

I recommend fixing:
1. Finding 1 (P1): go back to `read_resilient` and trim the key inside it.
2. Finding 2 (P1): rewrite `test_transient_error` to expect the retry to succeed, and add a test for three errors in a row.
3. Finding 3 (P2): add a test that `MissingPreference` is raised on the first attempt.
4. Finding 5 (P3): bring back the plain-key test next to `test_trim_key`.

I'd leave finding 4 (P3) as is unless you know callers can pass non-string or blank keys. The README only asks for trimming.

**How would you like to proceed?**
1. **Fix all**
2. **Fix the two P1s only**
3. **Fix specific items** (tell me which)
4. **No changes**
