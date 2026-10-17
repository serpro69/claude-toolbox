Knowledge base is empty (cold-start) — proceeding with standard guidelines per protocol. I've applied all four Python checklists and completed the self-check. Here's the review.

## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (`preview.py` new, `routes.py` modified)
**Overall assessment**: **COMMENT** — clean, well-scoped Task 1 wiring. No blocking issues. One maintainability finding worth addressing now because it affects whether the flag can ever be flipped; the rest are minor/observational.

**Profiles active**: `python` (triggered by `.py` extension — content signal). All four Python checklists applied (security, SOLID, code-quality, removal). No conditional checklists.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium

- **[routes.py:1]** Feature flag bound by value at import time — flag can't be toggled
  - Profile: python · Checklist: code-quality-checklist.md (Boundary/None handling → import semantics) / generic
  - Triggered by: content — `.py`
  - `from config import EXPORT_PREVIEW_ENABLED` copies the current `bool` into `routes`' namespace at import. Because it's an immutable value imported *by name*, later rebinding `config.EXPORT_PREVIEW_ENABLED = True` (at runtime, or via `monkeypatch`/`patch` in a test) will **not** change what `get()` sees — it keeps the snapshot taken at import. This is the classic "import the module, not the value" footgun, and it's especially relevant here because the entire purpose of a feature flag is to be flipped. Concretely: a Task 2 test that tries to exercise the enabled path by patching `config.EXPORT_PREVIEW_ENABLED` would still hit the `404` branch, silently passing/failing for the wrong reason.
  - Confidence: 85% — Python import semantics make the behavior certain; the 15% is whether the project intends deploy-time-constant flags (in which case this is moot) vs. runtime/test toggling (very likely given it's named as a rollout flag).
  - Suggested fix: import the module and dereference at call time:
    ```python
    import config
    from preview import render_preview
    from settings import current_settings

    def get(path):
        if path == "/settings":
            return 200, current_settings()
        if config.EXPORT_PREVIEW_ENABLED and path == "/export-preview":
            return 200, render_preview()
        return 404, None
    ```

### P3 - Low

- **[routes.py:10]** No exception boundary around `render_preview()` once the flag flips
  - Profile: python · Checklist: code-quality-checklist.md (Error Handling) / security-checklist.md (Runtime Risks)
  - Triggered by: content — `.py`
  - `render_preview()` currently always `raise`s `NotImplementedError` (correct for a Task 1 placeholder). But the flag and the implementation land in separate tasks: if `EXPORT_PREVIEW_ENABLED` is set to `True` before Task 2 ships, `get("/export-preview")` propagates an uncaught exception out of the router instead of returning a graceful status. This is inert today (flag is `False`) and intentional staging — flagging it only as a rollout-ordering coupling to track, not a defect in Task 1's scope.
  - Confidence: 95% that the behavior is as described; low severity because it's gated and by-design for the staged rollout.
  - Suggested fix: no code change needed now — just ensure Task 2 (implementation) merges before/with any change that flips the flag. Optionally the router could wrap handler calls in a try/except → 500, but that's a broader change beyond this diff.

- **[routes.py:9]** New `/export-preview` endpoint has no auth/authorization guard
  - Profile: python · Checklist: security-checklist.md (AuthN/AuthZ)
  - Triggered by: content — `.py`
  - A new data-exposing endpoint with no auth check. However, this mirrors the existing `/settings` route and the router has no auth anywhere — so it's consistent with the established (toy) codebase pattern, not a regression introduced by this change. Noting for completeness; address at the app level if/when auth is introduced.
  - Confidence: 60% as a real concern — depends entirely on whether this router is meant to have auth at all; nothing in scope suggests it does.

- **[tests/test_routes.py:13]** Test covers only the flag-off path
  - Profile: python · Checklist: generic (test coverage)
  - Triggered by: —
  - `test_preview_route` correctly asserts `404` while the flag is off — good. There's no coverage for the enabled path. Note this interacts with the P2 finding: as `routes.py` is currently written, you *cannot* write that test by patching the config value (the import-by-value binding defeats it). Fixing the P2 finding is a prerequisite for a meaningful enabled-path test in Task 2.
  - Confidence: 90%.

---

## Removal/Iteration Plan
Not applicable — this is additive wiring, no dead/retired code. (`render_preview`'s placeholder body is intentional staging, not a removal candidate.)

## Additional Suggestions
- The diff is clean and proportionate: small, single-responsibility, flag-gated, and the placeholder clearly names its follow-up ("scheduled for Task 2"). No SOLID violations, no injection/SSRF/deserialization/crypto/race concerns in scope.

---

**Indexing (Step 9)**: No P0/P1 systemic findings — **no findings to index**.

---

## Next Steps

I found 4 issues (P0: 0, P1: 0, P2: 1, P3: 3).

The actionable items I recommend fixing:
1. **P2** — Change `routes.py` to `import config` and reference `config.EXPORT_PREVIEW_ENABLED` at call time, so the flag is actually toggleable (and testable in Task 2).

Items I recommend keeping as-is:
- **P3 (NotImplementedError)** — correct, intentional placeholder for Task 1; just coordinate the flag flip with Task 2's merge.
- **P3 (no auth)** — consistent with the existing router; not a regression from this change.
- **P3 (test coverage)** — the flag-off test is correct; the enabled-path test naturally belongs to Task 2 (and unblocks once the P2 fix lands).

**How would you like to proceed?**

1. **Fix all** — I'll implement all suggested fixes
2. **Fix P2 only** — Just the import-binding fix
3. **Fix specific items** — Tell me which
4. **No changes** — Review complete, no implementation needed

Please choose an option or provide specific instructions.
