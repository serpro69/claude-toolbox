Both reviewers complete, findings indexed. Here's the consolidated report.

## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent) · pal codereview (`gemini-3.1-pro-preview`)
**Files reviewed**: 2 files, ~5 lines changed (`client.py`, `tests/test_client.py`)
**Scope**: Task 1 (Client receipt handling, _done_, in scope). Task 2 (Provider receipts, _pending_, separate repo) treated as an intentional gap.
**Assessment**: REQUEST_CHANGES — both reviewers independently flagged the same blocker.

---

### Corroborated Findings (both reviewers — highest signal)

**1. `client.py:2,5` — Unconditional receipt enforcement breaks ordinary saves and defeats independent releasability** ⟨corroborated⟩
- Profile: python · cross-cuts security (data-integrity) + design-intent · Triggered by: content — `.py` extension
- **code-reviewer: P0 (85%)** · **pal: HIGH**
- The client now *always* sends `"require_receipt": True` and hard-fails when `response.get("applied") is not True`. The enforcement is unconditional — not gated on `enhanced_settings`, and not tolerant of a provider predating the receipt protocol. Since Task 2 (provider receipts) ships separately and isn't live yet, the eval-release provider returns no `applied` key → `None is not True` is truthy → **every ordinary save raises `RuntimeError("Provider did not acknowledge applied settings")`**. This forces lockstep client+provider deployment, directly violating design.md's *"ordinary saves must continue to work with the supported provider at eval-release"* and *"preserving independently releasable main."* This is an in-scope broken-contract finding (the client code itself encodes the hard requirement), **not** a report of missing provider work.
- Both reviewers also note the **`enhanced_settings` flag is near-inert** — threaded through only to the return payload (`"enhanced": enhanced_settings`), not used to gate the new behavior, despite the design stating the enhanced UI is "disabled by default." (pal scored this as a separate Medium; it's the natural fix site for the P0.)
- **Suggested fix (both converge):** gate `require_receipt` *and* the `applied` assertion behind `enhanced_settings`; and/or distinguish `"applied" not in response` (legacy provider → tolerate) from `response.get("applied") is False` (provider actively reported not-applied → reject).

**2. `tests/test_client.py:7-10` — New failure branches are untested; the test only patched the existing happy path** ⟨corroborated⟩
- Profile: python · Checklist: code-quality-checklist.md · Triggered by: content — `.py` extension
- **code-reviewer: P2 (95%)** · **pal: MEDIUM**
- The diff adds two raise paths but the sole test was edited to add `"applied": True` so the one happy-path assertion keeps passing. No coverage for: provider omits `applied` (the legacy/eval-release case that regresses per Finding 1), `applied: False`, or `ok: False`.
- **Suggested fix:** add tests for missing-`applied` (backward-compat), `applied: False` (raises), and `ok: False` (raises). These also pin down the Finding 1 decision.

---

### Code Reviewer Findings (single-reviewer)

**3. `client.py:3,5` — Generic `RuntimeError` for a protocol/acknowledgement failure**
- Profile: python · Checklist: code-quality-checklist.md · Triggered by: content — `.py` extension
- Severity: **P3 (60%)**
- Both failure modes raise bare `RuntimeError`, forcing callers to string-match to tell "save rejected" from "not acknowledged" — relevant because the ack path may warrant a retry while a hard rejection may not. Pre-existing pattern for the `ok` check; low priority. Suggested: a dedicated exception type (e.g. `SettingsNotAcknowledgedError`) if callers need to branch.

---

### Author-Sourced Notes (surfaced during annotation — weight accordingly)

- **Retry idempotency** ⟨author-sourced⟩: if a caller retries after the new `RuntimeError` and the provider *had* persisted the settings, the retry could re-apply/duplicate the write. Can't assess without provider semantics + caller retry logic — flagged, not scored.
- **`send` return contract** ⟨author-sourced⟩: `response.get(...)` assumes `send` returns a dict; a `None`/non-dict on transport failure raises `AttributeError`. Pre-existing (the `ok` check already assumes it), not introduced by this diff — not scored.

**Indexed:** Finding 1 recorded as `kk:review-findings` (lockstep-deploy / unconditional-enforcement anti-pattern) for recurrence detection in future reviews.

---

## Next Steps

I found **3 scored issues** (corroborated: 2 — one P0/HIGH, one P2/MEDIUM; code-reviewer only: 1 P3) plus 2 unscored author notes.

Actionable items I recommend fixing:

1. **P0 (corroborated)** — Gate the receipt enforcement behind `enhanced_settings` and tolerate `applied`-absent (legacy provider), rejecting only explicit `applied: False`. Restores backward compatibility / independent releasability.
2. **P2 (corroborated)** — Add the three missing test cases (missing `applied`, `applied: False`, `ok: False`), which also lock in the fix above.
3. **P3 (code-reviewer)** — Optional: dedicated exception type for the acknowledgement failure.

Items I'd keep as-is:
- `send` non-dict / `AttributeError`: pre-existing, not introduced here — out of scope for this diff.
- Retry idempotency: can't be resolved on the client alone; revisit alongside Task 2's provider semantics.

**How would you like to proceed?**

1. **Fix all** — implement 1, 2, and 3
2. **Fix corroborated + high severity** — address the P0 and the P2 test gap
3. **Fix specific items** — tell me which
4. **No changes** — review complete

I won't change anything until you choose.
