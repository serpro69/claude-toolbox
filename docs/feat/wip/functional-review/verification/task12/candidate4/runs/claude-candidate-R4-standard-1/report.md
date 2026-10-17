Finding indexed. Here is the review.

---

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (1 insertion, 3 deletions) — `reader.py`
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The staged diff removes the legacy-shape fallback from `reader.address_of`, reducing it to a single unconditional `row["destination"]["address"]`. Framed as a "destination reader cleanup." No `docs/feat/wip/` feature directory relates to this diff — **no task scope available**; reviewed on its own merits against the project README contract.
**Baselines**: Review base `b299f57` ("Review base"); candidate = staged index blob of `reader.py`. No separate deployed baseline — README states this is a local JSON model with no production environment.
**Profiles active**: `python` (extension `.py`). Checklists applied: security, SOLID, code-quality, removal-plan.

## Behavior and Compatibility

The authoritative contract is `README.md`, which states plainly:
- "Destination records can use legacy top-level `address` or current nested `destination.address`."
- "a deployment **must read both shapes until migration finishes**" / "Existing addresses must be preserved."
- "`data/records.json` is a **supported mixed snapshot**" and "there is **no startup migration gate**."

Traced behavior:
- `migration.migrate_batch(records, limit)` converts flat→nested **only up to `limit` per invocation** — mixed flat+nested state is the designed, expected state, not a transient edge.
- `api.list_destinations` maps `address_of` over **every** record in a list comprehension.
- `data/records.json` (the supported snapshot) contains `legacy-a` and `legacy-c` with a top-level `address` and **no `destination` key**.

Concrete scenario (candidate code, supported snapshot): `list_destinations(json.load(records.json))` → first row `legacy-a` → `address_of` evaluates `row["destination"]` → **`KeyError: 'destination'`**. The whole call aborts; **zero records are served** even though only legacy rows are affected.

| Dimension | Conclusion |
|---|---|
| Fully-migrated dataset (all nested) | **Supported** — works. |
| Mixed/partly-migrated dataset (the documented supported state) | **Blocked** — `KeyError` breaks the entire read path; violates "read both shapes until migration finishes" and "reads remain available." |
| New writes (`new_destination`) | **Supported** — produces nested shape; no *new* legacy rows created. |

---

## Findings

### P0 - Critical

(none — no data loss/corruption; failure is loud and fully recoverable by reverting. Local model, no production availability dimension per README.)

### P1 - High

- **[reader.py:2]** Removing the legacy fallback breaks reads of the documented mixed snapshot
  - Profile: python · Checklist: removal-plan.md / code-quality-checklist.md (boundary conditions — missing-key `KeyError`)
  - Triggered by: content — `.py` extension
  - Trigger/path: any record lacking a `destination` key (e.g. `legacy-a`, `legacy-c` in `data/records.json`) flows through `address_of` via `api.list_destinations`. Expected: the address string (README requires reading both shapes until migration finishes). Actual: `KeyError: 'destination'` that aborts the entire list comprehension, serving nothing.
  - Consequence: the primary read API is fully broken for any not-fully-migrated dataset — which is the designed state, since `migrate_batch` is bounded by `limit` and there is "no startup migration gate." This is a documented hard-contract violation, at the high end of P1 (total breakage of the default supported snapshot; held below P0 only because data is intact and the change is trivially reversible).
  - Confidence: 98% — directly reproduced against the committed supported fixture and confirmed against three independent sources (README contract, `migrate_batch` bounded semantics, `list_destinations` fan-out).
  - Suggested fix: restore dual-shape support until migration is provably complete, e.g. `d = row.get("destination"); return d["address"] if d else row["address"]`. Defer the cleanup per the removal-plan "Defer Removal" path (precondition: verification that zero legacy rows remain across all stores).

### P2 - Medium

- **[tests/test_destinations.py:8]** Test suite never exercises the legacy shape, so the regression passes green
  - Profile: python · Checklist: code-quality-checklist.md (error handling / coverage)
  - Triggered by: —
  - Both tests build rows via `new_destination` (nested only); no test feeds a legacy flat row through `list_destinations`. The documented dual-shape contract is untested, which is exactly why this breaking change looks safe.
  - Confidence: 95% — confirmed by reading the full test file.
  - Suggested fix: add a test that lists a mixed batch (one legacy flat row + one nested row), asserting both addresses are returned — ideally loading `data/records.json` directly.

### P3 - Low

(none)

---

## Removal/Iteration Plan

The deleted branch is **not dead code** — it has active consumers (legacy rows in the supported mixed snapshot). This is a **Defer Removal** case:
- **Preconditions before removal**: migration verified 100% complete (telemetry/scan shows zero rows without a `destination` key across every store, including `data/records.json`); confirm no path can introduce new legacy rows (`new_destination` already only writes nested).
- **Until then**: keep the fallback. Removing it now violates "read both shapes until migration finishes."

## Coverage and limits

- **Checked**: full `reader.py` diff; all callers (`api.py`), producers (`writer.py`), migration logic (`migration.py`), the test suite, the README contract, and the committed `data/records.json` fixture.
- **Not covered**: did not execute the test suite (no run performed) or dynamically run `list_destinations` — the `KeyError` is established by source trace against the committed fixture, not by execution. No other stores beyond `data/records.json` were located.
- **Indexing**: P1 systemic finding indexed as `kk:review-findings` (removing a compatibility fallback mid-migration).

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P1** — Restore dual-shape reading in `reader.address_of` (or revert this diff) so mixed snapshots still read; defer the cleanup until migration is provably complete.
2. **P2** — Add a legacy/mixed-shape test so the contract is guarded going forward.

Items I recommend keeping as is:
- Nothing — the simplification is correct *only* post-migration, which cannot be guaranteed given "no startup migration gate."

**How would you like to proceed?**

1. **Fix all** — restore the fallback and add the mixed-shape test
2. **Fix P1 only** — restore the reader fallback
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions.
