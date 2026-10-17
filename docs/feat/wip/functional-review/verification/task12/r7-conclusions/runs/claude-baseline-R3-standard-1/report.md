## Code Review Summary

**Files reviewed**: 2 files (`client.py`, `tests/test_client.py`), 6 lines changed (staged)
**Overall assessment**: **REQUEST_CHANGES**
**Profiles:** `python`, matched by the `.py` extension on both files. I applied all four of its checklists (security, SOLID, code quality, removal plan). No other profile matched and none of the checklist rules depend on file content.

I couldn't run the tests or try the change against the released provider because shell commands were blocked. The P0 below comes from reading the code: I compared the client against `git show eval-release:provider/settings.py`.

---

## Findings

### P0 - Critical

- **[client.py:5]** Every ordinary save now fails against the supported provider, even though the provider has already saved the values
  - Profile: python · Checklist: security-checklist.md (Data Integrity) + code-quality-checklist.md (Error Handling)
  - Triggered by: content — `.py` extension
  - The README says every client change must work with the provider at tag `eval-release`, including ordinary saves while `enhanced_settings` is false. That provider is:
    ```python
    def update_settings(storage, workspace_id, request):
        storage[workspace_id] = dict(request["settings"])
        return {"ok": True}
    ```
    It never returns `applied`. So `response.get("applied") is not True` is always true, and `save_settings` raises `"Provider did not acknowledge applied settings"` on every save, whatever the flag says. The provider has already written to `storage` by then. The caller is told the save failed when it actually succeeded, which breaks the README's rule that a successful save means "values were applied and the caller sees success". Callers may also retry a save that already went through. Task 2 (provider receipts) is still pending, and the README says a pending provider task can't change the supported baseline.
  - Confidence: 95%. The released provider source is short and clear, and the client check is unconditional. I'm not at 100% only because I couldn't run it.
  - Suggested fix: only require and check the receipt when the enhanced feature is on, and leave the ordinary path as it was:
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
    The enhanced UI is off by default (design.md), so this keeps `main` releasable on its own until Task 2 ships.

### P1 - High

- **[tests/test_client.py:8]** The test's fake provider was changed to the new response shape, which hid the regression
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The fake `send` now returns `{"ok": True, "applied": True}`, a response the released provider never sends. The only test therefore passes while real ordinary saves would fail. Nothing tests that the receipt is enforced (missing or `False` `applied`), and nothing tests `enhanced_settings=True`.
  - Confidence: 90%. I read the test file in full. It has one test, and its fake doesn't match `eval-release`.
  - Suggested fix: change `test_successful_save` back to return `{"ok": True}`, matching the released provider, and add:
    - an enhanced save with `applied: True`, which succeeds and sends `require_receipt`;
    - an enhanced save with `applied` missing or `False`, which raises;
    - optionally, a check that an ordinary save doesn't send `require_receipt`.

### P2 - Medium

(none)

### P3 - Low

(none). `require_receipt` is sent on every request, but the released provider only reads `request["settings"]`, so it does no harm. The P0 fix gates it anyway.

---

## Additional Suggestions

- Both new failure modes raise a bare `RuntimeError`. A specific exception for a missing receipt would let callers tell "the provider rejected the save" apart from "the save may have gone through but wasn't confirmed". That's optional and could wait until the enhanced UI uses it.

**Indexing:** I saved both patterns to `kk:review-findings`: the unconditional protocol requirement that breaks compatibility with the released provider, and the test fake that matches the new contract instead of the released one.

---

## Next Steps

I found 2 issues (P0: 1, P1: 1, P2: 0, P3: 0).

The actionable items I recommend fixing:
1. P0: only require the receipt (and send `require_receipt`) when `enhanced_settings` is on, in `client.py`.
2. P1: make the test fake match the released provider's `{"ok": True}` and add tests for the enhanced receipt path.

**How would you like to proceed?**

1. **Fix all**: I'll implement all suggested fixes
2. **Fix P0/P1 only**: same as option 1 here
3. **Fix specific items**: tell me which issues to fix
4. **No changes**: the review is done and nothing gets implemented
