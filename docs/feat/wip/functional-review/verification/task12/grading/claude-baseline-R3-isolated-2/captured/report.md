Indexed. Here is the review report.

---

## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent) ✅ · ~~pal codereview~~ ❌ **unavailable**
**Files reviewed**: 2 files, ~18 lines (`client.py`, `tests/test_client.py`)
**Profile**: python · **Scope**: mid-implementation (Task 1 `done` in scope; Task 2 `pending`/separate repo out of scope)

> ⚠️ **Degraded run — two environmental limitations:**
> 1. **`pal` MCP server failed to connect** (`CONNECTION_CLOSED`). The external second opinion could not run, so there are **no corroborated (two-model) findings** — everything below is single-reviewer signal.
> 2. **Bash/`git` is denied** in this session, so no `git diff` could be captured. The files are tiny and were reviewed in full from their current staged contents; the reviewer also confirmed it could not check out the `eval-release` provider snapshot to byte-verify the provider's response shape.

---

### Code Reviewer Findings

**P0 — Critical · [client.py:2,5-6]** Hard receipt enforcement breaks ordinary saves against the deployed provider
- Profile: python · Checklist: code-quality-checklist.md
- Triggered by: content — `.py` extension
- Confidence: 80%
- The client unconditionally sends `require_receipt: True` and raises `RuntimeError("Provider did not acknowledge applied settings")` whenever `response.get("applied") is not True`. The `applied` receipt is a **new** protocol element; the provider that emits it is **Task 2 — pending, separate repo, not deployed**. The supported `eval-release` provider returns no `applied`, so `response.get("applied")` is `None`, `None is not True` is `True`, and **every ordinary save against the currently deployed provider raises**. This violates two stated design constraints: ordinary saves must keep working with the supported provider, and client/provider must stay independently releasable. It is an **in-scope client bug** (the client's own contract is incompatible with today's provider), not an out-of-scope missing-provider gap.
- Suggested fix: only enforce the receipt when the field is actually present (`if "applied" in response and response["applied"] is not True: ...`), and/or gate the whole receipt requirement behind `enhanced_settings` (disabled by default per design).

**P2 — Medium · [tests/test_client.py:5-10]** Tests cover only the happy path; no legacy-provider / error coverage
- Profile: python · Checklist: code-quality-checklist.md
- Confidence: 95%
- The only test stubs `send` → `{"ok": True, "applied": True}`, i.e. the not-yet-deployed receipt-capable provider. Nothing covers a legacy provider returning `{"ok": True}` without `applied` (the exact compatibility scenario the design mandates), `ok: False`, or `enhanced_settings=True`. That missing test is *why* the P0 regression slips through.
- Suggested fix: add a test asserting a legacy `{"ok": True}` response still succeeds (post-fix), plus `ok: False` raising and an `enhanced_settings=True` case.

**P3 — Low · [client.py:1,7]** `enhanced_settings` gates no behavior — pure pass-through
- Profile: python · Checklist: solid-checklist.md
- Confidence: 70%
- The parameter is accepted and echoed into `{"enhanced": enhanced_settings}` but controls nothing — notably not `require_receipt`, which is always `True`. Given the design says the enhanced UI is disabled by default, you'd expect the new receipt protocol to be coupled to this flag. Resolving the P0 by gating on the flag would also resolve this.

---

### Author-Sourced Findings

**P3 — Low · [client.py:3,5] ⟨author-sourced⟩** No guard if `send` returns `None`
- Profile: generic · Checklist: —
- If the transport `send` callable ever returns `None`, `response.get(...)` raises `AttributeError` rather than a meaningful error. The reviewer flagged this under "areas not covered"; surfacing it as a minor robustness note since the `send` contract isn't pinned down in this increment. Low priority unless `send` is known to return `None` on transport failure.

---

## Next Steps

I found **4 issues** (corroborated: 0 — pal unavailable; code-reviewer: 3; author-sourced: 1).

The actionable items I recommend fixing:
1. **P0 (code-reviewer)** — Make receipt handling backward-compatible: only enforce `applied` when the provider actually returns it, and/or gate it behind `enhanced_settings`. This is a merge blocker — it breaks ordinary saves against the deployed provider.
2. **P2 (code-reviewer)** — Add the missing legacy-provider / error-path / `enhanced_settings=True` tests (the legacy-provider test is what would have caught the P0).
3. **P3 (code-reviewer)** — Couple `require_receipt` to `enhanced_settings` (likely folds into the P0 fix).
4. **P3 (author-sourced)** — Optionally guard against a `None` response from `send`.

Items I'd keep as-is:
- **Task 2 / provider receipts absence** — correctly out of scope (pending, separate repo); not a finding.
- **Removal plan** — nothing to retire; `client.py` is minimal with no dead code.

**Caveats to weigh:** The P0 rests on the `eval-release` provider not emitting `applied`, which the design/implementation/README state consistently but which I could **not byte-verify** (no git access to the tagged provider snapshot). And there was **no second (pal) reviewer** to corroborate. If you want more rigor before acting, reconnecting `pal` and enabling Bash would let me run the full isolated two-model pass with a real diff.

**How would you like to proceed?**
1. **Fix all** — implement all suggested fixes
2. **Fix high severity** — address the P0 (+ its P2 test) only
3. **Fix specific items** — tell me which
4. **No changes** — review complete

I will not implement anything until you confirm.

---

**Outputs verified:** ✅ Report presented · ✅ P0 systemic pattern indexed as `kk:review-findings` · ⏳ Awaiting your next-steps decision.
