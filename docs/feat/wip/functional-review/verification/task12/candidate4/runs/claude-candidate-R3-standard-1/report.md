Indexed. Here's the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 4 insertions / 2 deletions (staged)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Design `docs/feat/wip/enhanced-settings/` — add an application receipt to the client↔provider protocol while *preserving independently releasable main* and keeping *ordinary saves working with the supported provider at eval-release*. Current task: **Task 1 — Client receipt handling** (status: `done`, in scope). **Task 2 — Provider receipts** is `pending`, in a *separate provider repository* (out of scope, DO NOT flag as missing).
**Baselines**: Review base/candidate = staged working tree on `master` (`client.py`, `tests/test_client.py`). Release baseline = the *supported provider at eval-release*, which — because Task 2 is pending — does **not** yet emit a receipt.
**Mode**: mid-implementation (Task 2 pending).

## Behavior and Compatibility

Traced `save_settings` end-to-end. The change does two things: (1) adds `"require_receipt": True` to the outbound request, and (2) adds a hard post-condition — if the response's `applied` field is not exactly `True`, it raises `RuntimeError`.

- **New consumer / old (supported) provider → BLOCKED.** The eval-release provider returns `{"ok": True}` with no `applied` key. `response.get("applied")` → `None`; `None is not True` → raises `RuntimeError("Provider did not acknowledge applied settings")`. **Every** save fails against the current provider — including the default `enhanced_settings=False` path, even though the enhanced UI is "disabled by default." This is the exact new-consumer/old-provider incompatibility the design forbids.
- **Independently releasable main → BLOCKED.** The client increment cannot ship on its own; it hard-depends on the still-pending Task 2 provider change. The design's "preserving independently releasable main" is a hard delivery requirement, and a documented prerequisite (Task 2) does not satisfy it.
- **New provider / new client → Supported** (the only path the updated test covers).
- **Rollback → Not applicable / safe** (revert restores prior behavior).

This is in-scope: it's a defect *within* Task 1's own code, not a complaint about pending Task 2. Per the scope protocol, "a current consumer that already requires a pending provider change remains reviewable; pending work does not excuse current regressions."

---

## Findings

### P0 - Critical

(none — the breakage is recoverable via rollback, so it does not meet the P0 "catastrophic/irreversible" bar)

### P1 - High

- **[client.py:5]** Unconditional receipt enforcement breaks ordinary saves against the supported provider
  - Profile: python · Checklist: code-quality-checklist.md (error handling / boundary: None handling) + functional-review (compatibility)
  - Triggered by: content — `.py` extension (python profile)
  - **Trigger/path**: Any `save_settings` call against the eval-release provider (which lacks Task 2's receipt). `response.get("applied")` is `None` → `None is not True` → `RuntimeError`. **Expected**: ordinary (default, non-enhanced) saves continue to succeed against the supported provider. **Actual**: all saves raise. **Consequence**: client is not independently releasable and the default save flow is fully broken on deploy — violates two explicit design requirements.
  - Confidence: 90% — code path verified by inspection; rests on the design statement that provider receipts are pending/separate (so the current provider does not emit `applied`). Residual: if the eval-release provider already echoed `applied` for unrelated reasons the break wouldn't occur, but the docs indicate it does not.
  - **Suggested fix**: Make the receipt backward-compatible. Either (a) only fail on an *explicit* negative receipt — `if response.get("applied") is False: raise` — treating an absent field as a legacy provider that succeeds; or (b) gate enforcement behind capability negotiation / the `enhanced_settings` flag so it only applies once the provider is known to support receipts. Option (a) is the smaller, safer increment.

### P2 - Medium

- **[tests/test_client.py:8]** Test fixture mutated to pass instead of adding legacy-provider coverage
  - Profile: python · Checklist: code-quality-checklist.md (error handling) + functional-review (test adequacy)
  - Triggered by: content — `.py` extension (python profile)
  - **Trigger/path**: The only test's stub was changed from `{"ok": True}` to `{"ok": True, "applied": True}`. **Expected**: a test covering the supported-provider shape (`{"ok": True}` with no receipt) that proves ordinary saves still work. **Actual**: the fixture was edited to match the new code, so the suite is green while the real regression ships. There is also no test for the raising path. **Consequence**: the test actively masks the P1 — a legacy-provider test case would have failed and caught it.
  - Confidence: 95% — the diff shows exactly this fixture mutation and no added case.
  - **Suggested fix**: Keep/add a `test_legacy_provider_save` using `{"ok": True}` asserting success (after the P1 fix), plus a `test_rejected_receipt` asserting `RuntimeError` on an explicit negative.

### P3 - Low

- **[client.py:1-7]** `enhanced_settings` parameter is accepted and echoed but never governs behavior; the new receipt logic ignores it despite the feature being "disabled by default." Consider whether receipt enforcement should be scoped to the flag (folds into the P1 fix). Confidence: 70% — the protocol change may be intended as universal, but if so it must still be backward-compatible, which returns to the P1.

---

## Coverage and Limits

- **Checked**: full `save_settings` behavior and both response shapes; the updated test; all four Python checklists (security, SOLID, code-quality, removal) against the diff; all eight Known profiles for detection.
- **Security/SOLID/removal checklists**: no findings — no injection/secrets/crypto/deserialization surface, no dead code, no SOLID smell introduced by these 4 lines.
- **Not covered / residual**: Task 2 provider repo is separate and not inspected — I did not verify what the eval-release provider actually returns beyond the design's statement that receipts are pending (the basis for the P1); confirm the current provider's real response shape to pin confidence to 100%. Could not run the test suite (Bash restricted this session) — findings are from source inspection, not execution.
- **Detection note for maintainers**: `profiles/twelve-factor/` exists on disk but is absent from the authoritative Known-profiles list, so it was correctly not evaluated — the list and the directory tree are out of sync.

---

## Next Steps

I found 3 actionable issues (P0: 0, P1: 1, P2: 1, P3: 1).

Recommended fixes:
1. **P1** — Make receipt handling backward-compatible (`applied is False` → raise; absent → succeed), restoring independent releasability and ordinary saves.
2. **P2** — Add a legacy-provider success test and a rejected-receipt failure test instead of mutating the existing stub.
3. **P3** — Decide whether receipt enforcement should be gated on `enhanced_settings` (likely subsumed by the P1 fix).

Keep as-is:
- Sending `"require_receipt": True` in the request is fine as a forward signal — provided the *response* check tolerates providers that don't yet honor it.

**How would you like to proceed?**

1. **Fix all** — P1 + P2 + P3
2. **Fix P0/P1 only** — just the compatibility break
3. **Fix specific items** — tell me which
4. **No changes** — review complete

I won't make any edits until you confirm.
