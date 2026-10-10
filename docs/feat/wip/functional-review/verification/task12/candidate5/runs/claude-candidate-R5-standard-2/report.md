Knowledge base is empty (cold start) — proceeding with standard guidelines. No `kk:review-findings` or `kk:lang-idioms` to apply.

I have everything needed. Here's the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (`preview.py` +2 new, `routes.py` +4)
**Overall assessment**: ✅ **APPROVE** (scoped to Task 1 code)
**Intent and scope**: `tasks.md` → Task 1 "Prepare preview module" (status: *in-progress*) — add the preview module and a guarded route for the next increment while preserving existing routes with preview disabled. `README.md` is the acceptance contract: GET `/settings` response and routing behavior must remain unchanged; `EXPORT_PREVIEW_ENABLED` is fixed at `False` in the checked-in build (not request/env/config-driven); the increment must remain independently compatible while Task 2 is pending.
**Selected diff**: staged changes (no unstaged changes exist; matches the "staged Task 1" you described).
**Baselines**: Review base = `HEAD` (f1a16b5 "Review base"); candidate = staged index. No separate deployed baseline (README: "No deployment inventory is maintained").

**Task scope** (shape 2 — `tasks.md` present, no explicit task id passed; mode: **mid-implementation**):
- *In scope*: Task 1 (preview module + guarded route, disabled build).
- *Out of scope (pending — not flagged as missing)*: Task 2 — `render_preview` implementation, enabled-path tests, flipping the flag.

## Behavior and Compatibility

Traced all three routing paths at the candidate revision (`contract → state → operation → expected → candidate → evidence`):

| Path | Expected (contract) | Candidate result | Evidence |
|---|---|---|---|
| `get("/settings")` | `(200, {"theme":"light"})` | unchanged | `routes.py:7-8`, `test_current_settings` |
| `get("/unknown")` | `(404, None)` | unchanged | `routes.py:11`, `test_unknown_route` |
| `get("/export-preview")`, flag `False` | `(404, None)` | `EXPORT_PREVIEW_ENABLED and …` short-circuits → `render_preview()` never called → `(404, None)` | `routes.py:9`, `config.py:1`, `test_preview_route` |

- **Short-circuit is correct**: `EXPORT_PREVIEW_ENABLED` is `False`, so Python's `and` never evaluates `render_preview()`, so the `NotImplementedError` in `preview.py:2` is unreachable in this build. The placeholder raising is **intentional scaffolding for Task 2**, not a defect.
- **No import errors / no cycles**: `routes → {config, preview, settings}`; `preview` imports nothing. All three new/referenced symbols exist.
- **Compatibility — disabled configuration (flag `False`)**: **Supported.** `/export-preview` returns `404` exactly as it did before the module existed; `/settings` and unknown-path behavior are byte-identical. The increment is independently compatible with Task 2 pending, satisfying the README requirement.
- **Enabled configuration (flag `True`)**: **Not applicable to this increment** — that path is Task 2's deliverable (implement `render_preview`, add enabled-path tests, then flip the flag, per `tasks.md` Task 2).

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
(none that warrant a change in this increment)

I specifically considered and **rejected** these as findings, because they are intentional or out of scope:
- `render_preview` raising `NotImplementedError` — intentional, gated behind an always-`False` flag; implementing it is Task 2.
- The `/export-preview` branch being unreachable in the checked-in build — intentional scaffold, **not** a removal candidate (per removal guidance: a pending task's guarded scaffold is not a removal candidate).
- Missing enabled-path tests / missing auth on the endpoint — Task 2 scope; the endpoint is gated off and the existing app (`/settings`) has no auth layer either, so no regression is introduced here.

## Areas Not Covered / forward notes for Task 2

These are **not** Task 1 defects — flagged only so Task 2 doesn't trip on them:
- **Flag binding is import-time.** `routes.py:1` does `from config import EXPORT_PREVIEW_ENABLED`, which copies the value into the `routes` namespace at import. When Task 2 adds enabled-path tests, patching `config.EXPORT_PREVIEW_ENABLED` will **not** affect `routes`; the test must patch `routes.EXPORT_PREVIEW_ENABLED` (or `routes` must read `config.EXPORT_PREVIEW_ENABLED` at call time). Correct and compatible for Task 1's fixed-`False` build.
- **Auth/authorization on `/export-preview`** should be decided when the path is enabled in Task 2 (what does the preview expose?).
- I did **not** execute the test suite — `python3 -B -m unittest discover -s tests` was not run (Bash execution is denied in this session). The pass/fail conclusions above are from source tracing of three small, deterministic functions, not from a test run.

## Step 8 — Index findings

No P0/P1 systemic findings → **No findings to index.**

---

## Next Steps

I found **0 actionable issues** (P0: 0, P1: 0, P2: 0, P3: 0). This is a clean, well-scoped Task 1 increment: the guarded route preserves all existing behavior with the flag `False`, and the `NotImplementedError` scaffold is correctly unreachable and intentional for Task 2.

Items I recommend keeping as-is:
- The `NotImplementedError` placeholder and the gated route — intentional Task 2 scaffolding.
- The disabled `/export-preview` branch — not dead code to remove; it's planned scaffold.

Carry into Task 2 (not changes now): patch `routes.EXPORT_PREVIEW_ENABLED` (not `config`) in enabled-path tests; decide auth for the endpoint; implement `render_preview` and add tests *before* flipping the flag (as Task 2 already states).

**How would you like to proceed?**
1. **Approve & done** — no changes needed (my recommendation).
2. **Run the tests** — I can run `python3 -B -m unittest discover -s tests` if you approve Bash, to confirm the three assertions pass.
3. **Address a forward note now** — e.g., adjust the flag-read pattern for testability ahead of Task 2.
4. **Something else** — tell me what to focus on.
