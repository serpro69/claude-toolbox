# Tasks: settings-receipts

> Status: planned

## Task 1: Client acknowledgement
- **Status:** in-progress
- **Depends on:** —
- [ ] Send require_receipt in client.py and require applied=true on success.
- [ ] Verify client receipt handling and complete independent review.

### Execution context
- 2026-10-09 (observed): Profile detection → `python` (ext `.py` on `client.py`,
  `tests/test_client.py`). Loaded idioms/typing/errors-and-resources; `async.md`
  skipped (no async in target, none planned). No new dependencies.
- 2026-10-09 (observed): Current provider `provider.py` returns `{"ok": True}` with
  **no `applied` field** (receipt is Task 2). Existing test `test_ordinary_save`
  exercises the ordinary save path against this current provider.
- 2026-10-09 (unresolved → conflict): `implementation.md`/`tasks.md` say "reject a
  successful transport response unless applied is true." Taken unconditionally this
  breaks `design.md`'s **hard acceptance requirement**: "Every merged client
  increment must support the current provider in provider.py ... Ordinary saves must
  keep returning success after values are applied. The provider receipt is a later
  task." An unconditional reject makes ordinary saves fail against the current
  (no-receipt) provider. Design is authoritative; per skill guidance "pending future
  work is no excuse for breaking a current flow."
- 2026-10-09 (proposed): Reconcile by sending `require_receipt: true` and enforcing
  the receipt only when present — reject when `applied` is present and not true;
  when `applied` is absent (current provider), preserve the existing `ok`-based
  success. Satisfies send+enforce intent AND the independent-delivery guarantee.
  Awaiting user confirmation before editing `client.py`.

## Task 2: Provider acknowledgement
- **Status:** pending
- **Depends on:** Task 1
- [ ] Add applied receipts to provider.py.
