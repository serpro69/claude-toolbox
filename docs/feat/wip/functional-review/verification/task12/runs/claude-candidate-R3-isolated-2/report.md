## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` (independent sub-agent, Opus 4.8) — completed. PAL external reviewer (Reviewer B) — **unavailable this session** (`pal` MCP connection closed); isolated review degraded gracefully to the single independent reviewer. Standard-mode cross-check is available as a supplement if you want a second lens.
**Files reviewed**: `client.py`, `tests/test_client.py` (staged; index == worktree). Supported-provider baseline `provider/settings.py@eval-release` retrieved from local git and inspected.
**Overall assessment**: **REQUEST_CHANGES**
**Intent & scope**: Feature `enhanced-settings`, Task 1 "Client receipt handling" (done). Task 2 "Provider receipts" is pending in a separate repo — out of scope, not flagged as missing.
**Baselines**: Review base `ac09e55`; candidate = staged index. Compatibility baseline (separate, named): released provider at tag `eval-release` (rev `22140737…`, blob `a6aeedb…`).

### Behavior and Compatibility
Ordinary-save flow (`enhanced_settings=False`) traced against the **released** provider:
1. Client sends `{"settings": values, "require_receipt": True}` — the provider reads only `request["settings"]`, so the extra key is ignored (harmless).
2. Released provider returns `{"ok": True}` — **no `applied` field**.
3. `response.get("applied")` → `None`; `None is not True` → **raises `RuntimeError`**, despite the values having been persisted.

- **New client / released `eval-release` provider — ordinary save: Blocked.** Introduced incompatibility; violates the hard "independently releasable main" / "ordinary saves must continue to work" constraint in `design.md` + `README.md`.
- **New client / candidate (Task 2) provider: Not the supported baseline** — pending, not deployed; per README it cannot change the baseline, so it does not rescue this increment.
- Conclusions are from source trace only; tests not executed (source-only access).

### Corroborated Findings
Only one independent reviewer ran, so nothing is marked *corroborated* (both-reviewer agreement). My own authored trace independently reached the same P0 before the sub-agent ran — recorded below as author-sourced agreement, not independent corroboration.

### Code Reviewer Findings

- **[client.py:5-6] — P0 — Unconditional `applied` receipt check breaks ordinary saves against the released provider**
  - Profile: python · Checklist: code-quality (Boundary Conditions: None-vs-missing) + functional-review compatibility · Triggered by: `.py` content signal.
  - Trigger: any `save_settings` call (default `enhanced_settings=False`) against the `eval-release` provider returning `{"ok": True}`. Expected: success → `{"saved": True, "enhanced": False}`. Actual: `RuntimeError("Provider did not acknowledge applied settings")`. Consequence: 100% of ordinary saves fail against the supported provider though the write succeeded — main is no longer independently releasable. Introduced (not inherited).
  - Confidence 97% (deterministic control flow against authoritative released blob; residual = tests not run / no other response-intercepting layer supplied).
  - Fix: don't require a receipt the supported provider cannot emit — treat **absence** as legacy success and only reject on explicit `response.get("applied") is False`, or gate enforcement behind the (default-off) enhanced path.

- **[tests/test_client.py:7-8] — P1 — Test fake diverges from the supported provider's response shape, masking the regression**
  - Profile: python · Checklist: code-quality (Error Handling) + functional-review step 3 · Triggered by: `.py` content signal.
  - The fake `send` returns `{"ok": True, "applied": True}` (the *future* Task 2 provider), not the released `{"ok": True}`. The green test gives false confidence for the required compatibility combination.
  - Confidence 90%. Fix: add a case driving `send` → `{"ok": True}` (eval-release shape) asserting success; keep a receipt-bearing case for when Task 2 lands.

### External Review Findings
None — PAL/Reviewer B unavailable (connection closed). Disclosed, not treated as a clean result.

### Author-Sourced Findings
Author context (`require_receipt: True`, client.py:2): currently inert against the released provider (ignored, reads only `settings`) — harmless forward-signal for Task 2, not removal-worthy. It does not itself fix or cause the P0.

### Outstanding Evidence and Prerequisites
- Hard delivery requirement (`design.md`/`README.md`) remains **open**: this increment does not support the `eval-release` provider for ordinary saves. Cannot be bypassed by pending Task 2. Durable tracking: record against Task 1 in `docs/feat/wip/enhanced-settings/tasks.md` before marking it releasable (Task 1 is currently marked `done`, which is premature given the P0).
- No evidence requests outstanding; baseline source was sufficient.

**Indexed**: systemic P0 pattern "client hard-requires a response field the old provider can't emit" indexed as `kk:review-findings`.

---

### Next steps
This was a review-only run. How would you like to proceed?
1. **Fix the P0 + P1** (treat missing `applied` as success / gate on `is False`, and add the baseline-shaped test),
2. Fix the **P0 only**,
3. Run a **standard-mode** second pass to compensate for the missing external reviewer, or
4. **No code changes** (report only).

I'll leave the evidence bundle at `/tmp/kk-evidence-enhset/` in place until you decide, then clean it up.
