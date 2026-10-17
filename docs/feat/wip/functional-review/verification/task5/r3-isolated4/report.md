Indexed. Both independent reviewers finished and corroborate. Here is the consolidated report.

---

## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` sub-agent (Opus 4.8) ✓ · PAL `codereview` (gemini-3.1-pro-preview) ✓ — both succeeded; no failures. PAL `file_context: fully_embedded` (14 files embedded), so external source receipt is **verified**, not just path-supplied.
**Files reviewed**: 2 files, ~6 lines — `client.py` (+3/−1), `tests/test_client.py` (+1/−1)
**Active profile**: `python` (always-load: security, solid, code-quality, removal checklists)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Authoritative intent from `design.md` + `README.md`. Task 1 "Client receipt handling" (done, in-scope); Task 2 "Provider receipts" (separate repo, pending, correctly absent — not flagged). Diff selector: **staged** index blobs (matches worktree).
**Baselines**: Review base = `ac09e55`. Candidate = staged index blobs. Compatibility baseline (separate) = released provider `provider/settings.py` at tag **`eval-release`** (`22140737`, blob `a6aeedb`), materialized into the evidence bundle since provider sources were removed from HEAD after release.

### Behavior and Compatibility

Traced the one changed entry point `save_settings` against the authoritative released provider `update_settings`, which persists the settings, ignores unknown keys (`require_receipt`), and returns `{"ok": True}` — **no `applied` key**.

Ordinary save (`enhanced_settings=False`) against the released provider:
1. Client sends `{"settings": values, "require_receipt": True}`.
2. Provider **applies** the values, returns `{"ok": True}`.
3. `response.get("ok")` truthy → passes.
4. `response.get("applied") is not True` → `None is not True` → **raises `RuntimeError`**.

- **New client / released provider (required combination): Blocked.** Deterministic incompatibility on the default, flag-off path, caused by this change.
- **Feature flag as mitigation: Not applicable.** `enhanced_settings` only feeds the return value; it does not gate the receipt check, so "disabled by default" does not protect the baseline.
- **New client / candidate Task 2 provider: Unknown / out-of-scope.** The future provider is pending and not deployed; per README it cannot change the supported baseline, so it does not rescue this increment.

Evidence limit: source-traced, not run-observed (no reviewer executed `python3 -m unittest`); the trace is deterministic against the authoritative baseline.

---

### Corroborated Findings

**[client.py:5-6] Unconditional `applied` receipt check breaks ordinary saves against the released provider** ⟨corroborated⟩
- Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions — None vs missing; Data Integrity) · Triggered by: content — `.py`
- **code-reviewer: P0 (97%)** — provider applies the settings but client raises; a succeeded save is reported as failure. Violates the README hard constraint ("ordinary settings saves while enhanced_settings is false … values applied and the caller sees success") and is a data-integrity false-negative (storage mutated while caller believes failure; blind retries re-apply). Not gated by the flag, so the default path regresses.
- **PAL: [CRITICAL]** — "Unconditional receipt validation breaks backward compatibility and causes false failures… violates the hard delivery constraint and creates a data-integrity risk." Fix: gate the check behind `enhanced_settings`.
- Suggested fix (both): only enforce acknowledgement when `enhanced_settings` is true (and only send `require_receipt` then); otherwise treat missing `applied` as backward-compatible success and fail only on an explicit `applied: False`.

**[tests/test_client.py:7-8] Sole test exercises only the future provider shape, masking the regression** ⟨corroborated⟩
- Profile: python · Checklist: code-quality-checklist.md (tests must exercise the claimed contract) · Triggered by: content — `.py`
- **code-reviewer: P1 (90%)** — stub returns `{"ok": True, "applied": True}` (the pending Task 2 shape); the required released-provider path (`{"ok": True}`, no `applied`) is never tested, so the suite stays green while the required behavior is broken. Confirmed via grep that `save_settings`/`applied` appear only in these two files.
- **PAL: [HIGH]** — "Unit test masks regression by dropping legacy provider coverage… abandons testing the client's mandatory backward compatibility contract." Fix: restore a legacy-provider test (`{"ok": True}`) **and** add a separate `enhanced_settings=True` test.

### Code Reviewer Findings (not independently corroborated as a defect)

**[client.py:2] `require_receipt: True` sent unconditionally regardless of `enhanced_settings`**
- Profile: generic · Triggered by: —
- **code-reviewer: P3 (80%)** — harmless against the released provider (unknown key ignored), but signals the protocol change isn't actually gated by the flag; natural companion to the P0 fix.
- **PAL (differing view):** listed this same behavior as a **positive** — "unconditionally sending `require_receipt: True` is a safe pattern since the legacy provider simply ignores unknown dictionary keys." Both agree it is *not* currently harmful; they differ on whether to tidy it. Preserved as low-severity design-consistency only.

### Outstanding Prerequisites

- The hard delivery requirement (support the released provider at `eval-release` for ordinary saves) is **unmet** by this increment and must be satisfied before merge — independent of Task 2. A pending/future provider does not change the supported baseline (README), so this is a demonstrated code defect, not a deferrable rollout prerequisite.

### Indexing

Indexed the systemic P0/P1 pattern to `kk:review-findings` (unconditional new-protocol-field enforcement breaking an independently-released counterpart + the test-edited-to-new-shape coverage-loss anti-pattern). Knowledge base was previously empty — no duplicates.

### Evidence / cleanup

Evidence bundle retained at `/tmp/kk-review-enhanced-settings/` (diff, candidate snapshots, historical provider blob, manifest) in case you want fixes applied; I'll remove it once we're done.

---

## Next Steps

Two corroborated blocking issues (**P0: 1, P1: 1**) plus one **P3** consistency note. Both are fixed by the same small change:

1. **P0** `client.py` — gate the `applied` receipt check behind `enhanced_settings` (and send `require_receipt` only when enhanced), or treat missing `applied` as success and fail only on explicit `applied: False`.
2. **P1** `tests/test_client.py` — add a released-provider case (`{"ok": True}`, assert success) and keep a separate `enhanced_settings=True` acknowledgement case.
3. **P3** `client.py` — send `require_receipt` only when the flag is on (folds into fix #1).

**How would you like to proceed?**

1. **Fix all** — P0 + P1 + P3
2. **Fix P0/P1 only** — the blocking issues
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no edits

I won't make any edits until you choose.
