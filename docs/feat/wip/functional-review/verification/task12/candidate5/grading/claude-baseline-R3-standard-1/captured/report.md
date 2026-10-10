## Code Review Summary

**Files reviewed**: 2 files, ~4 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**

The change adds client-side receipt handling: it now sends `require_receipt: True` and raises if the provider response doesn't contain `applied: True`. The problem is that it enforces a provider capability that **has not shipped yet**, and it does so unconditionally rather than behind the feature flag that exists for exactly this purpose.

---

## Findings

### P0 - Critical

- **[client.py:5-6]** New receipt check breaks every ordinary save against the released provider
  - Profile: python · Checklist: solid-checklist.md (DIP / coupling) + generic correctness
  - Triggered by: content — `.py` extension
  - The released provider (`git show 2214073:provider/settings.py`) returns only `{"ok": True}` — it emits **no `applied` field** and ignores `require_receipt`. The provider-side receipt work is **Task 2, status pending, in a separate repo** (per `docs/feat/wip/enhanced-settings/{implementation,tasks}.md`). So `response.get("applied")` is `None`, `None is not True` is `True`, and **every save raises `RuntimeError("Provider did not acknowledge applied settings")`.**
  - This directly violates the design contract: *"Ordinary saves must continue to work with the supported provider at eval-release"* and *"preserving independently releasable main"* (`design.md`). The client is forward-coupled to a capability its counterpart doesn't have yet.
  - Confidence: 92% — verified against the actual released provider source and the feature docs. Residual uncertainty only if the provider was already upgraded out-of-band, which the docs explicitly contradict (Task 2 pending).
  - Suggested fix: gate the receipt protocol behind the `enhanced_settings` flag (disabled by default), so ordinary saves stay compatible:
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

### P1 - High

- **[client.py:1-7]** `enhanced_settings` flag is threaded through but ignored by the new behavior (OCP / dead switch)
  - Profile: python · Checklist: solid-checklist.md (OCP; `enhanced_settings` echoed in return only)
  - Triggered by: content — `.py` extension
  - The flag exists to toggle the enhanced path ("The enhanced UI is disabled by default"), yet the new strict protocol is applied on *every* call and the flag is only reflected back in the return value. This is the mechanism behind the P0: the feature was wired unconditionally instead of extending behind the existing switch. Fixing P0 as above resolves this too.
  - Confidence: 88% — the flag's name, default, and the design's "disabled by default" language all point to it being the intended gate.
  - Suggested fix: same as P0 — route `require_receipt` / `applied` enforcement through `if enhanced_settings`.

- **[tests/test_client.py:8]** Test was edited to feed the new field, masking the regression instead of protecting the contract
  - Profile: python · Checklist: code-quality-checklist.md (test coverage / boundary) 
  - Triggered by: content — `.py` extension
  - The only test now returns `{"ok": True, "applied": True}`, so it passes by construction. There is **no test for the released-provider shape** (`{"ok": True}` with no `applied`) — which is precisely the P0 regression. There's also no test for the receipt-failure path (`applied` missing/False → raise).
  - Confidence: 90% — the gap is directly visible in the single-test file.
  - Suggested fix: after gating, add (a) a backward-compat test where `send` returns `{"ok": True}` and `enhanced_settings=False` still succeeds, and (b) an enhanced-path test where missing/`False` `applied` raises.

### P2 - Medium

*(none)*

### P3 - Low

- **[client.py:5]** `response.get("applied") is not True` is a strict identity check; a future provider returning a truthy-but-non-`True` ack (e.g. `"true"`, `1`) would be rejected. Likely intentional strictness — flagging only so the contract for the `applied` value is decided deliberately in Task 2. Confidence: 55%.

---

## Additional Suggestions

- When Task 2 lands, make the request/response receipt contract explicit somewhere shared (the `design.md` "shared delivery contract") so client and provider versions can't drift — the P0 here is the classic symptom of that contract living only in code on two sides.

---

## Next Steps

I found 4 issues (P0: 1, P1: 2, P2: 0, P3: 1). Note the P0 and the two P1s are one root cause with one fix (gate the receipt protocol behind `enhanced_settings`) plus the test additions.

The actionable items I recommend fixing:
1. **P0** — Gate `require_receipt`/`applied` enforcement behind `enhanced_settings` so ordinary saves keep working against the released provider.
2. **P1** — (same fix) stop applying the enhanced protocol unconditionally; make the flag actually control behavior.
3. **P1** — Add backward-compat + receipt-failure tests.
4. **P3** — Decide whether the `applied` ack must be strictly `True` or merely truthy, and document it.

Items I recommend keeping as is:
- Sending `require_receipt` key itself is fine *once gated* — the current provider ignores unknown request keys, so it's harmless when enhanced is on against an old provider (though the `applied` check still needs the flag guard).

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes
2. **Fix P0/P1 only** — Address critical and high priority issues
3. **Fix specific items** — Tell me which issues to fix
4. **No changes** — Review complete, no implementation needed

Please choose an option or provide specific instructions. (Findings indexed to `kk:review-findings` for future reviews.)
