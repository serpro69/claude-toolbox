I changed `patch_settings` so that explicitly supplied values, including `None`, `""` and `False`, now replace the current value. I haven't run the tests: Bash is denied in this session, so the change is checked by reading the code only.

**The bug:** `settings.py` used `value or current.get(key)`, which threw away any "empty" value the caller sent and kept the old one. Because of that, `cli.clear_note` never actually cleared the note, and `api.update_preferences` couldn't turn `enabled` off or set an empty note.

**The fix** (`settings.py`):
```python
def patch_settings(current, patch):
    result = dict(current)
    result.update(patch)
    return result
```
- Keys left out of the patch keep their current values.
- It still returns a new dict and doesn't change `current` or `patch`.
- The name and signature are unchanged, so `api.py` and `cli.py` need no edits.
- No dependencies were added.

**Tests** (`tests/test_settings.py`): I kept the existing test and added tests that:
- check that `None`, `""` and `False` each replace the current value;
- check that an empty patch keeps every current value;
- check that neither input dict is changed;
- run `update_preferences` with empty values plus an extra key that should be ignored;
- check that `cli.clear_note` really sets the note to `None`.

The new tests for empty values would fail against the old code.

**Review:** an independent code reviewer found no P0, P1 or P2 issues and gave a COMMENT verdict (not approval) because the tests haven't run. The second reviewer, PAL, couldn't run because its server failed to connect. The reviewer also couldn't confirm the original file or that nothing else changed: git wasn't available, so it worked from my copy of the original code. It raised one low-severity point:
- **Wrong types can now be saved through the HTTP path** (`api.py:5`). Before, input like `{"enabled": null}` was accidentally ignored by the bug; now it's stored, even though the README says `enabled` is a boolean. Type checking was already missing before this change, so I left it out of scope. If you want it, the fix is a small type check in `update_preferences`; you'd need to decide whether bad values are rejected or ignored.

**Still open:**
- Run `python3 -B -m unittest discover -s tests`, or allow Bash so I can run it.
- Delete the review notes I left outside the repo at `/tmp/kk-review-code-patch-settings/` once you no longer need them.
