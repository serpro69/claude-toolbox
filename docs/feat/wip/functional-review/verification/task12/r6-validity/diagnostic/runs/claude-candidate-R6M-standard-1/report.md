## Code Review Summary

**Files reviewed:** 2 files, 2 lines changed (`config.py`, `tests/test_report.py`)
**Overall assessment:** **REQUEST_CHANGES**
**Intent and scope:** The contract is in `README.md`. This increment makes detailed output the default. Explicit plain/detailed overrides, counts and empty-batch reports must keep working ("Empty batches are valid in either mode and produce only `Items: 0`"). I reviewed the staged diff only; there were no unstaged changes. There's no task scope (`docs/feat/wip` doesn't exist).
**Baselines:** The review base is `a210364` (HEAD) and the candidate is the staged index. There's no release baseline: the README says historical installation settings aren't recorded and no deployment is requested.

## Behavior and Compatibility

How it works: `app.report(values, detailed=None)` uses `config.DETAILED_REPORT` when no mode is passed, then calls `stats.summarize` and `formatting.format_summary`.

| Scenario | Before (base) | After (candidate) | Evidence |
|---|---|---|---|
| `report([2, 4])` (default) | `Items: 2` | `Items: 2; Mean: 3` ✅ intended | updated test, passes |
| `report([2, 4], detailed=False)` | `Items: 2` | `Items: 2` ✅ | `test_plain_populated` |
| `report([2, 4], detailed=True)` | `Items: 2; Mean: 3` | same ✅ | `test_detailed_populated` |
| `report([], detailed=False)` | `Items: 0` | `Items: 0` ✅ | `test_plain_empty` |
| **`report([])` (default)** | `Items: 0` | **`ZeroDivisionError`** ❌ | reproduced |
| `report([], detailed=True)` | `ZeroDivisionError` (already broken) | same ❌ | read from source |

- **Explicit overrides:** they still work as before.
- **Default empty batch:** this flow breaks with the change. I ran the four tests on the staged candidate and they pass, but none of them covers an empty batch on the default path.
- **Existing installations:** not assessed. Settings history isn't recorded and no deployment was requested, so this doesn't affect the code verdict.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[stats.py:4 / config.py:1]** Turning detailed mode on by default makes `report([])` crash instead of returning `Items: 0`
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → division by zero, empty collections)
  - Triggered by: content — `.py` extension
  - **What happens:** `summarize` computes `sum(values) / len(values)` with no check for an empty list. Before, only callers who passed `detailed=True` reached that line. Now every default call does, so `report([])` raises `ZeroDivisionError` when the README says it should return `Items: 0`. I reproduced this on the candidate.
  - **Why it's a regression:** detailed mode crashing on an empty batch is an older bug, but this change moves it onto the default path, which is the one most callers use.
  - **Confidence:** 97%. I reproduced the crash, confirmed from the diff that the base default was `False`, and the README states the empty-batch requirement explicitly. The remaining uncertainty is only whether outside callers rely on the default.
  - **Suggested fix:** skip the mean when there are no values. That matches the README ("there is no mean to display"), and `format_summary` already leaves the mean out when it's missing:
    ```python
    if detailed and values:
        result["mean"] = sum(values) / len(values)
    ```

### P2 - Medium

- **[tests/test_report.py:16]** No tests for an empty batch on the default path or in explicit detailed mode
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The test change only covers a non-empty batch, so the suite stays green while a documented requirement fails. Add `report([])` → `Items: 0` and `report([], detailed=True)` → `Items: 0` alongside the P1 fix.
  - **Confidence:** 90%. I read the full test file; neither case appears in it.

### P3 - Low
(none)

---

**Indexed:** I saved one general lesson to the shared review knowledge base (`kk:review-findings`): when a default changes, re-test edge cases like empty input on the new default path. The knowledge base was empty before this, so there was no earlier guidance to check against.

**What I didn't cover:** I worked out the base behavior from source instead of running the old revision. I didn't look at callers outside this repository or at existing installations.

**Required before merge:** the P1 fix and the two empty-batch tests. Tell me if you'd like me to make those changes.
