Review complete. Here are the findings.

## Code Review Summary

**Files reviewed**: 2 files, 4 insertions / 2 deletions (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Requirement source `docs/feat/wip/enhanced-settings/{design,implementation,tasks}.md`. Current task = Task 1 "Client receipt handling" (status: **done**, in scope). Selected diff = **staged** (no unstaged changes present). Mode = mid-implementation (Task 2 "Provider receipts" pending, separate repo, out of scope).
**Baselines**: Review base = `ac09e55` (client.py returning `{"ok": True}` contract, no `applied` check). Released/deployed provider = `2214073` "Released provider" → `provider/settings.py.update_settings` returns `{"ok": True}` and ignores `require_receipt`. Profile active: **python** (checklists: security, solid, code-quality, removal).

## Behavior and Compatibility

The change makes `save_settings` (a) send `require_receipt: True` unconditionally and (b) raise `RuntimeError` unless the response contains `applied is True`.

Design contract is explicit: *"Ordinary saves must continue to work with the supported provider at eval-release"* and *"preserving independently releasable main."* The supported provider at eval-release is `2214073`, which returns only `{"ok": True}`.

I traced the concrete scenario: new client → released provider. `response.get("applied")` is `None` → `None is not True` → **raise `RuntimeError("Provider did not acknowledge applied settings")`**. This breaks **every** ordinary save, not just enhanced ones — the enforcement is ungated by `enhanced_settings`, even though the enhanced UI is "disabled by default." Worse, the released provider *persists the settings* (`storage[workspace_id] = dict(request["settings"])`) **before** returning, so the client reports failure for a save that actually succeeded.

| Dimension | Conclusion |
|---|---|
| New client / released provider (`2214073`) | **Blocked** — demonstrated: all ordinary saves raise; violates stated hard delivery requirement |
| New client / new provider (Task 2) | **Unknown/future** — would work only once the separate-repo provider emits `applied: True`; that task is pending |
| Old client / released provider | Not applicable — unaffected |

Evidence limits: Task 2's provider code lives in a separate repository not present here; I assessed only the client increment against the locally available released provider, per the implementation doc's instruction.

---

## Findings

### P0 - Critical
(none — the break is severe but recoverable: an error is raised and no irreversible/catastrophic loss occurs)

### P1 - High

- **[client.py:5-6]** New `applied` receipt check breaks ordinary saves against the supported provider / defeats independent releasability
  - Profile: python · Checklist: code-quality-checklist.md (boundary/None handling) + functional-review (compatibility)
  - Triggered by: content — `.py` extension (python profile active)
  - Trigger/path: new client calls the released provider (`{"ok": True}`). Expected: ordinary save succeeds (design: "must continue to work with the supported provider"). Actual: `response.get("applied")` is `None` → `None is not True` → `RuntimeError`. Consequence: **100% of ordinary saves fail** while the provider has silently persisted the data; `main` is no longer independently releasable because the client now hard-depends on the pending Task 2 provider change.
  - Confidence: 95% — verified against the actual released provider source at `2214073`; the only residual uncertainty is the real-world deploy ordering, but the design text explicitly mandates independent releasability and supported-provider compatibility.
  - Suggested fix: make the consumer tolerant of a not-yet-upgraded provider until Task 2 ships. Treat missing `applied` as backward-compatible, and only enforce the receipt when the provider participates — e.g. `if "applied" in response and response["applied"] is not True: raise`, or gate the whole receipt handshake behind the `enhanced_settings`/feature flag so the default (disabled) path matches the released contract. Confirm the chosen rollout order with the delivery policy.

### P2 - Medium

- **[tests/test_client.py:8]** Test fixture mutated to inject `applied: True`, masking the compatibility regression
  - Profile: python · Checklist: code-quality-checklist.md (error handling / coverage) · also test-patterns
  - Triggered by: content — `.py` extension
  - Trigger/path: the only test now returns `{"ok": True, "applied": True}`, so it never exercises the released provider's real `{"ok": True}` shape. Expected: a test suite that would catch a break against the supported provider. Actual: green suite that encodes the new, breaking assumption and hides finding #1. No test covers the new failure branch either.
  - Confidence: 90% — the fixture change directly corresponds to the new enforcement; it's a classic "test repeats the implementation's assumption" case.
  - Suggested fix: keep/add a test asserting an ordinary save still succeeds when the provider responds `{"ok": True}` (no `applied`), and add a test for the acknowledge-failure branch (`applied` falsy → `RuntimeError`).

### P3 - Low

- **[client.py:2]** `require_receipt: True` is sent unconditionally regardless of `enhanced_settings`. Harmless against the current provider (it ignores unknown keys), but if the receipt protocol is meant to ride with the enhanced feature, consider gating it with the flag for consistency with "disabled by default." Confidence: 55% — depends on intended protocol scope; design says the receipt is added to the protocol generally, so this may be intentional.

---

## Coverage and limits

- **Checked**: full staged diff; both changed files at the staged revision; the released-provider contract (`2214073`); design/implementation/tasks docs; all four python review-code checklists; SOLID/security/quality/boundary general categories.
- **Not covered**: Task 2 provider implementation (separate repo, not available) — out of scope; no CI/integration environment was exercised (source-only analysis, no tests run).
- **Residual risk / recommended follow-up**: verify the actual client↔provider deploy ordering against the "independently releasable main" policy; add the backward-compat and failure-path tests noted above.

Indexed finding #1 to `kk:review-findings` as a systemic independent-release compatibility pattern.

---

## Next Steps

I found 3 issues (P0: 0, P1: 1, P2: 1, P3: 1).

Actionable items I recommend fixing:
1. **P1** — Make `save_settings` tolerate a provider that doesn't emit `applied` (missing ⇒ backward-compatible, or gate behind the flag) so ordinary saves keep working and `main` stays independently releasable.
2. **P2** — Restore/add a test for the `{"ok": True}` (no `applied`) provider response and add a failure-branch test.
3. **P3** — Decide whether `require_receipt` should be gated by `enhanced_settings`.

Items to consider keeping as-is:
- P3 may be intentional if the receipt is a protocol-wide addition rather than an enhanced-only feature — your call.

**How would you like to proceed?**

1. **Fix all** — implement all suggested fixes
2. **Fix P0/P1 only** — address the compatibility break (+ I'd recommend the P2 test alongside it)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

I won't make any changes until you confirm.
