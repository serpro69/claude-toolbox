## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent). The external reviewer didn't run because the `pal` MCP server failed to connect this session, so nothing here is cross-checked by a second model.
**Files reviewed**: 1 file (`reader.py`), 1 line added, 3 removed
**Profile**: python. Applied its security, SOLID, code-quality and removal-plan checklists.

---

### Code Reviewer Findings

- **`reader.py:2`: Removing the legacy fallback makes un-migrated rows crash with `KeyError`**
  - Profile: python · Checklist: security-checklist.md (it's really a correctness and data-availability problem)
  - Severity: **P0** | Confidence: 97%
  - `address_of` now reads only `row["destination"]["address"]`. Legacy rows have a top-level `address` and no `destination` key, so they raise `KeyError: 'destination'`.
  - **I checked this against the repo:**
    - `README.md:5-12` says a deployment must read both shapes until migration finishes, and that there is no startup migration gate.
    - `migration.py` migrates at most `limit` rows per call, and nothing in the repo calls it.
    - In `data/records.json`, the documented supported snapshot, 2 of 3 records (`legacy-a`, `legacy-c`) use the legacy shape.
    - `api.py:5` builds its result in one list comprehension, so a single legacy row makes the whole `list_destinations` call fail. With the bundled snapshot, listing fails outright.
  - **Suggested fix:** keep the two-branch reader. Remove it only after something proves there are zero legacy rows in every store.

- **`tests/test_destinations.py:7-14`: No test covers legacy or mixed-shape reads**
  - Profile: python · Checklist: code-quality-checklist.md
  - Severity: **P1** | Confidence: 90%
  - Both tests use only rows built by `new_destination` or an empty list. That's why the P0 change would pass the test suite. (The reviewer inferred this by reading the code; neither of us ran the tests.)
  - **Suggested fix:** add a test that loads `data/records.json` and asserts all three addresses come back. Add another that reads after a partial `migrate_batch(records, 1)`.

**Removal plan (from the reviewer):** hold off removing the fallback. Conditions before removing it:
- a scan shows zero rows without `destination` in every store;
- `migrate_batch` has been run until it returns 0;
- `data/records.json` and the README's statement that the mixed snapshot is supported have been updated.

Rolling back is just restoring the two lines.

I didn't write this change, so I have no author context to add, and re-reading it turned up nothing new.

**Indexing:** I saved the P0 pattern (compatibility reader removed before migration finishes) to the knowledge base under `kk:review-findings`.

**Housekeeping:** I couldn't delete the temporary diff file `/tmp/kk-review-code-reader-staged.patch` because shell access was denied. You can remove it yourself.

---

## Next Steps

There are 2 findings, both from the code-reviewer only. Nothing is cross-checked because the external reviewer was unavailable.

The actionable items I recommend fixing:

1. **P0:** don't ship this cleanup. Unstage or revert `reader.py` so it keeps reading both shapes. The README explicitly requires dual-shape reads until migration finishes, and the bundled snapshot is mostly legacy rows.
2. **P1:** add mixed-snapshot and partial-migration tests so this regression fails CI next time.

Items I recommend keeping as is: none. Both findings hold up against the repo.

**How would you like to proceed?**

1. **Fix all:** restore the fallback and add the tests
2. **Fix high severity only:** restore the fallback
3. **Fix specific items:** tell me which ones
4. **No changes:** review complete

If you want a second opinion, you could reconnect `pal` and rerun, or run `/kk:review-code` in standard mode.
