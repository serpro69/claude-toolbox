Now the report. Note: Reviewer B (`pal` codereview) was unavailable — the `pal` MCP server failed to connect this session — so this is a **single-reviewer** isolated run (no corroboration possible). I verified the central finding against the design docs myself during annotation.

---

## Review Summary (Isolated Mode — degraded)

**Reviewers**: code-reviewer (Claude sub-agent) ✅ · pal codereview ❌ *(MCP server failed to connect — `CONNECTION_CLOSED`)*
**Files reviewed**: 2 files, ~6 lines changed (`client.py`, `tests/test_client.py`)
**Profile**: `python` (triggered by `.py` extension) · Checklists applied: security, solid, code-quality, removal-plan
**Scope**: mid-implementation — Task 1 (client receipts, done) in scope; Task 2 (provider receipts, pending, separate repo) out of scope
**Overall**: REQUEST_CHANGES

> ⚠️ Corroboration unavailable. Normally the external model independently confirms findings; with only one reviewer, weight findings on their own merits. The P0 below is logic-level unambiguous, so single-source confidence is still high.

---

### Code Reviewer Findings

**P0 — `client.py:5-6` · Unconditional `applied` receipt check breaks ordinary saves against the released provider**
- Profile: python · Checklist: code-quality (None-handling / data integrity)
- Triggered by: content — `.py` extension
- `if response.get("applied") is not True:` fires whenever the response *omits* `applied`. The released provider (Task 2 not yet shipped, separate repo) returns no `applied` field, so `None is not True` → `True` → every ordinary save raises `RuntimeError` even though `ok: True` means the save succeeded. Directly violates the design's "ordinary saves must continue to work with the supported provider" and "preserving independently releasable main." Shipping this client increment alone bricks all saves until Task 2 lands — the exact coupling the two-increment split exists to avoid.
- This is **in-scope**: it's a backward-incompatible contract change introduced *by the client code*, not the Task-2 "provider doesn't implement receipts yet" gap.
- Confidence: 95%
- Suggested fix: reject only an explicit negative (`if response.get("applied") is False:`) and/or gate on the flag (`if enhanced_settings and response.get("applied") is not True:`). Treat missing `applied` as a legacy-provider success.
- **Author context / annotation**: The regression signature is visible *inside this diff* — the sole happy-path test had to be edited to add `"applied": True` just to keep passing (see P1). That confirms the old `{"ok": True}` response now throws.

**P1 — `tests/test_client.py:8` · Only regression test mutated to the new contract; no guard for the compat constraint**
- Profile: python · Checklist: code-quality (error handling)
- The sole test was changed from `{"ok": True}` to `{"ok": True, "applied": True}`, encoding the new behavior as the only covered case and deleting the one case that would have caught the P0. No test covers a receipt-less (`{"ok": True}`) response — the thing the design says must keep working.
- Confidence: 90%
- Suggested fix: keep/add a test asserting success on `{"ok": True}` (legacy provider), plus negative cases for `applied: False` and `ok: False`.

**P2 — `client.py:2` · Receipt path ignores `enhanced_settings`; new behavior isn't actually opt-in**
- Profile: python · Checklist: solid (OCP / divergent change)
- `require_receipt: True` is sent and `applied` enforced unconditionally, yet the function already has `enhanced_settings=False` and the design says the enhanced UI is "disabled by default." The flag only flows into the return value, not the receipt logic. Fixing the P0 gating likely resolves this.
- Confidence: 70%

**P3 — `client.py:4,6` · Bare `RuntimeError` with no context**
- Profile: python · Checklist: code-quality (debuggability)
- Both failure paths raise static-string `RuntimeError`; hard to distinguish "save failed" from "saved but no receipt." Low severity.
- Confidence: 60%

### Areas Not Covered
- **Released-provider response shape**: the actual provider (separate repo, Task 2) wasn't inspectable; the P0 rests on the documented fact that it doesn't emit `applied`. If the released provider *already* emits `applied`, the P0 severity drops — worth a 10-second confirmation.
- No integration test exercises client ↔ live provider; the break is inferred from code + unit-test logic.

**Indexed to capy** (`kk:review-findings`): (1) backward-incompatible protocol tightening in multi-increment rollouts; (2) mutating the sole happy-path test hides a regression. ✅

---

## Next Steps

I found **4 issues** (corroborated: 0 — pal unavailable · code-reviewer: 4 · author-sourced: 0).

Recommended fixes:
1. **P0** — Make receipt enforcement tolerant of a missing `applied` (reject only `is False`) and/or gate it behind `enhanced_settings`, so the client increment stays independently releasable.
2. **P1** — Restore a test for the legacy `{"ok": True}` response; add `applied: False` and `ok: False` cases alongside the new one.
3. **P2** — Scope `require_receipt`/enforcement to the enhanced path (folds into the P0 fix).
4. **P3** — Optional: richer exception type/context for the two failure paths.

Keep as-is:
- Provider-side receipt emission — out of scope (Task 2, pending, separate repo). Correctly *not* flagged as missing.

**How would you like to proceed?**
1. **Fix all** — implement all four
2. **Fix P0/P1** — the release-blocking compatibility break + its test guard
3. **Fix specific items** — tell me which
4. **No changes** — review only

One housekeeping note: I couldn't remove the temp patch file (`/tmp/kk-review-code-enhanced-settings.patch`) — Bash is in don't-ask mode this session. You can delete it manually, or approve a Bash call and I'll clean it up.
