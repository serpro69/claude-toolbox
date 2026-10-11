# Tasks: settings-receipts

> Status: planned

## Task 1: Client acknowledgement
- **Status:** in-progress
- **Depends on:** —
- [ ] Send require_receipt in client.py and require applied=true on success.
- [ ] Verify client receipt handling and complete independent review.

### Execution context

- **2026-10-11 — observed:** Work is limited to Task 1. The starting worktree
  was clean at `5692f67322e81b0f532ec167a7bee727dfd6fed2`. No implementation
  or test files have been changed; Task 2 remains pending.
- **2026-10-11 — unresolved requirement conflict:** Task 1 above and
  `implementation.md` require rejecting every successful transport response
  unless `applied` is true. `design.md` separately requires every client
  increment to support the current provider, including ordinary saves with
  `enhanced_settings=False`. Neither requirement has an accepted exception.
- **2026-10-11 — observed boundary case:** `save_settings` in `client.py`
  always calls the provider, irrespective of `enhanced_settings`.
  `update_settings` in `provider.py` applies values and returns only
  `{"ok": True}`. A direct local probe with `require_receipt=True` stored
  `{"label": "blue"}` for workspace `w` and still returned `{"ok": True}`;
  `response.get("applied") is True` was false. Thus unconditional receipt
  enforcement would report failure after a successful ordinary save. Keeping
  the enhanced UI disabled does not avoid this client path.
- **2026-10-11 — proposals, not accepted decisions:** (A) Request receipts
  but require them only when `enhanced_settings=True`, preserving ordinary
  saves. This explicitly relaxes the unconditional rejection rule: with the
  flag false, `{"ok": True}` would be accepted without `applied`. (B) Implement
  provider receipts first, then enforce them in the client. This expands scope,
  reverses the task dependency, and requires provider availability before
  client activation; it changes the independent-delivery commitment rather
  than establishing compatibility with the original provider. No deployment
  baseline or rollout evidence is available.
- **2026-10-11 — verified baseline:** From the repository root,
  `python3 -B -m unittest discover -s tests` passed (1 test, 0 failures,
  exit 0) using `/usr/bin/python3` 3.10.12. The provider probe above also
  passed its assertions (exit 0). These results verify existing behavior,
  not receipt handling, deployment readiness, or the full Python 3.9+ matrix.
- **2026-10-11 — deferred:** Decision owner: user; implementation owner:
  implementing agent. Reason: the explicit requirements conflict. Next action:
  obtain and record the user's chosen requirement amendment, then implement
  within that scope. Verification condition: focused receipt tests and the
  ordinary-save compatibility case pass under the amended contract, followed
  by isolated code review. Receipt implementation, its tests, and independent
  review remain open; Task 1 is not complete.

## Task 2: Provider acknowledgement
- **Status:** pending
- **Depends on:** Task 1
- [ ] Add applied receipts to provider.py.
