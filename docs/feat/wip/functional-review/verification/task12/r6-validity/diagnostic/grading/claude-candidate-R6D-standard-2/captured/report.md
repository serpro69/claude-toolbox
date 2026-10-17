I approve the staged change. It switches the count label from "Items:" to "Records:" and changes nothing else, and I found no issues in it.

## Code Review Summary

**Files reviewed**: 2 files, 10 lines changed (5 added, 5 removed)
**Overall assessment**: APPROVE
**Intent and scope**: `README.md:11` says this increment changes the count label from Items to Records, and must keep counts, calculations, how the plain/detailed mode is chosen, and the `; Mean: M` suffix unchanged. No `docs/feat/wip` task docs exist, so there was no task scope to apply. I reviewed the staged diff only (`git diff --cached`); there were no unstaged changes.
**Baselines**: The base is `HEAD` (2b50e59, "Review base") and the candidate is the staged index. No release or deployed version was assessed, and the README says no live deployment is requested.

## Behavior and Compatibility

**Call path**: `app.report` picks the mode (an explicit argument wins, otherwise `config.DETAILED_REPORT`, which is `False`), then calls `stats.summarize`, then `formatting.format_summary`, which calls `format_count`. The diff only touches the string in `formatting.py:2`. `app.py`, `stats.py` and `config.py` are the same in base and candidate.

| Scenario | Expected | Candidate | Evidence |
| --- | --- | --- | --- |
| Plain report, empty batch | `Records: 0` | `Records: 0` | `test_plain_empty`, passed |
| Plain report, `[2, 4]` | `Records: 2` | `Records: 2` | `test_plain_populated`, passed |
| Detailed report, `[2, 4]` | `Records: 2; Mean: 3` | same | `test_detailed_populated`, passed |
| Mode left unset (uses config default) | plain report | `Records: 2` | `test_default_populated`, passed |
| Detailed report, empty batch | not specified by the README | `ZeroDivisionError` at `stats.py:4` | Read from the source, not run; same in base and candidate |

- **Label consumers**: `git grep -i items` (excluding `plugins/`) finds the old label only in the README's description of this change. Nothing else in the repo parses "Items:".
- **Tests**: `python3 -B -m unittest discover -s tests` ran 4 tests and all passed. The worktree matches the index, so this is the staged code.
- **Compatibility**:
  - **Count, mean and mode selection: Supported.** That code is unchanged, and the four tests cover each path.
  - **External tools that parse the old "Items:" output: Unknown.** The README says installation history isn't recorded, and checking them isn't part of this review. The label change is the stated goal, so this does not affect the verdict.
  - **Deployment, migration and rollback: Not applicable.** The change is a string constant and no deployment was requested.

**Pre-existing issue, not caused by this change**: calling `report([], detailed=True)`, or using a setup where `DETAILED_REPORT=True` with an empty batch, divides by zero at `stats.py:4`. The README only defines the mean suffix for non-empty batches. This change neither causes nor worsens it, and with the default config it is only reached when a caller asks for a detailed report explicitly.

**Evidence limits**:
- I wanted to run all five scenarios against both base and candidate with a script, but that command was denied. The empty detailed-report row is based on reading the source only.
- The knowledge base (`kk:review-findings`, `kk:lang-idioms`) was empty.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
(none)

I checked the change against the Python profile checklists (security, SOLID, code quality, removal plan) and the general review method. None of them applied to this change. There were no P0/P1 findings to add to the knowledge base.

No changes are recommended for this increment.
