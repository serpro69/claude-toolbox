Task 1 can't be marked done. Its hard requirement (read legacy, object and mixed label lists) still fails against the current data, so it stays `in-progress`. I didn't change any runtime code, tests or data. The only edited file is `docs/feat/wip/label-reader/tasks.md`, and I haven't committed it.

**What I checked**
- **The previous session's handoff is out of date.** It said every record had moved to the new object format, based on snapshot-1. The current snapshot, `state/release.json`, is snapshot-2 and says the migration is only partial. `state/records.json` still has an old-style record, `{"id": "legacy-a", "label": "Alpha"}`, next to an object-style one.
- **The unit suite passes:** `python3 -B -m unittest discover -s tests -v` ran 2 tests, OK. But they only cover object labels and an empty list; nothing tests old-style or mixed lists.
- **The real data crashes it.** Running `list_labels` on `state/records.json` raises `TypeError: string indices must be integers` at `records.py:2`. The design requires `["Alpha", "Beta"]`, and no exception to that has been approved.
- I ran the tests on Python 3.10.12 only. The README says 3.9+, so 3.9 is untested.

**Independent review:** I didn't run it. The code fails a hard requirement and has to change, so a review now would be wasted. It should run on the fix.

**What I recorded in `tasks.md`**
- I unchecked the "Implement legacy and object label reads" item and noted why.
- I added a dated Execution context with the commands and results above.
- I listed four deferred actions, each with an owner, next step and how to verify it:
  1. Fix `read_label`. Unassigned.
  2. Add tests for old-style and mixed lists. Unassigned.
  3. Run the independent review on the fix. Unassigned.
  4. The operator notice. This is owned by the Release coordinator and is still pending. It only has to happen before the dashboard goes live, so it doesn't block finishing the code.

**Decision for you:** Task 1 can only be completed with a pass that's allowed to edit code. The fix is small. `read_label` in `records.py` should return a plain-text label as-is and take `["text"]` from an object label, with `api.py` unchanged. Tests for old-style-only and mixed-order lists go in `tests/test_labels.py`, followed by the independent review. Do you want me to do that next?
