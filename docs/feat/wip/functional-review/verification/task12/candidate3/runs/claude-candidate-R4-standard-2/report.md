## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (1 insertion, 3 deletions) — staged `reader.py`
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Staged "destination reader cleanup" — removes the legacy-shape fallback in `address_of`, leaving only nested `row["destination"]["address"]` access. Scope = staged changes only; no unstaged changes, no `docs/feat/wip/` task scope (reviewed on its own merits + repo contracts).
**Baselines**: Review base `b299f57` → staged candidate. Store is a local JSON model (`data/records.json`); README states no production/external DB. No separate release baseline.

## Behavior and Compatibility

`address_of` is consumed by `api.list_destinations`, which maps **every** saved record through it. The README is explicit about the delivery contract:

> *"a deployment must read both shapes until migration finishes … `data/records.json` is a supported mixed snapshot … Existing addresses must be preserved."*

Migration (`migrate_batch`) is **incremental** — it converts up to `limit` rows per call with **no startup migration gate** — so legacy-shaped rows (top-level `address`, no `destination` key) provably coexist with nested rows at runtime. The removed `if "destination" in row` branch was the only handler for that shape.

- **Reproduced:** `list_destinations(json.load(open('data/records.json')))` → `KeyError: 'destination'` on the first legacy row (`legacy-a`). The list comprehension aborts, so the **entire read fails**, not just one row.
- **Mixed-shape read (migration in progress): Blocked** — demonstrated incompatibility against a documented, currently-reachable, required flow.
- **Nested-only / empty reads: Supported** — happy path works; the existing 2 tests pass green but cover only the nested shape and empty list, so they do not exercise the broken contract.
- **"Existing addresses must be preserved": Blocked** — legacy addresses become unreadable.

---

## Findings

### P0 - Critical

- **[reader.py:2]** Removing the legacy-shape fallback crashes reads of un-migrated records
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions — None/missing-key handling) + functional-review (compatibility)
  - Triggered by: content — `.py` extension activates python profile
  - **Trigger/path**: `api.list_destinations(records)` → `address_of(row)` for any row lacking a `destination` key (legacy shape). Expected: return `row["address"]` (prior behavior). Actual: `KeyError: 'destination'`, aborting the whole list comprehension.
  - **Consequence**: Every read over a dataset still containing ≥1 un-migrated row fails entirely. The shipped `data/records.json` (a *documented supported mixed snapshot*) crashes today — reproduced. Directly violates README's "read both shapes until migration finishes" and "existing addresses must be preserved" requirements. Since migration is bounded/incremental with no startup gate, the window where legacy rows exist is the normal operating state, not an edge case.
  - **Confidence: 99%** — Reproduced directly against the real fixture; the removed branch was the sole legacy handler; the contract is stated verbatim in the README and corroborated by `migration.py`, `writer.py`, and the mixed `data/records.json`. Only residual uncertainty is whether an out-of-band full migration is assumed to run first, but the README explicitly rules that out ("no startup migration gate").
  - **Suggested fix**: Do not remove the fallback until migration is proven complete and no legacy data can reach the reader. Restore shape-tolerant access:
    ```python
    def address_of(row):
        if "destination" in row:
            return row["destination"]["address"]
        return row["address"]
    ```
    If the goal is to eventually simplify, gate removal on a verified completed migration (and drop the fallback in the same change that guarantees all persisted rows are nested).

### P1 - High

*(none)*

### P2 - Medium

- **[tests/test_destinations.py:7]** Test suite has no legacy-shape coverage
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions) / functional-review (tests must exercise the claimed contract)
  - Triggered by: content — `.py`
  - **Trigger/path**: Tests cover only `new_destination` (nested) and the empty list. The README's core guarantee — reading legacy rows during migration — is untested, which is why this P0 regression passes CI green (`Ran 2 tests … OK`).
  - **Consequence**: The dual-shape contract can regress silently (and just did).
  - **Confidence: 95%** — Observed directly; tests pass despite the broken contract.
  - **Suggested fix**: Add a test asserting `list_destinations([{"id":"legacy","address":"x@example.test"}]) == [{"id":"legacy","address":"x@example.test"}]`, and ideally one over the full mixed `data/records.json` fixture.

### P3 - Low

*(none)*

---

## Coverage and limits

- **Checked**: the full change, all callers (`api.py`), both data producers (`writer.py` nested, `migration.py` legacy→nested), the persisted fixture (`data/records.json`), the README contract, and the test suite. Reproduced the crash and ran the suite.
- **Not covered**: no separate deployed/production environment exists per README (local JSON model), so there is no release-environment baseline to assess beyond the repo.
- **Residual risk**: none material beyond the findings above; the P0 is confirmed by execution.

**Indexed**: the P0 was indexed as `kk:review-findings` (systemic "premature compat-fallback removal during incremental migration" pattern).

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. **P0** — Restore the dual-shape fallback in `reader.py` (the cleanup is premature; it breaks the documented mixed-read contract and crashes the shipped snapshot).
2. **P2** — Add a legacy-shape test so this contract can't regress silently.

Items I recommend keeping as is:
- None — the cleanup's intent (simplifying once migration completes) is valid, but it cannot land until migration is proven complete.

**How would you like to proceed?**

1. **Fix all** — restore the fallback and add legacy-shape test coverage
2. **Fix P0 only** — restore the fallback
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions.
