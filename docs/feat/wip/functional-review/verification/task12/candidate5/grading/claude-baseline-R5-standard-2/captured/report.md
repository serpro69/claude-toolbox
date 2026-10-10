I now have the complete picture. Let me run the self-check before presenting.

**Context (Step 5–6):**
- `preview.py` (new): `render_preview()` is a stub that raises `NotImplementedError("Export preview is scheduled for Task 2")`.
- `routes.py`: wires a new `/export-preview` route, guarded by `EXPORT_PREVIEW_ENABLED`.
- `config.py`: `EXPORT_PREVIEW_ENABLED = False` — the flag is **off**.
- All imports resolve. No content-evaluable conditionals to resolve (python index has none).

Self-check findings: because the flag is `False`, `EXPORT_PREVIEW_ENABLED and path == "/export-preview"` short-circuits and `/export-preview` currently returns `404`. The stub is therefore **unreachable at runtime** — the `NotImplementedError` is intentional Task 1 scaffolding, not a bug. No P0/P1 survive. Capy KB is empty → "No findings to index."

---

## Code Review Summary

**Files reviewed**: 2 files (`preview.py` new, `routes.py` modified), 6 lines added
**Profile**: `python` (triggered by extension `.py`) — all 4 checklists applied (security, SOLID, code-quality, removal)
**Overall assessment**: **APPROVE** (with notes to carry into Task 2)

This is clean, minimal, correctly-scoped Task 1 scaffolding. The stub-behind-a-flag pattern is sound.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium

- **[config.py:1 / routes.py:9]** No safeguard against the flag being enabled before Task 2 lands
  - Profile: python · Checklist: code-quality-checklist.md (error handling / async-task boundaries) + security-checklist.md (runtime risks)
  - Triggered by: content — `.py` extension
  - The route is wired now but its handler intentionally raises. The only thing keeping `/export-preview` from returning a 500 is `EXPORT_PREVIEW_ENABLED = False`. There is no guard, test, or comment preventing someone from flipping that flag to `True` before `render_preview()` is implemented — doing so turns the endpoint into an unhandled `NotImplementedError`. `get()` has no try/except, so it propagates as a raw 500 (and, depending on the server, a stack trace).
  - Confidence: 70% — the behavior is certain; the severity is a judgment call. It is **not** a live bug (flag is off, endpoint returns 404 today), so this is a sequencing/footgun risk rather than a defect.
  - Suggested fix: add a test asserting `/export-preview` → `404` while the flag is off (locks in the staging contract), and/or a comment on the flag noting "do not enable until Task 2 implements `render_preview`." Optionally track flag-flip as a Task 2 acceptance gate.

### P3 - Low

- **[routes.py:9]** New endpoint has no auth/authorization guard
  - Profile: python · Checklist: security-checklist.md (AuthN/AuthZ — "new endpoints without auth guards")
  - Triggered by: content — `.py` extension
  - Confidence: 35% — flagged for completeness only. The existing `/settings` endpoint has no auth either and there is no auth framework anywhere in this codebase, so this almost certainly mirrors the intended (toy/minimal) design rather than a regression. Revisit in Task 2 if export-preview exposes sensitive data.

---

## Explicitly NOT flagged (verified correct)

- **`render_preview` raising `NotImplementedError`** — this is the *point* of Task 1 (stub for Task 2), not a defect, and not a removal candidate (it's planned, staged work). Correctly unreachable while the flag is off.
- **Imports** — `from config import EXPORT_PREVIEW_ENABLED`, `from preview import render_preview`, `from settings import current_settings` all resolve against the current tree. No import-time error.

## Additional Suggestions (non-blocking)

- `get()` has no error handling around handler dispatch — any exception from any handler becomes an unhandled 500. Generic and pre-existing, but worth a central try/except when the router grows.
- The `if path == …` chain is an OCP smell (adding a route edits `get()`), but at 3 branches a dispatch table would be premature. Note it, don't act on it yet.

**Index (Step 9):** No P0/P1 systemic findings → **nothing to index** as `kk:review-findings`.

---

## Next Steps

I found 2 notes worth carrying forward (P0: 0, P1: 0, P2: 1, P3: 1) — nothing blocks this Task 1 commit.

Actionable items I recommend:
1. **P2** — Add a test asserting `/export-preview` returns `404` while `EXPORT_PREVIEW_ENABLED` is off, and/or comment the flag to prevent premature enabling before Task 2.
2. **P3** — Decide auth posture for the endpoint as part of Task 2 (likely out of scope now).

Items I recommend keeping as-is:
- The `NotImplementedError` stub: intentional, correct staging for Task 2.
- No auth on the route: mirrors existing `/settings` behavior; no auth framework exists.

**How would you like to proceed?**

1. **Fix all** — I'll add the P2 guard/test and address the P3 note
2. **Fix P2 only** — Add the 404-while-off test + flag comment
3. **Fix specific items** — Tell me which
4. **No changes** — Review complete (this is a reasonable choice; nothing is blocking)
