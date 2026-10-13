## Review Summary (Isolated Mode)

**Verdict: REQUEST_CHANGES.** Every ordinary save against the released provider now fails. The fix is small.

**Reviewers**: The code-reviewer sub-agent completed. **PAL did not run**: no `pal` tools are available in this session. Every finding below therefore comes from a single reviewer, and nothing is corroborated.

**Files reviewed**: The staged diff, `client.py` and `tests/test_client.py` at the staged state (no unstaged edits), the released `provider/settings.py` at tag `eval-release`, the README, and the enhanced-settings `design.md`, `implementation.md` and `tasks.md`. **No tests were run** by me, the reviewer or the author. All conclusions come from reading source.

**Intent and scope**: The README and design doc require every client change to keep working with the provider released at `eval-release`, including ordinary saves with `enhanced_settings=False`. Task 1 (client receipt handling, done) is in scope. Task 2 (provider receipts, pending) is out of scope. I reviewed the staged diff only.

**Baselines**: The review base is HEAD `ac09e55`. The compatibility baseline is tag `eval-release` (`2214073`), file `provider/settings.py`, blob `a6aeedb`. I compared source only, not a deployment; the README says no live environment is needed.

### Behavior and Compatibility

| Scenario | Result |
| --- | --- |
| Released provider, ordinary save | **Blocked.** The provider stores the values and returns `{"ok": True}` with no `applied` key. The client then raises `RuntimeError`. |
| Released provider receives the new `require_receipt` key | **Supported.** The provider only reads `request["settings"]`, so the extra key is ignored. |
| Caller retries after the failure | **Blocked.** Every retry fails the same way. |
| Future provider that returns `applied: True` | **Supported for the client only.** Task 2's actual response shape isn't defined anywhere yet, so whether it matches is **Unknown**. |
| Independently releasable main (README requirement) | **Blocked** until the P1 below is fixed. |

### Code Reviewer Findings

- **P1 — `client.py:5`: the required `applied` receipt breaks saves against the released provider, and reports failure after the values were already applied.**
  - **Profile**: generic.
  - **What happens**: The provider persists the values, then returns `{"ok": True}`. In the client, `response.get("applied") is not True` is true, so it raises `RuntimeError`.
  - **Why it matters**: The README says a successful save means the values were applied and the caller sees success. Here the values are applied and the caller sees an error.
  - **Origin**: This change introduced it; the code before this change accepted `{"ok": True}`.
  - **Hidden by the test**: The test response changed from `{"ok": True}` (the released provider's shape) to `{"ok": True, "applied": True}` (the pending Task 2 shape). That removed the only coverage of the supported provider.
  - **Confidence**: 95%. Both sides are fully visible (3 provider lines, 7 client lines).
  - **Suggested fix**: treat a missing receipt as success from the released provider, and reject only an explicit non-`True` value:
    ```python
    if "applied" in response and response["applied"] is not True:
    ```
    Keep sending `require_receipt` and restore a `{"ok": True}` success test. Gating the check on `enhanced_settings` would be a weaker fix: enhanced saves would still fail after applying values, and it ties the protocol to a UI flag.
  - **Author context**: none on record.

- **P3 — `tests/test_client.py`: the new rejection branch has no tests.**
  - Nothing exercises `applied: False` raising, and nothing checks that the request includes `require_receipt`.
  - Confidence: 80%.
  - Suggested tests: `{"ok": True}` succeeds, `{"ok": True, "applied": False}` raises, and the sent request contains `"require_receipt": True`.

### Outstanding Evidence and Prerequisites

- **Still undefined**: the receipt contract (the `applied` key name and its strict boolean type). It becomes reviewable once Task 2 defines it; until then it's Unknown, not a defect.
- **Deferred tightening**: make the receipt mandatory only after the supported baseline moves to a provider that sends receipts. This isn't tracked anywhere yet; a natural home is the Execution context of Task 1 or Task 2 in `docs/feat/wip/enhanced-settings/tasks.md`.
- **Already broken before this change**: a non-dict `send` response raises `AttributeError` at `client.py:3`. Not reported as a finding.

**Indexing**: I recorded the P1 as a recurring pattern under `kk:review-findings`: a new client requiring a response field the released provider doesn't send, with the test updated to the future shape.

**Temporary files**: the evidence bundle is in `/tmp/kk-review-code-GQVKG1` and the instruction packets are in `/tmp/kk-review-instructions-*`. I've kept them in case you want a follow-up review after the fix.

**Next step**: should I apply the P1 fix and the P3 tests, then run `python3 -B -m unittest discover -s tests`? This was a review-only request, so I haven't edited anything.
