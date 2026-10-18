## Review Summary (Isolated Mode)

**Overall assessment: APPROVE for the staged code change only.** This is not a release or deployment sign-off. The Items→Records rename works as the README asks, and nothing else in the program changes.

**Reviewers:**
- **code-reviewer:** finished. It read all the instructions and source it was given.
- **PAL:** not available in this session (no PAL tools are installed here). With one reviewer, none of the findings are corroborated.

**Files reviewed:** `formatting.py` and `tests/test_report.py` as staged, 5 lines added and 5 removed. I also read the unchanged files they depend on (`app.py`, `stats.py`, `config.py`) and `README.md`, and compared against the HEAD version of `formatting.py`.

**Intent and scope:** `README.md` states the goal: change the count label from Items to Records and keep counts, calculations, mode selection and the `; Mean:` suffix as they are. I reviewed the staged changes; there were no unstaged changes. There are no task documents.

**Baselines:** I compared the staged changes against HEAD `2b50e59`. The `DETAILED_REPORT` values on real installations are unknown: the README says they aren't recorded, and the repo has one commit and no tags.

### Behavior and Compatibility

The only line that behaves differently is `formatting.py:2`. Everything else on the report path (`app.py`, `stats.py`, and the summary formatting) is identical to HEAD. A search of the repo (excluding `plugins/`) found nothing else that uses the old "Items:" text.

| Scenario | Before | After | Status |
| --- | --- | --- | --- |
| `report([], detailed=False)` | `Items: 0` | `Records: 0` | Works; tested |
| `report([2,4], detailed=False)` | `Items: 2` | `Records: 2` | Works; tested |
| `report([2,4], detailed=True)` | `Items: 2; Mean: 3` | `Records: 2; Mean: 3` | Works; tested |
| `report([2,4])` with the checked-in default | `Items: 2` | `Records: 2` | Works; tested |
| `report([2,4])` on an installation with `DETAILED_REPORT=True` | `…; Mean: 3` | Same, with the new label | Works (from reading the code; no test) |
| `report([], detailed=True)` | `ZeroDivisionError` | Same error | Existing bug, see below |

- **Unknown installation settings:** they don't affect this change, because the rename gives the same result in both modes.
- **Outside tools parsing "Items:":** I found no evidence either way. The rename is deliberate.
- **Stored data and rollout:** not applicable. The function keeps no state and nothing is being switched on.
- **Tests:** I ran `python3 -B -m unittest discover -s tests` on the staged code and all 4 tests passed.

### Code Reviewer Findings

The reviewer found no P0, P1 or P2 issues, and nothing from the security, SOLID or removal checklists.

- **[stats.py:4] (P3): a detailed report on an empty batch crashes with `ZeroDivisionError`.** This bug was already there; this change doesn't introduce or worsen it.
  - **Trigger:** `report([], detailed=True)`, or plain `report([])` on any installation with `DETAILED_REPORT=True`.
  - **Expected vs actual:** the README only adds the mean "for populated batches", so the result should probably be `Records: 0`. Instead, `sum(values) / len(values)` fails.
  - **Confidence:** 90%. The missing guard is clear in the code, but the README doesn't say exactly what an empty detailed report should look like.
  - **Fix, as a separate change:** only add the mean when `detailed and values`. Add a test that `report([], detailed=True) == "Records: 0"`.

### Outstanding Evidence and Prerequisites

Nothing is needed for this change. Before any release decision, someone would need to check each installation's `DETAILED_REPORT` setting, because that decides whether the empty-batch crash can happen by default.

---

**Verdict:** no changes are needed in this staged change. As a separate follow-up, fix the crash at `stats.py:4` as described above. It shouldn't block this change. There's no tracking for it yet; I can write a short review note if you'd like one.

**Indexing:** nothing to record in the knowledge base. The only finding is a P3 that was already in the code, and the knowledge base was empty when I searched it.

**Cleanup not done:** deleting the temporary review files was blocked by the permission mode. These folders are still there and can be removed (`rm -rf`):
- `/tmp/kk-review-evidence-HZv4wu`
- `/tmp/kk-review-instructions-bbrmpgpa`
- `/tmp/kk-review-instructions-jhwiguj3`
- `/tmp/kk-review-instructions-q8gn0kah`
