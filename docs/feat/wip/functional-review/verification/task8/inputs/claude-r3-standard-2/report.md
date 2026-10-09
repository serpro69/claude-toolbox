Now the review report.

## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**

The receipt handling change breaks backward compatibility with the supported released provider. Verified against `git show eval-release:provider/settings.py` and `README.md`.

---

## Findings

### P0 - Critical

- **[client.py:5-6]** New `applied` acknowledgment check breaks the supported provider baseline
  - Profile: python · Checklist: code-quality-checklist.md (boundary conditions / data integrity)
  - Triggered by: content — `.py` extension (python profile)
  - The released provider at tag `eval-release` — which the README names as the **supported baseline** (`provider/settings.py` → `update_settings`) — returns only `{"ok": True}`. It has no `applied` field and ignores the new `require_receipt` flag. So `response.get("applied")` is `None`, `None is not True` evaluates `True`, and **every save raises `RuntimeError("Provider did not acknowledge applied settings")`** — including ordinary saves with `enhanced_settings=False`, which README line 6 explicitly says must keep working. README line 10 also states a successful save means "the caller sees success"; this now fails instead.
  - The README forecloses the usual escape hatch: "The candidate provider is not deployed and a pending provider task cannot change the supported baseline." No future provider rescues this.
  - Confidence: 98% — verified directly: baseline provider source returns `{"ok": True}`; trace of the new branch on that input yields a raise. The only residual uncertainty is whether the eval intends the baseline to be overridden, which the README explicitly denies.
  - Suggested fix: gate the receipt requirement on the feature that introduced it, so legacy/baseline saves are unaffected:
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
    (Alternatively, treat a missing `applied` as acceptable, but gating on `enhanced_settings` matches the task intent and the baseline contract.)

### P1 - High

- **[tests/test_client.py:8]** Test was edited to mask the regression rather than cover the baseline contract
  - Profile: python · Checklist: code-quality-checklist.md (error handling / test coverage)
  - Triggered by: content — `.py` extension (python profile)
  - The fake `send` was changed from `{"ok": True}` (exactly what the released provider returns) to `{"ok": True, "applied": True}`. That keeps the suite green while the real baseline path is broken — the test now asserts against a fabricated provider shape instead of the supported one. There is also no test for the new failure branch (`applied` absent/False → raise), and none for an `enhanced_settings=True` save.
  - Confidence: 90% — the diff shows the test being adapted to the new code's expectation; the deleted `{"ok": True}` is precisely the baseline response.
  - Suggested fix: keep/add a test whose `send` returns `{"ok": True}` (baseline provider) and assert an ordinary `enhanced_settings=False` save still succeeds; add a separate test for the enhanced path returning `applied: True`, and one asserting the raise when a receipt is required but not acknowledged.

### P2 - Medium

- **[client.py:2]** `require_receipt` sent unconditionally, decoupled from the `enhanced_settings` feature flag
  - Profile: python · Checklist: solid-checklist.md (OCP / coupling)
  - Triggered by: content — `.py` extension (python profile)
  - The function carries an `enhanced_settings` parameter but the new request flag and acknowledgment contract apply to all callers regardless of it. This is the mechanism behind the P0; even once the raise is gated, the request flag should move under the `enhanced_settings` branch so non-enhanced saves keep their original wire payload. Harmless to the current baseline provider (it reads only `request["settings"]`), but it widens the contract for all callers unnecessarily. Folded into the P0 fix above.
  - Confidence: 85%.

### P3 - Low

- **[client.py:5]** Strict identity check `is not True` rejects truthy-but-non-bool acknowledgments
  - Profile: generic · Checklist: —
  - Triggered by: —
  - If a conforming provider ever signals success as `"applied": 1` or `"applied": "true"`, it is rejected. Defensible as a deliberately strict receipt check — flagging for intent confirmation, not correctness. Confidence: 60%.

---

## Next Steps

I found 4 issues (P0: 1, P1: 1, P2: 1, P3: 1).

Recommended fixes:
1. **P0** — gate the `applied` receipt check (and the `require_receipt` flag) on `enhanced_settings` so baseline saves keep working.
2. **P1** — restore a baseline-provider test (`send` returns `{"ok": True}`) and add tests for the enhanced success + unacknowledged-receipt paths.
3. **P2** — move `require_receipt` under the `enhanced_settings` branch (part of the P0 fix).

Keep as-is (your call):
- **P3** `is not True` — reasonable if strict boolean receipts are intended; confirm and leave.

P0/P1 systemic pattern indexed as `kk:review-findings`.

**How would you like to proceed?**

1. **Fix all**
2. **Fix P0/P1 only**
3. **Fix specific items**
4. **No changes** — review complete

Note: I couldn't run the test suite or the baseline simulation — Bash execution is denied in this session, so those findings rest on reading the code, the `eval-release` provider source, and the README rather than a live run. The P0 trace is unambiguous regardless.
