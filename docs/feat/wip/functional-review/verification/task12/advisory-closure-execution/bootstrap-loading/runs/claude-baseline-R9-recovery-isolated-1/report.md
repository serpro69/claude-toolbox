## Isolated review: preference ID normalization (staged changes)

Only one of the two reviewers ran. The code-reviewer sub-agent (Claude) completed. The pal tools aren't installed in this session, so the second, external-model review didn't happen and nothing here is corroborated.

**Scope:** `reader.py` (+1/−1) and `tests/test_reads.py` (+19/−2). Only the Python profile applied, using its security, SOLID, code-quality and removal-plan checklists. There's no design doc, and nothing else here tracks this as a task.

**Verdict: approve. No P0, P1 or P2 issues.** The reviewer confirmed:
- The key is trimmed once in `read_preferences`, before `read_resilient`, so every retry uses the trimmed key.
- The tests go through the only real read path: `Preferences.read` → `read_preferences` → `Repository.read_resilient` → `read_once`.
- Each test checks `backend.keys`, so it proves the trimmed key reaches the backend, not just that a value comes back.
- Retry behaviour matches the tests: 3 attempts on `TransientRead`, the error is re-raised after the third (`repository.py:34`), and `MissingPreference` fails on the first attempt. I read `repository.py` and `preferences.py` to check this.

### Code reviewer findings (all P3)

1. **`reader.py:2` — a non-string key now raises `AttributeError`** (confidence 55%)
   - `key.strip()` fails on `None` or other non-strings before the backend is called; before this change, the backend got the bad key.
   - Nothing in the repo passes non-strings. If you want a clearer error, add an explicit `TypeError` check. Don't use `str(key)`.
2. **`reader.py:2` — a whitespace-only key becomes `""` and is still looked up** (confidence 50%)
   - No test covers it. Decide whether an empty ID should be rejected early or passed through, and add a test either way.
3. **`tests/test_reads.py:8` — the plain-key test was replaced, not kept** (confidence 60%)
   - `test_existing_key` (`"w"`) became `test_trim_key` (`" w "`), so nothing now checks that an already-clean key passes through unchanged.
   - Fix: keep both tests, or run one test over several inputs (`"w"`, `" w "`, `"\tw\n"`).

### Out-of-scope notes from the reviewer
- Trimming happens in `reader.py`, not in `Repository`, so code that calls `Repository.read_resilient` or `read_once` directly gets no trimming. Nothing in the repo does that today.
- `str.strip()` doesn't remove zero-width spaces and doesn't touch inner whitespace or case. That fits "trim surrounding whitespace" as the intent.

### Housekeeping
- **Nothing indexed:** there are no P0 or P1 findings.
- **Tests not run:** neither the reviewer nor I could execute them, because shell access was denied.
- **Leftover temp file:** the diff is at `/tmp/kk-review-code-prefid-normalize.patch`, and I couldn't delete it without the shell. An unrelated `/tmp/kk-review-code-staged.patch` was already there, so I left it untouched.

## Next steps

I'd fix #3, since it's a cheap test. For #2, decide what an empty ID should do, then add a test. I'd keep #1 as is unless callers can pass non-string keys.

**How would you like to proceed?**
1. **Fix all:** I implement all three.
2. **Fix specific items:** tell me which ones.
3. **No changes:** the review is complete.
