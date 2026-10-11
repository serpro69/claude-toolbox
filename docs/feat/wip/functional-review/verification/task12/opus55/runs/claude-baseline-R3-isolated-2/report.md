## Review Summary (Isolated Mode, run with only one reviewer)

This was not a full isolated review. Three steps didn't run as the workflow intends:
- **No pal reviewer.** The pal MCP server failed to connect (`CONNECTION_CLOSED`), so Reviewer B didn't run and nothing could be corroborated. Run `/mcp` to reconnect it if you want a second opinion.
- **No exact diff.** Bash is denied in this session, so I couldn't run `git diff --cached`. The code-reviewer looked at the full staged contents of `client.py` and `tests/test_client.py` (both are small, 18 lines in total), so it can't say which lines are new.
- **Provider not checked.** The released provider (`provider/settings.py` at tag `eval-release`) exists only in Git history and none of us could read it. The P0 and P2 findings assume it returns `{"ok": True}` with no `applied` field. That fits the docs: receipts are new protocol work, and Task 2, the provider side, is still pending.

**Reviewers:** code-reviewer (Claude sub-agent) only
**Files reviewed:** 2 files
**Profile and checklists:** python (all four checklists: security, SOLID, code quality, removal plan), triggered by the `.py` extension

### Code Reviewer Findings

- **`client.py:5`: The receipt check breaks ordinary saves against the released provider** (P0, confidence 85%)
  - The `applied is not True` check runs on every save, including when `enhanced_settings=False`, which is the default.
  - A provider without receipts would apply the values, and then the client would raise `RuntimeError` anyway.
  - That breaks the README's rules that every merged client increment must work with `eval-release`, and that a successful save means "the caller sees success."
  - It also makes this increment depend on the pending Task 2.
  - **Suggested fix:** Treat `ok: True` with no `applied` key as success, and fail only on an explicit `applied: False`. Alternatively, require the receipt only once support has been negotiated.

- **`tests/test_client.py:6-10`: No test covers the released provider's response or any failure** (P1, confidence 90%)
  - The only fake provider returns `{"ok": True, "applied": True}`, which is the shape of the new provider that isn't deployed yet. The suite passes while the delivery contract is broken.
  - **Suggested fix:** Add tests for:
    - the released response `{"ok": True}` with `enhanced_settings=False` → success
    - `{"ok": False}` → raises
    - `{"ok": True, "applied": False}` → raises
    - what the client actually sends to the provider

- **`client.py:2`: `require_receipt: True` is always sent** (P2, confidence 50%)
  - The released provider doesn't know this field. If it rejects unknown keys, every save breaks a second way.
  - **Suggested fix:** Send it only when receipt support is available, or confirm that `eval-release` ignores unknown keys.

- **`client.py:1,7`: `enhanced_settings` changes nothing** (P3, confidence 60%)
  - The flag is only echoed back in the result. Readers may assume it controls whether a receipt is required, and it doesn't.

- **`client.py:3-6`: Generic `RuntimeError`, and no check that the response is a dict** (P3, confidence 55%)
  - Callers can't tell a rejected save from a missing receipt without parsing the message. If `send` returns `None`, they get an `AttributeError`.

### Indexing

I saved the P0 to the capy knowledge base as `kk:review-findings`. The general pattern: a client requires a new protocol field before the provider ships it, without a flag or capability check.

---

## Next Steps

I found 5 issues: 0 corroborated, 5 from code-reviewer, 0 from pal, 0 from me.

I recommend fixing:
1. **P0, `client.py:5`:** Accept a response with no `applied` field as success, and fail only on `applied: False` or when receipts have been negotiated.
2. **P1, tests:** Add a regression test for the released provider's response plus the failure cases.
3. **P2, `client.py:2`:** Send `require_receipt` only when receipts are supported.

These are optional: the two P3s (the unused flag and the exception types).

If you can run `git show eval-release:provider/settings.py` yourself, it would settle the assumption behind the P0 and P2.

**How would you like to proceed?**
1. **Fix all:** I'll implement all suggested fixes.
2. **Fix high severity:** Fix P0, P1 and P2.
3. **Fix specific items:** Tell me which ones.
4. **No changes:** The review is complete.
