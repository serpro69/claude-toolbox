## Code Review Summary

**Files reviewed**: 2 files (`formatting.py`, `tests/test_report.py`), 5 lines changed
**Overall assessment**: **APPROVE**
**Profiles**: `python`, detected from the `.py` extension on both files. I applied its four standard checklists: security, SOLID, code quality and removal. No other profile matched.

---

## Findings

### P0 – Critical
None.

### P1 – High
None.

### P2 – Medium
None.

### P3 – Low
None.

---

## What was checked

- **Scope against the README.** The README asks for the count label to change from Items to Records, with counts, calculations, mode selection and the mean suffix left alone. The diff changes only the text in `formatting.py:2`. `format_summary` still builds the mean suffix on top of `format_count`, so detailed output reads `Records: N; Mean: M`.
- **No leftover old label.** A search of the repo, excluding the plugin folder, finds no `Items` text in code or tests. The only mention is in the README describing the change.
- **Tests.** All four assertions were updated to `Records:` and they cover plain-empty, plain-populated, detailed and default mode. `python3 -B -m unittest discover -s tests` runs 4 tests, all OK.
- **Security, SOLID, code quality, removal.** No input handling, I/O, shared state or new structure was added, and nothing became dead code. No checklist item applies.

## Things I didn't flag (not introduced by this change)

- **Detailed mode crashes on an empty batch.** `stats.py:4` divides by `len(values)`, so `report([], detailed=True)` raises `ZeroDivisionError`. The README only defines detailed output for populated batches and says detailed mode isn't being activated here. Worth a follow-up ticket before anyone turns it on.
- **One test depends on the config file.** `test_default_populated` passes only because `config.py` sets `DETAILED_REPORT = False`. The README says installation settings aren't recorded in the repo, so an install with that flag on would produce different default output than the test expects.
- **Anything outside the repo that reads the old label will break.** If a log parser, dashboard or script matches `Items:`, it stops matching. Nothing in the repo does, but I can't see beyond it. The rename is the intended change, so this is something to tell those consumers about, not a code fix.

**Capy:** `kk:review-findings` and `kk:lang-idioms` are both empty. **No findings to index.**

---

## Next Steps

I found 0 issues (P0: 0, P1: 0, P2: 0, P3: 0). The staged change does what the README asks and the tests pass.

**How would you like to proceed?**

1. **No changes:** review complete, ready to commit
2. **Open follow-ups:** I'll draft notes for the empty-batch crash and the config-dependent test
3. **Something else:** tell me what you'd like
