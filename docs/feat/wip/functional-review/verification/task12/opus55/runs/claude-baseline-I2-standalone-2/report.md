I fixed `patch_settings`. A supplied key now always replaces the current value, including `None`, `""` and `False`, and keys left out of the patch are untouched. The test suite passes and the independent review approved the change with no findings.

**The bug:** `settings.py:4` used `result[key] = value or current.get(key)`, so any falsey value was quietly swapped back to the old one. One visible effect was that the command-line `clear_note` didn't actually clear the note. The line is now `result[key] = value`. The function still copies `current` and only reads `patch`, so it doesn't change the caller's dictionaries. `api.py`, `cli.py` and the function's signature are unchanged, and no dependencies were added.

**Tests** (`tests/test_settings.py`): I kept the existing test and added regression tests for:
- `None` and `""` notes, and `enabled=False`, sent through the HTTP handler
- an empty patch, which returns a new, equal dict
- `clear_note` setting the note to `None`
- neither input dictionary being changed

```
$ python3 -B -m unittest discover -s tests
Ran 5 tests in 0.000s
OK
```

I didn't run the new tests against the old code. They should fail on it, since the old fallback would have restored `"before"`.

**Review:** I could only run one of the two reviewers the skill asks for. The `pal` server failed to connect, so the second reviewer was skipped. I also couldn't write the diff to a temp file, so I pasted it into the reviewer's prompt. The reviewer that ran found no P0–P3 issues, so there was nothing to index.

The reviewer raised two risks outside this change:
- **Types aren't checked.** Nothing confirms `note` is text or `None`, or that `enabled` is a boolean. Before the fix, a wrong-typed falsey value like `0` was silently ignored; now it gets stored, and something like `enabled: "false"` from an HTTP request would be stored as text.
- **Unknown keys get added.** `patch_settings` accepts any key, even one not already in the settings. Today only the HTTP handler restricts this, to `note` and `enabled`.

Both were already true before this change. Should I add validation, or leave it as is?

Nothing is committed.
