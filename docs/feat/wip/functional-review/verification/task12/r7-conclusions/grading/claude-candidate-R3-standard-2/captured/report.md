## Code Review Summary

**Files reviewed**: 2 files, 6 lines changed (staged: `client.py`, `tests/test_client.py`)
**Overall assessment**: **REQUEST_CHANGES**
**Intent and scope**: Task 1 of enhanced-settings, "Client receipt handling" (status: done). Task 2, provider receipts in a separate repo, is pending and out of scope. The requirements come from `README.md` and `docs/feat/wip/enhanced-settings/{design,implementation,tasks}.md`. Each client increment must work with the released provider at `eval-release` and keep main independently releasable. Ordinary saves must keep working while `enhanced_settings` is false.
**Baselines**: Review base is `ac09e55` and the candidate is the staged index. The release baseline is tag `eval-release` = `2214073`, file `provider/settings.py`. I read it from local Git because the file was removed from the working tree.

## Behavior and Compatibility

| Scenario | Expected | Candidate | Evidence |
|---|---|---|---|
| Ordinary save (`enhanced_settings=False`) against the released provider | Values stored, caller sees success | Values stored, then the client raises `RuntimeError("Provider did not acknowledge applied settings")` | Ran it: `storage == {'w': {'label': 'blue'}}` and the client raised |
| Released provider receives the extra `require_receipt` key | Ignored | Ignored: the provider only reads `request["settings"]` | Source at `eval-release` |
| Save against a provider that returns `applied: True` | Success | Success | Unit test passes (1 test, OK) |
| `ok: False` | Raise | Raise (unchanged) | Source |

- **New client against the released provider: Blocked.** This is a demonstrated failure on the main path, and it happens with the feature disabled.
- **New client against the pending Task 2 provider: Unknown.** That provider isn't written yet. The client-only test uses a fake shaped like the new protocol, so it says nothing about the real provider contract.
- **Disabled-flag safety: Blocked.** The receipt check doesn't depend on `enhanced_settings`.
- **Live/deployed environment: Not applicable.** The README says no live environment is available or required.

---

## Findings

### P0 - Critical
(none)

### P1 - High

- **[client.py:5]** The client always requires `applied: True`, so every ordinary save fails against the released provider
  - Profile: python · Checklist: code-quality-checklist.md (error handling / boundary conditions), plus the generic functional/compatibility method
  - Triggered by: content — `.py` extension
  - **Trigger/path:** any `save_settings(...)` call, including the default `enhanced_settings=False`, sent to the `eval-release` provider. That provider stores the values and returns `{"ok": True}` with no `applied` key.
  - **Expected:** the save succeeds. The README defines success as "values were applied and the caller sees success", and the design requires ordinary saves to keep working with `eval-release`.
  - **Actual:** the settings are written, then the client raises `RuntimeError`. The caller sees a failure for a save that actually took effect, which can also lead to pointless retries or a misleading error in the UI. Main can't be released on its own until Task 2 ships. That breaks the independent-release requirement, and the pending task doesn't excuse it.
  - **Confidence:** 97%. I reproduced it by running the staged `client.py` against `provider/settings.py` from `git show eval-release:`. Nothing in the code reads `enhanced_settings` before the check.
  - **Suggested fix:** require the receipt only when the protocol is active, for example only when `enhanced_settings` is true. Keep the legacy path, where `ok` alone means success, for ordinary saves. Sending `require_receipt` is harmless to the old provider, but it could also be sent only when gated. Add tests that:
    - run `{"ok": True}` (the released shape) with the flag off and expect success
    - check that a missing or false `applied` raises when the receipt is required

### P2 - Medium
(none separate. The missing test for the legacy response shape is part of the P1 fix.)

### P3 - Low
(none)

---

## Coverage and limits

- **Checked:**
  - the full staged diff and both staged files
  - README and the feature docs
  - the released provider source at `eval-release`
  - the existing unit suite (1 test, passes)
  - a reproduction against the released provider
  - the Python security, SOLID, code-quality and removal checklists. No security, injection, concurrency or removal concerns apply to this 4-line change.
- **Not covered:** the Task 2 provider (pending, in another repository), so whether the receipt protocol actually works end to end is still Unknown. Once Task 2 lands, check that the provider's `applied` field matches what the client expects.
- **Indexed:** the "unconditional dependency on a new provider field breaks independent release" pattern, as `kk:review-findings`.
- **Knowledge base:** `capy` had no prior entries to search (cold start).

## Next steps

One fix is required: make the receipt check conditional so ordinary saves succeed against `eval-release`, and add a test with the legacy response shape. This was a review-only request, so I haven't changed any files. Should I make that fix?
