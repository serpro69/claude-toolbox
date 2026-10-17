# Isolated review of the staged Task 1 client receipt handling

**Don't merge this as it stands.** Once the client change ships, every ordinary settings save against the supported provider will fail.

**Reviewers:** the code-reviewer sub-agent ran. The second reviewer, pal codereview, didn't run because pal isn't available in this session, so every finding below comes from one reviewer. Running standard `/kk:review-code` would give you a second pass.

**Scope:** `client.py` and `tests/test_client.py`, 6 changed lines. The python profile applied, so the security, SOLID, code-quality and removal-plan checklists were used. Task 1 was reviewed; Task 2 (provider receipts, pending) was excluded.

## Code reviewer findings

**P0: Every ordinary save fails against the supported provider** (`client.py:5`, confidence 97%)
- The supported provider is `provider/settings.py` at tag `eval-release`. It stores the values and returns only `{"ok": True}`. It never sends `applied`.
- The new check `response.get("applied") is not True` runs on every save, even when `enhanced_settings=False`. So every save raises.
- That breaks the README and design.md rule that ordinary saves must keep working with `eval-release`.
- The values are already written when the error is raised. The caller sees a failure for a save that actually worked, and may retry it.
- The README says "a pending provider task cannot change the supported baseline", so Task 2 being pending doesn't excuse this.
- I checked this myself against the `eval-release` source. It wasn't confirmed by running anything: shell commands are blocked in this session.

**P1: The test was changed to the new response shape, which hides the break** (`tests/test_client.py:8`, confidence 92%)
- The fake provider now returns `{"ok": True, "applied": True}`. No supported provider sends that.
- Nothing tests the real `{"ok": True}` response any more.
- There's also no test for the rejection path or for the `require_receipt` field in the request.
- **Fix:** keep a test that uses the `eval-release` response and checks both success and that the values were stored. Add tests for `applied: False` (should raise) and `applied: True` (should succeed).

**P3: Two different failures raise the same `RuntimeError`** (`client.py:6`, confidence 60%)
- "Save rejected" and "saved but not acknowledged" look the same to callers, though they need different retry handling.
- **Fix:** use a specific subclass for the receipt case.

## Author-sourced findings
These are my own notes from checking the findings, so weigh them accordingly.

- **Two ways to fix the P0:**
  - **Reviewer's suggestion:** treat a missing `applied` as success and reject only an explicit non-`True`. That works with `eval-release`. But if a receipt-capable provider ever omits the field, the client will quietly accept it, which weakens the receipt guarantee.
  - **Stricter option:** only require the receipt when `enhanced_settings=True`, or when the provider signals it supports receipts. That keeps ordinary saves (enhanced is off by default) on the old behaviour and avoids that silent acceptance.
- **The new request field is harmless:** `"require_receipt": True` is safe on its own, because the released provider only reads `request["settings"]` and ignores other keys.

## Index
I saved the P0 pattern, with the test-fake problem that hid it, to the knowledge base as a `kk:review-findings` entry: one side of a split client/provider change requiring a field the released counterpart doesn't send.

---

## Next steps

There are 3 code-reviewer findings (P0, P1, P3) and 1 author-sourced note. I'd fix:
1. The P0, using either the tolerant check or the stricter gated check.
2. The P1, by restoring a test against the `eval-release` response and adding tests for both receipt cases.
3. The P3 if you want; it's optional.

How would you like to proceed?
1. **Fix all**
2. **Fix P0 and P1 only**: tell me whether you want the tolerant or the gated check.
3. **Fix specific items**
4. **No changes**

The temp files `/tmp/kk-review-code-staged.patch` and `/tmp/kk-review-code-eval-release-provider-settings.py` are still there because shell commands are blocked. You can delete them when you're done.
