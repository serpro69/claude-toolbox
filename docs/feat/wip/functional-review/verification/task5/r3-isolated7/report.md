Systemic pattern indexed. Both reviewers are in — here is the combined report.

---

## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` sub-agent (Opus, source-only) ✅ · PAL `codereview` (gemini-3.1-pro-preview, 15 files embedded — source receipt observable) ✅ — both succeeded, no failures or coverage gaps.
**Files reviewed**: `client.py`, `tests/test_client.py` (staged diff, ~7 lines) + materialized baseline `provider/settings.py@eval-release`.
**Overall assessment**: **REQUEST_CHANGES** — both reviewers independently landed here.
**Intent and scope**: Specified (authority: `design.md` + `README` delivery contract + your request). Task 1 (client receipt handling) in scope; Task 2 (provider receipts, separate repo, pending) out of scope. Selector: staged (`git diff --cached`); working tree == index.
**Baselines**: review base `ac09e55`; candidate = staged increment. **Separate** compatibility baseline: supported provider `provider/settings.py` at tag `eval-release` (`22140737`), materialized read-only outside the worktree.

### Behavior and Compatibility

`save_settings` is the only entry point (no other in-repo consumers). Traced against the authoritative supported provider, whose `update_settings` persists `request["settings"]` and returns `{"ok": True}`:

- `require_receipt: True` in the request — released provider ignores unknown keys; values still persist. **Not applicable** as a break on its own (both reviewers agree).
- `response.get("applied") is not True` — released provider returns no `applied` key → `None is not True` → **raises `RuntimeError`** after the provider already mutated storage.
- The check is **not gated on `enhanced_settings`**, so it fires on the default/"disabled by default" ordinary-save path.

**New-consumer / released-provider, `enhanced_settings=false`: BLOCKED.** This is precisely the combination the README hard-requires and `design.md` restates. Introduced by this increment (not inherited), reachable in the default config → a current regression, not a pending-task gap. Per README, the pending Task 2 provider cannot change the supported baseline.

### Corroborated Findings

- **[client.py:5–6]** Unconditional `applied` receipt check breaks ordinary saves against the supported released provider ⟨**corroborated**⟩
  - Profile: python · Checklist: code-quality (Boundary — None vs missing) + functional-review compatibility method · Triggered by: `content: .py`
  - **code-reviewer**: **P0**, 98% confidence. `save_settings(..., enhanced_settings=False)` vs `eval-release` provider → `{"ok": True}.get("applied")` is `None` → raises, though settings were persisted. False-negative that violates README's success definition ("values applied and caller sees success") and the hard independently-releasable-main requirement. Fix: gate `require_receipt`/`applied` enforcement on `enhanced_settings`; treat missing `applied` as backward-compatible success.
  - **PAL**: **CRITICAL** (`client.py:5`). Same trace and data-integrity mismatch (caller sees failure, state mutated). Fix: `if enhanced_settings and response.get("applied") is not True:`.
  - Author context (author-sourced, non-overriding): the enhanced UI is "disabled by default" per `design.md`, which is exactly why reviewers flag the *ungated* enforcement as the defect — the disabled default does not protect a check that isn't conditioned on the flag.

- **[tests/test_client.py:8]** Test mocks pending provider behavior and never exercises the supported-provider contract, masking the P0 ⟨**corroborated**⟩
  - Profile: python · Checklist: code-quality (test adequacy) + functional-review step 3 · Triggered by: `content: .py`
  - **code-reviewer**: **P1**, 95%. Mock returns `{"ok": True, "applied": True}` (the *pending* Task 2 shape), not the released `{"ok": True}`. Green suite gives false confidence; a faithful test (released shape, `enhanced_settings=False`) would fail today. Fix: add a test driving `{"ok": True}` with `enhanced_settings=False` asserting success; keep strict-receipt assertion in a separate `enhanced_settings=True` test.
  - **PAL**: **HIGH** (`tests/test_client.py:7`). Same conclusion and same split-test remediation.
  - Both note test pass/fail is author-attributed; neither executed the suite (source-only access).

### Outstanding Evidence and Prerequisites

- **Hard delivery requirement unmet** for the new-client / released-provider (`enhanced_settings=false`) combination. Must be resolved *in this increment* — code approval cannot be conditioned on the pending provider, which per README cannot change the supported baseline.
- After the fix, enhanced-path receipt enforcement stays coupled to Task 2 (provider receipts) landing and deploying. Track that in `implementation.md`/`tasks.md` so the strict path isn't active by default before the provider supports it.
- **Evidence limits**: no test execution (source-only / source-level traces, deterministic against the `eval-release` snapshot); candidate provider (Task 2) not inspected; no live environment (none required per README).

**Indexed**: one systemic pattern to `kk:review-findings` (ungated new-protocol enforcement breaking a released provider + companion test mocking unshipped behavior).

---

Both reviewers converge on **REQUEST_CHANGES**, driven by the corroborated P0/Critical. The suggested fix (gate the receipt requirement — both the `require_receipt` send and the `applied` check — on `enhanced_settings`, and split the test) is consistent across both.

How would you like to proceed? I can:
1. **Apply the fix** to `client.py` + split the test in `tests/test_client.py`, or
2. **Fix only the P0** (client gating) and leave the test to you, or
3. **Make no changes** — review only.

Default is review-only; I won't edit without your go-ahead.
