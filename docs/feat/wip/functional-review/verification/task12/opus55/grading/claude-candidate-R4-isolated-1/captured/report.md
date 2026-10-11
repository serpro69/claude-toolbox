## Code review (isolated mode): staged `reader.py` cleanup

**Verdict: REQUEST_CHANGES.** The cleanup removes the fallback for old-shape records, so `list_destinations` crashes on the supported mixed snapshot and stays down until migration finishes. That breaks a requirement written in the README.

**Reviewers:** only one of the two ran. The code-reviewer sub-agent (claude-opus-5-5) finished and its reported coverage matches the evidence I gave it. The external PAL reviewer didn't run because its server failed to connect this session, so no finding is confirmed by two reviewers.

**What was reviewed:** the staged change only (there were no unstaged changes): `reader.py`, 1 line added and 3 removed. The staged and working-tree copies are identical, and the base is `b299f57`. Both reviewers also read the code that calls or depends on it: `api.py`, `migration.py`, `writer.py`, `data/records.json`, `tests/test_destinations.py` and the README.

**Requirements:** they come from `README.md:5-12`: read both record shapes until migration finishes, keep reads available while migration runs in batches, there's no startup migration gate, and existing addresses must be preserved. Your message gave no other rationale, so I've assumed the intent was "read only the new nested shape". There's no task document, and the README says there's no deployed or production environment to compare against.

### What happens in each state
| State | Expected | With this change |
|---|---|---|
| Mixed snapshot `data/records.json` (2 old-shape, 1 new) | 3 entries | `KeyError: 'destination'`, the whole list fails |
| Partway through migration (after `migrate_batch(records, 1)`) | 3 entries | `KeyError` on `legacy-c` |
| Fully migrated | 3 entries | Works |
| New write / empty list | Works | Works (both existing tests cover only these) |
| Rollback | Old behaviour back | Works: the reader writes nothing, so reverting is enough |

These results come from reading the code. No tests were run: Bash execution was blocked in this session, and the sub-agent only reads files.

### Findings from the code-reviewer

**P1: old-shape read removed before migration finishes** (`reader.py:2`)
- **Where it breaks:** `api.list_destinations` (`api.py:5`) calls `address_of(row)`, which does `row["destination"]` and raises an uncaught `KeyError`. Because the whole list is built in one expression, a single old-shape record means no records are returned at all, including new-shape ones.
- **What the README requires:** both shapes stay readable during the batched migration (README:7-8, 10-11). Nothing like a migration gate or flag prevents the new code from meeting unmigrated data.
- **Not P0:** stored data isn't touched, and reverting the change fixes it.
- **Confidence:** 97%. I confirmed it in `reader.py` (the staged copy). The remaining uncertainty is only that nothing was executed.
- **Fix:** keep the old fallback until migration is confirmed complete:
  ```python
  def address_of(row):
      if "destination" in row:
          return row["destination"]["address"]
      return row["address"]
  ```

**P3: no tests for old-shape or mixed records** (`tests/test_destinations.py:8-14`)
- This gap already existed before your change, but it's why the regression wouldn't show up: the test suite would still pass with this change.
- **Confidence:** 90%.
- **Fix:** load `data/records.json` and check that all three id/address pairs come back:
  - before migration;
  - after `migrate_batch(records, 1)`;
  - after migration is complete.

The sub-agent also flagged a possible issue in existing code at `migration.py:7`: `pop` runs before the nested `destination` is assigned, so a concurrent reader could briefly see neither key. Nothing in the code runs concurrently and this change didn't introduce it, so I'm not counting it as a finding.

### Before the nested-only reader can ship
- Migration must be finished: `migrate_batch` returns 0 and no record lacks `destination`. The README doesn't define a completion signal.
- Removing the fallback is follow-up work with no owner or tracking place yet. It should be recorded wherever you track work.

### Housekeeping
- **Knowledge base:** it was empty, so there were no earlier findings to compare with. I saved this pattern (removing an old-shape read during a batched migration) under `kk:review-findings`.
- **Temporary files:** I couldn't remove them because Bash was blocked. You can delete these directories:
  - `/tmp/kk-review-code-isolated-reader`
  - `/tmp/kk-review-instructions-fr7ifb78`
  - `/tmp/kk-review-instructions-uyfx1a8l`
  - `/tmp/kk-review-instructions-ahr98tr0`

This was a review only and I haven't changed anything. Do you want me to restore the fallback in `reader.py` and add the mixed-snapshot tests?
