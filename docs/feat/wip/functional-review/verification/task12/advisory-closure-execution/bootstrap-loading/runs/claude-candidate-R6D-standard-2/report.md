## Code Review Summary

**Files reviewed**: 2 files, 5 lines changed (`formatting.py`, `tests/test_report.py`)
**Overall assessment**: **APPROVE**
**Intent and scope**: `README.md` says this increment changes the count label from `Items` to `Records`. Counts, calculations, mode selection and the mean suffix must stay the same. There's no task scope (no `docs/feat/wip/`), so the diff was reviewed against the README contract.
**Baselines**: Review base `2b50e59`; candidate is the staged index. There were no unstaged changes, so the worktree matches the index. The README says no release or deployment assessment is requested.

## Behavior and Compatibility

The only label source is `format_count` (`formatting.py:2`). `format_summary` uses it for both plain and detailed output, so one edit relabels every mode. `app.py`, `stats.py` and `config.py` are unchanged.

| Scenario | Expected | Candidate | Evidence |
|---|---|---|---|
| Plain, empty `[]` | `Records: 0` | `Records: 0` | unittest (ran) |
| Plain, `[2, 4]` | `Records: 2` | `Records: 2` | unittest (ran) |
| Detailed, `[2, 4]` | `Records: 2; Mean: 3` | same | unittest (ran) |
| Default mode (`DETAILED_REPORT=False`) | `Records: 2` | same | unittest (ran) |
| Detailed, `[0.1, 0.2]` / `[1e7]` | mean uses `g` format | `Mean: 0.15` / `Mean: 1e+07` | ran manually; matches the README's `g` contract |

- **Tests:** `python3 -B -m unittest discover -s tests` ran 4 tests, all OK.
- **In-repo consumers:** Supported. A grep outside `plugins/` found no other references to `Items` or to the formatter functions.
- **Installation settings:** Supported. The label works the same whether `DETAILED_REPORT` is True or False, so unrecorded historical settings don't change this conclusion.
- **External parsers of the output string:** Unknown, but intended. The README explicitly requests the label change, so outside consumers matching `Items:` are an accepted contract change. None are visible in this repo.

---

## Findings

### P0 – P2
None introduced by this change.

### Inherited (pre-existing, not caused by this diff)

- **[stats.py:4]** A detailed report on an empty batch raises `ZeroDivisionError`
  - Profile: python · Checklist: code-quality-checklist.md (Boundary Conditions → Division by zero)
  - Triggered by: content: `.py` extension
  - `report([], detailed=True)` crashes in `summarize`. I reproduced it. The README attaches the mean suffix only to "populated batches", which suggests the output should be `Records: 0`; that expectation is my inference, since the README doesn't state it directly. The same crash would hit the default path in any installation with `DETAILED_REPORT = True`. `stats.py` is unchanged here, and the README says the detailed path isn't being changed in this increment, so this isn't a condition for approval.
  - Confidence: 95%. Reproduced directly; the only uncertainty is the inferred expected output.
  - Separate follow-up: guard with `if detailed and values:` in `summarize`, and add a `report([], detailed=True)` test.

---

**Checklists applied**: python security, SOLID, code-quality and removal-plan. None of them apply to a string-literal change: no new input handling, dependencies or abstractions, and nothing removed.

**Not covered**: deployed or released revisions, and any external consumers of the report text.

**Indexing**: No findings to index (nothing P0/P1 was introduced; the knowledge base was empty, so there was nothing to search).

No changes are recommended for this staged increment. The empty-batch crash above is the only follow-up I'd suggest, as its own change.
