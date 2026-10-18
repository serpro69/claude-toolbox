## Code Review Summary

**Files reviewed**: 2 staged files (`config.py`, `tests/test_report.py`), 2 lines changed. I also read `app.py`, `stats.py`, `formatting.py` and `README.md` for context.
**Active profile**: `python`, because the changed files end in `.py`. I applied all four of its checklists: security, SOLID, code quality and removal.
**Overall assessment**: **REQUEST_CHANGES**

The four existing tests pass, but the change breaks the README rule for empty batches.

---

## Findings

### P0 - Critical

- **[stats.py:4]** With detailed reports on by default, `report([])` now crashes with `ZeroDivisionError`
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → division by zero, empty list not handled)
  - Triggered by: content — `.py` extension
  - `config.py:1` now makes the detailed mode the default, so `report(values)` with no mode argument runs `summarize(values, detailed=True)`. That function computes `sum(values) / len(values)` without checking for an empty list. Before this change, the bug only showed up if a caller passed `detailed=True` explicitly. Now every default call with an empty batch crashes. `README.md:9-13` says empty batches are valid in either mode, must return `Items: 0`, and that this change must keep empty-batch reports working.
  - Confidence: 98%. I reproduced it: `python3 -B -c "from app import report; report([])"` raised `ZeroDivisionError: division by zero`. The tests still pass because none of them covers an empty batch in the default or detailed mode.
  - Suggested fix: only compute the mean when there are values. `formatting.py` already leaves out the mean when it's missing, so the output becomes `Items: 0`:
    ```python
    if detailed and values:
        result["mean"] = sum(values) / len(values)
    ```

### P2 - Medium

- **[tests/test_report.py:16]** No test covers the default empty-batch case
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The test file updates the populated default case but adds nothing for the new default's edge cases. That gap is why the P0 bug got through with all tests passing.
  - Confidence: 95%. The four tests cover plain empty, plain populated, detailed populated and default populated. Nothing covers default empty or detailed empty.
  - Suggested fix: add tests that `report([])` and `report([], detailed=True)` both return `"Items: 0"`.

### P1 / P3

(none)

---

**What else I checked:** I found no security issues (no input or output handling, secrets, or deserialization involved) and no SOLID or removal concerns. Passing `detailed=False` or `detailed=True` still overrides the default as the README requires.

**Indexing:** The P0 is a repeatable pattern: turning on a non-default path by default exposed an untested edge case in it. I saved it to the knowledge base under `kk:review-findings`.

---

## Next Steps

I found 2 issues (P0: 1, P1: 0, P2: 1, P3: 0).

The fixes I recommend:
1. P0: in `stats.summarize`, only compute the mean when the batch isn't empty.
2. P2: add tests for empty batches in the default and detailed modes.

**How would you like to proceed?**

1. **Fix all**: I'll make both fixes.
2. **Fix P0/P1 only**: I'll only fix the empty-batch crash.
3. **Fix specific items**: tell me which issues to fix.
4. **No changes**: the review is complete and nothing needs changing.
