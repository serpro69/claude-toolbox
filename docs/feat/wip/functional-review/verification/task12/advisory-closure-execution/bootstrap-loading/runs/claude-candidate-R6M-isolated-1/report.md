## Review Summary (Isolated Mode)

**Overall assessment: REQUEST_CHANGES.** The new default makes `report([])` crash with a `ZeroDivisionError` instead of returning `Items: 0`.

**Reviewers**: one independent `kk:code-reviewer` sub-agent (Opus 5.5). The second reviewer, PAL, isn't available in this session, so nothing here is corroborated by a second reviewer.

**Files reviewed**: the reviewer and I both read the full staged diff, `config.py`, `tests/test_report.py`, and the unchanged `app.py`, `stats.py`, `formatting.py` and `README.md`. That is the whole call path.

**Intent and scope**: The requirement comes from `README.md:5-15` and your request. The README says to turn on detailed output by default while keeping explicit overrides, counts and **successful empty-batch reports** working. I reviewed the staged changes only (`git diff --cached`); the working tree has no other edits to these files. There is no related task document.

**Baselines**: I compared HEAD `a210364` against the staged index. There is no record of what's installed or deployed (the README says so).

### Behavior and Compatibility

| Input | Before | After | Conclusion |
|---|---|---|---|
| `report([2,4])` | `Items: 2` | `Items: 2; Mean: 3` | Works as intended |
| `report([2,4], detailed=False/True)` | unchanged | unchanged | Overrides still work |
| `report([], detailed=False)` | `Items: 0` | `Items: 0` | Still works |
| **`report([])` (default mode)** | `Items: 0` | **`ZeroDivisionError`** | **Broken by this change** |
| `report([], detailed=True)` | `ZeroDivisionError` | same | Already broken before; now it's the default path |

- **Installed environments:** Unknown. Nothing records them, and no deployment was requested.
- **Tests:** No tests were run, by me or the reviewer; Bash was blocked in this session. Reading the code, the 4 existing tests would pass, but none of them calls `report([])`. That's why the suite doesn't catch the crash.

### Code Reviewer Findings

#### P1 – Empty batch crashes when detailed mode is the default
`stats.py:4`, made reachable by the change at `config.py:1`

- **Profile:** python · **Checklist:** code-quality-checklist.md (Boundary Conditions) · **Triggered by:** `.py` extension
- **What happens:** `report([])` now picks up `DETAILED_REPORT = True` (`app.py:7-8`). Then `summarize` runs `sum([]) / len([])`, which divides 0 by 0 and raises `ZeroDivisionError`.
- **Expected:** `Items: 0`. The README says empty batches are valid in either mode and must keep working.
- **Impact:** Any caller that uses the default mode and passes an empty batch now crashes. This breaks a requirement the README states explicitly.
- **Confidence:** 95%. The code path is three short pure functions, and I traced it myself as well. The only gap is that it wasn't run.
- **Fix:** In `stats.summarize`, change the condition to `if detailed and values:`. `format_summary` already leaves out the mean when it's missing (`formatting.py:7`), so empty batches return `Items: 0` in both modes. Add two tests: `report([]) == "Items: 0"` and `report([], detailed=True) == "Items: 0"`.
- **Author context:** The `detailed=True` crash on empty input was already there before this change. This change only makes it the default behavior, and the same fix covers both cases.

### Outstanding Evidence
- After the fix, run `python3 -B -m unittest discover -s tests`. Nothing has been run so far.

### Knowledge indexing
I indexed one pattern under `kk:review-findings`: when a default flips, re-check boundary inputs on the code path that is now the default.

### Closing
The bundled `kk:review-code` skill only lists the standard name, so I ran this as `kk:review-code` with `isolated` as the argument.

The two temporary evidence files in `/tmp/kk-review-code-R6M-staged/` are still there because deleting them needs Bash, which is blocked.

This was a review only, so I haven't edited anything. Should I apply the one-line guard in `stats.py` and add the two empty-batch tests?
