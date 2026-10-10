Knowledge base is empty (cold start) — proceeding with standard guidelines. I have everything needed. Here's the review.

## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (`preview.py` new +2, `routes.py` +4)
**Overall assessment**: **APPROVE**
**Intent and scope**: Task 1 of the "Export preview" work (`tasks.md`, status: in-progress). Per `README.md`, this increment prepares the preview module and a *guarded* route while keeping the build independently compatible; the existing `GET /settings` response and routing behavior are the acceptance contract. Activation (`render_preview` implementation + enabling the flag + enabled-path tests) is explicitly **Task 2 (pending)**.
**Scope selector**: staged changes (no unstaged changes present). No `docs/feat/wip/` directory; task scope taken from root `tasks.md` + `README.md`.
**Baselines**: Review base = `f1a16b5` ("Review base") + staged index; candidate = staged blobs (worktree identical). `README.md` states no deployment inventory is maintained, so no separate release baseline exists.
**Profiles active**: `python` (all other 7 known profiles evaluated and non-matching).

## Behavior and Compatibility

Traced `routes.get` through its three branches at the reviewed revision, against `config.py` (`EXPORT_PREVIEW_ENABLED = False`), `settings.py`, `preview.py`, and the existing `tests/test_routes.py`:

| Path | Current build (flag `False`) | Baseline / test | Conclusion |
|------|------|------|------|
| `GET /settings` | `(200, {"theme": "light"})` | `test_current_settings` | **Supported** — contract preserved |
| `GET /unknown` | `(404, None)` | `test_unknown_route` | **Supported** |
| `GET /export-preview` | `(404, None)` — `and` short-circuits on `False`, so `render_preview()` is never evaluated | `test_preview_route` expects `(404, None)` | **Supported** — independently compatible with Task 2 pending |

- **Independent-delivery requirement** (README: "must remain independently compatible while that task is pending"): **Supported**. The flag is a fixed in-source constant (`False`), not request/env/config-driven, so the `/export-preview` branch is unreachable in the checked-in build. The `NotImplementedError` stub in `preview.py` is correctly gated behind the flag and cannot be hit.
- **Import safety**: `from preview import render_preview` and `from config import EXPORT_PREVIEW_ENABLED` execute side-effect-free modules; no import-time risk, name binds cleanly.
- **Task 2 (render_preview implementation, flag enablement, enabled-path tests)**: genuinely pending — **not** treated as a missing-implementation finding, per the stated scope.

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
(none blocking — see Additional Suggestions)

---

## Additional Suggestions (forward-looking, for Task 2 — non-blocking)

- **`routes.py:1` — flag is imported by value; in-process toggling won't be observed.** `from config import EXPORT_PREVIEW_ENABLED` binds the current `False` into the `routes` namespace. This is correct for the real delivery model (Task 2 edits `config.py` and a fresh process picks up the new value). However, when Task 2 writes its "enabled-path tests," a test that sets `config.EXPORT_PREVIEW_ENABLED = True` at runtime will **not** affect `routes.EXPORT_PREVIEW_ENABLED` — the enabled branch would still be skipped. Task 2's tests must either monkeypatch `routes.EXPORT_PREVIEW_ENABLED` or have `routes` reference `config.EXPORT_PREVIEW_ENABLED` at call time (`import config` then `config.EXPORT_PREVIEW_ENABLED`). Flagged here, not as a P-level finding, because it is only consequential once pending Task 2 work lands. Confidence: 92% — verified Python import-binding semantics against the code; the "fixed build constant" model in README means it is not a current defect.

## Areas Not Covered / Residual Risks

- Did not execute the test suite (`python3 -B -m unittest discover -s tests`) — Bash `cat` was denied in this session and I did not run tests. The pass/fail conclusions above are by source trace of `routes.get` against the asserted tuples, not observed execution. Recommend running the suite to confirm.
- `render_preview`'s actual output/behavior is out of scope (Task 2) and was not assessed beyond confirming its stub is unreachable while the flag is off.
- No deployment/environment baseline exists per README; compatibility conclusions are limited to the checked-in source build.

## Findings indexing

No P0/P1 systemic findings → **No findings to index.**

---

## Next Steps

I found **0 blocking issues** (P0: 0, P1: 0, P2: 0, P3: 0). The increment is clean and correctly scoped: it preserves the `GET /settings`/routing acceptance contract and stays independently compatible with the preview flag off.

One **non-blocking forward note** for Task 2:
1. Flag is imported by value (`routes.py:1`) — Task 2's enabled-path tests must patch `routes.EXPORT_PREVIEW_ENABLED` (or switch to call-time `config.` access), or they'll silently test the disabled path.

Items I recommend keeping as-is:
- `preview.py` `NotImplementedError` stub: correct scaffolding — gated behind the flag, unreachable in this build; implementing it is Task 2.
- The guarded `/export-preview` branch: correctly short-circuits with the flag `False`; matches `test_preview_route`.

**How would you like to proceed?**

1. **Fix all** — apply the Task 2 forward note now (e.g., switch `routes` to call-time `config.EXPORT_PREVIEW_ENABLED` access for testability)
2. **No changes** — review complete, carry the note into Task 2
3. **Fix specific items** — tell me which

Since there are no blocking findings, my recommendation is **option 2** (approve as-is, carry the note forward). Let me know.
