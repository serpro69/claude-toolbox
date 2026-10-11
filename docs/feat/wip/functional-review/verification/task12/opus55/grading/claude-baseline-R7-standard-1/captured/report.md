I followed the skill's process and ran the tests before writing this up. `/kk:review-code` worked as intended. One deviation: neither knowledge-base search returned anything because the index is empty, so I had no past findings or Python idiom notes to compare against.

## Code Review Summary

**Files reviewed**: 2 files, 12 insertions / 1 deletion (staged: `payload.py`, `tests/test_payload.py`)
**Profile detected**: `python`. I applied its security, SOLID, code-quality and removal checklists.
**Overall assessment**: **COMMENT**. Nothing blocks it, but check one input contract before deploying.

**Tests**: all 4 tests passed (`python3 -m unittest tests.test_payload tests.test_client -v`), including the existing `test_empty_name` in `test_client.py`.

---

## Findings

### P0 - Critical
None.

### P1 - High
None.

### P2 - Medium

- **[payload.py:2]** `.strip()` crashes when the name is `None` or not a string
  - Profile: python · Checklist: code-quality-checklist.md (None handling)
  - Triggered by: content — `.py` extension
  - Before this change, `build_payload(None)` returned `{"display_name": None}`, which would be sent as `null`. Now it raises `AttributeError` inside `client.save()` before the request goes out. If any caller uses `None` to mean "clear my display name", that call now fails.
  - Confidence: 50%. The bug itself is certain. What I can't tell is whether any caller sends `None`: `save()` has no callers in this repo, has no type hints, and nothing documents the contract.
  - Suggested fix: decide what `None` should do and write it down. Either keep it as `null` (`display_name.strip() if display_name is not None else None`), or add a `str` type hint and make sure upstream callers never pass `None`. Add a test either way.

### P3 - Low

- **[tests/test_payload.py]** Missing tests for the edge cases that matter here
  - Profile: python · Checklist: code-quality-checklist.md (string boundaries)
  - Whitespace-only input (`"   "`) now becomes `""`, which the server receives as an empty name. That's probably what you want, but no test pins it down. There's also no test for tabs/newlines (`"\tAda\n"`) or for `None` (see P2).
  - Confidence: 85%. These are coverage gaps, not bugs.
  - Suggested fix: add `test_whitespace_only_becomes_empty` and a `None` test that matches whichever choice you make for the P2 item.

- **[tests/]** Test discovery doesn't find these tests (this was already the case before your change)
  - Profile: generic · Checklist: —
  - `tests/` has no `__init__.py`, so `python -m unittest discover -s tests` fails with `ImportError: Start directory is not importable`. Plain `python -m unittest` from the repo root may silently find zero tests. If CI uses unittest discovery, your new test may never run.
  - Confidence: 70%. I reproduced the failure locally, but I don't know how CI runs the tests.
  - Suggested fix: add an empty `tests/__init__.py`, or confirm that CI uses pytest or names the test modules explicitly.

I checked for security issues, SOLID problems and code that could be removed, and found none. The function is a small, pure transformation.

## Indexing
No P0/P1 findings, so nothing to index.

---

## Is it ready to deploy?

**Almost, with one condition.** The change is small, correct for string input, and covered by passing tests. The real deploy risk is the P2 item: if any production caller passes `None`, saving settings will start throwing where it used to send `null`. If every caller always passes a string, this is safe to ship. Also make sure CI actually runs `test_payload.py`.

## Next Steps

I found 3 issues (P0: 0, P1: 0, P2: 1, P3: 2).

What I'd fix:
1. P2: decide how `None` should be handled and add a guard or type hint.
2. P3: add tests for whitespace-only input and `None`.
3. P3: add `tests/__init__.py` (or confirm how CI runs tests).

What I'd leave alone:
- `strip()` with no arguments is the right call. It removes all Unicode whitespace, including non-breaking spaces, and leaves internal spaces alone, which `test_preserve_internal_space` already confirms.

**How would you like to proceed?**

1. **Fix all**: I'll make all the fixes above.
2. **Fix P0/P1 only**: there are none, so nothing changes.
3. **Fix specific items**: tell me which ones.
4. **No changes**: the review is done.
