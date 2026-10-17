Knowledge base is empty (cold-start — proceeding with standard guidance). I have everything needed. Here's the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (`preview.py` +2, `routes.py` +4)
**Overall assessment**: **APPROVE** (scoped to code; Task 1 increment)
**Intent and scope**: Task 1 "Prepare preview module" (status: in-progress) — add the preview module and a flag-guarded `/export-preview` route while preserving existing routing, with the feature disabled in the checked-in build. Requirement source: `tasks.md` + `README.md`. Selected diff: **staged** changes (user staged Task 1; no unstaged changes exist).
**Baselines**: Review base = `HEAD` (`f1a16b5 Review base`); candidate = staged index. No deployment/release baseline — `README.md` states no deployment inventory is maintained; `EXPORT_PREVIEW_ENABLED` is a fixed checked-in constant, not request/env/config-supplied.

**Task scope** (shape 2, mid-implementation):
- *In scope* — Task 1: preview module + guarded route, existing routes preserved with preview disabled.
- *Out of scope (pending, not flagged as missing)* — Task 2: implement `render_preview` and its enabled-path tests before flipping the build setting.

## Behavior and Compatibility

Traced `routes.get` for all three paths at the candidate revision:

| Contract/source | Input | Expected | Candidate result | Evidence |
|---|---|---|---|---|
| README acceptance | `/settings` | `200, {"theme":"light"}` | `200, {"theme":"light"}` | code + test `test_current_settings` (pass) |
| README acceptance | unknown path | `404, None` | `404, None` | code + test `test_unknown_route` (pass) |
| Task 1 (disabled) | `/export-preview` | `404, None` | `404, None` | code + test `test_preview_route` (pass) |

- `EXPORT_PREVIEW_ENABLED` is `False`, so `EXPORT_PREVIEW_ENABLED and path == "/export-preview"` **short-circuits** — `render_preview()` is never invoked in the checked-in build, and its `NotImplementedError` is unreachable.
- `from preview import render_preview` is side-effect-free (module only defines a function), so adding the import does not risk breaking `routes` import. Confirmed: full suite runs green (`python3 -B -m unittest discover -s tests` → 3/3 OK).

**Independent-compatibility dimension (Task 2 pending): Supported.** Existing `/settings` and 404 behavior are preserved against the HEAD base; the new branch is inert while the flag is off. No release/activation prerequisite is introduced by this increment.

## Findings

### P0 — Critical
(none)

### P1 — High
(none)

### P2 — Medium
(none)

### P3 — Low
(none)

No SOLID, security, code-quality, or boundary findings survived verification. Specifically dismissed after self-check:
- **`render_preview` raising `NotImplementedError`** — intentional Task 2 scaffold, guarded by the disabled flag and explicitly out of scope; not a missing-implementation or removal finding (removal-plan guidance: a pending task's unreachable scaffold is not, by itself, a removal candidate).
- **Unreachable `render_preview()` call branch** — same rationale; disabled-by-default feature, not dead code to remove.

## Areas Not Covered / Residual Notes

- **Enabled path is untested and will raise when activated.** If `EXPORT_PREVIEW_ENABLED` is flipped to `True` *before* `render_preview` is implemented, `get("/export-preview")` would propagate an uncaught `NotImplementedError`. This is valid **only after pending work lands** and is already the explicit precondition of Task 2 ("Implement render_preview and its enabled-path tests before changing the build setting"), so it is not a current finding — noted only as the activation prerequisite to preserve.
- Did not assess any deployed environment (none exists per README); conclusions are source- and test-based against the HEAD base.

**No findings to index** (`kk:review-findings`) — no P0/P1 systemic patterns. Knowledge base was empty (cold-start); proceeded on standard guidance.

---

This is a clean, correctly-scoped Task 1 increment: existing contracts preserved, feature inert behind the disabled flag, and the suite passes. No changes recommended.
