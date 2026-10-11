## Review Summary (Isolated Mode)

**Verdict: REQUEST_CHANGES.** The trim works, but the change removes the retry on reads, which the README says must stay.

**Reviewers**: one of two ran.
- **code-reviewer (Claude sub-agent):** finished; it read the diff, the changed files, `preferences.py`, `repository.py` and the README.
- **PAL codereview:** did not run, because the `pal` MCP server failed to connect this session. There is no external opinion, so nothing here is "corroborated" by a second reviewer.

**Files reviewed**: `reader.py` and `tests/test_reads.py` (staged), plus the unchanged `preferences.py`, `repository.py` and `README.md`.

**Intent**: `README.md` asks for two things: trim whitespace from the preference ID, and keep the existing read behaviour. That behaviour is up to 3 attempts on `TransientRead`, returning the first success; `MissingPreference` fails straight away. There are no design or task docs.

**Baseline**: the change is compared against HEAD `7c0410c`; no release or deployed version was named.

**Workflow note**: the repo ships its own `plugins/kk`. It has the same 0.23.0 version number as the installed copy but different content, and it matches the command you ran, so I used it. Its packet helper script couldn't run because shell commands are restricted here, so I read every instruction file directly.

### Behaviour, before and after

The path is `Preferences.read` → `read_preferences` → `Repository`. `preferences.py:9` is the only caller of `read_preferences`.

| Scenario | Expected (README) | After this change |
|---|---|---|
| Key `" w "`, read succeeds | value returned, lookup uses `"w"` | Works (`test_trim_key`) |
| Transient error, then success | retries and returns the value | **Raises `TransientRead`.** `test_transient_error` checks for this wrong result |
| Transient, transient, success | returns the value on the 3rd try | **Raises on the 1st try**; no test |
| 3 transient errors | `TransientRead` after 3 attempts | `TransientRead` after 1 attempt; no test |
| `MissingPreference` | fails on the 1st attempt | Same; no test (none before either) |
| Transient error, then `MissingPreference` | `MissingPreference` on the 2nd attempt | `TransientRead` on the 1st; no test |
| No side effects | nothing modified | `strip()` creates a new string, so no change |

**Against the README: blocked.** Four of the documented cases now behave differently. Persistence and rollout don't apply: there's no stored data and no feature flag.

### Code Reviewer Findings

- **[reader.py:2] The change drops the retry: `read_resilient` was swapped for `read_once`**
  - P1, confidence 97%. Profile: python · Checklist: code-quality-checklist.md · Triggered by: `.py` extension
  - **What happens:** the first `TransientRead` now reaches the caller, where the old code recovered from it. When every attempt fails, the error comes after 1 attempt instead of 3. `read_resilient` is now called from nowhere.
  - **Fix:** trim the key first, then hand it to the retrying method, so every attempt uses the trimmed key:
    ```python
    return repository.read_resilient(key.strip())
    ```

- **[tests/test_reads.py:13-17] The new test checks for the wrong behaviour, and several failure cases have no tests**
  - P2, confidence 95%. Profile: python · Checklist: code-quality-checklist.md
  - **What happens:** `test_transient_error` asserts that a raise happens and that `keys == ["w"]`. Under the README it should get `{"color": "blue"}` back with `keys == ["w", "w"]`. Once the P1 fix is in, this test fails as written.
  - **Fix:** rewrite that test to expect success after one retry. Add tests for 3 transient errors, for `MissingPreference` on the first attempt, and optionally for a transient error followed by `MissingPreference`. Use `" w "` throughout, so the tests also show every retry uses the trimmed key.

**Not reported as findings:** the README doesn't say what should happen to a whitespace-only ID or a non-string key (`None.strip()` would raise), and nothing shows callers send either.

### What was and wasn't verified
- I ran `python3 -B -m unittest discover -s tests` on the staged code: both tests pass. That doesn't mean the behaviour is right, because one of the passing tests checks for the regression.
- The reviewer worked from source only; it couldn't run anything.
- The knowledge base had no earlier review findings or Python idiom notes to draw on.

### Housekeeping
- **Indexed:** one entry under `kk:review-findings`. It records the pattern of a small change switching a call away from the retrying method while the tests are rewritten to match.
- **Not cleaned up:** I couldn't delete the temp file `/tmp/kk-review-code-r9-staged-7c0410c.patch` because shell commands are restricted. Please remove it yourself (`rm /tmp/kk-review-code-r9-staged-7c0410c.patch`).

## Next Steps

I recommend fixing both findings: the one-line change in `reader.py:2` and the test updates. No findings look like false positives.

Should I go ahead?
1. **Fix both** (P1 + P2)
2. **Fix the P1 only**
3. **No changes**
