## Code Review Summary

**Files reviewed**: 1 file (`reader.py`), 4 lines changed (+1/−3), staged
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The README says reads must support both the legacy top-level `address` and the nested `destination.address` "until migration finishes". The stated intent is to tidy up the destination reader. There's no `docs/feat/wip`, so no task scope is available.
**Baselines**: Review base `b299f57` vs. the staged index blob of `reader.py`. The README says no production environment exists, so there's no separate release baseline.

## Behavior and Compatibility

The change deletes the legacy branch from `address_of`. The only caller is `api.list_destinations` (`api.py:5`), which maps every record through `address_of`.

| Scenario | Expected (README) | Candidate result | Evidence |
| --- | --- | --- | --- |
| Supported mixed snapshot `data/records.json` (2 legacy, 1 nested) | All 3 listed | `KeyError: 'destination'`; the whole listing fails | Executed |
| Partway through migration (`migrate_batch(rows, 1)`) | All listed | `KeyError: 'destination'` (legacy-c still unmigrated) | Executed |
| Fully migrated | All listed | All 3 listed correctly | Executed |
| New write via `writer.new_destination` | Listed | Listed | Existing test, passes |
| Empty list | `[]` | `[]` | Existing test, passes |

- **Reads during migration: Blocked.** Migration runs in bounded batches and there's no startup gate, so legacy rows are expected to be present when this code runs. The README explicitly requires the reader to handle both shapes until then.
- **Rollback/reverting: Supported.** The change only touches reads; no stored data is modified.
- **Tests:** `python3 -B -m unittest discover -s tests` passes (2 tests). Both tests build rows with the new writer, so neither covers the legacy shape. A green suite doesn't show the change is safe here.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[reader.py:2]** Dropping the legacy-shape fallback breaks listing for any unmigrated record
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions / Missing error handling)
  - Triggered by: content — `.py` extension
  - **Trigger:** `api.list_destinations` gets any record with only a top-level `address`, as in the supported snapshot or any state partway through migration.
  - **Expected:** That record's address is returned, per the README's dual-read requirement.
  - **Actual:** `row["destination"]` raises `KeyError`. Because the list comprehension covers every row, one legacy record fails the entire response.
  - **Consequence:** Destination listing is unavailable until every batch has run. The stored data stays intact, so this is recoverable and not P0.
  - Confidence: 97%. I reproduced it against `data/records.json` and after a partial `migrate_batch`. The README's contract is explicit and nothing else enforces that migration has finished. The remaining 3% is the possibility of an undocumented completion guarantee, and none is visible in the repo.
  - **Suggested fix:** Unstage this change and restore the two-shape read. Remove the fallback only after migration completion is actually enforced, not just planned. Also add a test that lists a mixed-shape fixture, e.g. `data/records.json` or a legacy row built inline, so this regression gets caught next time.

### P2 - Medium
(none)

### P3 - Low
(none)

---

## Coverage and limits

- **Checked:** the full staged diff; the staged `reader.py` blob; every consumer (`api.py`); `migration.py`, `writer.py`, the snapshot data and the tests. I ran the suite and a reproduction script.
- **Applied checklists:** python security, SOLID, code quality and removal plan, plus the general method. Nothing showed up in security or SOLID for a change this size.
- **Removal-plan view:** this is a deferred removal whose precondition (migration complete and enforced) isn't met yet. It isn't safe to delete now.
- **Knowledge base:** `kk:review-findings` and `kk:lang-idioms` were empty. I indexed this finding under `kk:review-findings` as a recurring pattern: removing the legacy read path before migration completes.

**Recommended action:** unstage or revert `reader.py`. I haven't made any edits. If you want, I can restore the fallback and add the mixed-shape test.
