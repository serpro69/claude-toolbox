## Code Review Summary

**Files reviewed**: 2 files, 2 lines changed (`config.py`, `tests/test_report.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: The goal, from `README.md`, is to make detailed output the default. The README also requires that explicit plain/detailed overrides keep working, that counts stay correct, and that empty batches keep reporting successfully as `Items: 0` in either mode. The diff is the staged changes. There are no unstaged changes, so the working tree matches what's staged. There's no task-scope document, so I reviewed the diff on its own merits against that README contract.
**Baselines**: The base is `HEAD` (`a210364`) and the candidate is the staged index. There's no release or deployed baseline: the README says installation settings aren't recorded and no deployment is requested.

## Behavior and Compatibility

I traced `report()` (`app.py`) through `summarize()` (`stats.py`) to `format_summary()` (`formatting.py`). The scenarios below come from reading the source, except where marked as executed:

| Scenario | Base | Candidate | Contract |
|---|---|---|---|
| `report([2, 4])` (default) | `Items: 2` | `Items: 2; Mean: 3` | ✅ intended change |
| `report([2, 4], detailed=False/True)` | plain / detailed | unchanged | ✅ overrides preserved |
| **`report([])` (default)** | `Items: 0` | **`ZeroDivisionError`** | ❌ regression |
| `report([], detailed=True)` | `ZeroDivisionError` | same | ❌ already broken before this change; same root cause |
| `report([], detailed=False)` | `Items: 0` | unchanged | ✅ |

- **Executed:** `python3 -B -m unittest discover -s tests` ran 4 tests, all passed. None of them exercises an empty batch in default or detailed mode, so the suite can't catch this regression.
- **Not executed:** my ad-hoc script comparing base and candidate on empty input was denied. The empty-batch rows above come from reading the code, not from running it.
- **Default-mode compatibility: Blocked.** The README requires empty batches to succeed in either mode, and the default path no longer does.
- **Downstream consumers: Unknown.** Callers that compare against the exact plain `Items: N` string would see the new format by default. That's the intended change; whether any such consumers exist isn't in the repo.
- **Rollback: Supported.** Setting the constant back to `False` restores the old default.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[stats.py:4 / config.py:1]** Turning on detailed mode by default makes `report([])` crash
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → Division by zero)
  - Triggered by: content — `.py` extension (`config.py`, `tests/test_report.py`)
  - **Path:** `report([])` sets `detailed` from `DETAILED_REPORT`, which is now `True`. Then `summarize([], detailed=True)` evaluates `sum([]) / len([])`, which raises `ZeroDivisionError`.
  - **Expected vs actual:** Expected `"Items: 0"` (README: empty batches are valid in either mode and produce only `Items: 0`). Actual: an unhandled exception.
  - **Consequence:** Any caller that relies on the default and passes an empty batch now crashes where it used to succeed. The explicit `detailed=True` empty case was already broken before this change. This diff exposes the same bug to every default caller.
  - **Confidence: 95%.** It's a three-function trace with no config or framework indirection, and the README contract states this case explicitly. The remaining uncertainty is only that I couldn't run the empty case myself.
  - **Suggested fix:** In `stats.summarize`, guard the mean with `if detailed and values:`. `format_summary` already omits the mean when the key is absent, so both modes then produce `Items: 0`. Add `test_default_empty` and `test_detailed_empty`, each asserting `report([]) == "Items: 0"` (with and without `detailed=True`).

::code-comment{file="stats.py" line="4" severity="P1"}
With DETAILED_REPORT now True, `report([])` reaches `sum(values) / len(values)` with an empty list and raises ZeroDivisionError. The README requires `Items: 0` for empty batches in either mode. Guard with `if detailed and values:` and add default-mode and detailed-mode empty-batch tests.
::

### P2 - Medium
(none)

### P3 - Low
(none)

---

**Coverage:** I read the README contract, the staged diff and the full staged contents of all source and test files. I checked the default, override and empty-batch scenarios against the contract.

**Not covered:**
- Downstream consumers of the report string, since none are in the repo.
- Installed or deployed configurations, which the README says aren't recorded.
- Running the empty-batch scenarios myself, because that command was denied.

**Indexing:** I added this finding to the `kk:review-findings` knowledge base as a general pattern: flipping a default exposed an untested boundary case. The knowledge base was empty before this.

The intended change itself, the new default output for non-empty batches, looks right. Approval is blocked only by the empty-batch regression. The fix is the one-line guard plus the two tests above. I haven't edited anything; tell me if you want me to apply the fix.
