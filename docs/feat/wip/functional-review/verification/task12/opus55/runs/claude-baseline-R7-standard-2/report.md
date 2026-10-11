I ran `/kk:review-code` in standard mode. Only the `python` profile matched, so I applied all four Python checklists (security, SOLID, code quality, removal).

## Code Review Summary

**Files reviewed**: 2 files, 12 insertions and 1 deletion (`payload.py`, `tests/test_payload.py`). I also read `client.py`, which calls the changed function.
**Overall assessment**: **COMMENT**. The change is small and correct for normal string input. Before deploying, you need to answer one question about what inputs the function must accept.
**Tests**: `python3 -B -m unittest discover -s tests` passes all 4 tests. Nothing is unstaged, so the tests ran against exactly what's staged.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[payload.py:2]** `.strip()` crashes on `None` (and any other non-string), where the old code passed it through
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → None Handling)
  - Triggered by: content — `.py` extension
  - Before, `save(transport, None)` sent `{"display_name": None}` (JSON `null`), which a settings API often reads as "clear this field." Now it raises `AttributeError: 'NoneType' object has no attribute 'strip'` before the request is sent. The same goes for any non-string value.
  - Confidence: 55%. I confirmed the old behaviour passed `None` through and the new code raises. Nothing in the repo passes `None`: the only caller is `client.save`, and the tests use strings only. But there are no type hints or docs saying what's allowed, so I can't tell whether outside callers rely on `None` meaning "clear." If `display_name` is always a `str`, this finding goes away.
  - Suggested fix: if `None` is allowed, keep it:
    ```python
    def build_payload(display_name):
        if display_name is None:
            return {"display_name": None}
        return {"display_name": display_name.strip()}
    ```
    If it isn't allowed, add a `str` type hint so the contract is written down.

::code-comment{file="payload.py" line="2" severity="P1"}
`display_name.strip()` raises AttributeError for None, which the old code passed through as JSON null. Confirm None isn't a valid "clear name" input, or guard it explicitly.
::

### P2 - Medium

- **[tests/test_payload.py:7-11]** Tests skip the inputs where behaviour actually changed
  - Profile: python · Checklist: code-quality-checklist.md (String Boundaries)
  - Triggered by: content — `.py` extension
  - The two tests cover the easy cases. They don't cover a whitespace-only name like `"   "`, which now becomes `""`. That changes what gets sent, and the server may treat `""` differently from a real name or from `null`. They also don't cover `None` or tabs and newlines.
  - Confidence: 80%. These are plain coverage gaps; whether they matter depends on the server.
  - Suggested fix: add `build_payload("   ") == {"display_name": ""}` (or whatever the intended result is), plus a `None` test that matches whichever choice you make for the P1.

### P3 - Low

- **[payload.py:1]** No type hints on `build_payload`. Adding `display_name: str` (or `Optional[str]`) would answer the P1 question in the code itself. Profile: generic · Confidence: 70%.

---

Nothing came up on security, SOLID or removal. The function stays a pure single-purpose helper, no input reaches a dangerous call, and nothing is left unused.

**Indexing:** No findings to index. The P1 is specific to this function, not a pattern across the codebase. The capy knowledge base was empty, so there were no earlier findings or language-idiom notes to check against.

## Is it ready to deploy?

**Yes, if `display_name` is always a string.** In that case the change is correct, small and tested, and only the P2 tests are left as a nice-to-have.
**No, if any caller sends `None` to clear the name.** Those calls will start crashing before the request goes out. This review can't settle that from the repo alone. You'd need to check the API contract or the callers outside this repo.

## Next steps

I found 3 issues (P0: 0, P1: 1, P2: 1, P3: 1).

What I recommend fixing:
1. P1: decide whether `None` is allowed, then guard it or add a type hint
2. P2: add tests for whitespace-only input and the `None` case
3. P3: add type hints

**How would you like to proceed?**
1. **Fix all**
2. **Fix P0/P1 only**
3. **Fix specific items**
4. **No changes**

I won't change anything until you choose.
