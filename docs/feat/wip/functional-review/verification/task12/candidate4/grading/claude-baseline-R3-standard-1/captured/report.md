## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: REQUEST_CHANGES

**Profile detection**: `python` active (content signal: `.py` extension on both files). `twelve-factor` is design-only and does not activate in review-code; no other profile matched. Checklists applied: security, SOLID, code-quality, removal.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[client.py:2,5]** Receipt enforcement is not gated behind the `enhanced_settings` flag — breaks existing callers
  - Profile: python · Checklist: solid-checklist.md (OCP) + code-quality (data integrity)
  - Triggered by: content — `.py` extension
  - The feature is literally "task 1 of enhanced-settings," yet the `enhanced_settings=False` parameter is **inert**: it is never read except to be echoed into the return dict. Meanwhile the new receipt behavior — sending `require_receipt: True` and raising when `response.get("applied") is not True` — runs **unconditionally** for every caller. Any existing caller (`enhanced_settings=False`) that talks to a provider returning `{"ok": True}` without an `applied` key now raises `RuntimeError`. That's a backward-compatibility break for the non-enhanced path, and it makes the flag that names the feature do nothing.
  - Confidence: 70% — the logic reading is certain (flag inert, receipt logic unconditional); the 30% is the absence of a design doc (`docs/` has no `enhanced-settings` spec) to confirm the receipt path is *meant* to be gated. Either the enforcement should be `if enhanced_settings:` guarded, or the parameter is redundant and should be removed. Both are defects.
  - Suggested fix: gate the new behavior, e.g. only send `require_receipt`/require `applied` when `enhanced_settings` is true:
    ```python
    payload = {"settings": values}
    if enhanced_settings:
        payload["require_receipt"] = True
    response = send(workspace_id, payload)
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    if enhanced_settings and response.get("applied") is not True:
        raise RuntimeError("Provider did not acknowledge applied settings")
    ```

### P2 - Medium

- **[client.py:5]** Raising after `ok: True` creates an ambiguous partial-success state with no idempotency guarantee
  - Profile: python · Checklist: security-checklist.md (Data Integrity / idempotency)
  - Triggered by: content — `.py` extension
  - When the provider returns `ok: True` but `applied` is not `True`, the save has very likely been accepted server-side, yet the client raises as if it failed. A caller that retries on the exception will re-send the save — without an idempotency key, that's a double-apply. The exception also loses the actual `applied` value, making the failure hard to debug.
  - Confidence: 65% — depends on provider semantics for `ok` vs `applied`, which aren't documented here; the retry-without-idempotency risk is real regardless.
  - Suggested fix: document/confirm the `ok`-but-not-`applied` contract; include the observed value in the error message; consider an idempotency token so retries are safe.

- **[tests/test_client.py:8]** New raise branch is untested; test was only patched to keep the happy path green
  - Profile: python · Checklist: code-quality-checklist.md (error handling coverage)
  - Triggered by: content — `.py` extension
  - The diff adds a whole new failure mode (`applied is not True` → raise) and a new request field (`require_receipt`), but the test change merely appends `"applied": True` to the stub so the existing assertion still passes. There is no test asserting `RuntimeError` when `applied` is missing/`False`, and none asserting the request carries `require_receipt`.
  - Confidence: 90% — directly visible in the diff.
  - Suggested fix: add `assertRaises(RuntimeError)` cases for `{"ok": True}` (no `applied`) and `{"ok": True, "applied": False}`, plus a test capturing the `request` arg to assert `require_receipt` is present (and, once gating is fixed, absent when `enhanced_settings=False`).

### P3 - Low

- **[client.py:3]** Pre-existing: `response.get(...)` assumes `send` never returns `None`; a `None` response raises `AttributeError` rather than a meaningful error. Not introduced by this diff — noting only, no change required here.

**What checked out (no finding):** `response.get("applied") is not True` is correctly written — it treats missing/`None`/`False` all as non-acknowledgment, avoiding the truthiness trap. No security issues (no secrets, injection, deserialization, or crypto surface). `send` is dependency-injected (clean DIP).

---

## Findings indexed

Indexed the P1 as a systemic `kk:review-findings` pattern: *feature-named flag parameter is inert while the feature's new enforcement runs unconditionally → gating bug / backward-compat break.*

---

## Next Steps

I found 4 issues (P0: 0, P1: 1, P2: 2, P3: 1).

Actionable items I recommend fixing:
1. **P1** — Gate receipt enforcement behind `enhanced_settings` (or remove the dead parameter).
2. **P2** — Add idempotency/clearer error for the `ok`-but-not-`applied` partial-success state.
3. **P2** — Add tests for the new raise branch and the `require_receipt` payload field.

Items to keep as-is:
- `is not True` check on `applied`: correct, keep it.
- Line 3 `None`-response gap: pre-existing, out of scope for this task.

**How would you like to proceed?**

1. **Fix all** — implement all suggested fixes
2. **Fix P0/P1 only** — just the gating issue
3. **Fix specific items** — tell me which
4. **No changes** — review complete

The P1 hinges on design intent I couldn't confirm (no `enhanced-settings` spec in `docs/`). If you can point me at the design doc — or confirm whether receipt handling is meant to be enhanced-only — I'll tailor the fix.
