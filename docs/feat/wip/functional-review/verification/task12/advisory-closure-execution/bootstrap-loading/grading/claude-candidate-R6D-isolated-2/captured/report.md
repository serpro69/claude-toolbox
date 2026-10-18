## Review Summary (Isolated Mode)

**Verdict: APPROVE.** This covers the staged code only. I couldn't run the tests, so that approval rests on reading the source.

**Reviewers**:
- The `kk:code-reviewer` sub-agent finished. It confirmed it loaded all 8 instruction files before looking at any evidence.
- PAL could not run. No `pal` tools are installed in this session, so there is no second reviewer and no finding below counts as corroborated.

**Files reviewed**: `formatting.py`, `tests/test_report.py` (5 lines changed each way), plus the unchanged `app.py`, `stats.py`, `config.py` and `README.md`. Both the sub-agent and I read all of them.

**Intent and scope**: `README.md` lines 11–15 say this change renames the count label from "Items" to "Records". Counts, calculations, mode selection and the `; Mean:` suffix must stay the same. I reviewed only the staged changes, since nothing was unstaged. The worktree matches the index, so the files on disk are what's being reviewed. There's no task or feature design doc.

**Baselines**: I compared against HEAD `2b50e59`. There's no record of a released or deployed version; the README says installation settings aren't recorded.

### Behavior and Compatibility
The call chain is `app.report` → `stats.summarize` → `format_summary` → `format_count`. The only production change is the string at `formatting.py:2`.

| Scenario | Expected | Result | Source |
|---|---|---|---|
| `report([], detailed=False)` | `Records: 0` | ✔ | `test_plain_empty` |
| `report([2,4], detailed=False)` | `Records: 2` | ✔ | `test_plain_populated` |
| `report([2,4], detailed=True)` | `Records: 2; Mean: 3` | ✔ | `test_detailed_populated` |
| `report([2,4])` with the default setting (`False`) | `Records: 2` | ✔ | `test_default_populated` |
| `report([], detailed=True)` | Probably `Records: 0`, going by the README | `ZeroDivisionError`, before and after this change | Not tested (see the finding below) |

- **Counts, mean calculation, mode selection and suffix are unchanged:** confirmed. The diff only replaces the label text.
- **Nothing else in the repo uses the old label:** confirmed. Searching for `Items` and the formatting functions found only the tests and the README.
- **Outside code that reads the `Items:` text:** unknown. That breakage is the point of the rename, but whether any external parser depends on it hasn't been checked.
- **Deployment and activation:** not applicable. No deployment is requested and no config changes.
- **Tests:** not run. I wasn't allowed to run shell commands in this session, and the sub-agent has no shell. The new assertions match the output I traced through the code.

### Code Reviewer Findings
- **[stats.py:4]** A detailed report on an empty batch raises `ZeroDivisionError`. This bug predates your change and isn't made worse by it.
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions) · Triggered by: `.py` extension
  - **Severity:** code-reviewer rated it P2 with 90% confidence. The only doubt is what an empty detailed report should print, which the README implies but doesn't spell out.
  - **How it happens:** `report([], detailed=True)` computes `sum([]) / len([])`. Plain `report([])` would crash the same way in any installation that sets `DETAILED_REPORT = True`.
  - **Expected vs actual:** the README (lines 7–9) says the mean is added only for non-empty batches, so this should probably print `Records: 0`. It raises instead.
  - **Suggested fix, as a separate change:** change the guard in `summarize` to `if detailed and values:` and add a test that `report([], detailed=True) == "Records: 0"`. It shouldn't hold up this change.

I independently traced this code path and reached the same result.

### Outstanding Evidence and Prerequisites
- **Run the tests:** `python3 -B -m unittest discover -s tests` against the staged changes. This would confirm the result, not change the verdict.
- **Before release:** check that no outside consumer reads the `Items:` text, and confirm which installations set `DETAILED_REPORT`. Both are outside this code review.

**Knowledge base:** nothing to record. There are no P0 or P1 findings, and the knowledge base was empty, so I used the standard checklists.

**Cleanup not done:** because shell access was denied, I couldn't delete the temporary review files. You can remove `/tmp/kk-review-code-r6d2-evidence/` and `/tmp/kk-review-instructions-{kzs1msse,50xg0kg1,1hsh1d9d}/`. None of them contain source code from your repo.

No changes are needed to the staged label change. For the existing empty-batch crash, should I fix it as a separate change or add a short review note for it?
