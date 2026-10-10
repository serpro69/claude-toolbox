Indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Requirement source `docs/feat/wip/enhanced-settings/{design,implementation,tasks}.md`. Current task = **Task 1: Client receipt handling** (status: `done`). Selected diff = **staged** changes (no unstaged present). Review mode = **mid-implementation** (Task 2 `pending`).
**Baselines**: Review base/candidate = `HEAD` (`ac09e55`) → staged index. Separate **release baseline** = deployed provider from commit `2214073` "Released provider" (`provider/settings.py`), which returns `{"ok": True}` and nothing else.

**Task Scope**
- In scope: Task 1 (client.py, tests/test_client.py) — done.
- Out of scope (do not flag as missing): Task 2 — Provider receipts, separate repo, pending.

**Profiles**: `python` active (`.py` extension). All four Python checklists applied (security, SOLID, code-quality, removal). No other profile matched (no Go/Java/JS-TS/Kotlin/K8s signals; no `SKILL.md` ancestor).

## Behavior and Compatibility

The change makes the client (1) send `require_receipt: True` in the request and (2) **unconditionally** require `response["applied"] is True`, raising `RuntimeError` otherwise — regardless of the `enhanced_settings` flag.

Scenario trace — **new client × released provider** (`contract → state → result`):
- Released provider `update_settings` persists `storage[workspace_id] = dict(request["settings"])` then returns `{"ok": True}`. It ignores the extra `require_receipt` field (request side is forward-compatible — good) and **never emits `applied`**.
- New client: `response.get("applied")` → `None`; `None is not True` → **raises `RuntimeError("Provider did not acknowledge applied settings")`** — on *every* save, including ordinary non-enhanced saves.
- Net effect: the provider **has already written the data**, but the client reports failure. The documented hard requirement *"Ordinary saves must continue to work with the supported provider at eval-release"* is violated, and *"preserving independently releasable main"* is broken: client-main cannot be released independently of the (pending, separate-repo) Task 2 provider.

| Dimension | Conclusion |
|---|---|
| New consumer / old (released) provider | **Blocked** — demonstrated breakage; confirmed against `provider/settings.py` @ `2214073`. |
| Request forward-compat (`require_receipt`) | **Supported** — released provider ignores unknown keys. |
| New consumer / new provider (post–Task 2) | **Not applicable to this diff** — Task 2 pending; not a finding. |

---

## Findings

### P0 - Critical

(none — the break fails loud via `RuntimeError` and the provider still persists data, so it's recoverable, not irreversible/silent loss. It borders P0 because it breaks the entire save flow against the deployed provider; see P1.)

### P1 - High

- **[client.py:5]** Unconditional `applied` receipt check breaks ordinary saves against the released provider (violates independently-releasable-main)
  - Profile: python · Checklist: code-quality-checklist.md (boundary/None handling) + functional-review compatibility
  - Triggered by: delivery-contract trace — design "ordinary saves must continue to work… preserving independently releasable main"; released provider `provider/settings.py@2214073` returns `{"ok": True}` with no `applied`.
  - Trigger/path: any `save_settings` call against the deployed provider → `response.get("applied")` is `None` → `None is not True` → `RuntimeError`. Provider has already written the data, so the caller sees a failure for a succeeded write (integrity/UX harm) and will likely retry.
  - Expected vs actual: expected ordinary save to succeed against the eval-release provider; actual it always raises.
  - Confidence: **95%** — confirmed against actual released-provider source and the design's stated hard requirement. Residual uncertainty: whether production wires the client to anything other than the released provider (no adapter exists in-repo).
  - Suggested fix: make the receipt check backward-compatible — only fail on an explicit negative, e.g. `if response.get("applied") is False: raise RuntimeError(...)`. That keeps ordinary saves working against the old provider while still enforcing receipts once the Task 2 provider ships `applied: true/false`. (Alternatively gate enforcement behind a negotiated capability; gating behind `enhanced_settings` alone is weaker since the design frames the receipt as a protocol-level, not UI-gated, addition.)

### P2 - Medium

- **[tests/test_client.py:8]** Test edit masks the backward-incompatibility instead of catching it
  - Profile: python · Checklist: code-quality-checklist.md (test/coverage) + functional-review ("green implementation-shaped tests don't prove a business operation")
  - Trigger/path: the only test was changed from `{"ok": True}` to `{"ok": True, "applied": True}`, modeling the *future* provider. The suite is green while the real released-provider contract (`{"ok": True}`, no `applied`) is never exercised — the exact regression path in the P1 finding.
  - Confidence: 90%.
  - Suggested fix: add a test asserting a save succeeds against a provider returning `{"ok": True}` (no `applied`) — this would fail today and guard the independent-release contract. Also add tests for `applied: False` → `RuntimeError` and the existing `ok: False` path, which are currently uncovered.

### P3 - Low

- **[client.py:4-6]** Both failure modes raise bare `RuntimeError`, so callers cannot distinguish "save rejected" (`ok` false) from "receipt not acknowledged" (write may have succeeded). Consider distinct exception types/messages if callers branch on outcome. Confidence: 60% — depends on caller needs (none visible in-repo).

---

## Removal/Iteration Plan

None — no dead code or removal candidates in this diff.

---

## Next Steps

I found 3 issues (P0: 0, P1: 1, P2: 1, P3: 1).

Actionable items I recommend fixing:
1. **P1 — client.py:5**: make the `applied` check backward-compatible (`is False` only) so ordinary saves keep working against the released provider and main stays independently releasable.
2. **P2 — test_client.py**: add a test for the old-provider contract (`{"ok": True}`, no `applied`) plus `applied: False` and `ok: False` paths.
3. **P3 — client.py**: optionally differentiate the two failure modes.

Items I recommend keeping as is:
- Sending `require_receipt: True` in the request — released provider ignores unknown keys, so this is forward-compatible.
- Task 2 provider work absent from the diff — correctly out of scope (pending, separate repo); not flagged.

**Coverage & limits**: Reviewed both staged `.py` files in full against the released-provider baseline (`provider/settings.py@2214073`). I did not execute the test suite (source-only inspection). The production wiring of `send` lives outside this repo; my compatibility conclusion rests on the design doc's stated eval-release provider and the committed released-provider source.

**How would you like to proceed?**

1. **Fix all** — implement all suggested fixes
2. **Fix P1/P2 only** — the independent-release break + its test gap
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or give specific instructions. (I won't make changes until you confirm.)
