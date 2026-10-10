Finding indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file, 4 lines changed (reader.py; 1 insertion, 3 deletions)
**Overall assessment**: **REQUEST_CHANGES**

---

## Findings

### P0 - Critical

- **[reader.py:2]** Removal of the legacy-shape fallback breaks reads of un-migrated records
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions — None/missing handling) + removal-plan.md
  - Triggered by: content — `.py` extension (python profile)
  - The diff removes the `if "destination" in row` branch and the `return row["address"]` fallback, leaving `address_of` to unconditionally access `row["destination"]["address"]`. This is **not dead code** — it is load-bearing during an active migration:
    - `README.md:5-8` states a deployment **"must read both shapes until migration finishes. Existing addresses must be preserved."**
    - `data/records.json` currently holds legacy flat records (`legacy-a`, `legacy-c`) that have no `destination` key.
    - `migration.py` migrates only `limit` rows per call with **"no startup migration gate"** (`README.md:11`), so legacy rows are guaranteed to exist at read time.
    - `api.list_destinations` (`api.py:5`) maps `address_of` over *every* record, so listing the current snapshot now raises `KeyError: 'destination'` on the first legacy row.
  - Confidence: 98% — Verified: the removed branch exactly handled the legacy shape; live data fixture still contains that shape; the sole caller iterates all records; README documents the dual-shape contract as mandatory. Residual uncertainty only if the real deployment data were already fully migrated — but the committed fixture and docs say otherwise.
  - Suggested fix: Revert this change. The compatibility branch is a **deferred-removal** item, not an immediate cleanup — it can only be removed after migration completes for all records (telemetry/snapshot showing zero legacy rows). If you want a tidier reader meanwhile:
    ```python
    def address_of(row):
        dest = row.get("destination")
        if dest is not None:
            return dest["address"]
        return row["address"]
    ```

### P1 - High

- **[tests/test_destinations.py:8]** Test suite has no coverage for the legacy shape, masking the regression
  - Profile: generic · Checklist: —
  - Triggered by: —
  - `test_new_write_can_be_listed` only exercises `new_destination` (nested shape) and `test_empty_list` covers the empty case. No test feeds a legacy flat record through `list_destinations`, which is why this P0 passes `unittest`. The dual-shape contract in the README is untested.
  - Confidence: 90% — the test file is not part of this diff, but the coverage gap is what lets the breaking change ship green.
  - Suggested fix: Add a test asserting `list_destinations([{"id": "legacy", "address": "x@example.test"}]) == [{"id": "legacy", "address": "x@example.test"}]`, and ideally one over the mixed `data/records.json` snapshot. This test would fail against the current diff and pass against the fix above.

### P2 - Medium

(none)

### P3 - Low

(none)

---

## Removal/Iteration Plan

Per the removal checklist, the removed branch fails the pre-removal gates:

| Field | Details |
|-------|---------|
| **Item** | Legacy-shape fallback in `address_of` |
| **Why defer** | Active consumers remain — un-migrated records in `data/records.json`; README mandates dual-shape reads until migration completes |
| **Preconditions** | Migration finished for all records; snapshot/telemetry shows zero rows lacking `destination` |
| **Validation** | Legacy-shape test green; full `data/records.json` lists without error |
| **Rollback** | Restore the `if "destination" in row` branch |

---

## Next Steps

I found 2 issues (P0: 1, P1: 1, P2: 0, P3: 0).

The actionable items I recommend fixing:
1. **P0** — Revert the removal in `reader.py` (or use the `.get`-based dual-shape reader); the fallback is required until migration finishes.
2. **P1** — Add a legacy-shape test to `tests/test_destinations.py` so this regression can't recur silently.

Items I recommend keeping as is:
- Nothing — the staged change should not merge in its current form.

**How would you like to proceed?**

1. **Fix all** — I'll revert reader.py and add the legacy-shape test
2. **Fix P0/P1 only** — same as above (both findings are P0/P1)
3. **Fix specific items** — tell me which
4. **No changes** — review complete, no implementation

Please choose an option or provide specific instructions.
