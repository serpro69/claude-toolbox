## Isolated review of the staged preference ID normalization change

**Reviewers:** only the code-reviewer sub-agent ran. The second reviewer, pal codereview, couldn't run because its MCP server failed to connect, so nothing here was confirmed by a second model.
**Files reviewed:** 2 files (`reader.py`, `tests/test_reads.py`), about 20 lines changed
**Profile:** python, with its 4 standard review checklists, triggered by the `.py` extension
**Spec context:** none. There are no design docs; I used `README.md` as the contract.

### Findings

- **`reader.py:2` — the change also removes retries** · **P1** · 97% confidence
  - The change was described as "trim the ID", but it also swaps `read_resilient(key)` for `read_once(key.strip())`. Any `TransientRead` now reaches callers on the first attempt.
  - `README.md:5-12` says the opposite: "preserve the existing resilient-read contract… up to three attempts on `TransientRead`", and `read_resilient` owns the retry policy.
  - `Repository.read_resilient` (`repository.py:29-35`) now has no callers.
  - **Fix:** `return repository.read_resilient(key.strip())`
  - I read `README.md` and `repository.py` and confirmed this.

- **`tests/test_reads.py` (`test_transient_error`) — the new test locks in the bug** · **P1** · 95%
  - The backend is scripted as `[TransientRead("busy"), {"color": "blue"}]`. Under the contract, the read should retry and return `{"color": "blue"}`, with `backend.keys == ["w", "w"]`.
  - Instead the test expects `TransientRead` to be raised after one attempt. That hides the regression and would fail as soon as retries are restored.
  - **Fix:** assert the retry succeeds with the trimmed key on both attempts.

- **No tests for the other retry rules** · P2 · 75%
  - Nothing checks that `MissingPreference` is raised on the first attempt without retrying, or that retries stop after 3 transient errors.
  - Without these, a future broad `except` would go unnoticed.

- **`reader.py:2` — odd keys** · P3 · 50%
  - `key.strip()` raises `AttributeError` for a `None` key.
  - A key of only whitespace becomes `""` and is sent to the backend.
  - It's worth deciding on purpose what should happen in both cases.

- **`tests/test_reads.py:22` — renamed test** · P3 · 40%
  - `test_existing_key` was repurposed, so no test reads a key that has no whitespace to trim.

I didn't write this change, so I have no reasoning behind it to add. Reading the code again turned up nothing beyond the sub-agent's findings.

**Saved for future reviews:** I recorded the first P1 as a recurring risk in the local review knowledge base: a "normalization" change that also drops a retry wrapper, with a test rewritten to expect the failure.

**Not covered:**
- Tests weren't run; the sub-agent had no shell.
- Callers outside this repo weren't checked.
- Bash was blocked, so I wrote the diff to `/tmp/kk-review-code-staged.patch` and couldn't delete it. Remove it when convenient.

---

## Next steps

There are 5 findings: 2 P1, 1 P2 and 2 P3. I recommend fixing these:

1. **P1:** go back to `read_resilient(key.strip())` in `reader.py`.
2. **P1:** rewrite `test_transient_error` so the retry succeeds and `backend.keys == ["w", "w"]`.
3. **P2:** add tests for "raised after 3 transient errors" and "`MissingPreference` with no retry".
4. **P3:** keep a test for a key with no whitespace next to `test_trim_key`.

I'd leave the `None`/empty-key P3 alone unless you want a defined behavior for it. The README treats keys as IDs, so it isn't clearly a bug.

**How would you like to proceed?**

1. **Fix all:** I'll make every fix above.
2. **Fix high severity:** only the two P1s.
3. **Fix specific items:** tell me which.
4. **No changes:** stop here.
