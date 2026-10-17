Knowledge base is empty (cold start) — proceeding with standard guidelines. I have everything needed. Applying the checklists and self-check, here is the review.

---

## Code Review Summary

**Files reviewed**: 2 files, 6 lines added (`preview.py` new, `routes.py` +4)
**Overall assessment**: **APPROVE** (scoped to code; Task 1 increment)
**Intent and scope**:
- Requirement source: `tasks.md` (Task 1 "Prepare preview module", **in-progress**) + `README.md` acceptance contract.
- Current task: Task 1 — add preview module + guarded route, keep preview **disabled** in the checked-in build, preserve existing routing.
- Selected diff: **staged** (no unstaged changes exist). Candidate state = index blobs.
- Out of scope: Task 2 ("Implement `render_preview`" + enabled-path tests, **pending**, depends on Task 1).

**Baselines**: Review base = `HEAD` (`f1a16b5`); candidate = staged index. No deployment/release baseline exists (README: "No deployment inventory is maintained in this small source repository").

## Behavior and Compatibility

Traced `routes.get(path)` at the staged revision against the acceptance contract:

| Path | Flag | Result | Contract |
| --- | --- | --- | --- |
| `/settings` | — | `(200, {"theme": "light"})` | ✓ preserved |
| `/export-preview` | `False` | `(404, None)` | ✓ disabled as required |
| `/unknown` | — | `(404, None)` | ✓ preserved |

- **Short-circuit verified**: `EXPORT_PREVIEW_ENABLED and path == "/export-preview"` — with the flag `False`, Python short-circuits and **never calls `render_preview()`**, so the `NotImplementedError` stub is unreachable in this build. The guarded route is correct.
- **Import resolves**: `from preview import render_preview` loads cleanly because `preview.py` is added in the same staged set; defining the stub (vs. calling it) is harmless.
- **Tests executed** (`python3 -B -m unittest discover -s tests`): **3/3 pass**, including `test_preview_route` which pins the disabled `/export-preview → 404` contract.

**Compatibility conclusions:**
- **Independent compatibility while Task 2 pending** (README hard requirement) — **Supported**: existing flows preserved, flag `False`, stub unreachable, suite green.
- **Activation vs. deployment** — **Not applicable / Supported**: the increment ships disabled; no activation path is reachable.
- **Mixed/old-new consumer** — **Not applicable**: single-process, single-repo; no external consumers.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low

- **[routes.py:1]** `from config import EXPORT_PREVIEW_ENABLED` binds the flag **by value** at import time
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` import-binding idiom
  - Path/consequence: The guard reads a value captured once at module load, not `config.EXPORT_PREVIEW_ENABLED` live. For **this** increment this is correct and matches the contract (README: the setting "is not supplied by a request, environment variable or external config" and is a fixed build constant flipped by editing source + restart). It is **not a defect now**.
  - Confidence: 70% that it is a worthwhile forward-looking note; ~95% that it is **not** a current bug. Verified: README explicitly scopes the flag as a static build constant; a fresh process after Task 2 edits `config.py` will import `True` correctly.
  - Suggested fix (defer to Task 2, non-blocking): when Task 2 adds enabled-path tests, toggle via `import config; config.X = True` **and** have `routes` reference `config.EXPORT_PREVIEW_ENABLED` through the module (or re-import), otherwise monkeypatch-style tests will still see the stale `False`. Flagging now only so the Task 2 author isn't surprised.

---

## Considered and dismissed (not findings)

- **`render_preview` raising `NotImplementedError`** — intentional Task 2 stub, unreachable while the flag is `False`. Per scope protocol this is expected pending work, **not** a missing-implementation finding.
- **`/export-preview` returning 404** — the required disabled behavior, pinned by `test_preview_route`. Correct.
- **Security checklist** — no user input, injection, deserialization, secrets, crypto, or concurrency surface in the diff. Not applicable.
- **OCP if-chain growth in `get`** — real but trivial at this scale (2 routes); not worth a refactor finding.

## Coverage and limits

- **Checked**: full staged diff, both changed files at the staged revision, `config.py`/`settings.py` contracts, the test suite (executed), README acceptance contract, `tasks.md` scope.
- **Not covered**: Task 2 implementation (out of scope); no CI/deployment environment exists to verify beyond local `unittest`.
- **Residual risk**: none for the current increment; the P3 is a forward-looking note for Task 2.

**Indexing**: No P0/P1 systemic findings — **nothing to index** as `kk:review-findings`.

---

## Next Steps

I found **1 issue** (P0: 0, P1: 0, P2: 0, P3: 1). The increment is clean, correctly guarded, and the existing acceptance contract is preserved with the suite green.

The actionable item I recommend:
1. **P3** — carry the by-value-import note forward to Task 2's test design (no change to Task 1 code required).

Items I recommend keeping as is:
- The `NotImplementedError` stub: correct intentional pending work, unreachable while the flag is off.
- `/export-preview → 404`: correct disabled behavior per the contract.
- The by-value import **for this increment**: matches the fixed-build-constant contract.

**How would you like to proceed?**

1. **Fix all** — apply the P3 (I'd only add a note/adjustment anticipating Task 2)
2. **Fix P0/P1 only** — nothing to do
3. **Fix specific items** — tell me which
4. **No changes** — review complete (my recommendation, since Task 1 is sound as-is)

Please choose an option or give specific instructions.
