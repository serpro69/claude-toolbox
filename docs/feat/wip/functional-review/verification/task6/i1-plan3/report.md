Task 1 is complete. (Temp review files live only under `/tmp` — harmless; Bash cleanup is blocked in this session, nothing left in the repo.)

## Task 1 — Client acknowledgement: done ✅

**What changed**
- `client.py`: `save_settings` sends `require_receipt: True` and rejects a transport-successful response only when `applied` is **present-and-falsey**; accepts a receipt-less `{"ok": True}` from the current provider. Signature and `{"saved", "enhanced"}` return contract unchanged.
- `tests/test_client.py`: +5 focused tests covering every branch.
- `docs/feat/wip/settings-receipts/tasks.md`: Task 1 → `done`, checkboxes ticked, Execution context records the conflict, resolution, verification, and review.

**Key decision** — I surfaced and resolved a genuine conflict: `implementation.md`'s literal "require `applied`=true" vs. `design.md`'s **hard independent-delivery requirement** (the client must keep working against the current provider, which sends no `applied`). Resolved by design authority — enforce the receipt only when present. Both independent reviewers concurred this is the only reading that satisfies both.

**Verification**: `python3 -B -m unittest discover -s tests -v` → **6 run, 0 failed, 0 skipped**.

**Review (isolated)**: `kk:code-reviewer` → APPROVE; PAL `gemini-3.1-pro-preview` → 0 issues. No P0/P1/P2. One non-blocking P3 (terse error messages) left as a recorded optional follow-up.

**Completion vs. release**: Task 1 code is complete. The end-to-end receipt guarantee and the enhanced-settings UI remain gated on **Task 2** (provider applied receipts) — still `pending` and tracked. When Task 2 lands, confirm `applied` is a strict boolean always emitted when receipts are enabled (noted in the task's Execution context).

You asked for Task 1 only, so I'm stopping here. Say the word to proceed to Task 2.
