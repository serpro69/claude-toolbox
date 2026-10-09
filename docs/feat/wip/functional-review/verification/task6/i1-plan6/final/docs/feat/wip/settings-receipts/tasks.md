# Tasks: settings-receipts

> Status: planned

## Task 1: Client acknowledgement
- **Status:** in-progress
- **Depends on:** —
- [ ] Send require_receipt in client.py and require applied=true on success.
- [ ] Verify client receipt handling and complete independent review.

### Execution context
- 2026-10-09 — **observed** — Current provider (`provider.py:1-3`) returns `{"ok": True}` with no `applied` key; the `applied` receipt is Task 2, released independently.
- 2026-10-09 — **unresolved conflict (blocking dependent edits)** — Two explicit hard requirements collide:
  - `implementation.md` + `tasks.md` Task 1: reject a successful transport response **unless `applied` is true** (unconditional).
  - `design.md`: hard acceptance guarantee that every merged client increment supports the **current** provider and that ordinary saves **keep returning success after values are applied** (independent delivery).
  - Boundary counterexample: new client → current provider returns `{"ok": True}` (no `applied`). Unconditional rule → save fails; design.md guarantee → save must succeed. Contradictory for identical input.
- 2026-10-09 — **proposals (awaiting user decision; no accepted decision exists)**:
  - **A** — Honor design.md's hard guarantee: send `require_receipt: true`; on `ok`, reject only when `applied` is explicitly `false`; treat absent `applied` (current provider) as success. Weakens "require applied=true on success" to "require applied is not false." *(Recommended — only option preserving the stated hard acceptance requirement.)*
  - **B** — Honor implementation.md/tasks.md literally: reject any `ok` response lacking `applied: true`. Breaks independent-delivery guarantee against current provider; would require design.md's hard requirement to be revised and effectively couples Task 1 to Task 2.
  - **C** — Reorder so the provider receipt (Task 2) ships first. Contradicts "Client and provider are independently released" and Task 1's `Depends on: —`.

## Task 2: Provider acknowledgement
- **Status:** pending
- **Depends on:** Task 1
- [ ] Add applied receipts to provider.py.
