All context gathered. Step 6 is a no-op (the Python profile declares no conditional entries). Capy KB is empty (cold start) — proceeding with standard guidance. Here's the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (`preview.py` new, `routes.py` modified)
**Overall assessment**: **APPROVE** (with minor suggestions)

**Context**: This is Task 1 scaffolding of the export-preview feature — a flag-gated route (`EXPORT_PREVIEW_ENABLED = False`) wired to a stub (`render_preview` raising `NotImplementedError`, deferred to Task 2). Reviewed against the active **python** profile checklists (triggered by `content: extension .py`): security, SOLID, code-quality, removal. The change is small, internally consistent, and the existing test correctly encodes the flag-off behavior. No correctness or security defects.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium

- **[tests/test_routes.py:13]** Enabled-flag path is untested
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The only new test, `test_preview_route`, exercises the route with `EXPORT_PREVIEW_ENABLED = False` (the default), asserting `(404, None)`. The actual new behavioral branch — `if EXPORT_PREVIEW_ENABLED and path == "/export-preview"` with the flag **on** — has no coverage. If Task 2 flips the flag, nothing in the suite verifies the wiring. A test that patches the flag to `True` and asserts `render_preview` is invoked (currently: raises `NotImplementedError`) would lock in the staging contract and catch regressions when Task 2 lands.
  - Confidence: 80% — the gap is real; severity is moderate because the enabled path is intentionally a stub for now.
  - Suggested fix: add `test_preview_route_enabled` that monkeypatches `routes.EXPORT_PREVIEW_ENABLED = True` and asserts `render_preview` is reached (e.g. `assertRaises(NotImplementedError)` today, updated in Task 2).

### P3 - Low

- **[routes.py:1]** Feature flag value is snapshotted at import time
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — extension `.py`
  - `from config import EXPORT_PREVIEW_ENABLED` binds the flag's *value* (`False`) into `routes.py` at import. A runtime change to `config.EXPORT_PREVIEW_ENABLED` would not be seen by `get()` — the dispatcher keeps the stale snapshot. This is fine if flags are only changed by editing `config.py` and restarting (the apparent model here), but if dynamic toggling is ever expected, use `import config` and read `config.EXPORT_PREVIEW_ENABLED` at call time.
  - Confidence: 70% — correct Python behavior; impact is currently nil since no runtime-toggle mechanism exists.
  - Suggested fix: if live toggling matters, switch to `import config` + `config.EXPORT_PREVIEW_ENABLED` in the branch; otherwise leave as-is and treat flag flips as restart-gated.

- **[routes.py:10]** Stub raises straight through the dispatcher when enabled
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — extension `.py`
  - `get()` has no error boundary, so enabling the flag before Task 2 completes turns `/export-preview` into an unhandled `NotImplementedError` (a 500-equivalent) rather than a graceful response. This is by design for staged work — flagging it only so the sequencing constraint is explicit: **Task 2 must land before the flag is flipped.** No change needed in Task 1.
  - Confidence: 90% that this is intentional staging, not a defect.
  - Suggested fix: none for Task 1; ensure Task 2 replaces the stub before any environment sets the flag `True`.

---

## Additional Suggestions

- No security concerns: the diff introduces no user-controlled input, injection sink, or deserialization. The new endpoint lacks auth, but so does every existing route (`/settings`) — it's consistent with the codebase, not a regression.
- `render_preview()` takes no arguments and the `NotImplementedError` message names the follow-up task — good, self-documenting stub.

---

## Step 9 — Index findings

No P0/P1 systemic findings. **No findings to index.**

---

## Next Steps

I found 3 issues (P0: 0, P1: 0, P2: 1, P3: 2).

The actionable items I recommend:
1. **P2** — Add a test for the flag-*enabled* path (`tests/test_routes.py`).
2. **P3** — Decide the flag model: import-time snapshot (current) vs. call-time read in `routes.py`.

Items I recommend keeping as-is:
- **P3 stub-raises-through-dispatcher**: correct, intentional staging — the whole point of Task 1 is a flag-gated stub. Just sequence Task 2 before flipping the flag.
- **Flag-off 404 test**: correct — it accurately documents current behavior.

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes
2. **Fix P2 only** — Add the enabled-path test
3. **Fix specific items** — Tell me which
4. **No changes** — Review complete

Please choose an option or provide specific instructions.
