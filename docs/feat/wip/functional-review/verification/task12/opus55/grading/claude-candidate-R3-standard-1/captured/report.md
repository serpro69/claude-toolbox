## Code Review Summary

**Overall assessment:** REQUEST_CHANGES. The staged client breaks every ordinary settings save against the released provider.

**Files reviewed:** 2 files (`client.py`, `tests/test_client.py`), 4 lines added and 2 removed (staged diff; nothing unstaged).

**Intent and scope:** Task 1 of `docs/feat/wip/enhanced-settings` (status: done) adds client-side receipt handling. Task 2, provider receipts, is pending and out of scope. The README and `design.md` set a hard rule: every merged client increment must work with the released provider at tag `eval-release`, including ordinary saves while `enhanced_settings` is false.

**Baselines:** The review base is `ac09e55` (HEAD) and the candidate is the staged index. The release baseline is `eval-release` → `2214073`, `provider/settings.py` (blob `a6aeedb`).

## Behavior and Compatibility

I traced one ordinary save through the staged client and the released provider:

| Path | Released provider | Staged client | Result |
|---|---|---|---|
| `save_settings(send, "w", {...})` with the flag off | Writes `storage[w]` and returns `{"ok": True}` | `ok` check passes. `response.get("applied")` is `None`, and `None is not True`, so it raises `RuntimeError` | **Blocked** |
| Request shape | Reads only `request["settings"]` and ignores `require_receipt` | Sends the extra key | Supported |
| New client with the Task 2 provider | Not written yet | — | Out of scope (pending) |
| Rollback | Client-only change, no stored state | — | Not applicable |

**Evidence limits:** This is all from reading the code. My requests to run the unit tests and a check against the released provider were denied, so nothing was executed. The trace is short and conclusive, but it hasn't been run.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[client.py:5]** The new receipt check rejects every save against the released provider, and those settings have already been written.
  - Profile: generic · Checklist: — (also covered by python/code-quality-checklist.md, Error Handling and None handling)
  - Triggered by: python content signal (`.py` extension)
  - **Trigger:** Any `save_settings` call against the `eval-release` provider, whether the flag is on or off. That provider never returns `applied`.
  - **Expected:** Ordinary saves succeed (README: "every merged client increment must support the released provider… including ordinary settings saves while enhanced_settings is false"). A successful save means values were applied and the caller sees success.
  - **Actual:** The provider stores the values, then the client raises `RuntimeError("Provider did not acknowledge applied settings")`. Every ordinary save fails. The caller is told the save failed when it actually went through, so retries and error messages are wrong too.
  - **Why the test misses it:** `tests/test_client.py:8` was updated to return `applied: True`, a response shape only the pending Task 2 provider will send. It no longer covers the released provider.
  - **Confidence:** 95%. I read both files at the exact revisions. The `.get()` call returns `None` and the `is not True` check raises. The only remaining doubt is that I couldn't run it.
  - **Suggested fix:** Only enforce the receipt when the provider supplies one. For example, raise only if `"applied" in response and response["applied"] is not True`, or tie strict enforcement to a negotiated provider capability. Don't tie it to `enhanced_settings` alone, because ordinary saves would still need the old-provider path once the flag is turned on. Add tests for:
    - the released-provider response `{"ok": True}` succeeding
    - `applied: False` raising
    - `applied: True` succeeding

### P2 / P3
(none)

---

**What else was checked:** No security problems (no injection, deserialization or secrets). No SOLID problems at this size. Nothing to remove.

**Knowledge base:** It was empty, so there were no earlier findings or Python idioms to compare against. I indexed this P1 finding under `kk:review-findings` as a reusable pattern: a new client requiring a response field that only an unreleased provider sends.

**Next step:** This was a review only, so I haven't changed any code. The P1 needs fixing before merge. Should I apply the suggested fix and the three tests?
