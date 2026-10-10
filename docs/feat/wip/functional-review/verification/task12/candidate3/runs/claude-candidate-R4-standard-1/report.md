Review complete. Here are the results.

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (+1 / −3)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: "Destination reader cleanup" — simplify `reader.address_of` by dropping the legacy-shape fallback. Selected diff = **staged** `reader.py` (no unstaged changes). Candidate state = index blob.
**Baselines**: Review base `b299f57` → staged candidate. No separate deployed baseline — README states the store is a local JSON model with no production/external DB.
**Profile**: `python` (always-load checklists applied: security, SOLID, code-quality, removal). No other profile matched.

## Behavior and Compatibility

`address_of` is the single shared reader (`api.list_destinations` → `address_of`). The documented contract (README) is explicit:

> *"Destination records can use legacy top-level `address` or current nested `destination.address`… a deployment must read both shapes until migration finishes… `data/records.json` is a supported mixed snapshot… there is no startup migration gate."*

The change removed exactly the branch that satisfied that contract:

```python
# before
if "destination" in row:
    return row["destination"]["address"]
return row["address"]          # ← legacy shape, removed
# after
return row["destination"]["address"]
```

- **Partly-migrated data (mixed snapshot): Blocked.** `migrate_batch` migrates only up to `limit` rows per call and has no startup gate, so legacy rows are a normal live state. The committed `data/records.json` contains two legacy rows (`legacy-a`, `legacy-c`).
- **Repro (verified, not hypothetical):** `list_destinations(json.load(data/records.json))` → `KeyError: 'destination'`. The list comprehension fails on the first legacy row, so the *entire* listing dies — including the already-migrated record. Existing addresses are no longer served, violating README's "Existing addresses must be preserved."
- **Tests: green but non-covering.** `test_destinations.py` exercises only the nested shape (`new_destination`) and the empty list. Both pass, masking the regression — a classic case of implementation-shaped tests not proving the business contract.

---

## Findings

### P0 - Critical

- **[reader.py:2]** Reader no longer handles legacy top-level `address`; crashes on supported mixed data
  - Profile: python · Checklist: code-quality-checklist.md (Boundary / None handling), removal-plan.md
  - Triggered by: content — `.py` extension (python profile)
  - **Trigger/path**: any record lacking a `"destination"` key (legacy shape) reaches `address_of` via `api.list_destinations`. Expected: return the top-level `address`. Actual: `KeyError: 'destination'`, propagating out of the list comprehension and failing the whole call.
  - **Consequence**: Complete data-availability loss for any dataset with ≥1 unmigrated record — the normal state given bounded, gateless migration. Directly violates README's hard requirements ("read both shapes until migration finishes", "Existing addresses must be preserved"). Reproduced against the committed `data/records.json`.
  - **Confidence: 98%** — verified by the README contract, the committed mixed snapshot, the bounded/gateless `migrate_batch`, and a live `KeyError` repro. Residual doubt (an external migration-completion gate) is closed by README's explicit "there is no startup migration gate."
  - **Suggested fix**: keep the fallback until the legacy shape is provably extinct:
    ```python
    def address_of(row):
        if "destination" in row:
            return row["destination"]["address"]
        return row["address"]
    ```
    This "cleanup" is a **defer-removal** per the removal template: preconditions (migration complete, 0 legacy rows in all snapshots, no `data/records.json` legacy entries) are not met.

### P1 - High

_(none)_

### P2 - Medium

- **[tests/test_destinations.py:8]** No test covers the legacy / mixed-shape read path
  - Profile: python · Checklist: code-quality-checklist.md
  - The suite only validates nested writes and the empty list, so it stays green while the documented "read both shapes" contract is broken. A test feeding a legacy row (or the `data/records.json` snapshot) through `list_destinations` would have caught the P0.
  - **Confidence: 95%** — observed directly from the test file and the passing run.
  - **Suggested fix**: add a case asserting `list_destinations([{"id":"legacy","address":"x@example.test"}])` returns `[{"id":"legacy","address":"x@example.test"}]`, ideally plus a mixed-snapshot case.

### P3 - Low

_(none)_

---

## Removal/Iteration Plan

The legacy branch is a **defer-removal**, not a safe-delete-now:
- **Preconditions before it can be removed**: `migrate_batch` run to completion across all stores; `data/records.json` (and any other snapshot) contains zero top-level-`address` rows; a migration-complete gate or telemetry confirms 0 legacy reads.
- **Safer sequencing**: migrate data → verify 0 legacy rows → then drop the branch in a follow-up, adding a legacy-shape regression test first so the removal is behavior-preserving.

## Coverage & limits

- **Checked**: full staged diff, all callers (`api.py`) and producers (`writer.py`, `migration.py`), the data snapshot, README contract, and the test suite; ran the tests and a direct repro.
- **Not covered**: no runtime/production environment exists per README (local JSON only), so no deployment verification was needed. Knowledge base was empty (cold start) — no prior-pattern corroboration.
- **Indexed**: P0 pattern recorded under `kk:review-findings`.

---

## Next Steps

I found **2 issues** (P0: 1, P1: 0, P2: 1, P3: 0).

Actionable items I recommend fixing:
1. **P0** — Restore the legacy-shape fallback in `reader.address_of` (the "cleanup" is premature while migration is incomplete).
2. **P2** — Add a legacy/mixed-shape test so the contract is actually guarded.

Items to keep as-is: none — the simplification itself is only valid *after* migration completes and legacy rows are gone.

**How would you like to proceed?**

1. **Fix all** — restore the fallback + add the legacy test
2. **Fix P0 only** — restore the fallback
3. **Fix specific items** — tell me which
4. **No changes** — review only

I won't make any edits until you confirm.
