## Code Review Summary

**Overall assessment: REQUEST_CHANGES.** This change breaks ordinary settings saves against the released provider.

- **Files reviewed:** 2 files (`client.py`, `tests/test_client.py`), 4 lines added and 2 removed.
- **Intent and scope:** Task 1 of enhanced-settings ("Client receipt handling", marked done). Task 2, provider receipts, is pending and out of scope. The README sets a hard rule: every merged client increment must still work with the provider at `eval-release`, including ordinary saves while `enhanced_settings` is false. It also defines success as "values were applied and the caller sees success."
- **Baselines:** the review covers the staged index against `HEAD` (`ac09e55`). The worktree has no unstaged changes. The release baseline is tag `eval-release` (`2214073`), file `provider/settings.py`, read from local Git.

## Behavior and Compatibility

The released provider stores the settings and returns only `{"ok": True}`:
```python
storage[workspace_id] = dict(request["settings"])
return {"ok": True}
```

| Scenario | Expected | Candidate result |
|---|---|---|
| New client sends the extra `require_receipt` field to the released provider | Provider ignores it | Works. The provider only reads `request["settings"]`. |
| Ordinary save, `enhanced_settings=False`, released provider | Values stored, caller sees success | **Values are stored, but the client raises `RuntimeError("Provider did not acknowledge applied settings")`** |
| Provider returns `ok: False` | Client raises | Unchanged |
| Provider returns `ok: True, applied: True` (the not-yet-built Task 2 provider) | Success | Success; this is the only case the test covers |

- **New client with the released provider:** **Blocked.** Every save fails this way.
- **Old client with a new provider:** not applicable to this diff.
- **Feature flag:** it gives no protection, because `enhanced_settings` is never checked before the new check runs.

**Evidence limits:**
- The unit suite passed (1 test).
- My attempt to actually run the client against the released provider was denied, so the failing row comes from tracing the source, not from running it.
- No live environment was available or needed.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[client.py:5]** The client now requires an `applied` receipt that the released provider never sends, so every ordinary save fails after the values have already been stored.
  - Profile: generic · Checklist: —, plus python · `code-quality-checklist.md` (error handling) · Triggered by: content — `.py` extension
  - **What happens:** `save_settings(send, ws, values)` with the default `enhanced_settings=False` against the `eval-release` provider. The provider writes the values and returns `{"ok": True}`. `response.get("applied")` is `None`, so the client raises.
  - **Expected vs actual:** the caller should see success. Instead it gets an error even though the values were saved. This breaks the README's definition of success and its rule that each client increment can ship on its own. Callers may retry or show a failure for a save that actually worked.
  - **The test hides it:** `tests/test_client.py:8` was changed to return `applied: True`, so no test uses the released provider's response.
  - **Confidence: 95%.** The provider and client sources are both short and fully read, and there is no other code path. The remaining doubt is only that I didn't get to run the replay.
  - **Suggested fix:**
    - Treat a missing `applied` key as success from an older provider, and fail only on an explicit `applied: False`. For example: `if "applied" in response and response["applied"] is not True: raise ...`.
    - Optionally require the receipt only when the provider supports it, or when `enhanced_settings` is on.
    - Add tests for three cases: the released `{"ok": True}` response succeeds, `{"ok": True, "applied": False}` raises, and the existing receipt case still passes.

### P2 / P3
(none)

---

**Not covered:** behavior of the Task 2 provider, which doesn't exist yet. I only checked the receipt check against the shape the design describes (`applied: True`).

**Indexed:** the P1 is saved to the knowledge base as a reusable pattern (`kk:review-findings`): a client starting to require a new provider response field without checking the released provider.

This was a review only, so I haven't changed any code. Want me to apply the fix and the three tests?
