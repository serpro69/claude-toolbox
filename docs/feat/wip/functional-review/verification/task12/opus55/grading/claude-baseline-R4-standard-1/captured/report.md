## Code Review Summary

**Files reviewed**: 1 file (`reader.py`), 1 line added, 3 removed (staged)
**Overall assessment**: **REQUEST_CHANGES**
**Profiles active**: `python` (`reader.py` has a `.py` extension). Its security, SOLID, code-quality and removal-plan checklists were applied.

---

## Findings

### P0 - Critical

- **[reader.py:2]** Removing the legacy-shape fallback breaks reads of rows that haven't been migrated yet
  - Profile: python · Checklist: removal-plan.md, code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - The README says the store holds two shapes at once: legacy top-level `address` and the new nested `destination.address`. `migrate_batch` only converts up to `limit` rows per call, there's no startup gate, and "a deployment must read both shapes until migration finishes." `api.list_destinations` sends every record through `address_of`. With the fallback gone, any legacy row raises `KeyError: 'destination'`. Because the error happens inside a list comprehension, the whole listing fails, not just that row.
  - **Reproduced:** `list_destinations(json.load(open("data/records.json")))` raises `KeyError: 'destination'` on `legacy-a`. That file is the README's "supported mixed snapshot."
  - Against the removal-plan checklist, this is a "Defer removal" item, not "Safe to remove now." The code still has active consumers (the 2 of 3 rows in the snapshot that are unmigrated), and the precondition (migration finished) isn't met.
  - Confidence: 98%. I confirmed it by running the code, and the README states the contract explicitly. Remaining uncertainty: none for this repo, since the README says there's no separate production store.
  - Suggested fix: unstage this change and keep the dual read. If the goal is just tidier code, this keeps the behaviour:
    ```python
    def address_of(row):
        if "destination" in row:
            return row["destination"]["address"]
        return row["address"]
    ```
    Remove the fallback only after a check confirms that no record still lacks `destination`.

### P2 - Medium

- **[tests/test_destinations.py]** No tests cover legacy or mixed-shape reads, so the test suite stays green despite the P0
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - `python3 -B -m unittest discover -s tests` passes (2 tests, OK) with the regression staged. Both tests only use new-shape rows from `writer.new_destination`.
  - Confidence: 95%. I ran the suite and read both tests.
  - Suggested fix: add a test that lists a legacy-only row and one that lists the `data/records.json` mixed snapshot. Optionally add one that lists records after a partial `migrate_batch(records, 1)`.

### P1 / P3

None.

---

## Removal/Iteration Plan

**Defer: dropping the legacy `address` fallback in `address_of`**

| Field | Details |
|---|---|
| Location | `reader.py:1-4` (original) |
| Why defer | Unmigrated rows still exist; batched migration has no completion gate |
| Preconditions | Every record has `destination`, checked by a scan or by `migrate_batch` returning 0 on a full pass |
| Validation | A mixed-snapshot test passes before the change; after migration, a scan finds no top-level `address` |
| Rollback | Restore the `if "destination" in row` branch |

**Indexing:** I saved the P0 pattern (removing dual-shape read support while a batched migration is still running) to the knowledge base as `kk:review-findings`.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

What I recommend fixing:
1. **P0:** restore the legacy-shape fallback in `reader.py` (or unstage the change).
2. **P2:** add tests for legacy-row and mixed-snapshot reads.

**How would you like to proceed?**

1. **Fix all**: I'll implement both fixes.
2. **Fix P0/P1 only**: restore the fallback only.
3. **Fix specific items**: tell me which.
4. **No changes**: the review is complete.
