## Review Summary (Isolated Mode)

**This change shouldn't merge as it stands.** With the new default, `report([])` crashes with `ZeroDivisionError`. All 4 tests still pass, so the suite doesn't catch it.

**Reviewers**: one reviewer only. The code-reviewer sub-agent (Claude) ran. The second reviewer, pal codereview, couldn't run because its tools aren't available in this session, so no findings are corroborated.
**Files reviewed**: 2 files, 2 lines changed (`config.py`, `tests/test_report.py`)
**Checklists applied**: Python security, SOLID, code-quality and removal-plan.

---

### Code Reviewer Findings

- **`stats.py:4`: an empty batch now crashes by default**
  - Severity: P0 | Confidence: 97%
  - Here is what happens when no mode is passed:
    1. `report(values)` falls back to `DETAILED_REPORT`, which is now `True` (`app.py:8`).
    2. It calls `summarize(values, detailed=True)`.
    3. `summarize` runs `sum(values) / len(values)` with no empty-input check.
    4. For `[]` this divides by zero.
  - The README says empty batches are valid in either mode and return `Items: 0`. It also says this change must keep empty-batch reports working. Before the flip, the crash only happened if a caller passed `detailed=True` on purpose. Now it happens on the default path.
  - **Fix**: in `stats.summarize`, change the check to `if detailed and values:`. `format_summary` already handles a summary with no mean, so nothing else needs to change.
  - **I checked this myself**: I ran `python3 -B -c "from app import report; print(report([]))"` and got `ZeroDivisionError: division by zero`. `python3 -B -m unittest discover -s tests` reports `Ran 4 tests ... OK`.

- **`tests/test_report.py`: no test for an empty batch in detailed or default mode**
  - Severity: P1 | Confidence: 95%
  - The only empty-input test sets `detailed=False` explicitly. The default and detailed tests only use `[2, 4]`. The diff updated one expected string but added no test for the case this change exposes.
  - **Fix**: add two tests:
    - `report([], detailed=True)` returns `"Items: 0"`
    - `report([])` returns `"Items: 0"`

- **`app.py:1`: the flag's value is copied when `app` is imported**
  - Severity: P3 | Confidence: 70%
  - `from config import DETAILED_REPORT` copies the value once. Changing `config.DETAILED_REPORT` later has no effect; only patching `app.DETAILED_REPORT` does. Nothing breaks today, but it's easy to get wrong in tests. Using `None` as the default argument is correct.
  - **Fix**: optionally, `import config` and read `config.DETAILED_REPORT` inside `report()`.

**Gaps:**
- Anything that parses report output exactly will now see `; Mean: M` added for non-empty batches. Settings for existing installations aren't recorded in the repo, so I couldn't check who depends on the old format.
- No security findings.
- No code became unused, so no removal plan is needed.

---

## Next Steps

There are 3 findings, all from the code-reviewer: P0 1, P1 1, P3 1.

I recommend fixing:
1. **P0**: add the empty-input check in `stats.summarize`. It should land with the flag flip, not after it.
2. **P1**: add the two empty-batch tests (detailed and default).

I'd leave as is:
- **P3 (flag copied at import)**: nothing changes the flag while the program runs today, so it's optional.

**Housekeeping:**
- I saved the general lesson to the review knowledge base: "flipping a default exposes edge cases in the code path it switches on."
- I couldn't delete the temporary diff file `/tmp/kk-review-code-detailed-report.patch` because the shell command was denied. You can remove it yourself.

**How would you like to proceed?**
1. **Fix all**
2. **Fix P0 and P1 only** (no findings are corroborated, since only one reviewer ran)
3. **Fix specific items**
4. **No changes**
