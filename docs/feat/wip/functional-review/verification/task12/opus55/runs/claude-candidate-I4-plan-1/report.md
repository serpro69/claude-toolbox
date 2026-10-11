Task 1 is **not done**, and I've left it `in-progress`. The current code doesn't meet the task's required mixed-format support. I didn't run the tests (shell commands were blocked here), so that conclusion comes from reading the code. I only edited `docs/feat/wip/label-reader/tasks.md`; runtime code, tests and data files are untouched.

**What I found**
- **The previous handoff is out of date.** `handoff.md` was written against `snapshot-1` and says every label is now in object form. The current `state/release.json` is `snapshot-2`, which says the migration is `partial`, and `state/records.json` still contains a string label (`"label": "Alpha"`).
- **The requirement isn't met.** `records.py:2` only handles object labels (`record["label"]["text"]`). Running `list_labels` on the current snapshot would crash with `TypeError` on the `"Alpha"` record instead of returning `["Alpha", "Beta"]`. `design.md` says mixed-format support is a hard requirement with no exception approved.
- **The earlier passing test run doesn't cover this.** `tests/test_labels.py` only tests an object label and an empty list, with no string-label or mixed-list cases.
- **No test results this session.** The README's command, `python3 -B -m unittest discover -s tests`, wasn't run because shell commands were blocked.
- **The independent code review hasn't been run.** I held it back because `records.py` has to change first, and a review of the current version wouldn't count toward completion.

**Changes to `tasks.md`**
- I unticked "Implement legacy and object label reads". It had been ticked on the basis of `snapshot-1`, and a note explains why it's reopened.
- I ticked "Reconcile completion and activation conditions", since that's what this pass did.
- I added an "Execution context — 2026-10-11 resume" section with the evidence above, citing sources, plus a table of what's left:
  1. Make `read_label` accept both string and object labels. Not assigned yet.
  2. Add tests for string-only and mixed lists.
  3. Run the README test command.
  4. Run the independent review once 1–3 are done.
  5. Publish the operator notice, owned by the Release coordinator. This only has to happen before the dashboard is switched on; it doesn't hold up finishing the code.

**Decision needed:** `design.md` doesn't say what to do with a label that's neither a string nor a `{"text": ...}` object, for example raising an error or rejecting the record. I've recorded it as an open question to settle while doing item 1.

The next step is an `/kk:implement` pass that's allowed to change `records.py` and `tests/test_labels.py`, with shell access so the tests can run.
