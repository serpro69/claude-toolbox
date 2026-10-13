## Code Review Summary

**Files reviewed**: 2 files (`client.py`, `tests/test_client.py`), 4 insertions, 2 deletions (staged)
**Overall assessment**: **REQUEST_CHANGES**

The `python` profile was the only one that matched. I applied all four of its checklists (security, SOLID, code-quality, removal-plan) and checked the change against `docs/feat/wip/enhanced-settings/*`, the README's delivery rules, and the released provider at tag `eval-release`.

---

## Findings

### P0 - Critical

- **[client.py:5]** The new receipt check makes every ordinary save fail against the released provider
  - Profile: python · Checklist: code-quality-checklist.md (missing/None handling) + security-checklist.md (Data Integrity)
  - Triggered by: content — `.py` extension
  - At `eval-release`, `provider/settings.py` writes the settings and returns only `{"ok": True}`. It has no `applied` field. `response.get("applied")` therefore returns `None`, `None is not True` is true, and `save_settings` raises `RuntimeError` on every save, including the default `enhanced_settings=False` path. That breaks the README requirement that every merged client increment support ordinary saves with the released provider. It is also a data-integrity problem: the provider has **already stored** the values when the client raises, so the caller is told the save failed when it succeeded. Callers may then retry or show false errors.
  - Confidence: 97%. I read the provider source from the tag with `git show eval-release:provider/settings.py`, and the logic is easy to trace. I couldn't run the test suite here because shell access was restricted after the first commands, so this rests on reading the code, not on a run.
  - Suggested fix: only send the receipt request and check the receipt when the enhanced feature is on, so ordinary saves keep the released protocol:
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
    Leftover risk: with `enhanced_settings=True` and the released provider, the "already applied but reported as failed" problem still happens until Task 2 ships. That's acceptable only because the enhanced UI is off by default. It should be noted in the implementation doc.

### P1 - High

- **[tests/test_client.py:8]** The test fake was changed to fit the new client, which hides the incompatibility
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The fake `send` now returns `{"ok": True, "applied": True}`, a response the supported provider never sends. The only test therefore passes while real ordinary saves break. There's no test for the released response shape, for a missing or `False` `applied`, or for what the request contains.
  - Confidence: 95%. The fake's return value is the only thing that differs from the released provider's response.
  - Suggested fix: keep a fake that returns exactly `{"ok": True}` (the released shape) and assert success with `enhanced_settings=False`. Add tests that (a) enhanced mode raises when `applied` is missing or `False`, (b) enhanced mode succeeds with `applied: True`, and (c) `require_receipt` is sent only when enhanced mode is on.

### P2 - Medium

(none)

### P3 - Low

(none)

---

## Additional Suggestions

- Extra request keys are safe: the released provider reads only `request["settings"]`, so `require_receipt` alone doesn't break anything. The problem is the response check.
- I found no security, SOLID, or removal concerns in this small diff.
- Indexing: I indexed the P0 pattern as `kk:review-findings`: "a client-side protocol addition must tolerate the released counterpart's response, and test fakes must mirror the released contract". The knowledge base was empty before this, so there were no earlier findings to compare against.

---

## Next Steps

I found 2 issues (P0: 1, P1: 1, P2: 0, P3: 0).

The actionable items I recommend fixing:
1. P0: put both the `require_receipt` request and the `applied` check behind `enhanced_settings` (`client.py:2-6`)
2. P1: restore a test fake with the released provider's response shape and add tests for the receipt paths (`tests/test_client.py`)

Also, `tasks.md` marks Task 1 as **done**. It should probably go back to in-progress until the P0 is fixed.

**How would you like to proceed?**

1. **Fix all**: I'll implement all suggested fixes
2. **Fix P0/P1 only**: Address critical and high priority issues
3. **Fix specific items**: Tell me which issues to fix
4. **No changes**: Review complete, no implementation needed
