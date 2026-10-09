# Tasks: settings-receipts

> Status: planned

## Task 1: Client acknowledgement
- **Status:** done
- **Depends on:** —
- [x] Send require_receipt in client.py and require applied=true on success.
- [x] Verify client receipt handling and complete independent review.

### Execution context
- 2026-10-09 (observed): `client.py:save_settings` currently sends `{"settings": values}`
  and returns success solely on `response.get("ok")`. `provider.py:update_settings`
  returns `{"ok": True}` with **no `applied` field** and ignores unknown request keys
  (it only reads `request["settings"]`). Task 2 (later) adds the provider receipt.
- 2026-10-09 (accepted, authority: design.md): Independent delivery is a **hard
  acceptance requirement** — the Task-1 client must keep working against the *current*
  provider (no `applied` field), and ordinary saves must keep returning success after
  values are applied, including when `enhanced_settings` is false.
- 2026-10-09 (inferred → resolved): A literal reading of implementation.md/tasks.md
  ("reject unless applied is true") would hard-reject every save against the current
  provider, breaking the hard acceptance requirement and making Task 1 un-shippable
  alone. Resolved by receipt negotiation that honors both documents:
  client sends `require_receipt: true`; if the response carries an `applied` receipt
  it must be truthy (else raise), but an **absent** `applied` key falls back to the
  legacy `ok`-based success path. Presence is checked with `"applied" in response`
  (per idioms.md: distinguish missing from falsey), so an explicit `applied: false`
  is rejected while a legacy provider's omission is accepted.
- 2026-10-09 (verified): `python3 -B -m unittest discover -s tests` → 7 passed, 0 failed,
  0 skipped (Python 3.14.8; project floor is 3.9+, newer-version-only behavior not used).
  Covers: ordinary save via the real current provider, require_receipt sent, applied=true
  success, present-but-not-true receipt rejected, applied=false rejected, transport
  (`ok` false) rejected, and `enhanced_settings=false`.
- 2026-10-09 (review, isolated): `/kk:review-code:isolated` — independent `kk:code-reviewer`
  and PAL (gemini-3.1-pro-preview, 14 files embedded) both **APPROVE** (scoped to Task 1
  code) and independently concur the design.md hard requirement governs and the receipt
  negotiation is the correct reconciliation. No P0/P1/P2. One corroborated P3 at
  `client.py:9` (non-strict boolean handling of a *present* receipt) — **resolved**:
  tightened to `response["applied"] is not True` so only an explicit boolean `True`
  confirms a present receipt; absent key still falls back to legacy success. Added
  `test_present_non_true_receipt_is_rejected`. No systemic P0/P1 findings to index.
- 2026-10-09 (follow-up, proposed — unassigned; needs user authorization before editing
  requirement docs): implementation.md:3 and the tasks.md Task 1 checkbox state "require
  applied=true on success" unconditionally; read literally this contradicts design.md's
  hard independent-delivery requirement. The code is correct, but the unqualified wording
  is a maintenance trap. Proposed reconciliation wording: "require `applied=true` only
  when the response carries an `applied` receipt; a response omitting `applied` (current
  provider) remains a success." Not applied here — a requirement-doc change needs explicit
  user sign-off. Verification condition: both docs state the negotiated contract and no
  longer read as an unconditional reject.
- 2026-10-09 (note for Task 2): the client trusts a present `applied` only when it is
  boolean `True`. Task 2's provider must send `applied: true` (bool) on success and
  **omit** the key for legacy/unknown rather than sending `None`, or the client will
  reject it.

## Task 2: Provider acknowledgement
- **Status:** pending
- **Depends on:** Task 1
- [ ] Add applied receipts to provider.py.
