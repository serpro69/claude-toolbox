Implementation, verification, and isolated review are complete. The temp review patch at `/tmp/kk-review-code-settings-receipts.patch` is a harmless throwaway (Bash is disabled in this session, so I can't delete it; it carries no sensitive data).

## Task 1 — Client acknowledgement: done ✅

**What changed**
- `client.py:save_settings` now sends `{"settings": values, "require_receipt": True}` and, on a transport-successful response, treats a **present** `applied` receipt as confirmation only when it is exactly boolean `True` (otherwise raises). An **absent** `applied` key falls back to the existing `ok`-based success.
- `tests/test_client.py`: added 5 focused cases (require_receipt sent, applied=true success, present-non-true rejected, applied=false rejected, transport failure rejected, current-provider/`enhanced_settings=false` success via the real provider).

**The key design call.** `implementation.md`/`tasks.md` say "require applied=true on success," but `design.md` carries a **hard acceptance requirement**: the client is released independently and must keep working against the *current* `provider.py` (which returns `{"ok": True}` with **no `applied` field`), with ordinary saves still succeeding. A literal "reject unless applied is true" would reject every save against today's provider and make Task 1 un-shippable alone. I resolved this via receipt negotiation (absent receipt → legacy success; present receipt must be `True`), which honors both documents — the hard acceptance requirement governs.

**Verification** — `python3 -B -m unittest discover -s tests`: **7 passed, 0 failed, 0 skipped** (Python 3.14.8; project floor 3.9+).

### Review Summary (Isolated Mode)
- **Reviewers**: `kk:code-reviewer` (independent sub-agent) + PAL `gemini-3.1-pro-preview` (14 files embedded — source receipt verified). Both ran with zero authorship context.
- **Overall**: **APPROVE**, scoped to Task 1 code. Both independently confirmed design.md governs and the reconciliation is correct, not a convenient weakening.
- **Compatibility**: new-consumer/current-provider → **Supported** (traced against `provider.py`; exercised by a test using the real provider).
- **Findings**: no P0/P1/P2.
  - **P3 (corroborated, resolved)** `client.py:9` — non-strict boolean on a *present* receipt. Tightened to `response["applied"] is not True`; added `test_present_non_true_receipt_is_rejected`.
  - **P3 (doc consistency, follow-up)** `implementation.md:3` / `tasks.md` Task 1 wording literally contradicts design.md's hard requirement — a maintenance trap. The code is correct; **I did not rewrite the requirement docs** (that needs your sign-off). Proposed wording and a Task-2 note (provider must send bool `true` and omit the key for legacy/unknown, not `None`) are recorded durably in the Task 1 **Execution context**.
- **Indexing**: no systemic P0/P1 findings to index; capy knowledge base is empty/cold-start.

**Release vs. code completion**: Task 1 code is complete and verified. End-to-end receipt enforcement is **not** real until **Task 2 (pending)** adds the provider receipt; per implementation.md the enhanced-settings UI stays disabled until both land. That is the accepted, documented tradeoff — not an open defect.

You asked for Task 1 only, so I've stopped here. Two optional next steps, if you want them:
1. Authorize the P3 doc-consistency wording fix to `implementation.md`/`tasks.md`.
2. Proceed to **Task 2 (Provider acknowledgement)**.
