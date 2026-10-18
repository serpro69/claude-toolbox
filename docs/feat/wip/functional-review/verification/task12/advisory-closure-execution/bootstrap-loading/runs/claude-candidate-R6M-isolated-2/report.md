## Review Summary (Isolated Mode)

**Verdict: REQUEST_CHANGES.** With detailed reports on by default, calling `report([])` without a mode now crashes with `ZeroDivisionError` instead of returning `Items: 0`. The README says empty-batch reports must keep working, so this breaks the stated contract.

**Reviewers**: one independent reviewer (the `kk:code-reviewer` sub-agent) ran. The second one, the external PAL model, couldn't run because no `pal` tools are available in this session. So nothing is corroborated by two reviewers; the finding rests on the sub-agent plus my own reading of the same source.

**Files reviewed**: `config.py` and `tests/test_report.py` (the changed files), plus `app.py`, `stats.py` and `formatting.py` (unchanged code the change runs through) and `README.md` (the contract).

**Intent and scope**: The README asks this change to turn on detailed output by default while keeping the explicit `detailed=` choice, the counts, and empty-batch reports working. I reviewed your staged changes against HEAD `a210364`; there are no unstaged changes. There's no task document, so there's no task scope.

**Baselines**: At HEAD, `DETAILED_REPORT = False`; the staged version has it `True`. The README says historical installation settings aren't recorded, so I couldn't check older installs, and you didn't ask for that.

### Behavior and Compatibility

| Call | Before | After | Status |
|---|---|---|---|
| `report([2, 4])` (default) | `Items: 2` | `Items: 2; Mean: 3` | Works as intended; covered by the updated test |
| `report([])` (default) | `Items: 0` | **`ZeroDivisionError`** (`stats.py:4`) | **Broken by this change**; no test |
| `report([], detailed=True)` | `ZeroDivisionError` | `ZeroDivisionError` | Already broken before; now it's the default path |
| `report(..., detailed=False)`, empty and populated | unchanged | unchanged | Works; covered by tests |

- **README contract: blocked.** Empty batches no longer report successfully when no mode is passed.
- **Explicit `detailed=True` / `detailed=False` calls: still behave as before.**
- **Existing installations:** unknown, and outside the requested scope.
- **Limits:** this is all from reading the source. I couldn't run the test suite because shell commands were denied in this session.

### Code Reviewer Findings

**P1 — `config.py:1` (root cause in `stats.py:3-4`): the new default makes `report([])` crash**
- Profile: python · Checklist: code-quality-checklist.md (boundary conditions) · Triggered by: `.py` extension
- **What happens:** `report([])` falls back to the config value, which is now `True` (`app.py:7-8`). `summarize` then computes `sum([]) / len([])`, which divides by zero.
- **Expected:** `"Items: 0"` (README lines 9–10 and 13).
- **Why the tests miss it:** they only check the default with a populated batch (`test_report.py:17`). Nothing tests an empty batch in default or detailed mode.
- **Before vs. after:** the default-path crash is new in this change. The explicit `detailed=True` crash on empty input already existed and has the same fix.
- **Confidence:** 95%. The trace is short and fully determined; I'm not at 100% only because it wasn't run.
- **Suggested fix:** in `stats.summarize`, change the condition to `if detailed and values:`. `format_summary` already leaves the mean out when there isn't one, so this returns `Items: 0` with no other changes. Keep the config flip. Add two tests: `report([]) == "Items: 0"` and `report([], detailed=True) == "Items: 0"`.

### Indexing

I saved the general pattern (changing a default sends normal calls down a previously opt-in path with untested edge cases) to the `kk:review-findings` knowledge base.

### Housekeeping

I couldn't delete the temporary files because shell commands were denied. You can remove them yourself:
- `/tmp/kk-review-code-R6M-20261018/` (the patch and change-context notes)
- `/tmp/kk-review-instructions-{mv8xzdcd,xsqxp80b,e7sy20_g}/` (instruction packets)

I didn't edit anything. Should I apply the one-line fix in `stats.py` and add the two empty-batch tests?
