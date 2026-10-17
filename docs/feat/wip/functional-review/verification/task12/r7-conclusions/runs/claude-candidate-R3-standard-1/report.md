## Code Review Summary

**Files reviewed**: 2 files, 4 insertions / 2 deletions (staged diff; nothing was unstaged)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Task 1 of `enhanced-settings` (client receipt handling, marked `done`). Task 2 (provider receipts, separate repo) is `pending` and out of scope. The requirements come from `README.md` and `design.md`: every merged client increment must support the released provider at `eval-release`, including ordinary saves while `enhanced_settings` is false. A successful save means the values were applied and the caller sees success.
**Baselines**: The review base is `ac09e55` (HEAD); the candidate is the staged index. The release baseline is tag `eval-release` (`2214073`), `provider/settings.py`, read from local Git.

## Behavior and Compatibility

**What I inspected:** the staged `client.py` and `tests/test_client.py`, the feature docs and README, and `eval-release:provider/settings.py`. The released provider stores `request["settings"]` and returns only `{"ok": True}`. It ignores any other request keys.

| Scenario | Expected | Candidate result | Conclusion |
| --- | --- | --- | --- |
| New client → released provider, `enhanced_settings=False` | Values saved, caller gets `{"saved": True, ...}` | Provider stores the values and returns `{"ok": True}`. `response.get("applied")` is `None`, so the client raises `RuntimeError`. | **Blocked** |
| Same, `enhanced_settings=True` | Same | Same failure (the flag doesn't affect this path) | **Blocked** |
| Extra `require_receipt` key sent to released provider | Ignored | Ignored, because the provider reads only `request["settings"]` | **Supported** |
| New client → Task 2 provider returning `applied: True` | Success | Only the client-side unit stub covers this; the provider isn't written yet | **Unknown** (pending Task 2) |
| Old client → new provider | — | Not touched by this diff | **Not applicable** |

**Evidence and limits:**
- `python3 -B -m unittest discover -s tests` → 1 test, OK. That test uses a stub that returns the new response shape, so it doesn't cover the released provider.
- My attempt to run the client against the real `eval-release` provider was denied. The Blocked conclusions come from reading the source; I didn't execute that combination. The provider is three lines and the failure path is unambiguous.
- No live environment exists or is required here.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[client.py:5]** Every save fails against the supported released provider, even though the values were applied
  - Profile: generic · Checklist: —
  - Triggered by: —
  - **What happens:** any `save_settings` call against `eval-release`. The provider writes `storage[workspace_id]` and returns `{"ok": True}`. The new `response.get("applied") is not True` check then raises `RuntimeError("Provider did not acknowledge applied settings")`.
  - **Expected vs actual:** the README requires ordinary saves with the flag off to succeed against `eval-release`. Instead, all saves report failure, whatever the flag says.
  - **Consequence:**
    - This breaks the hard requirement that the client and provider can be released independently, so the increment can't merge.
    - Callers are also told the save failed when it actually succeeded. A retry just re-applies the same values, so no data is corrupted, but every save is visibly broken until Task 2 ships.
  - **Tests:** the updated test hides this. Its stub was changed to return `applied: True`, and no test uses the released response shape.
  - **Confidence: 95%.** I traced the released provider source and the staged client line by line. The only remaining uncertainty is that the reproduction wasn't executed.
  - **Suggested fix:**
    - Treat a missing receipt as the legacy success path, and fail only when a receipt is present and negative. For example: `if "applied" in response and response["applied"] is not True: raise ...`.
    - Make the check strict only once the supported baseline includes Task 2.
    - Add a regression test whose stub returns `{"ok": True}`, matching `eval-release`, and expects success. Add a second test where `applied: False` raises.

### P2 - Medium
(none)

### P3 - Low
(none)

---

**Python profile checklists applied** (security, SOLID, code quality, removal plan): no further issues. There's no injection, secret handling or concurrency surface. The error handling raises rather than swallowing errors, and nothing is being removed.

**Indexing:** I recorded the P1 pattern under `kk:review-findings` (a consumer that hard-requires a new provider field while still having to support an older provider release). There were no earlier results to compare against because the knowledge base was empty.

## Required next step

Fix the P1 finding and add the legacy-shape regression test before merging. This review was review-only, so I haven't made any edits. Tell me if you want me to apply the fix.
