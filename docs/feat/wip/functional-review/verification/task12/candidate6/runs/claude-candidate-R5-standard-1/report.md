Knowledge base is empty (cold-start) — proceeding on standard guidelines, as the protocol directs.

I now have everything needed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (`preview.py` new, `routes.py` modified)
**Overall assessment**: **APPROVE** (scoped to Task 1 code)
**Intent and scope**: Requirement source = `README.md` + `tasks.md`. Current task = **Task 1 "Prepare preview module"** (status: in-progress → in scope): preserve existing routes with preview disabled, and add the preview module + guarded route for the next increment. **Task 2** (implement/enable `render_preview`) is `pending` → **out of scope**. Selected diff = **staged** index (no unstaged changes present).
**Baselines**: Review base = `f1a16b5` ("Review base"); candidate = staged working tree. No separate released/deployed baseline — README states no deployment inventory is maintained.

## Behavior and Compatibility

Traced `routes.get(path)` against the three documented routes and the acceptance contract ("existing GET /settings response and routing behavior remain the acceptance contract"):

| Contract/source | Input | Expected | Candidate result | Evidence |
|---|---|---|---|---|
| README acceptance | `GET /settings` | `(200, {"theme": "light"})` | `(200, current_settings())` → unchanged | `routes.py:6-7`, `settings.py`; `test_current_settings` |
| README routing behavior | `GET /unknown` | `(404, None)` | `(404, None)` fall-through | `routes.py:10`; `test_unknown_route` |
| Task 1 "disabled in checked-in build" | `GET /export-preview` | `(404, None)` | `EXPORT_PREVIEW_ENABLED` is `False` → `and` short-circuits → falls through to `(404, None)` | `config.py` (`= False`), `routes.py:8-9`; `test_preview_route` |

- **Stub reachability:** `render_preview()` (raises `NotImplementedError`) is **never invoked** while the flag is `False` — Python `and` short-circuits before the guarded body runs, and the body is the only call site. The stub is legitimate Task 2 scaffolding, deliberately pending. Per the review-scope and removal protocols, an unreachable, flag-gated scaffold for a pending task is **not** a defect and **not** a removal candidate.
- **Import integrity:** `routes.py` imports `render_preview` (preview.py, new) and `EXPORT_PREVIEW_ENABLED` (config.py, exists). No circular imports — `preview`/`config`/`settings` do not import `routes`. Importing a module that merely *defines* a stub function has no side effect.
- **Flag binding:** `from config import EXPORT_PREVIEW_ENABLED` binds the value at import time. This matches README's explicit contract that the setting is a fixed checked-in build constant, not request/env/config-supplied — so import-time binding is correct for the stated contract, not a defect.

**Compatibility conclusions:**
- **Supported** — existing-consumer/current-flow compatibility: GET /settings and 404 routing are byte-for-byte preserved; all three tests pass by trace. Baseline = review base `f1a16b5`.
- **Not applicable** — old-consumer/new-provider, data migration, mixed-version: no persisted state, no data shape, no external consumers in this single-process stdlib repo.
- **Unknown (out-of-scope)** — behavior of the *enabled* `/export-preview` path (auth/authz, input handling, output): belongs to Task 2 and was not assessed; the flag is off in this increment.

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
(none)

**Checklists applied** (python profile — security, SOLID, code-quality, removal): no issues on the staged lines. Notably rejected on self-check:
- *"`render_preview` NotImplementedError makes /export-preview return 500"* — **rejected** (~99%): flag `False` + short-circuit means the stub is unreachable; it is in-scope-pending Task 2 work, which the scope protocol says must not be flagged as missing/broken.
- *"ISP: `NotImplementedError` stub"* — **rejected**: the checklist item targets interface/subclass stubs; this is a module-level placeholder for a pending increment, with no implementers.
- *"Dead code / removal candidate: `render_preview`"* — **rejected**: `removal-plan` and the general removal guidance explicitly exclude a pending task's unreachable scaffold.

## Indexing

No P0/P1 systemic findings → **No findings to index.** (Knowledge base is empty/cold-start; standard guidelines applied.)

## Coverage and limits

- **Checked:** full staged diff, both changed files at the reviewed revision, the flag value, import resolution, and all three route behaviors against the README acceptance contract and `tasks.md` scope.
- **Not covered:** the enabled `/export-preview` behavior (Task 2) — including any auth/authz, input validation, and output encoding that the real `render_preview` will need. That is correctly deferred; flag `EXPORT_PREVIEW_ENABLED` and `render_preview` must be reviewed together when Task 2 flips the setting.
- **Residual risk:** none for this increment under its stated delivery contract.

This is a clean, correctly-scoped Task 1 increment: the new export-preview route is added behind a disabled flag, the stub is unreachable, and the existing acceptance contract is preserved. No changes recommended.
