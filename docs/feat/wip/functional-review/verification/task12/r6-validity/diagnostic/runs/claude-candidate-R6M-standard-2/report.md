## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`config.py`, `tests/test_report.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: `README.md` says this increment makes detailed reports the default. It must keep explicit plain/detailed overrides, counts, and empty-batch reports (`Items: 0` in either mode) working. There are no task docs, so there is no task scope. I reviewed the staged diff only; there were no unstaged changes.
**Baselines**: Review base is `a210364` (HEAD) and the candidate is the staged index. The README says historical installation settings aren't recorded, so there's no separate release baseline.

## Behavior and Compatibility

The flag is used in one place: `report()` (`app.py:6-10`) falls back to `DETAILED_REPORT` when `detailed` is omitted. It passes the result to `summarize()` (`stats.py`), and `format_summary()` (`formatting.py`) adds the mean only when `"mean"` is in the summary.

| Scenario (README contract) | Before | Candidate | Evidence |
| --- | --- | --- | --- |
| `report([2, 4])` (default, populated) | `Items: 2` | `Items: 2; Mean: 3` ✅ intended | test + reproduction |
| `report([2, 4], detailed=False)` | `Items: 2` | `Items: 2` ✅ | test |
| `report([2, 4], detailed=True)` | `Items: 2; Mean: 3` | unchanged ✅ | test |
| `report([], detailed=False)` | `Items: 0` | `Items: 0` ✅ | test + reproduction |
| **`report([])` (default, empty)** | `Items: 0` | **`ZeroDivisionError`** ❌ | reproduction |
| `report([], detailed=True)` | `ZeroDivisionError` | `ZeroDivisionError` ❌ (already broken before this change) | source |

- **Explicit overrides**: still work. Both modes are tested and pass.
- **Default empty batch**: **Blocked.** This change breaks it.
- **Deployed installations**: **Not applicable.** The README says no live deployment is requested and installation history isn't recorded.

`python3 -B -m unittest discover -s tests` ran 4 tests and all passed. None of them covers an empty batch on the default or detailed path.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[stats.py:4] Default `report([])` now raises `ZeroDivisionError` (triggered by `config.py:1`)**
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions: division by zero / empty collections)
  - Triggered by: content: `.py` extension
  - **Trigger/path:** `report([])` → `detailed = DETAILED_REPORT` (now `True`) → `summarize([], detailed=True)` → `sum([]) / len([])`.
  - **Expected vs actual:** The README says empty batches are valid in either mode and return `Items: 0`. Before the change they did on the default path. Now the call raises `ZeroDivisionError: division by zero`; I reproduced this directly.
  - **Consequence:** Every caller that relies on the default mode now crashes on an empty batch instead of getting a successful report. The missing guard in `summarize()` already existed (explicit `detailed=True` failed the same way). Flipping the default moves it onto the main path. The updated test only covers a populated batch, so the suite stays green.
  - **Confidence: 97%.** Reproduced on the staged code and matched against the README. The only open question is whether any real caller sends empty batches, but the README explicitly promises they're valid.
  - **Suggested fix:** Skip the mean when there are no values:
    ```python
    if detailed and values:
        result["mean"] = sum(values) / len(values)
    ```
    `format_summary()` already prints just `Items: 0` when there's no `"mean"`, so this also fixes the explicit `detailed=True` case. Add `report([])` and `report([], detailed=True)` tests, both expecting `"Items: 0"`.

### P2 / P3

(none)

---

**Coverage and limits:** I read every tracked source file, the README contract, and the staged diff, ran the test suite, and reproduced the scenarios above. The only consumer of `DETAILED_REPORT` and `report()` in the repository is `app.py`; I didn't check any callers outside it. No security, SOLID, or removal concerns apply to a one-constant change.

**Indexing:** The pattern behind the P1 (flipping a default puts an opt-in branch's missing boundary check on the default path) is indexed as `kk:review-findings`. The knowledge base was empty before this.

**Next step:** Fix the P1 with the guard in `stats.py` and the two empty-batch tests above. This was a review only, so I haven't changed anything. Do you want me to apply the fix?
