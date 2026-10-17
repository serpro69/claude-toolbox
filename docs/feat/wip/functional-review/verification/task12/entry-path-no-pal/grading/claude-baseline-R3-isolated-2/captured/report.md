# Isolated review: enhanced-settings task 1 (staged changes)

This change breaks every ordinary settings save against the provider you have released, so it shouldn't merge as it is. The test was updated to the new response shape, which is why the suite still passes.

Only the `code-reviewer` sub-agent ran. The second reviewer (`pal codereview`) isn't available in this environment, so nothing here is confirmed by two reviewers. If you want a second pass, run `/kk:review-code` (standard mode).

**Scope:** 2 files, 6 lines changed, Python profile with all 4 checklists. Task 1 was reviewed; task 2 (provider receipts) is pending, so it was out of scope.

## Code reviewer findings

**1. P0, 97% confidence: every ordinary save fails against the released provider** (`client.py:5-6`)
- The released provider (`git show eval-release:provider/settings.py`) always returns `{"ok": True}` and never sends `applied`.
- So `response.get("applied") is not True` is always true, and `save_settings` raises on every call, including the default `enhanced_settings=False` path.
- It's worse than a plain failure: that provider has already stored the values before it returns. The caller is told the save failed when the values were actually applied.
- This contradicts README.md lines 4–6 and 9–10 and design.md line 3. README line 10 also says a pending provider task can't change the supported baseline, so task 2 being pending doesn't excuse it.
- **Fix:**
  - **Option A:** treat a missing `applied` as an older provider, where `ok` already means applied. Raise only when `applied` is present and not `True`.
  - **Option B:** enforce the receipt only when `enhanced_settings=True`, until the receipt-capable provider becomes the supported release.
- I checked this myself against the provider source at the `eval-release` tag, and the reviewer's trace is correct.

**2. P1, 92% confidence: the test fixture was changed to match the new client, which hides the regression** (`tests/test_client.py:8`)
- The fake `send` used to return exactly what the released provider returns. It now returns a response shape that no supported provider produces.
- There's also no test for the new failure branch.
- **Fix:** keep a test that returns `{"ok": True}` (the released provider's response) and assert the save succeeds. Add a separate test with `applied: True`, and a negative test with `applied: False` that expects an error.

**3. P3, 60% confidence: a rejected save and a missing receipt raise the same error** (`client.py:4,6`)
- Both are a plain `RuntimeError`, so callers can only tell "nothing was saved" from "saved but not confirmed" by matching the message. That matters when deciding whether to retry.
- **Fix:** use a separate exception type for the missing receipt and include the response fields in it.

## My own observation (I'm the coordinator, not an independent reviewer, so weight it accordingly)

- **About option A for finding 1** (`client.py`): if a missing `applied` counts as success, the client can't tell an older provider from a new one that left out its receipt. The receipt then guarantees nothing until a strict check is turned on later. If the receipt needs to mean something during the rollout, a better approach is to enforce it only when the provider says it supports receipts, or when `enhanced_settings` is on.

## Indexing
I saved finding 1 as a reusable pattern (`kk:review-findings`) for future reviews: an increment enforces a new protocol field before the other side has shipped it, and an updated test fake hides the break. Findings 2 and 3 are specific to this change, so I didn't index them.

## Notes on the process
- I couldn't write the diff to a temp patch file, so I gave it to the reviewer directly in its prompt. No temp file needs cleaning up.
- Neither I nor the reviewer ran the test suite. The verdict comes from reading the code and the released provider source.

## Next steps

I recommend fixing:
1. **P0** (finding 1): option B, or option A combined with my note above.
2. **P1** (finding 2): add the released-provider test, the `applied: True` test and the `applied: False` test.
3. **P3** (finding 3): optional; useful if callers retry on failure.

**How would you like to proceed?**
1. **Fix all**
2. **Fix high severity** (P0 and P1)
3. **Fix specific items**: tell me which
4. **No changes**: the review is complete
