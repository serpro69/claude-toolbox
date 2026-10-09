## Review Summary (Isolated Mode)

**Reviewers**: `kk:code-reviewer` sub-agent (Opus 4.8) + PAL `codereview` (gemini-3.1-pro-preview, 15 files embedded — source receipt **verified**). Both succeeded; no degradation.
**Files reviewed**: `client.py`, `tests/test_client.py` (staged; worktree == index). Candidate = staged index blobs; base = HEAD `ac09e55`.
**Overall assessment**: **REQUEST_CHANGES** (both reviewers independently; code verdict).
**Intent & scope**: Authority = `design.md` + `implementation.md`. In scope: Task 1 (client receipt handling, `done`). Out of scope: Task 2 (provider receipts, pending, separate repo) — **not** flagged as missing.
**Baselines**: review base HEAD `ac09e55`; compatibility baseline = currently supported/deployed provider, whose source is in a **separate repo not available locally** (its exact contract is Unknown — see Outstanding Evidence).

### Behavior & Compatibility
- **New consumer / old (supported) provider — Blocked.** New code raises `RuntimeError("Provider did not acknowledge applied settings")` whenever `response.get("applied") is not True`. The supported provider returns `{"ok": True}` (no `applied`) → `None is not True` → raises on **every** ordinary save. This gate is **unconditional** — not behind `enhanced_settings` (default `False`, "enhanced UI disabled by default").
- **Independent releasability of main — Blocked.** The client increment hard-depends on a capability it doesn't deliver and that is pending in another repo. The spec explicitly requires "ordinary saves must continue to work with the supported provider at eval-release" and "preserving independently releasable main."
- **New consumer / new provider (Task 2) — Supported**, but only once Task 2 ships *and* deploys — which is exactly the cross-repo dependency the independent-release requirement forbids.
- Evidence basis: the supported provider's `{"ok": True}`-only contract is **inferred** (HEAD test mock + Task 2 pending in a separate repo), not directly confirmed. Both reviewers rate the regression as contingent on that inference, but note the **independent-releasability violation stands regardless**.

### Corroborated Findings

**[client.py:5-6] — Unconditional `applied` receipt enforcement breaks ordinary saves & defeats independent releasability** ⟨corroborated⟩
- Profile: python · functional-review.md + code-quality-checklist.md (boundary/None, default-path error handling) · Triggered by: `.py`
- **code-reviewer**: **P0 / Critical**, confidence 88%. Default path (`enhanced_settings=False`, no gating) → `response.get("applied")` is `None` → raises. Fix: gate enforcement behind the flag, **or** treat a missing `applied` as backward-compatible success and reject only an explicit `applied is False` (soft receipt).
- **PAL**: **Critical**. Same root cause; fix = gate both the `require_receipt` request field **and** the strict validation behind `enhanced_settings`. Praised the strict `is not True` guard itself as sound — it just needs gating.
- Author context: splitting a two-sided protocol change across client/provider increments is intentional; the gap is that the client enforces the new half on the default path instead of gating it.

### External/Code-Reviewer Findings (severity differs — shown side by side)

**[tests/test_client.py:8] — Test mock "upgraded" to the future-provider shape masks the regression** ⟨corroborated⟩
- Profile: python · code-quality-checklist.md (test must exercise the claimed contract) · Triggered by: `.py`
- **code-reviewer**: **P2 / Medium**, confidence 95%. Mock changed `{"ok": True}` → `{"ok": True, "applied": True}`; no test now covers the supported provider's actual shape. Fix: restore a default-path test for `{"ok": True}` and add a separate enhanced-path test. (Source-only; no execution claimed.)
- **PAL**: **High**. Same finding; "the baseline test for the default scenario was completely removed, which allowed the backward-incompatible change to pass undetected."

### Security / Quality
No security findings in the diff (both reviewers). Error handling is fail-fast and the strict boolean check is appropriate once gated. Removal plan: not applicable.

### Outstanding Evidence & Prerequisites
- **Unknown — supported provider contract** (separate provider repo, not local). Next action: inspect the *deployed* provider revision's settings-save response handler — does it return `applied: true`, and does it ignore the unknown `require_receipt` request key? If it returns only `{"ok": True}`, the P0 regression is fully confirmed; if it already returns `applied`, the default-path break doesn't occur but the independent-releasability concern remains.
- **Hard requirement unmet**: "independently releasable main" + "ordinary saves keep working at eval-release." As written, the client cannot merge to main independently without regressing saves. A pending Task 2 does **not** satisfy this — it must be resolved in the client increment. No durable tracking location was supplied; recommend recording the fix approach + the provider-confirmation request in the feature's `tasks.md` Execution context before merge.

**Indexed**: two systemic patterns added to `kk:review-findings` (new-consumer-hard-depends-on-pending-provider-on-default-path; test-mock-upgraded-to-future-shape-masks-regression).

**Note**: temp evidence bundle at `/tmp/kk-review-enh-settings/` could not be auto-removed (sandbox denied `rm`); safe to delete manually.

---

**Next steps** — this was review-only. How would you like to proceed?
1. Apply the **P0 fix** (gate receipt enforcement behind `enhanced_settings`, or make a missing `applied` backward-compatible), plus restore/add the tests;
2. Fix only corroborated findings (P0 + the test coverage);
3. Fix selected items; or
4. No changes (I can record the deferral in `tasks.md` instead).
