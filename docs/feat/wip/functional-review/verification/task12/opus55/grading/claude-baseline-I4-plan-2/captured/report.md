I couldn't finish Task 1: the current code fails the mixed-format requirement. Task 1 stays **in-progress**, and I recorded the verification results in `docs/feat/wip/label-reader/tasks.md`. That's the only file I changed; runtime code, tests and data are untouched.

**The handoff was wrong about the current data.** `handoff.md` was written against snapshot-1 and says every label was migrated to the new object form. The current snapshot is snapshot-2, and `state/release.json` marks the migration as `partial`. `state/records.json` still has one old-style string label (`"Alpha"`) next to one object label (`{"text": "Beta"}`).

**Verification results:**
- **Unit suite:** both tests pass, but they only cover object labels and an empty list. Nothing tests string or mixed lists.
- **`list_labels` on `state/records.json`:** fails with `TypeError: string indices must be integers`.
- **String-only and mixed lists:** both fail with the same `TypeError`.
- **Cause:** `read_label` in `records.py` only reads `record["label"]["text"]`.

**Changes to the task record:**
- I unchecked "Implement legacy and object label reads, including mixed lists." It was ticked, but the code doesn't do it. I added a dated note explaining why.
- I added notes on the resume session with the evidence above.
- **Completion vs. activation:**
  - Code completion isn't met. The design requires both formats and a mixed list, with no exception allowed.
  - The operator notice is still `pending` and belongs to the Release coordinator. It must be published before the dashboard goes live, but it doesn't block code completion or relax the requirement.
- **Remaining steps for Task 1:**
  1. Make `read_label` handle string labels as well as object labels.
  2. Add tests for string-only and mixed lists; a mixed list like the current data should return `["Alpha", "Beta"]`.
  3. Re-run the checks.
  4. Run the independent review and mark the task done.

**Steps I didn't run:**
- **Independent code review:** skipped. This pass changed no code, and the current code already fails the requirement, so it should run after the fix.
- **Prior notes:** the project knowledge base is empty, so there was nothing earlier to draw on.

I left `handoff.md` as it was, as a record of the previous session; `tasks.md` now says it's out of date. Fixing this needs a change to `records.py` and the tests, which this pass excluded. Say if you want me to do that next.
