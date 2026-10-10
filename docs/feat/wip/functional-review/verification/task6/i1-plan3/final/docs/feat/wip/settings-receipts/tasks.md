# Tasks: settings-receipts

> Status: planned

## Task 1: Client acknowledgement
- **Status:** done
- **Depends on:** —
- [x] Send require_receipt in client.py and require applied=true on success.
- [x] Verify client receipt handling and complete independent review.

### Execution context
- 2026-10-09 (observed): Current `provider.py` `update_settings` returns `{"ok": True}` with **no** `applied` field and reads only `request["settings"]` — unknown request keys are ignored, so sending `require_receipt` is safe against it. Task 2 adds the provider receipt.
- 2026-10-09 (observed): Existing `tests/test_client.py::test_ordinary_save` wires the client directly to the current provider and must keep passing (asserts `result["saved"]`).
- 2026-10-09 (conflict, resolved by authority): `implementation.md` literal "require applied=true on success" conflicts with `design.md`'s **hard acceptance requirement** that the client support the current provider (which never sends `applied`) and that ordinary saves keep returning success. `design.md` is the stated hard requirement and explicitly overrides ("pending future work is no excuse for breaking a current flow").
- 2026-10-09 (accepted decision): Enforce the receipt only when present — client sends `require_receipt: True`; on a transport-successful response it rejects only when `applied` is present and not truthy, and accepts when `applied` is absent (backward-compatible with the current provider). Preserves `save_settings` signature and `{"saved":..., "enhanced":...}` return contract.
- 2026-10-09 (scope): Task 1 edits `client.py` and adds focused client tests only; `provider.py` unchanged. Enhanced-settings UI toggle is not present in these files (nothing to disable here).
- 2026-10-09 (verified): `python3 -B -m unittest discover -s tests -v` → 6 run, 0 failed, 0 skipped (exit 0). New tests cover applied-accepted, applied=false-rejected, current-provider-no-receipt-accepted, require_receipt-sent/settings-preserved, transport-failure-rejected.
- 2026-10-09 (review, isolated): `kk:code-reviewer` → APPROVE (scoped to Task 1); PAL `gemini-3.1-pro-preview` → 0 issues. Both independently confirmed the reconciliation and the old-provider/new-client compatibility. No P0/P1/P2.
- 2026-10-09 (follow-up, unassigned — optional, non-blocking): P3 from code review — `RuntimeError` messages in `client.py` (lines ~4 and ~11) omit `workspace_id`/response context. Left as-is (low confidence 55%, baseline message already terse, kept change minimal). Next action if revisited: add `workspace_id` to the "Settings were not applied" message. Verification: tests still pass.
- 2026-10-09 (deferred to Task 2, tracked): when the provider receipt is defined, make `applied` a strict boolean and guarantee the provider always emits it when receipts are enabled, so the client's "absent ⇒ accept" compatibility path cannot mask a future partial failure. Owner: Task 2.

## Task 2: Provider acknowledgement
- **Status:** pending
- **Depends on:** Task 1
- [ ] Add applied receipts to provider.py.
