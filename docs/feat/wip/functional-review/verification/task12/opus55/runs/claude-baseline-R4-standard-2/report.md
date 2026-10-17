## Code Review Summary

**Files reviewed**: 1 file (`reader.py`), 1 line added and 3 removed (staged)
**Overall assessment**: **REQUEST_CHANGES**. This change breaks reads of records that haven't been migrated yet.

Only the `python` profile applied. I checked the change against its security, SOLID, code-quality and removal checklists.

---

## Findings

### P0 - Critical

- **[reader.py:2]** The fallback for old-format records was removed before the migration has finished
  - Profile: python · Checklist: removal-plan.md / code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - **Problem:** `address_of` now always reads `row["destination"]["address"]`. Any record still in the old format (`address` at the top level) raises `KeyError`. `api.list_destinations` builds its whole list in one comprehension, so a single old-format record makes the entire listing fail, not just that row.
  - The README requires reading both shapes: "a deployment must read both shapes until migration finishes", "there is no startup migration gate", and `data/records.json` is "a supported mixed snapshot". `migrate_batch` only converts up to `limit` rows per call, so old-format rows are expected to exist while it runs.
  - **Confirmed by running it:** `list_destinations(json.load(open("data/records.json")))` → `KeyError: 'destination'` (`legacy-a` and `legacy-c` are still in the old format).
  - Confidence: 98%. I reproduced it on the supported snapshot, and the README states the contract outright. The 2% covers the chance the migration has finished somewhere I can't see, but the repo shows no sign of that.
  - **Fix:** Drop this change and keep the fallback until removal is safe (see plan below). If you want to tidy it in the meantime, keep both shapes: `if "destination" in row: return row["destination"]["address"]` / `return row["address"]`.

### P2 - Medium

- **[tests/test_destinations.py]** No test covers old-format records, which is why the suite still passes
  - Profile: python · Checklist: code-quality-checklist.md
  - Triggered by: content — `.py` extension
  - The tests only cover new-format writes and an empty list, so they pass (`Ran 2 tests … OK`) even though the snapshot can't be read.
  - Confidence: 95%. I ran the suite and it passed despite the breakage.
  - **Fix:** Add a test that runs `list_destinations` on an old-format row, or on `data/records.json`, and checks every address comes back unchanged. Ideally also check that `migrate_batch` keeps the output identical.

### P1 / P3

None.

---

## Removal/Iteration Plan

The fallback should be **deferred, not deleted now**:

| Field | Details |
|---|---|
| Location | `reader.py:2–4` (the old-format branch) |
| Why defer | Old-format rows still exist (`data/records.json`), the migration is incremental, and there's no startup gate |
| Preconditions | 1. The migration has converted every row (checked: no row lacks `destination`). 2. The mixed snapshot is converted or retired. 3. The README's both-shapes requirement is updated. |
| Verification | The old-format regression test passes before removal. After removal, update that test along with the README. |
| Rollback | Restore the two-line fallback. |

## Indexing

The P0 is a reusable pattern (removing a compatibility read before an incremental migration finishes), so I added it to the `kk:review-findings` knowledge base.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

What I recommend fixing:
1. **P0:** unstage or revert the `reader.py` change and keep the fallback for old-format records.
2. **P2:** add a regression test that reads old-format and mixed records.

**How would you like to proceed?**

1. **Fix all**: revert the reader change and add the regression test
2. **Fix P0/P1 only**: just restore the fallback
3. **Fix specific items**: tell me which
4. **No changes**: review complete
