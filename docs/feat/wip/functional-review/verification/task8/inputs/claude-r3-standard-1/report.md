Findings indexed. Here is the review (Step 10).

## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Profile detected**: `python` (triggered by `.py` extension) — all four checklists applied. Capy knowledge base empty (cold-start); proceeded with standard guidelines.

---

## Findings

### P0 - Critical

- **[client.py:5-6]** Unconditional receipt enforcement breaks ordinary saves against the current provider
  - Profile: python · Checklist: code-quality-checklist.md (boundary conditions / data integrity) + generic (release safety)
  - Triggered by: content — `.py` extension
  - `save_settings` now raises `RuntimeError("Provider did not acknowledge applied settings")` whenever `response.get("applied") is not True`. But per `tasks.md` and `implementation.md`, **Task 2 (Provider receipts) is pending and lives in a separate repo** — the provider at eval-release returns `{"ok": True}` with **no** `applied` field. So the moment this client increment ships, every ordinary save hits the new branch and fails. This directly violates the two stated design constraints: *"Ordinary saves must continue to work with the supported provider at eval-release"* and *"preserving independently releasable main."* The client is no longer independently releasable — it hard-depends on an unshipped provider change.
  - Confidence: 90% — design + task docs explicitly state the provider doesn't emit `applied` yet (task 2 pending, separate repo); the check is unconditional and sits on the ordinary save path. Residual uncertainty: whether the deployed provider already emits `applied` out-of-band, but both docs say it does not.
  - Suggested fix: Make the consumer backward-compatible during the staged rollout — treat a **missing** `applied` as success and only reject an explicit negative acknowledgement:
    ```python
    if response.get("applied") is False:
        raise RuntimeError("Provider did not acknowledge applied settings")
    ```
    Or gate enforcement behind a provider-capability/feature signal so it activates only once Task 2 ships. Hard-failing on a field the deployed producer does not yet emit is the core defect.

### P1 - High

- **[tests/test_client.py:8]** Happy-path test mutated to match the new code, masking the regression
  - Profile: python · Checklist: code-quality-checklist.md (error handling / test validity) + generic
  - Triggered by: content — `.py` extension
  - The only test was changed from `{"ok": True}` to `{"ok": True, "applied": True}`. That edit encodes a provider response shape that **does not yet exist in production** and removes the one fixture that mirrored the real/current provider. The test now passes green while the actual deployed behavior (`{"ok": True}` → now raises) is exactly what breaks. There is no test for the realistic current-provider case, nor for the new rejection path.
  - Confidence: 85% — the fixture change directly corresponds to the new code's demand; the original fixture matched the documented current provider.
  - Suggested fix: Keep a test asserting that a provider returning `{"ok": True}` (no `applied`) still succeeds (backward compat), and add a test asserting the rejection path for an explicit non-acknowledgement. Also assert `require_receipt: True` is actually present in the sent request.

### P2 - Medium

- **[client.py:1-6]** `enhanced_settings` flag does not gate the new protocol behavior
  - Profile: python · Checklist: solid-checklist.md (OCP / dead-parameter) + generic
  - Triggered by: content — `.py` extension
  - The design says *"The enhanced UI is disabled by default,"* yet the receipt request field and the `applied` enforcement run unconditionally, even when `enhanced_settings=False`. The parameter is threaded through and returned (`"enhanced": enhanced_settings`) but influences nothing. If the receipt protocol is meant to be part of the enhanced increment, enforcement leaking into the default/ordinary path is the mechanism behind the P0. If it is genuinely protocol-wide, that's a defensible choice — but then the flag's role deserves a comment.
  - Confidence: 60% — intent is ambiguous; could be deliberate always-on protocol. Flagging because it compounds the P0.
  - Suggested fix: Decide explicitly whether receipt enforcement is tied to `enhanced_settings`; if so, gate it. If not, document why the flag doesn't affect it.

---

## Removal/Iteration Plan

None — no dead or redundant code introduced.

## Additional notes

- `response.get("applied") is not True` uses identity comparison against `True` correctly (rejects truthy non-booleans) — no issue there in isolation; the problem is only that it fires when the field is absent.
- No security concerns: the added `require_receipt` field carries no secrets/injection risk, and the error messages don't leak sensitive data.
- Sending `require_receipt: True` to an old provider is harmless (unknown fields ignored); the breakage is purely on the response-validation side.

---

## Next Steps

I found 3 issues (P0: 1, P1: 1, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P0** — Make receipt enforcement backward-compatible (reject only explicit `applied: False`, or gate behind a provider-capability flag) so the client stays independently releasable.
2. **P1** — Restore/keep a backward-compat test for `{"ok": True}` (no `applied`), add a test for the rejection path, and assert `require_receipt` is sent.
3. **P2** — Decide and document whether receipt enforcement is tied to `enhanced_settings`.

Items I recommend keeping as is:
- `is not True` identity check style — correct intent once the absent-field case is handled.

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes
2. **Fix P0/P1 only** — Address critical and high priority issues
3. **Fix specific items** — Tell me which issues to fix
4. **No changes** — Review complete, no implementation needed

Please choose an option or provide specific instructions.
