Finding indexed. Here is the review.

## Code Review Summary

**Files reviewed**: 1 file (`reader.py`), 1 insertion / 3 deletions
**Overall assessment**: **REQUEST_CHANGES**

The diff is a three-line deletion, but the deleted lines were load-bearing. Reading the surrounding modules (`migration.py`, `api.py`, `writer.py`, tests) shows the fallback protected an in-progress data migration.

---

## Findings

### P0 — Critical

- **[reader.py:2]** Removing the flat-row fallback breaks reads of not-yet-migrated rows
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions — None/missing-key handling) + removal-plan.md (verify no consumers before removal)
  - Triggered by: content — `.py` extension (python profile)
  - **Before**, `address_of` tolerated two row shapes:
    ```python
    if "destination" in row:
        return row["destination"]["address"]
    return row["address"]          # legacy flat row
    ```
    **After**, it only handles the nested shape, so a legacy flat row raises `KeyError: 'destination'`.
  - This is not a dead branch. `migration.py:migrate_batch` converts flat → nested rows **in bounded batches** (`if migrated >= limit: break`). A batched, limited migrator is the defining signature of an *incomplete* migration: legacy flat rows still exist in the dataset until every batch has run. Meanwhile `api.list_destinations` passes **every** row through `address_of`:
    ```python
    return [{"id": row["id"], "address": address_of(row)} for row in records]
    ```
    So the first legacy row in any list crashes the whole read path with an unhandled `KeyError`.
  - **Confidence: 88%** — Verified: the fallback existed solely for flat rows; a bounded migrator for flat→nested exists; the only caller feeds all rows unconditionally. Residual uncertainty: if the migration is already 100% complete in every environment (no flat rows remain anywhere), this is safe and reduces to dead-code removal. The code gives no such guarantee — the bounded migrator is evidence to the contrary. Treat as P0 until migration completeness is proven; downgrade to a clean removal only once telemetry shows zero flat rows.
  - **Suggested fix** (pick one):
    - **Keep the fallback** until the migration is verified complete (recommended while `migrate_batch` is still in use).
    - If removal is truly intended, first confirm 0 un-migrated rows (telemetry/one-shot full migration), **and** replace the raw `KeyError` with an explicit, diagnosable error, e.g.:
      ```python
      def address_of(row):
          try:
              return row["destination"]["address"]
          except KeyError:
              raise ValueError(f"row missing migrated 'destination': {row.get('id')!r}")
      ```

### P1 — High

- **[tests/test_destinations.py:8]** Test suite does not cover the legacy flat-row path
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions)
  - Triggered by: content — `.py` extension (python profile)
  - Both tests construct rows via `new_destination`, which only ever emits the **nested** shape, plus an empty-list case. No test exercises a flat `{"id": ..., "address": ...}` row — the exact shape the diff stops supporting. That is why this regression passes CI silently.
  - **Confidence: 95%** — directly verified from the test file; `new_destination` never produces a flat row.
  - **Suggested fix**: add a test asserting `list_destinations([{"id": "legacy", "address": "x@y.test"}])` behaves correctly (returns the address, or raises the intended explicit error) — this test should fail on the current diff, which is the point.

### P2 / P3

None.

---

## Removal/Iteration Plan

The removal-plan preconditions are **not met**. Per the checklist: "Searched codebase for all references" and "Feature-flag/telemetry reviewed" — the codebase search surfaces an active `migrate_batch` that still produces/expects flat rows, so there is active evidence that consumers of the fallback remain. The fallback is a *Defer Removal* item, not *Safe to Remove Now*: remove it only after the migration is confirmed complete (0 flat rows), with a guarding test added first.

---

## Next Steps

I found 2 issues (P0: 1, P1: 1, P2: 0, P3: 0).

Actionable items I recommend addressing:
1. **P0** — Restore the flat-row fallback in `reader.py`, OR prove the migration is complete and replace the bare `KeyError` with an explicit error.
2. **P1** — Add a test covering the legacy flat-row path so this regression can't pass CI.

Items to keep as-is:
- Nothing — the single change under review is the source of the regression.

**How would you like to proceed?**

1. **Fix all** — restore the fallback and add the legacy-row test
2. **Fix P0 only** — restore the fallback (or add explicit error after confirming migration status)
3. **Fix specific items** — tell me which
4. **No changes** — if you can confirm the migration is already 100% complete in all environments, I can note that and close the review

If you can tell me whether `migrate_batch` has finished running everywhere (no flat rows remain), I can firm up the P0 severity accordingly.
