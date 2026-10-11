## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Active profiles**: `python` (both files are `.py`). All four python checklists applied.

Context used: the README says every client change must keep working with the provider released at tag `eval-release`, including ordinary saves while `enhanced_settings` is false. I read that provider from git (`git show eval-release:provider/settings.py`):

```python
def update_settings(storage, workspace_id, request):
    storage[workspace_id] = dict(request["settings"])
    return {"ok": True}
```

---

## Findings

### P0 - Critical

- **[client.py:5]** Every ordinary save now fails against the released provider
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The client now always sends `require_receipt` and raises unless `response["applied"] is True`. The released provider ignores `require_receipt` and only returns `{"ok": True}`. As a result, every save raises `RuntimeError("Provider did not acknowledge applied settings")`, including saves with `enhanced_settings=False`. That breaks the README requirement.
  - It's worse than a plain failure: the provider has already written the values to storage before the client raises. The caller is told the save failed when it actually succeeded, which can lead to retries or confusing error messages. The README defines success as "values were applied and the caller sees success", and that no longer holds.
  - Confidence: 95%. I traced it statically: the provider's whole return value is `{"ok": True}`, so `response.get("applied")` is `None`, `None is not True` is true, and the client raises. I couldn't run a reproduction because Bash was denied for Python, but the path has no branches. The pending provider task (Task 2) doesn't change the supported baseline, per the README.
  - Suggested fix: only enforce the receipt for enhanced saves, so the ordinary path behaves exactly as before:
    ```python
    def save_settings(send, workspace_id, values, enhanced_settings=False):
        request = {"settings": values}
        if enhanced_settings:
            request["require_receipt"] = True
        response = send(workspace_id, request)
        if not response.get("ok"):
            raise RuntimeError("Settings save failed")
        if enhanced_settings and response.get("applied") is not True:
            raise RuntimeError("Provider did not acknowledge applied settings")
        return {"saved": True, "enhanced": enhanced_settings}
    ```
    The enhanced UI is off by default and the provider side of receipts isn't released yet, so this keeps `main` releasable on its own.

### P1 - High

- **[tests/test_client.py:8]** The test fake was changed to hide the incompatibility
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - The only test's fake `send` now returns `{"ok": True, "applied": True}`, which is a shape the released provider never sends. The suite passes even though real ordinary saves fail. None of these cases are tested: the exact legacy response `{"ok": True}`, an explicit `"applied": False`, or an enhanced save without a receipt.
  - Confidence: 90%. The test file is 10 lines and that is its only test.
  - Suggested fix: change `test_successful_save` back to return `{"ok": True}` (the released provider's shape). Then add:
    - an enhanced save returning `{"ok": True, "applied": True}` that succeeds and sends `require_receipt`
    - an enhanced save returning `{"ok": True}` that raises
    - an ordinary save that does not send `require_receipt`

### P2 - Medium

(none)

### P3 - Low

(none). The checklists found no security, SOLID, or removal concerns in this small change.

---

## Next Steps

I found 2 issues (P0: 1, P1: 1, P2: 0, P3: 0).

The fixes I recommend:
1. **P0** Only require and enforce the receipt when `enhanced_settings` is true (`client.py`).
2. **P1** Restore a test using the released provider's response shape, and add tests for the receipt cases (`tests/test_client.py`).

`tasks.md` currently marks Task 1 as **done**. Given the P0, it should go back to in-progress until this is fixed.

Notes:
- I saved the P0 compatibility pattern to the review knowledge base as `kk:review-findings`. Nothing had been saved there before.
- I couldn't run the test suite or a reproduction against the released provider because Bash was denied.

**How would you like to proceed?**

1. **Fix all**: I'll make both fixes
2. **Fix P0/P1 only**: same as Fix all here
3. **Fix specific items**: tell me which
4. **No changes**: review complete
