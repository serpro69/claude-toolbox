## Review Summary (Isolated Mode)

**Overall assessment: REQUEST_CHANGES.** The staged change breaks reads for any record that hasn't been migrated yet. It only works once every row is in the new shape.

**Reviewers:** only one ran. The `kk:code-reviewer` sub-agent completed. PAL could not be the second reviewer because its MCP server failed to connect this session, so there are no corroborated findings. Please reconnect PAL and rerun if you want the second opinion.

**Files reviewed:** `reader.py` (staged: 1 line added, 3 removed). Both the reviewer and I also read `README.md`, `api.py`, `migration.py`, `writer.py`, `data/records.json` and `tests/test_destinations.py`.

**Intent and scope:** there's no spec or task document, so I took the intent from your description: remove the old-shape branch from `address_of`. The rules come from `README.md`. I reviewed only the staged changes; there were no unstaged ones.

**Baselines:** the review base is HEAD `b299f57` and the candidate is the staged version. The README describes a local JSON model with no deployed environment, so there's no deployment to compare against.

### Behavior and Compatibility

| Scenario | Expected | Result with this change | Conclusion |
|---|---|---|---|
| Listing the shipped mixed snapshot `data/records.json` | 3 addresses | `KeyError: 'destination'` on `legacy-a`; the whole call fails | **Blocked** (I reproduced it) |
| Listing after `migrate_batch(records, 1)` | 3 addresses | `KeyError` on `legacy-c` | **Blocked** (traced in the source) |
| Listing after a full migration | 3 addresses | Works | Supported (traced in the source) |
| Listing a new write, or an empty list | Listed / `[]` | Works | Supported (the 2 existing tests pass) |
| Reverting the change | Old behavior back | `address_of` only reads data, so no stored data is lost | Supported |

### Code Reviewer Findings

**P1: `reader.py:2` no longer reads old-shape records, which breaks `list_destinations` for mixed and partly migrated data**
- **What happens:** any row that still has a top-level `address` makes `api.list_destinations` (`api.py:5`) call `address_of`, which looks up `row["destination"]` and raises `KeyError`. One bad row fails the whole list, including rows already in the new shape.
- **What the README says:** "a deployment must read both shapes until migration finishes" (line 8). `data/records.json` is a "supported mixed snapshot" (line 10). Migration runs in limited batches with no startup gate (lines 11–12).
- **Why it's P1, not P0:** no data is lost and reverting fixes it, but it breaks an explicit requirement.
- **Confidence:** 97%, because the failure is deterministic. I reproduced the traceback against `data/records.json`.
- **Fix:** restore the `if "destination" in row` fallback. Add tests that list the mixed snapshot and list after a partial migration; the current tests only cover new-shape rows, which is why they still pass.
- **Removing the fallback later:** wait until migration is confirmed complete (no rows without `destination`) and the README no longer promises reads of both shapes. Nobody owns this yet and it isn't tracked anywhere.

### Coverage and limits
- I ran the two existing tests (both pass) and a one-off script that listed the snapshot. The reviewer only read the source.
- Rows with neither shape fail in both the old and new code, so this change didn't cause that. The reviewer noted it but didn't report it as a finding.
- I saved this pattern to the knowledge base under `kk:review-findings`, since it's a likely repeat mistake: dropping the old-shape fallback while a migration is still running.
- I couldn't delete the temporary review files: Bash was blocked for `rm`. They're in `/tmp/kk-review-code-pvjSVj` and three `/tmp/kk-review-instructions-*` folders, and you can delete them safely.

### Next step
The staged change should be reverted, or left unstaged until migration is finished. Want me to restore the fallback and add the mixed-snapshot and partial-migration tests?
