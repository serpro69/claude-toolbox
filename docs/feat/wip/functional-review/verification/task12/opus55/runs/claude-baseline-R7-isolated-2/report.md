## Review summary (isolated mode)

**Verdict: not ready to deploy yet.** The change is one line and correct for normal names. It adds a crash path for `None` that nothing tests, and the tests have not been run.

**Reviewers:** only the `code-reviewer` sub-agent ran. The external `pal codereview` reviewer couldn't run because the `pal` MCP server failed to connect. Nothing below is corroborated by a second model.

**Files reviewed:** `payload.py` (modified) and `tests/test_payload.py` (new). The reviewer also checked the only caller, `client.py`, and its tests in `tests/test_client.py`.

**Scope note:** Bash was denied in this session, so I couldn't run `git diff --cached` or the test suite. Since `git status` showed no unstaged edits, the files on disk match what's staged. But the old version of `payload.py` wasn't visible, so "behavior before the change" is an assumption.

---

### Code reviewer findings

Profile: python. Checklists used: security, solid, code-quality, removal-plan.

- **`payload.py:2`: `.strip()` crashes on `None` or any non-string value.** P1, confidence 60%
  - `client.save()` (`client.py:4-5`) passes `display_name` through with no check. A caller that sends `None` to clear the field, or a JSON body with `"display_name": null`, now raises `AttributeError` before the PUT is sent.
  - Suggested fix: decide what `None` should do (pass through or raise a clear error), add a type hint, and test it.
  - My note: I confirmed the code matches this. Whether any real caller sends `None` can't be checked from this repo.

- **`payload.py:2`: input that is only whitespace now becomes `""`.** P2, confidence 65%
  - `"   "`, `"\t\n"` and a non-breaking space all collapse to an empty string and go out as `display_name: ""`.
  - My note: `tests/test_client.py:21-24` (`test_empty_name`) already expects `""` to be sent unchanged. So an empty name is already accepted, and this case may be intended. What's new is that it is now reachable from input that isn't empty.

- **`tests/test_payload.py:7-11`: the tests only cover the safe inputs.** P2, confidence 90%
  - There's no test for `None`, `""`, whitespace-only input, tabs or newlines, or non-strings. There's also no client-level test showing that `save(t, "  Ada  ")` sends `{"display_name": "Ada"}`.

- **`payload.py:1`: no type hint or docstring** saying a `str` is required and gets trimmed. P3

### My own observations (not from the reviewer)

- **`tests/test_payload.py:3`: the tests import with `from payload import build_payload`.** That only works if the repo root is on `sys.path` when tests run. `tests/test_client.py` uses the same pattern, so it's probably fine with your runner, but I couldn't confirm it without running the tests.

### Indexing

No findings to index. The P1 is a single missing input check, not a pattern that repeats across the code.

---

## Next steps

There are 5 findings: 1 P1, 2 P2 and 1 P3 from the reviewer, plus 1 of my own.

**What I recommend fixing before deploy:**
1. **P1:** decide what `build_payload(None)` should do and enforce it in the code.
2. **P2:** add tests for `None`, whitespace-only input, `"\tAda\n"`, and a `save()` test showing the name is trimmed.
3. **P3:** add `display_name: str` (or `str | None`) and a one-line docstring.
4. **Run the test suite.** I couldn't run it here, so "existing tests still pass" is from reading the code, not from a run.

**What I'd leave alone:** whitespace-only input becoming `""` is fine as long as you pin it in a test, since `test_empty_name` already treats `""` as allowed.

To get the second reviewer, reconnect the `pal` server and rerun `/kk:review-code:isolated`.

**How would you like to proceed?**
1. **Fix all:** I implement all the fixes above.
2. **Fix the P1 and P2s:** the `None` handling and the missing tests only.
3. **Fix specific items:** tell me which.
4. **No changes:** the review is done.
