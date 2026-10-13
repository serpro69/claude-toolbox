I've finished the review. I wasn't able to run the tests here because the shell was denied, so everything below comes from reading the code.

## Code Review Summary

**Files reviewed**: 2 files, 12 insertions, 1 deletion (`payload.py`, `tests/test_payload.py`)
**Profiles**: `python` (both files are `.py`), using all four Python checklists
**Overall assessment**: **COMMENT**. It's a small change and correct for the cases it tests. It's ready to deploy only if you can confirm the two behaviour changes below are intended.

The change: `build_payload` now trims spaces from the start and end of the display name. `client.save()` (`client.py:5`) is the only caller, and it passes the user's input straight through.

## Findings

### P0 / P1
None.

### P2 - Medium

- **[payload.py:2]** `None` input now crashes instead of being passed through
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → None handling)
  - Triggered by: content — `.py` extension
  - Before this change, `save(transport, None)` sent `{"display_name": None}`. Now `None.strip()` raises `AttributeError` before the request is sent. Nothing in this repo passes `None`, and nothing declares the input as `str`. But `save()` is the client's public entry point, and in a settings API `None` often means "clear" or "unset".
  - Confidence: 60%. Nothing in the repo calls it with `None`. I can't see external callers or the server contract.
  - Fix: if `None` is a valid input, use `display_name.strip() if display_name is not None else None`. If it isn't, add a `str` type hint so the rule is explicit.

- **[payload.py:2]** A name made only of spaces now becomes an empty string
  - Profile: python · Checklist: code-quality-checklist.md (String Boundaries → whitespace-only)
  - Triggered by: content — `.py` extension
  - Input like `"   "` used to be sent unchanged. Now it's sent as `""`. `tests/test_client.py:21-24` already treats `""` as a valid payload. If the server reads `""` as "clear my display name", a user who accidentally types spaces would silently lose their name. Before, the server would have stored or rejected the spaces.
  - Confidence: 55%. This may be exactly what you want. The concern is that no test covers it, so it's unclear whether the choice was deliberate.
  - Fix: decide what should happen (send `""`, reject it, or leave the field out) and add a test that locks it in.

### P3 - Low

- **[tests/test_payload.py]** The new tests are missing some edge cases
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - Only plain spaces are tested. Nothing covers spaces-only input, `None`, tabs or newlines, or Unicode spacing. Note that `str.strip()` removes non-breaking spaces (`\u00a0`) but not zero-width spaces (`\u200b`).
  - Confidence: 85%.
  - Fix: add a test for each of the two P2 decisions above, plus one for tabs and newlines.

No security, SOLID, performance or removal issues: it's a one-line, pure function that does no I/O.

## Deployment readiness

- **By reading the code, all tests should pass.** The two new tests should pass. The existing `test_save` and `test_empty_name` should be unaffected, since `"Ada"` and `""` don't change when trimmed. I didn't run them. Please run `python -m unittest discover -s tests` before deploying.
- **The decision is whether these two behaviour changes are acceptable:** `None` now crashes, and spaces-only input is now sent as `""`. If no caller sends `None` and an empty name is acceptable, this is low-risk and fine to deploy. If either one breaks how the server or other callers expect it to work, fix that first.

Index step: there are no P0/P1 systemic findings, so I didn't index anything. The knowledge base was empty, with no earlier findings or Python idioms stored.

---

## Next Steps

I found 3 issues (P0: 0, P1: 0, P2: 2, P3: 1). I recommend:
1. P2: decide how `None` should be handled, then guard it or add a type hint.
2. P2: decide what spaces-only input should produce, and add a test for it.
3. P3: add tests for tabs, newlines and Unicode spacing.

**How would you like to proceed?**
1. **Fix all**
2. **Fix P0/P1 only** (nothing to fix at that level)
3. **Fix specific items**
4. **No changes**
