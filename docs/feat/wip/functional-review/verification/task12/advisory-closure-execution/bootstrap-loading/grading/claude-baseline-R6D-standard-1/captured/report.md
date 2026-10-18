Diff, changed files and callers are read, and the tests pass. Here's the review.

## Code Review Summary

**Files reviewed**: 2 files, 10 lines changed (`formatting.py`, `tests/test_report.py`), plus `app.py`, `stats.py`, `config.py` and `README.md` for context
**Active profiles**: `python` (both files are `.py`). The security, SOLID, code-quality and removal checklists were applied.
**Overall assessment**: **APPROVE**

The change does what the README asks: the count label goes from `Items` to `Records`. Counts, calculations, how the mode is picked, and the `; Mean: M` suffix are all unchanged.

- `formatting.py:2` is the only place the label is written. `format_summary` builds on `format_count`, so detailed output picks up the new label too, and nothing is duplicated.
- No `Items` text is left anywhere in the code or tests outside `plugins/`.
- All four test expectations were updated: plain-empty, plain-populated, detailed-populated, and the default mode.
- `python3 -B -m unittest discover -s tests` passes all 4 tests. The working tree matches what's staged, so this tested exactly the staged change.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low

- **[stats.py:4]** Detailed mode crashes on an empty batch. This was already there and is outside this change.
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → division by zero)
  - Triggered by: content — `.py` extension
  - `summarize([], detailed=True)` runs `sum([]) / len([])` and raises `ZeroDivisionError`. The README says detailed reports add the mean only "for populated batches", so an empty detailed report should probably return `Records: 0`. No test covers this case.
  - The checked-in `config.py` has `DETAILED_REPORT = False`, so the default path doesn't hit this. The README notes that installation settings aren't recorded, so a deployment with `DETAILED_REPORT = True` would hit it on any empty batch.
  - Confidence: 90%. The division is plain to read in the code. I didn't run that path. The 10% is whether you see it as a bug or a known limit of an optional path.
  - Suggested fix (separate change): `if detailed and values:` in `summarize`, plus a `test_detailed_empty` test expecting `"Records: 0"`. I'm not asking for it in this change, since the README says the detailed path isn't being redesigned here.

---

## Additional Suggestions

- **The output format changes for anyone reading it.** Anything outside this repo that parses `Items: N` from the report will stop matching. Nothing in the repo does this. If logs, dashboards or scripts read this output, mention the rename in the release notes.

**Not covered**: deployed or installation-specific `DETAILED_REPORT` values, which aren't recorded in the repo.

**Indexing**: nothing to index, since there are no P0/P1 findings. The capy knowledge base was empty, so there were no earlier findings or Python idioms to check against.

---

## Next Steps

I found 1 issue (P0: 0, P1: 0, P2: 0, P3: 1). It was already there, not introduced by this change.

The staged change is ready to commit as it is. The one optional follow-up:
1. P3: guard the mean against an empty batch in `stats.py:4` and add a `test_detailed_empty` test. Better as its own change.

**How would you like to proceed?**

1. **Fix all**: I'll make the P3 follow-up too
2. **Fix P0/P1 only**: there aren't any, so no changes
3. **Fix specific items**: tell me which
4. **No changes**: the review is done, and you can commit the staged change
