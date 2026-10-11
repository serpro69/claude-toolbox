## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent). The `pal` codereview reviewer couldn't run because the `pal` MCP server failed to connect this session, so nothing here is corroborated by a second model.
**Files reviewed**: 2 files, 6 lines changed (staged)
**Task scope**: Task 1 (client receipt handling, done) was reviewed. Task 2 (provider receipts, pending) was treated as out of scope.

**Verdict: don't merge yet.** With this change, every ordinary save fails against the provider that's actually released.

---

### Code Reviewer Findings

- **`client.py:5-6`: every ordinary save now fails against the released provider, after the values are already saved**
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - Severity: **P0** | Confidence: 97%
  - At tag `eval-release`, the provider's `update_settings` stores the settings and returns only `{"ok": True}`. It never sends `applied`, and it ignores `require_receipt`. So the new `applied is not True` check raises on every save, whatever `enhanced_settings` is set to.
  - This breaks two requirements:
    - The design and README require ordinary saves to keep working with the `eval-release` provider. The README also says a pending provider task can't change that baseline.
    - The README defines success as "values were applied and the caller sees success". Here the values are stored but the caller gets an error.
  - Suggested fix: when `applied` is missing, treat it as the legacy provider and don't fail. Fail only when `applied` is present and not `True`. A better option is to enforce the receipt only once the provider says it supports receipts. Don't use `enhanced_settings` as the only gate.
  - Author context: I checked this myself with `git show eval-release:provider/settings.py`. The provider has a single return path, `return {"ok": True}`.

- **`tests/test_client.py:6-10`: the test was changed to fit the new behaviour, which hides the break**
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - Severity: **P1** | Confidence: 92%
  - The stub used to return the released provider's response, `{"ok": True}`. It now returns the shape of the undeployed provider, `{"ok": True, "applied": True}`. That's why the suite passes even though compatibility is broken. Nothing tests the new failure path (`applied: False`) or what the request contains.
  - Suggested fix:
    - Keep a test whose stub behaves like the `eval-release` provider, and assert that the save succeeds and the values are stored.
    - Add tests for `applied: True`, `applied: False` and `ok: False`.

- **`client.py:4,6`: callers can't tell "save failed" apart from "outcome unconfirmed"**
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - Severity: **P3** | Confidence: 60%
  - Both failures raise a plain `RuntimeError`. In the second case the provider accepted the save, so a caller might want to re-read the settings rather than retry blindly. If a strict receipt path survives the P0 fix, consider a dedicated subclass such as `SettingsNotAcknowledged(RuntimeError)`.

### Author-Sourced Findings

- **`client.py:6`: the lenient fix weakens the receipt guarantee** ⟨author-sourced⟩
  - Profile: generic · Checklist: —
  - Triggered by: —
  - If "no `applied` field" is treated as success, the client can't tell an old provider from a new one that wrongly leaves the field out. That's acceptable for now. It's the reason to prefer the capability-based check once Task 2 defines the contract.

**Indexed**: I saved the P0 as a reusable pattern under `kk:review-findings`: making an unreleased protocol field mandatory in an increment that has to ship on its own, and a test stub changed to hide it.

**Temp files**: The shell couldn't write files, so I couldn't delete the two I made with the file tool: `/tmp/kk-review-code-enhanced-settings-t1.patch` (the staged diff) and `/tmp/kk-review-code-eval-release-provider-settings.py` (a copy of the released provider).

---

## Next Steps

I found 4 issues: 3 from code-reviewer, 1 of my own, none from `pal` (it didn't run).

The actionable items I recommend fixing:

1. **P0**: make the receipt check work with the `eval-release` provider (`client.py:5-6`).
2. **P1**: put back a test that uses the released provider's response, and add tests for the receipt passing and failing (`tests/test_client.py`).
3. **P3**: optionally, a dedicated exception for "not acknowledged".

Item I recommend keeping as is:

- The author-sourced point is a known trade-off of the lenient fix, not something to fix now. It goes away once Task 2 adds a capability signal.

**How would you like to proceed?**

1. **Fix all**: I'll implement all suggested fixes.
2. **Fix high severity**: P0 and P1 only.
3. **Fix specific items**: tell me which.
4. **No changes**: the review is complete.

You can also rerun once `pal` reconnects to get the second-model check.
