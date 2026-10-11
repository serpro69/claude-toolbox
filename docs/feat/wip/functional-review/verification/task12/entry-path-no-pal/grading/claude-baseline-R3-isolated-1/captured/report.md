## Review Summary (Isolated Mode)

**Reviewers:** code-reviewer (Claude sub-agent) only. The second reviewer, pal codereview, couldn't run because no pal tools are available in this session. That means nothing below is corroborated by a second model, and the "External Review Findings" section is left out.
**Files reviewed:** 2 files, 6 lines changed (staged)
**Task scope:** mid-implementation. Task 1 (client receipt handling) is in scope; Task 2 (provider receipts) is pending and out of scope.

---

### Code Reviewer Findings

- **[client.py:5-6]** The receipt check breaks every ordinary save against the supported provider
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — extension .py
  - Severity: **P0** | Confidence: 97%
  - The released provider (`eval-release:provider/settings.py`) stores the values and returns only `{"ok": True}`. It never sends `applied`. So `response.get("applied") is not True` is always true, and `save_settings` raises on every call, including when `enhanced_settings=False`.
  - This breaks the README contract ("must support the released provider at `eval-release`, including ordinary settings saves while enhanced_settings is false") and design.md ("ordinary saves must continue to work… independently releasable main").
  - The values are already stored when the client raises. The caller sees a failure for a write that worked, and a retry would send the same write again.
  - Task 2 can't fix this: the README says "a pending provider task cannot change the supported baseline."
  - Suggested fix: only send or enforce the receipt on the enhanced path. Treat a missing `applied` as a legacy success, and fail only on an explicit `applied: False`.
  - Author context: I checked the provider snapshot myself with `git show eval-release:provider/settings.py`. It is exactly `storage[workspace_id] = dict(request["settings"]); return {"ok": True}`. The extra `require_receipt` key in the request is harmless because that provider only reads `request["settings"]`. The breakage comes entirely from the new `applied` check.

- **[tests/test_client.py:8]** The test was changed to an unreleased response shape, which hides the regression
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — extension .py
  - Severity: **P1** | Confidence: 92%
  - The stub used to return `{"ok": True}`, which matches the released provider. It now returns `{"ok": True, "applied": True}`, which no deployed provider sends. Left unchanged, the old test would have caught the P0.
  - Nothing now tests the released baseline, the `ok: False` path, or a missing or negative receipt.
  - Suggested fix: bring back a test that uses `{"ok": True}` with `enhanced_settings=False` and expects success. Add tests for `applied: True`, `applied: False` (raises) and `ok: False` (raises). If the enhanced path requires a receipt, test it with and without one.

The reviewer had one other note, not a finding: once Task 2 defines the contract, the strict `is True` check will reject truthy values like `1`.

### Indexing
I indexed the P0 pattern in capy as `kk:review-findings`: a protocol requirement enforced without the flag gate breaks the released counterpart, and the test was edited to hide it.

The temp review files are in `/tmp/kk-review-code-enhanced-settings-t1/`. Bash cleanup was denied, so you can delete that folder whenever you like.

---

## Next Steps

There are 2 issues, both from the code-reviewer; none are corroborated or author-sourced.

I recommend fixing both:
1. **P0** `client.py`: make the receipt check backward compatible. Gate it on `enhanced_settings` and accept a missing `applied` on ordinary saves.
2. **P1** `tests/test_client.py`: bring back the `eval-release` response-shape test and add the receipt and error-path tests.

**How would you like to proceed?**

1. **Fix all**: I'll implement both fixes.
2. **Fix corroborated + high severity**: here this is the same as option 1, since both are P0/P1.
3. **Fix specific items**: tell me which ones.
4. **No changes**: the review is done.

One thing to decide if I fix it: once `enhanced_settings=True`, should a missing receipt fail, or be accepted until the provider increment ships? Either way, ordinary saves have to keep working.
