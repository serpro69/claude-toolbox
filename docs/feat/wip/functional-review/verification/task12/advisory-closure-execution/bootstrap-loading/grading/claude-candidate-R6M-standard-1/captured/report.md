## Code Review Summary

**Files reviewed**: 2 files, 4 lines changed (`config.py`, `tests/test_report.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The contract is in `README.md`. This increment should turn on detailed output by default and still keep explicit plain/detailed overrides, counts, and **successful empty-batch reports**. There's no `docs/feat/wip` task scope, so I reviewed the diff against the README contract.
**Baselines**: I compared `HEAD` (a210364, "Review base") with the **staged** index. There were no unstaged changes. I didn't assess any release or deployed baseline; the README says installation settings aren't recorded and no deployment is requested.

## Behavior and Compatibility

I traced `app.report` → `stats.summarize` → `formatting.format_summary`. Scenario rows:

| Scenario | Before (HEAD) | Candidate (staged) | Contract | Status |
| --- | --- | --- | --- | --- |
| `report([2, 4])` (default) | `Items: 2` | `Items: 2; Mean: 3` | detailed by default | Supported (intended) |
| `report([2, 4], detailed=False)` | `Items: 2` | `Items: 2` | preserve override | Supported |
| `report([2, 4], detailed=True)` | `Items: 2; Mean: 3` | same | preserve override | Supported |
| `report([], detailed=False)` | `Items: 0` | `Items: 0` | `Items: 0` | Supported |
| **`report([])` (default)** | `Items: 0` | **`ZeroDivisionError`** | `Items: 0` | **Blocked: introduced regression** |
| `report([], detailed=True)` | `ZeroDivisionError` | `ZeroDivisionError` | `Items: 0` | Blocked: existing bug, now on the default path |

- **Callers using the default mode:** blocked for empty batches. They also get the intended format change for populated batches.
- **Installed settings:** Unknown. Historical installation settings aren't recorded. This is outside the requested review and doesn't change the verdict.

**Evidence limits:** The verdict comes from reading the source only. I could not run tests because Bash was denied partway through the review. That means I haven't seen `python3 -B -m unittest discover -s tests` pass or fail on the staged state. Reading the code, I expect the 4 existing tests to pass, because none of them covers an empty batch on the default or detailed path.

---

## Findings

### P0 - Critical

(none)

### P1 - High

- **[stats.py:4]** Default reports now crash on empty batches
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → Division by zero; Empty collections)
  - Triggered by: content — `.py` extension (`config.py`, `tests/test_report.py`)
  - **How it fails:** `report([])` with no `detailed` argument now picks up `DETAILED_REPORT = True` (`config.py:1`, read via `app.py:7-8`). It then calls `summarize([], detailed=True)`, which computes `sum([]) / len([])`. **Expected:** `"Items: 0"` (README lines 9–10 and 13: "Empty batches are valid in either mode", "Preserve … successful empty-batch reports"). **Actual:** `ZeroDivisionError`. Any caller using the default mode that passes an empty batch now crashes instead of getting a report. The missing guard was already in the code, but it was only reachable through an explicit `detailed=True`. This change puts it on the default path, so it's a regression introduced by the increment.
  - **Confidence:** 95%. I followed every line of the three-function call chain. `format_summary` already omits the mean when the `"mean"` key is absent, so the fix fits the existing design. The remaining uncertainty is only that I couldn't run the tests.
  - **Suggested fix:** Only compute the mean when there are values. This also fixes the existing `detailed=True` empty case:
    ```python
    def summarize(values, detailed=False):
        result = {"count": len(values)}
        if detailed and values:
            result["mean"] = sum(values) / len(values)
        return result
    ```
    Add tests for the contract rows that are currently missing:
    ```python
    def test_default_empty(self):
        self.assertEqual(report([]), "Items: 0")

    def test_detailed_empty(self):
        self.assertEqual(report([], detailed=True), "Items: 0")
    ```

::code-comment{file="stats.py" line="4" severity="P1"}
With DETAILED_REPORT now True, `report([])` reaches `sum([]) / len([])` and raises ZeroDivisionError, which breaks the README contract that empty batches produce `Items: 0` in either mode. Guard with `if detailed and values:` and add default-empty and detailed-empty tests.
::

### P2 - Medium

(none)

### P3 - Low

(none)

---

**Other checks (no issues):** The flag flip and the updated `test_default_populated` expectation (`"Items: 2; Mean: 3"` via `:g`) are correct. `from config import DETAILED_REPORT` is read at import time, which matches how it's used. The python security, SOLID and removal checklists found nothing that applies to this diff.

**Indexing:** I indexed one systemic P1 pattern as `kk:review-findings`: flipping a default flag puts a hidden bug from an opt-in path onto the default path.

**Next step:** Apply the guard and the two tests above in `stats.py` and `tests/test_report.py`, then run `python3 -B -m unittest discover -s tests`. This was a review-only request, so I haven't edited anything. Want me to make the fix?
