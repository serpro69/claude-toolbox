Investigation complete. The trace is deterministic and conclusive against the materialized supported-provider baseline.

## Code Review Findings

**Files reviewed**: 2 files (`client.py`, `tests/test_client.py`), ~7 lines changed
**Active profiles**: python
**Overall assessment**: REQUEST_CHANGES
**Intent and scope**: Specified (authority: design.md + README delivery contract + user request). Task 1 (client-side receipt handling) in scope; Task 2 (provider receipts, separate repo) pending/out-of-scope. Diff selector: staged (`git diff --cached`); candidate identity working tree == index.
**Baselines**: Review base commit `ac09e55` (candidate = staged client increment). Compatibility baseline (separate): supported provider `provider/settings.py` at tag `eval-release` / commit `22140737`, materialized at `/tmp/kk-review-code-evidence/provider-settings.eval-release.py`.

### Behavior and Compatibility

Traced `save_settings` (the only entry point; confirmed no other in-repo consumers) against the authoritative supported-provider baseline `update_settings`, which does `storage[workspace_id] = dict(request["settings"]); return {"ok": True}`.

- The new client sends `{"settings": values, "require_receipt": True}`. The released provider reads only `request["settings"]` and ignores `require_receipt` — so the settings values are still applied and persisted; the extra field is harmless to the old provider. **Not applicable** as a break on its own.
- The new client then enforces `response.get("applied") is not True`. The released provider returns `{"ok": True}` with no `applied` key → `None is not True` → **raises `RuntimeError`**. The provider mutated storage (values applied) but the caller sees a failure.
- This check is **unconditional** — it is not gated on `enhanced_settings`. With `enhanced_settings=False` (the default / "disabled by default" configuration), ordinary saves against the supported provider therefore fail.

**Compatibility dimension — new consumer / released (old) provider, enhanced_settings=false: BLOCKED.** This is the exact combination the README hard-requires ("Every merged client increment must support the released provider at `eval-release`, including ordinary settings saves while `enhanced_settings` is false") and the design restates ("Ordinary saves must continue to work with the supported provider at eval-release"). The failure is introduced by this increment, not inherited, and the affected path is reachable in the default configuration — so it is a current regression, not a pending-task gap. Task 2 (provider receipts) is pending in a separate repo and explicitly not deployed; per README a pending provider task cannot change the supported baseline.

---

### P0 - Critical

- **[client.py:5-6]** Unconditional `applied` receipt check breaks ordinary saves against the supported released provider
  - Profile: python · Checklist: /private/tmp/fr-task5-actors-x3akibin/r3-isolated7/plugins/kk/profiles/python/review-code/code-quality-checklist.md (Boundary Conditions — None vs missing inconsistency) + functional-review compatibility method
  - Triggered by: content: extension .py — client.py
  - Trigger/path: any call to `save_settings(..., enhanced_settings=False)` (the default, "disabled by default" path) against the `eval-release` provider. Expected (per README/design): the save succeeds and the caller sees success, because the released provider applies the values and returns `{"ok": True}`. Actual: `response.get("applied")` is `None`, `None is not True` is `True`, so the client raises `RuntimeError("Provider did not acknowledge applied settings")`. Consequence: the provider has already persisted the settings (`storage[workspace_id]` mutated) but every caller observes a hard failure — a false-negative that violates the README's definition of a successful save ("values were applied and the caller sees success") and the hard independently-releasable-main / supported-provider delivery requirement. The enhanced receipt enforcement must not apply when the feature is disabled and the supported provider cannot yet emit a receipt.
  - Confidence: 98% — the baseline provider source is the authoritative materialized snapshot and the client logic is a deterministic source-level trace; `{"ok": True}.get("applied")` is unambiguously `None`. Not 100% only because I cannot execute tests from source-only access (I do not claim execution).
  - Suggested fix: gate the receipt requirement on capability/feature state rather than enforcing it unconditionally — e.g. only send `require_receipt` and require `applied is True` when `enhanced_settings` is true, and otherwise accept `{"ok": True}` from the released provider (treat a missing `applied` as backward-compatible success). This preserves ordinary saves against `eval-release` while keeping the enhanced path strict once the provider increment ships.

### P1 - High

- **[tests/test_client.py:8]** Test mocks pending provider behavior and does not exercise the supported-provider contract, masking the P0 regression
  - Profile: python · Checklist: /private/tmp/fr-task5-actors-x3akibin/r3-isolated7/plugins/kk/profiles/python/review-code/code-quality-checklist.md (Error Handling / test adequacy) + functional-review step 3
  - Triggered by: content: extension .py — tests/test_client.py
  - Trigger/path: `test_successful_save` stubs `send` to return `{"ok": True, "applied": True}`. That shape matches the **pending, undeployed** provider (Task 2), not the released/supported provider, which returns `{"ok": True}` with no `applied`. Expected: a test guarding the delivery contract would exercise the released provider's response shape (no `applied`) for the default `enhanced_settings=False` path. Actual: the only test asserts success against a mock of future behavior. Consequence: the suite reports green (author-attributed claim; I did not run it) while the supported-provider contract is in fact broken — the test provides false confidence and fails to catch the P0. A faithful test using the `eval-release` response (`{"ok": True}`) with `enhanced_settings=False` would (correctly) fail today, surfacing the regression.
  - Confidence: 95% — response-shape mismatch between the mock and the materialized baseline is directly verifiable; the "passes" status is an attributed author claim, not my execution.
  - Suggested fix: add a test that drives the supported-provider response shape (`{"ok": True}`, no `applied`) with `enhanced_settings=False` and asserts the ordinary save succeeds; keep the strict-receipt assertion in a separate test scoped to `enhanced_settings=True`. This locks the delivery contract into CI.

### P2 - Medium

(none)

### P3 - Low

(none)

---

### Removal/Iteration Plan

Not applicable — no dead/feature-flagged-off code introduced. The `require_receipt` field and `applied` enforcement are new active behavior, not removal candidates; the fix is to scope them, not delete them.

### Areas Not Covered

- Test pass/fail is author-attributed; I have source-only access and did not execute `tests/test_client.py` or any provider code. The behavioral conclusions are source-level traces, not runtime observations.
- The candidate provider (Task 2, separate repository) was not inspected and is out of scope; its receipt semantics are unverified. The strict `applied` enforcement would become appropriate only once that provider ships and is deployed — relevant only to pending work, not a current defect.
- No live environment exists or is required (per README); deployment state is not verified, only source compatibility against the `eval-release` snapshot.

### Evidence Requests

None — the materialized `eval-release` provider baseline and provenance manifest are sufficient to reach the P0/P1 conclusions. No additional source is needed to establish the incompatibility.

### Outstanding Prerequisites

- The README delivery contract is a hard independently-releasable-main requirement; the P0 leaves it unmet for the required new-client / released-provider (`enhanced_settings=false`) combination. This must be resolved in this increment (code approval cannot be conditioned on the pending provider, which per README cannot change the supported baseline).
- Once fixed, enhanced-path receipt enforcement remains dependent on Task 2 (provider receipts) landing and being deployed — track that coupling in `docs/feat/wip/enhanced-settings/implementation.md` / `tasks.md` so the strict path is not activated by default before the provider supports it.
