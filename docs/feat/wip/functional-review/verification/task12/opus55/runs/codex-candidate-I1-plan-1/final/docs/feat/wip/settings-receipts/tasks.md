# Tasks: settings-receipts

> Status: planned

## Task 1: Client acknowledgement
- **Status:** in-progress
- **Depends on:** —
- [ ] Send require_receipt in client.py and require applied=true on success.
- [ ] Verify client receipt handling and complete independent review.

### Execution context

- 2026-10-11 — **Observed:** Investigation began from clean revision
  `5692f67322e81b0f532ec167a7bee727dfd6fed2`. Scope is task 1 only;
  provider receipts remain task 2. No runtime or test files have been changed.
- 2026-10-11 — **Unresolved:** This task and `implementation.md` require
  unconditional rejection of successful responses without `applied: true`.
  `design.md` separately makes compatibility with the current provider a hard
  acceptance requirement, including ordinary saves with `enhanced_settings=False`.
  Neither document supplies an accepted exception or resolves the conflict.
- 2026-10-11 — **Observed boundary case:** `provider.py:update_settings` applies
  values and returns only `{"ok": True}`, even when the request includes
  `require_receipt: True`. `client.py:save_settings` currently returns
  `{"saved": True, "enhanced": False}` for that ordinary save. An unconditional
  receipt check would reject after the write, violating independent delivery.
  Disabling the enhanced UI does not change this ordinary-save response.
- 2026-10-11 — **Proposed, not accepted:** (A) Preserve independent delivery by
  allowing legacy success for ordinary saves and requiring receipts only when
  `enhanced_settings=True`; this changes the unconditional rejection requirement
  because an ordinary save without a receipt would still succeed. (B) Keep
  unconditional receipt rejection and coordinate release with task 2; this changes
  the independent-delivery guarantee because the current provider remains
  incompatible. Neither alternative satisfies both original requirements.
- 2026-10-11 — **Verified baseline:** On Python 3.10.12, the README command
  `python3 -B -m unittest discover -s tests` passed (1 test, exit 0). A read-only
  in-memory probe confirmed both the ordinary-save result and the missing receipt
  after a write with `require_receipt: True`. These results describe the unchanged
  local revision; no deployed revision or Python 3.9 run was verified. Required
  implement/test Python guidance was loaded; scoped Capy searches were empty.
- 2026-10-11 — **Pending decision:** Owner: user. Choose a requirement change or
  another resolution; the clarification was requested in this session. Dependent
  implementation is paused under `kk:implement` Step 2.3 because the requirements
  conflict. Next action: record explicit authorization and its rationale before
  editing dependent code. Verification condition: an agreed receipt contract and
  delivery policy that give a consistent outcome for the boundary case above.
- 2026-10-11 — **Pending execution/review:** Owner: implementing agent, after the
  decision. Implement the authorized contract, verify receipt handling and the
  agreed compatibility cases, and complete isolated code review before marking
  task 1 done. Baseline tests alone do not establish task completion or release
  readiness; no independent implementation review has occurred.

## Task 2: Provider acknowledgement
- **Status:** pending
- **Depends on:** Task 1
- [ ] Add applied receipts to provider.py.
