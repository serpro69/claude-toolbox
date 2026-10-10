Cold-start KB (empty) — proceeding on standard guidance; no prior findings to correlate.

I have everything needed. Here's the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (`preview.py` +2 new, `routes.py` +4)
**Overall assessment**: **APPROVE** (scoped to the Task 1 code increment)
**Intent and scope**: Requirement source — `tasks.md` (Task 1 "Prepare preview module", in-progress) + `README.md` (acceptance contract). Current request — review staged Task 1. Selected diff — **staged changes** (no unstaged changes exist); candidate = git index.
**Baselines**: Review base = `HEAD` (f1a16b5 "Review base"); candidate = staged index. No separate deployed baseline — README states no deployment inventory is maintained.

**Task scope** (mid-implementation): Task 1 **in scope**; Task 2 ("Implement `render_preview` and enabled-path tests before changing the build setting") **pending — out of scope**, its gaps are expected and not flagged.

## Behavior and Compatibility

The contract (README) is: GET `/settings` response and existing routing behavior are preserved, the checked-in build setting is fixed at `False`, and the increment must be independently compatible while Task 2 is pending.

Traced behavior with the checked-in `EXPORT_PREVIEW_ENABLED = False`:

| Contract / source | Operation | Expected | Candidate result | Evidence |
|---|---|---|---|---|
| README: `/settings` is the acceptance contract | `get("/settings")` | `(200, {"theme":"light"})` | identical | `test_current_settings` PASS |
| README: routing behavior preserved | `get("/unknown")` | `(404, None)` | `(404, None)` | `test_unknown_route` PASS |
| Task 1: preview disabled in checked-in build | `get("/export-preview")` | `(404, None)` | `(404, None)` | `test_preview_route` PASS |

Key correctness point: the guard `if EXPORT_PREVIEW_ENABLED and path == "/export-preview":` short-circuits on the `False` flag, so `render_preview()` — which raises `NotImplementedError` — is **never evaluated** in the checked-in build. The scaffold cannot leak into the disabled path. Ran `python3 -B -m unittest discover -s tests` → **3/3 OK**.

- **Compatibility — existing-flow preservation**: **Supported** (base = HEAD). `/settings` and the 404 fallthrough are byte-identical in behavior; the new imports (`config`, `preview`) are plain module-level defs/constants and introduce no import-time failure.
- **Independent releasability**: **Supported**. Flag is a fixed source constant (not request/env/external-config supplied, per README), so the increment ships safely with preview inert.

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low

- **[routes.py:1]** Flag is imported by value, which will make Task 2's enabled-path tests patch the wrong name
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `from config import EXPORT_PREVIEW_ENABLED`
  - `from config import EXPORT_PREVIEW_ENABLED` binds a snapshot of the boolean into the `routes` namespace. Task 2's "enabled-path tests" that attempt `monkeypatch`/`patch` on `config.EXPORT_PREVIEW_ENABLED` will **not** affect routing — they must patch `routes.EXPORT_PREVIEW_ENABLED` instead. No impact on the Task 1 disabled build; purely a forward-looking testability nuance.
  - Confidence: 80% — standard Python import-binding semantics, verified against the module; it is idiomatic and not a defect in the current increment, hence P3 only.
  - Suggested fix (optional, defer to Task 2): `import config` and reference `config.EXPORT_PREVIEW_ENABLED` at call time, so tests can toggle the flag on the single source of truth.

## Areas Not Covered / Residual Notes

- **Enabled path (`flag=True`)** is Task 2 scope and intentionally not exercised; `render_preview()` raising `NotImplementedError` is expected pending work. `tasks.md` already correctly orders "implement `render_preview` and enabled-path tests **before** changing the build setting," so the scaffold ordering is sound — not a finding.
- No `capy` prior findings available (knowledge base empty / cold start).

**Index:** No systemic P0/P1 findings — **nothing to index** as `kk:review-findings`.

---

## Next Steps

I found 1 issue (P0: 0, P1: 0, P2: 0, P3: 1).

Actionable items I recommend:
1. P3 (optional, can defer to Task 2) — in `routes.py`, reference the flag as `config.EXPORT_PREVIEW_ENABLED` rather than importing it by value, so Task 2's enabled-path tests can toggle it.

Items I recommend keeping as is:
- The `NotImplementedError` scaffold in `preview.py`: correct — unreachable while disabled and explicitly Task 2's responsibility.
- The `EXPORT_PREVIEW_ENABLED and path == ...` guard: correct — short-circuits cleanly, preserves `/settings` and 404 behavior.

**How would you like to proceed?**

1. **Fix all** — apply the P3 improvement
2. **Fix P0/P1 only** — nothing to do (none found)
3. **Fix specific items** — tell me which
4. **No changes** — review complete

I recommend **option 4** (the increment is correct and ships safely) or **option 1** if you want the testability tweak in place before Task 2.
