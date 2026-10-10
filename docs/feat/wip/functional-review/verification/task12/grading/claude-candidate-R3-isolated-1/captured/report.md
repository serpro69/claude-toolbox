## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` (independent sub-agent) — completed. **PAL (external model): UNAVAILABLE** — the `pal` MCP server reported `CONNECTION_CLOSED` this session, so Reviewer B could not run. Proceeded with the single independent reviewer per the skill's graceful-degradation rule. **No two-reviewer corroboration is available** — findings below rest on the independent reviewer plus my own parent trace against the released-provider source, not on independent cross-confirmation.
**Files reviewed**: `client.py` (+3/−1), `tests/test_client.py` (+1/−1) — staged (git index); worktree identical (no unstaged changes).
**Overall assessment**: **REQUEST_CHANGES** (violated hard delivery requirement).
**Intent and scope**: enhanced-settings Task 1 "Client receipt handling" — adds a client-side application receipt to the settings-save protocol. Task 2 (provider receipts, separate repo) is pending and out of scope *as an implementation target*, but the delivery contract still applies.
**Baselines**: review base `ac09e55`; candidate = staged index. Supported compatibility baseline = released provider `provider/settings.py` at tag **`eval-release`** (rev `22140737`, blob `a6aeedb`) — returns `{"ok": True}` only, **no `applied` key**, and ignores `require_receipt`.

### Behavior and Compatibility
Traced the candidate `save_settings` against the released provider `update_settings`:
1. Client sends `{"settings": values, "require_receipt": True}`.
2. Released provider persists the values (`storage[...] = dict(request["settings"])`), ignores `require_receipt`, returns `{"ok": True}`.
3. `response.get("ok")` → `True`, first guard passes.
4. `response.get("applied")` → `None`; `None is not True` → **raises `RuntimeError`**.

Net: values **are** persisted but the caller sees an exception.

- **New client / released provider (eval-release)** — **Blocked.** Demonstrated, deterministic from source.
- **Ordinary save, `enhanced_settings=False`** — **Blocked.** The guard is unconditional, not gated by the flag.
- **New client / future Task-2 provider** — **Not applicable (out of scope).** Pending provider work cannot change the supported baseline (README), so it can't rescue the verdict.

### Findings (independent reviewer; parent trace agrees)

**P0 — `client.py:5-6` · Unconditional `applied` receipt check breaks ordinary saves against the released provider**
- Profile: python · Checklist: `code-quality-checklist.md` (boundary/None handling) + functional compatibility method.
- Expected: ordinary saves succeed and the caller sees success when values are applied (README: "a successful save means values were applied and the caller sees success"). Actual: released provider applies the values and returns `{"ok": True}`, but the client raises because `applied` is absent.
- Consequence: violates the **hard** requirement that every merged client increment support the released provider at `eval-release` including ordinary saves while `enhanced_settings` is false, and breaks independently-releasable main. Introduced (not inherited — review base had no `applied` check).
- Confidence: ~99% (provider baseline supplied; control flow deterministic).
- Fix: treat an absent receipt as legacy success — `if response.get("applied") is False: raise RuntimeError(...)` — so receipts still work for the future provider while ordinary saves against `eval-release` keep working. `require_receipt: True` is harmless to the released provider (ignored), though consider gating it to the receipt feature rather than sending it unconditionally.

**P1 — `tests/test_client.py:8` · Test uses the new-provider response shape, masking the P0**
- The sole test's mock returns `{"ok": True, "applied": True}` — the shape Task 2 will produce, not the released provider's `{"ok": True}`. The suite stays green while the supported baseline is broken. Green implementation-shaped tests don't prove the operation against the supported provider.
- Fix: add a test with mock `{"ok": True}` (no `applied`) asserting `save_settings` returns `{"saved": True, "enhanced": False}` (no raise); optionally a `{"ok": True, "applied": False}` case asserting the RuntimeError to pin receipt semantics.
- Note: source-only review — tests were **not** executed.

**P3 — `client.py:5` · `is not True` rejects truthy non-bool acknowledgements** (forward-looking, depends on unspecified Task-2 receipt encoding; largely dissolves if the `is False` fix lands).

### Author-/parent-sourced observation
`enhanced_settings` is accepted and echoed but gates nothing. design.md implies the receipt is protocol-level (independent of the enhanced UI), so this is likely acceptable — flagged only to confirm the receipt was *not* meant to be gated by the flag.

### Outstanding Evidence and Prerequisites
- **Coverage limits**: single independent reviewer (PAL down → no corroboration); tests not executed (source-only); capy KB was empty (cold start — nothing to compare against). No other consumers of `save_settings` exist in this checkout.
- The P0 is a violated **hard** delivery requirement; per the verdict mapping it cannot be waived by pending Task 2 and stays open unless you explicitly accept an exception (with recorded rationale). The fix belongs in **this** increment. No durable tracker was supplied — recommend recording against Task 1 of enhanced-settings.
- **Indexed**: the systemic pattern (receipt guard breaking new-consumer/old-provider compat, masked by a co-changed test) was indexed to `kk:review-findings`.

---

**Verdict: REQUEST_CHANGES** — the client increment does not support the released provider; ordinary saves break.

How would you like to proceed?
1. **Apply the P0 + P1 fix** (change to `is False`, add a released-provider-shape test),
2. **Fix all** (incl. P3/flag-gating discussion),
3. **Fix selected items**, or
4. **No changes** (review only).

Temp evidence is retained at `/tmp/kk-evidence-enhset/` in case you want a fix; I'll remove it once we're done. PAL was unavailable — tell me if you'd like to retry isolated mode once the server reconnects, or run standard `/kk:review-code` as a supplement.
