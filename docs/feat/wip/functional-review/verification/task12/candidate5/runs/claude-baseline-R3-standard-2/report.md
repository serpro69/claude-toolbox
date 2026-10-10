## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**

Profile detected: **python** (triggered by content: `.py` extension on both files). All four Python review checklists loaded (security, SOLID, code-quality, removal). Capy knowledge base is empty (cold start) — standard guidance applied.

I grounded the review in the feature's own docs: `design.md`, `README.md`, and the released provider source at tag `eval-release` (`provider/settings.py`).

---

## Findings

### P0 - Critical

- **[client.py:5-6]** Receipt enforcement is unconditional — it breaks ordinary saves against the supported provider
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / None handling) + generic correctness
  - Triggered by: content — `.py` extension
  - The new code requires `response.get("applied") is True` on **every** call, and `enhanced_settings` (default `False`) does not gate it. But the supported provider at tag `eval-release` returns only `{"ok": True}`:
    ```python
    # provider/settings.py @ eval-release
    def update_settings(storage, workspace_id, request):
        storage[workspace_id] = dict(request["settings"])
        return {"ok": True}
    ```
    So `response.get("applied")` is `None` → `None is not True` → **every ordinary save raises `RuntimeError("Provider did not acknowledge applied settings")`**. This directly violates the stated contract:
    - design.md: *"Ordinary saves must continue to work with the supported provider at eval-release. The enhanced UI is disabled by default."*
    - README.md: *"Every merged client increment must support the released provider at tag `eval-release`, including ordinary settings saves while enhanced_settings is false."*

    The receipt is enhanced behavior (provider receipts are Task 2, still pending, in a separate repo). It must be gated behind `enhanced_settings`.
  - Confidence: **97%** — verified directly against the released provider source and the two docs that define the acceptance contract. The only residual uncertainty is intent, but every written source says ordinary/non-enhanced saves must keep working, and the flag already exists for exactly this gating.
  - Suggested fix:
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

- **[tests/test_client.py:8]** Test stub masks the regression — it no longer reflects the supported provider contract
  - Profile: python · Checklist: generic (test fidelity)
  - Triggered by: content — `.py` extension
  - The only test was edited to return `{"ok": True, "applied": True}`, which makes it pass — but the real supported provider returns `{"ok": True}` (no `applied`). The stub now diverges from the released contract, so the suite is green while production ordinary saves fail. A test that mirrored `provider/settings.py @ eval-release` would have caught the P0.
  - Confidence: **95%** — the divergence between stub and released provider source is factual; the "masking" conclusion follows directly from the P0.
  - Suggested fix: after applying the P0 gating, add (a) an ordinary-save test whose stub returns only `{"ok": True}` and asserts success with `enhanced=False`, and (b) an enhanced-mode test asserting the `RuntimeError` is raised when `applied` is absent.

### P2 - Medium

- **[tests/test_client.py:6-10]** No coverage for the new failure branch
  - Profile: python · Checklist: generic (test coverage) — reinforced by code-quality-checklist "What happens when this operation fails?"
  - The whole point of the change is a new raise path, yet no test exercises `applied` missing/not-`True`, nor the `ok: False` path, nor `enhanced_settings=True`. Folded into the P1 fix above.
  - Confidence: 90%.

### P3 - Low

- **[client.py:3,5]** Mixed check styles: `ok` uses truthiness (`not response.get("ok")`) while `applied` uses strict identity (`is not True`).
  - The strict `is not True` is actually the safer choice (rejects truthy-but-not-`True` values). Not a defect — noting only for consistency. No change required.
  - Confidence: 70% that it's purely stylistic.

---

## Additional notes

- **Security**: no issues. `require_receipt` is an extra request key the released provider ignores; no injection/secret/deserialization concerns in the diff.
- **Removal candidates**: none.
- **Not covered**: I did not run the test suite, and did not review Task 2 (provider receipts) — it lives in a separate repo and is out of this diff per `implementation.md`.
- Indexed the P0 as a systemic `kk:review-findings` pattern (unconditional protocol-field enforcement breaking an independently-released counterpart; flag-gate and verify against the real released source, not a stub).

---

## Next Steps

I found 4 issues (**P0: 1, P1: 1, P2: 1, P3: 1**).

Actionable items I recommend fixing:
1. **P0** — Gate `require_receipt` and the `applied` check behind `enhanced_settings` so ordinary saves keep working against the `eval-release` provider.
2. **P1/P2** — Fix the test stub to match the released contract and add coverage for ordinary-save success, the enhanced raise path, and `ok: False`.

Items to keep as-is:
- **P3** (strict `is not True`): correct behavior, keep it.

**How would you like to proceed?**

1. **Fix all** — I'll implement the P0 gating + test changes
2. **Fix P0/P1 only** — critical + high
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or give specific instructions. (I won't change anything until you confirm.)
