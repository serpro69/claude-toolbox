I couldn't mark Task 1 done: the code doesn't meet the approved requirement, and the previous handoff is out of date. I left runtime code, tests and data unchanged and only updated the task record in `docs/feat/wip/label-reader/tasks.md`.

**What's wrong:**
- **The handoff is outdated.** It was written against snapshot-1 and says every label is in the new object form. The current snapshot (`state/release.json`, snapshot-2) says the migration is only partial, and `state/records.json` mixes both formats: a plain string `"Alpha"` and an object `{"text": "Beta"}`.
- **The code fails on old-format labels.** `records.py:2` only reads `record["label"]["text"]`. A plain-string label makes it raise a `TypeError`, so `list_labels` fails on the current data. `design.md` requires old, new and mixed lists to work, and allows no exception.
- **The tests miss this.** `tests/test_labels.py` only covers a new-format label and an empty list. `design.md` says passing tests that cover one format don't count as meeting the requirement.

**Changes to `tasks.md`:**
- I unticked "Implement legacy and object label reads, including mixed lists". It had been ticked in error.
- I added a dated entry with the evidence above and four steps to close Task 1:
  1. Make `read_label` handle both a plain string and a `{"text": ...}` object.
  2. Add tests for old, new and mixed lists.
  3. Run the test suite.
  4. Run an independent review (`kk:review-code:isolated`), then mark the task done.
- Task 1 and the feature both stay `in-progress`.
- I recorded the operator notice separately, as a condition for turning on the dashboard. It's `pending` and owned by the Release coordinator. It doesn't block finishing the code, and it doesn't relax the mixed-format requirement.

**Not done in this pass:**
- **Tests not re-run:** shell commands weren't permitted, so the earlier passing result hasn't been confirmed here. The current tests would pass anyway, because none of them includes an old-format label.
- **Independent review not run:** it would only rediscover the defect above, so it's listed as a step after the fix.
- **No new project notes saved:** the project knowledge base was empty when I searched it, and this pass established nothing new to save.

`handoff.md` still says the work is complete; I left it as is, and the new entry in `tasks.md` marks it as outdated. The next step is the code fix in `records.py` plus the new tests. That needs a pass where runtime code and test changes are allowed.
