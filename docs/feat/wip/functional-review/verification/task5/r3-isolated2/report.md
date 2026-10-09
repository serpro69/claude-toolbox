Both independent reviewers are complete and the systemic finding is indexed. Here's the consolidated report.

---

## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` sub-agent (Opus 4.8) + PAL `codereview` (`gemini-3.1-pro-preview`) — both completed, no failures, full source coverage.
**Files reviewed**: `client.py`, `tests/test_client.py` (staged; +4/−2). Compatibility baseline `provider/settings.py` @ `eval-release` materialized as historical evidence.
**Overall assessment**: **REQUEST_CHANGES** (both reviewers independently; hard delivery-contract violation — cannot be approved as independently releasable).
**Intent & scope**: enhanced-settings Task 1 (client receipt handling, status `done`). Task 2 (provider receipts, separate repo, `pending`) is out of scope — *not* flagged as missing.
**Baselines**: Review base `ac09e55`; candidate = staged index. Separate compatibility baseline = `provider/settings.py` @ `22140737` (tag `eval-release`, blob `a6aeedb`) — returns `{"ok": True}`, no `applied` key, ignores unknown request keys. No live env (none required per README).

### Behavior & Compatibility

Traced the contract-required combination — **new client + released `eval-release` provider + ordinary save (`enhanced_settings=False`)**:

1. Client sends `{"settings": values, "require_receipt": True}`.
2. Released provider persists `request["settings"]`, drops `require_receipt`, returns `{"ok": True}` (no `applied`).
3. Client: `ok` is truthy → passes; then `response.get("applied")` is `None`, `None is not True` → **raises `RuntimeError`**.

| Combination | Verdict |
|---|---|
| New client + released provider, ordinary save | **Blocked** — regression introduced by this change |
| New client + new provider (`applied: True`) | Supported (only the updated unit test; source-only, not executed) |
| `{"ok": False}` path | Not applicable (unchanged) |
| Old client + new provider | Not applicable (provider pending, separate repo) |

### Corroborated Findings

**[client.py:5-6] Unconditional `applied` receipt check breaks ordinary saves against the released provider ⟨corroborated⟩**
- Profile: python · Checklist: code-quality (None/boundary handling) + functional-review compatibility mapping · Triggered by: content (`.py`)
- **code-reviewer** — **P0** (98%): The check never consults `enhanced_settings` (default `False`, the disabled-UI/ordinary path). Against the released provider the values *are* persisted, but the caller sees an exception — a reported-failure/actual-success divergence that invites spurious retries. Violates README's hard "every merged client increment MUST support the released provider at `eval-release`, including ordinary saves while `enhanced_settings` is false" and "a successful save means values were applied and the caller sees success." Introduced regression, defeats independently-releasable-main; a pending provider task cannot change the supported baseline.
- **PAL** — **[CRITICAL] client.py:5**: "Breaks backward compatibility with the currently released provider… ordinary saves will crash in production until the new provider is deployed, directly violating the delivery contract." Suggested fix: `if enhanced_settings and response.get("applied") is not True:`
- Suggested correction (both): gate enforcement on the feature — only require `applied` when `enhanced_settings` is true; a missing receipt from the released provider must remain a success.

**[tests/test_client.py:7-10] Test suite omits the required released-provider combination and masks the regression ⟨corroborated; differing severity⟩**
- Profile: python · Checklist: code-quality (tests must exercise the claimed contract) · Triggered by: content (`.py`)
- **code-reviewer** — **P1** (95%): The only test was edited so the fake `send` returns the *new-provider* shape `{"ok": True, "applied": True}`. No test covers the released-provider response `{"ok": True}` with `enhanced_settings=False`. Green CI gives false confidence and hides the P0.
- **PAL** — **[MEDIUM] tests/test_client.py:6**: "Fell into the common pitfall of 'updating the test to make it pass' rather than preserving existing contractual tests… which is why the suite failed to catch the critical regression." Suggested: separate legacy-provider and enhanced-provider tests.

### Code Reviewer Findings (not corroborated)

**[client.py:2] `require_receipt: True` sent unconditionally — P2** (code-reviewer, 80%): Couples the ordinary-save request shape to the enhanced feature. Harmless *today* (released provider ignores unknown keys) but recommends sending it only when `enhanced_settings` is true, paired with the P0 fix.
- **Disagreement preserved** — PAL listed this same behavior as a **positive aspect**: "pragmatic, forward-compatible… the legacy provider safely ignores unknown keys, reducing unnecessary branching." Not corroborated; your call which lens applies.

### Areas Not Covered
- **Test execution**: both reviewers worked source-only; neither ran `python3 -m unittest`. The passing updated test is author-attributed evidence, and it covers only the new-provider shape.
- **Real caller of `save_settings`**: only the in-repo test imports it; the UI caller that interprets the raised `RuntimeError` lives outside this checkout. The "caller sees failure after successful persist" consequence is reasoned from the documented contract, not observed.
- **Task 2 provider**: out of scope / separate repo — its absence is an expected gap, not a finding. The P0/P1 are current-increment regressions independent of Task 2 landing.

### Outstanding Prerequisites
- The hard README requirement (independently-releasable main; ordinary saves working against `eval-release`) is **not satisfied** by this increment. It cannot ship as independently releasable until the `applied` check tolerates a missing receipt from the released provider (gate on `enhanced_settings`) **and** a test covers the released-provider `{"ok": True}` shape.

**Indexed**: systemic P0 pattern → `kk:review-findings` ("unconditional new-protocol-field enforcement breaks the independently-releasable baseline").

---

### Next steps?

This is review-only — I've made no code changes. How would you like to proceed?
1. **Apply the corroborated fix** — gate the `applied` check (and optionally `require_receipt`) on `enhanced_settings`, and add the released-provider + enhanced-provider tests.
2. **Fix the P0 only** (minimal: make the receipt check tolerant of the released provider).
3. **Fix selected items** (tell me which).
4. **No changes** — leave as-is.

I've retained the evidence bundle at `/tmp/kk-review-enhanced-settings/` pending your decision; I'll clean it up when we're done.
