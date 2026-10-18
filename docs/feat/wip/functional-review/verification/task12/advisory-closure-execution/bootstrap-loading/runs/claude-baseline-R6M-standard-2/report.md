## Code Review Summary

**Files reviewed**: 2 files, 2 lines changed (staged: `config.py`, `tests/test_report.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Active profile**: `python` (both files are `.py`). Applied its security, SOLID, code-quality and removal checklists.

---

## Findings

### P0 - Critical

- **[stats.py:4]** Calling `report([])` with the default mode now crashes with `ZeroDivisionError`
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → Division by zero / Empty collections)
  - Triggered by: content — `.py` extension
  - `summarize` runs `sum(values) / len(values)` whenever `detailed` is true. Before this change, only `report([], detailed=True)` hit that line. With `DETAILED_REPORT = True`, every caller that leaves out `detailed` hits it too, so `report([])` goes from returning `"Items: 0"` to raising. The README says "Empty batches are valid in either mode and produce only `Items: 0`" and asks this change to keep empty-batch reports working, so this breaks the contract.
  - Confidence: 99%. I reproduced it: `python3 -B -c 'from app import report; print(report([]))'` raises `ZeroDivisionError: division by zero`. The test suite still passes (4/4 OK) because no test covers an empty batch in detailed or default mode.
  - Suggested fix: skip the mean when there are no values. `format_summary` already leaves out the mean when the key is missing, so the output becomes `Items: 0`:
    ```python
    if detailed and values:
        result["mean"] = sum(values) / len(values)
    ```

::code-comment{file="stats.py" line="4" severity="P0"}
With DETAILED_REPORT now True, report([]) reaches this division by default and raises ZeroDivisionError. That breaks the README rule that empty batches produce "Items: 0" in either mode. Guard with `if detailed and values:`.
::

### P1 - High

(none)

### P2 - Medium

- **[tests/test_report.py:16]** No tests for empty batches in default or detailed mode
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The updated test covers only the populated default case. Nothing checks `report([])` or `report([], detailed=True)`, which is how the P0 above got through with a green suite.
  - Confidence: 95%. Checked all four tests; none pass an empty list except `test_plain_empty`, which forces `detailed=False`.
  - Suggested fix: add `test_detailed_empty` (`report([], detailed=True) == "Items: 0"`) and `test_default_empty` (`report([]) == "Items: 0"`).

### P3 - Low

(none)

---

## Additional Suggestions

- `test_default_populated` depends on the value checked into `config.py`. That's fine as a regression guard for this change, but it will need editing every time the default flips. It's acceptable as is.
- Callers that leave out `detailed` will now get `; Mean: …` added to their output. That's the intended change, but the README says past installation settings aren't recorded, so check whether any downstream code parses the exact `Items: N` string.

What I checked: the diff, `app.py`, `stats.py`, `formatting.py`, the README contract, and a full test run. No security, SOLID or removal issues apply to a one-line config flip.

Indexed: the P0 pattern (turning a flag on by default exposes edge-case bugs that were only reachable when opted in) is saved as `kk:review-findings`.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

The actionable items I recommend fixing:
1. P0: guard the mean calculation in `stats.py:4` for empty input
2. P2: add empty-batch tests for detailed and default modes

**How would you like to proceed?**

1. **Fix all**: I'll make both fixes
2. **Fix P0/P1 only**: just the `stats.py` guard
3. **Fix specific items**: tell me which ones
4. **No changes**: the review is complete and I won't change anything
