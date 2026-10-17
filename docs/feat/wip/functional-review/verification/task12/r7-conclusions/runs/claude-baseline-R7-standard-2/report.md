## Code Review Summary

**Files reviewed**: 2 files, 12 lines added, 1 removed (`payload.py`, `tests/test_payload.py`, both staged)
**Overall assessment**: COMMENT (approve with minor comments)
**Profile**: `python`, detected from the `.py` extensions. I applied all four of its checklists: security, SOLID, code quality and removal.

The change trims leading and trailing whitespace from `display_name` in `build_payload`. `client.save` (`client.py:5`) is the only caller in the repo, so every `PUT /settings` body is now trimmed.

---

## Findings

### P0 - Critical
None.

### P1 - High
None.

### P2 - Medium

- **[payload.py:2]** A `None` display name now crashes instead of being sent as-is
  - Profile: python · Checklist: code-quality-checklist.md (None handling)
  - Triggered by: content: `.py` extension
  - Before this change, `build_payload(None)` returned `{"display_name": None}`, which would be sent as JSON `null` (possibly how a name gets cleared). Now it raises `AttributeError: 'NoneType' object has no attribute 'strip'` before any request goes out.
  - Confidence: 45%. Nothing in this repo passes `None`, and there are no type hints or docs saying what input is allowed. The risk depends on callers outside this repo and on what the settings API accepts. If `None` is never valid, this isn't an issue.
  - Suggested fix: if `None` is valid, use `display_name.strip() if display_name is not None else None` and add a test. If it isn't, add a `str` type hint so the rule is written down.

### P3 - Low

- **[tests/test_payload.py]** Whitespace-only input isn't tested
  - Profile: python · Checklist: code-quality-checklist.md (String boundaries)
  - Triggered by: content: `.py` extension
  - `"   "` now becomes `""`. That's probably fine, since `tests/test_client.py:21-24` already treats `""` as a valid value. But it's a quiet behaviour change for names that are only spaces, and no test pins it down. `.strip()` also removes tabs, newlines and Unicode whitespace, which is probably what you want.
  - Confidence: 70%. This is a test gap, not a bug.
  - Suggested fix: add `test_whitespace_only_becomes_empty` and, optionally, a client-level trimming case in `tests/test_client.py`.

---

## Is it ready to deploy?

**Probably yes, with two checks first:**

1. **Tests haven't been run.** My first attempt failed because `tests/` has no `__init__.py`, so `unittest discover -s tests` can't import it from the repo root. The retry with `PYTHONPATH=.` was blocked by the permission mode. Reading the code, all four existing tests should pass: both `test_payload` cases and `test_client`'s `"Ada"` and `""` cases. Still, run `PYTHONPATH=. python3 -m unittest discover -s tests` before deploying. CI might hit the same discovery problem if it calls it the same way.
2. **Check whether any caller sends `None`** (the P2 above). If none do, nothing in this diff blocks the deploy.

Not covered: the settings server's contract (whether it accepts `""` or `null`, and whether it also trims), callers outside this repo, and any deploy config.

**Indexing**: nothing to index, since there are no P0/P1 findings. The capy knowledge base was empty, so there were no earlier findings for these files.

---

## Next Steps

I found 2 issues (P0: 0, P1: 0, P2: 1, P3: 1).

Fixes I recommend:
1. P2: handle `None` explicitly, or add a `str` type hint, depending on what the API allows.
2. P3: add a whitespace-only test case.

**How would you like to proceed?**

1. **Fix all**: I'll make both changes.
2. **Fix P0/P1 only**: there's nothing at that level, so no changes.
3. **Fix specific items**: tell me which ones.
4. **No changes**: the review is complete.

I won't change anything until you choose.
