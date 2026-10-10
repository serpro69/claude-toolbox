## Loading checkpoint

- **Common instructions read**: review-process, shared-capy-knowledge-protocol, shared-change-context, functional-review, shared-review-scope-protocol, shared-profile-detection ✓
- **Profile detection** (all 8 known profiles evaluated against the one scoped file `reader.py`):
  - `python` → **MATCH** (content signal: `.py` extension, authoritative)
  - `go`, `java`, `js_ts`, `kotlin`, `k8s`, `k8s-operator`, `skill-md` → no match (no filename/content signal fires on `reader.py`)
- **Checklists loaded** (python / review-code, all "Always load"): `security-checklist.md`, `solid-checklist.md`, `code-quality-checklist.md`, `removal-plan.md` ✓
- **Scope**: staged changes only (`M reader.py`); working tree clean. Baseline = `b299f57 "Review base"` via `git show HEAD:reader.py`.
- **Capy**: available; `kk:review-findings` empty at search (cold start), finding indexed.

---

## Code Review Summary

**Files reviewed**: 1 file, 2 lines removed (fallback branch deleted)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: "Destination reader cleanup" — staged simplification of `reader.address_of`. No `docs/feat/wip/` relates to this diff → **no task scope available**; reviewed on its own merits.
**Baselines**: Review base/candidate = `b299f57` → staged index blob. No separate release baseline; README states "no production environment or external database required."

The diff:

```python
# BEFORE (b299f57)                             # AFTER (staged)
def address_of(row):                           def address_of(row):
    if "destination" in row:                       return row["destination"]["address"]
        return row["destination"]["address"]
    return row["address"]
```

The "cleanup" removed the legacy-shape fallback (`return row["address"]`).

## Behavior and Compatibility

I traced the single caller, `api.list_destinations` (`api.py:5`), which calls `address_of` for **every** record, and the documented data contract (`README.md`).

- **Contract (README.md:5-13)**: records may use legacy top-level `address` *or* nested `destination.address`; "a deployment **must read both shapes until migration finishes**"; "Existing addresses **must be preserved**"; `data/records.json` is "a supported mixed snapshot"; `migrate_batch` is bounded-per-call with "**no startup migration gate**."
- **Shipped data (`data/records.json`)**: 3 rows, two of which (`legacy-a`, `legacy-c`) are legacy top-level shape with **no `"destination"` key**.

**Concrete scenario** — `list_destinations(json.load(open("data/records.json")))`:
- Row `legacy-a = {"id": "legacy-a", "address": "a@example.test"}` → `address_of` now evaluates `row["destination"]` → **`KeyError: 'destination'`**. The exception propagates out of the list comprehension, so the *entire* call fails and **zero** records are returned.

**Compatibility dimension — mixed-shape read (old data / new reader): BLOCKED.** Demonstrated incompatibility introduced by this change against the documented current flow. Migration is bounded-batch with no startup gate, so legacy rows are guaranteed present during the migration window — the fallback was load-bearing, not dead code.

Why the test suite is green anyway: `tests/test_destinations.py` only exercises `new_destination` (nested shape) and the empty list. It never feeds a legacy-shaped row, so it cannot catch this regression (classic "green implementation-shaped tests don't prove the business operation").

---

## Findings

### P0 - Critical

(none — no production environment/irreversible loss; data on disk is intact and the change is trivially reversible, so this stays P1 per severity guidance)

### P1 - High

- **[reader.py:2]** Removing the legacy fallback breaks reads of mixed/legacy data (crashes the whole read path)
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / None-vs-missing) + removal-plan.md
  - Triggered by: content — `.py` extension (python profile)
  - **Trigger/path**: `list_destinations` → `address_of(row)` for any row lacking `"destination"` (e.g. `legacy-a`, `legacy-c` in the supported `data/records.json`).
  - **Expected vs actual**: Contract requires reading both shapes until migration completes and preserving existing addresses → expected `"a@example.test"`. Actual: `KeyError: 'destination'`, which aborts the whole list comprehension so `list_destinations` returns nothing.
  - **Consequence**: Violates two hard acceptance requirements in README ("must read both shapes until migration finishes", "existing addresses must be preserved"). Full read-path failure on the shipped mixed snapshot during the migration window.
  - **Confidence: 97%** — verified against the actual single caller, the documented contract, and the shipped data file; KeyError is deterministic for legacy rows. Residual 3%: a hypothetical caller that guarantees migration is 100% complete before any read — but README explicitly rules this out ("no startup migration gate," "supported mixed snapshot").
  - **Suggested fix**: Restore the dual-shape read until migration is provably complete:
    ```python
    def address_of(row):
        if "destination" in row:
            return row["destination"]["address"]
        return row["address"]
    ```
    If the goal is genuinely to retire the legacy shape, defer the removal behind a precondition (telemetry shows 0 legacy rows / migration gate added) per `removal-plan.md` → "Defer Removal."

### P2 - Medium

- **[tests/test_destinations.py:8]** Test suite has no coverage for the legacy shape
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions)
  - Triggered by: —
  - The suite only covers the nested shape and empty list, so a regression that breaks every legacy read passes CI green. This coverage gap is why the cleanup looked safe.
  - **Confidence: 95%** — the test file is fully read; no legacy-shaped row appears.
  - **Suggested fix**: Add a case asserting `list_destinations([{"id": "x", "address": "x@example.test"}])` returns `[{"id": "x", "address": "x@example.test"}]` (would fail today, guarding the fallback).

### P3 - Low

(none)

---

## Removal/Iteration Plan

The deletion is a **Defer Removal** case, not **Safe to Remove Now** — the "legacy shape" still has active consumers (the mixed snapshot + in-flight migration).

- **Preconditions before removing the fallback**: `migrate_batch` run to completion across the whole store; verification that 0 rows use the top-level shape; a startup/read gate (or one-shot full migration) so new reads can't race ahead of migration.
- **Verification**: the P2 legacy-shape test must pass *with* the fallback, then be updated only after the data is provably all-nested.

## Additional Suggestions

- `migration.py:7` uses `row.pop("address")` — fine today, but once the reader stops accepting the legacy shape, make sure no reader observes a row mid-migration; the current in-place batch mutation is safe only because `address_of` still tolerates both shapes.

---

## Next Steps

I found 2 issues (P0: 0, P1: 1, P2: 1, P3: 0). This is a **REQUEST_CHANGES** — the staged cleanup regresses a documented hard requirement.

The actionable items I recommend fixing:
1. **P1** — Restore the legacy fallback in `reader.address_of` (or defer the removal behind a migration-complete precondition).
2. **P2** — Add a legacy-shape test to `tests/test_destinations.py` so the regression can't recur silently.

Items I recommend keeping as is:
- Nothing — the change as staged should not merge in its current form.

**How would you like to proceed?**

1. **Fix all** — restore the fallback + add the legacy-shape test
2. **Fix P1 only** — restore the fallback
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions. (I'll make no edits until you confirm.)
