Finding indexed. Here's the review.

## Code Review Summary

**Files reviewed**: 2 files (`client.py`, `tests/test_client.py`), 4 insertions / 2 deletions
**Overall assessment**: **REQUEST_CHANGES**

**Profiles active**: `python` (triggered by `.py` extension on both files). Checklists applied: security, SOLID, code-quality, removal-plan.

---

## Findings

### P0 - Critical

- **[client.py:5-6]** Unconditional `applied` check breaks the supported provider baseline
  - Profile: python · Checklist: code-quality-checklist.md (None vs missing inconsistency / data integrity)
  - Triggered by: content — `.py` extension
  - The new guard `if response.get("applied") is not True: raise RuntimeError(...)` rejects any response that lacks an `applied` field. The supported released provider — `provider/settings.py` at git tag `eval-release` — returns **`{"ok": True}`** and nothing else, and ignores the new `require_receipt` flag entirely. Against that provider, `response.get("applied")` is `None`, so `None is not True` → the client raises on **every** save.
  - This directly violates the README contract: *"Every merged client increment must support the released provider at tag `eval-release`, including ordinary settings saves while `enhanced_settings` is false"* and *"A successful settings save means values were applied and the caller sees success."* The provider actually stores the values (`storage[workspace_id] = dict(request["settings"])`) — the save succeeds — but the caller is handed a `RuntimeError`. Success is reported as failure.
  - Note the check is **unconditional** — it is not gated by `enhanced_settings`, so it breaks ordinary (non-enhanced) saves too, which is exactly the scenario the README calls out as mandatory. The README also states the candidate provider is not deployed and a pending provider task cannot change the baseline, so you cannot assume a future provider will emit `applied`.
  - Confidence: 97% — verified by reading the released provider source at `eval-release` (`return {"ok": True}`) and tracing the guard. Only residual uncertainty: whether some other, deployed provider is in play — the README rules that out.
  - Suggested fix: Gate the receipt requirement behind capability/negotiation and the `enhanced_settings` flag, treating an absent `applied` as "not supported / assume applied" rather than failure. E.g. only enforce acknowledgement when `enhanced_settings` is true **and** the provider opted into receipts; otherwise preserve the current `ok`-only success path. (Blocking this merge against the supported baseline.)

### P1 - High

- **[tests/test_client.py:8]** Test fake diverges from the real supported provider contract, masking the P0
  - Profile: python · Checklist: code-quality-checklist.md (error handling / correctness of coverage)
  - Triggered by: content — `.py` extension
  - The fake `send` was changed to return `{"ok": True, "applied": True}`, which does **not** match the released provider's actual `{"ok": True}`. The single test therefore stays green while real usage against the supported provider fails. This is the only test covering `save_settings`, so it gives false confidence and actively hides the breakage above. There is also no test exercising the `enhanced_settings=True` path or the new error path.
  - Confidence: 93% — the fake's shape vs. the released provider's shape is directly verifiable; "masks the regression" follows from the P0.
  - Suggested fix: Keep a baseline-compatibility test whose fake mirrors the released provider exactly (`{"ok": True}`, no `applied`) and asserts success. Add separate tests for the enhanced/receipt path and for the acknowledgement-failure case.

### P2 - Medium

- **[client.py:2,5]** New provider-capability coupling with no gating or negotiation (OCP/DIP)
  - Profile: python · Checklist: solid-checklist.md (OCP/DIP)
  - Triggered by: content — `.py` extension
  - `require_receipt: True` is sent on every request and the acknowledgement is enforced on every response, regardless of `enhanced_settings`. The client hard-couples to a provider capability absent from the supported baseline, with no version/capability negotiation and no extension point. Even if gated on `enhanced_settings`, the baseline provider still wouldn't emit `applied` — so the feature needs a capability-detection story, not just a flag. (Root cause behind the P0; fixing P0 as suggested resolves this too.)
  - Confidence: 80% — design judgment; depends on the intended rollout model for enhanced settings.

### P3 - Low

- **[client.py:6]** `RuntimeError` is generic for two distinct failures (save-rejected vs. no-acknowledgement). A dedicated exception type (or distinct message/structured detail) would help callers distinguish "provider said not-ok" from "provider didn't acknowledge." Confidence: 70%.

---

## Removal/Iteration Plan

Not applicable — no dead/removable code introduced.

---

## Next Steps

I found 4 issues (P0: 1, P1: 1, P2: 1, P3: 1).

The actionable items I recommend fixing:
1. **P0** — Stop breaking the `eval-release` baseline: don't fail when `applied` is absent; gate receipt enforcement behind `enhanced_settings` + capability detection.
2. **P1** — Fix the test fake to mirror the real provider (`{"ok": True}`) and add tests for the enhanced path and the failure path.
3. **P2** — Add capability negotiation / flag-gating so the client doesn't hard-require an un-baselined provider field.
4. **P3** — Use a distinct exception/message for the acknowledgement failure.

Items I recommend keeping as is:
- Nothing — the receipt feature itself is reasonable; it's the unconditional enforcement and the misleading test that are the problems.

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes
2. **Fix P0/P1 only** — Address the compatibility break and the test
3. **Fix specific items** — Tell me which issues to fix
4. **No changes** — Review complete, no implementation needed

Please choose an option or provide specific instructions. (I won't change anything until you confirm.)
