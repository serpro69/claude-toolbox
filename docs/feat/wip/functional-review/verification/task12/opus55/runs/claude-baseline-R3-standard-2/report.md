## Code Review Summary

**Files reviewed**: 2 files (`client.py`, `tests/test_client.py`), 6 lines changed (staged)
**Profiles**: `python`. I applied all four of its always-load checklists (security, SOLID, code quality, removal-plan) plus the generic categories.
**Overall assessment**: **REQUEST_CHANGES**. This change breaks every ordinary settings save against the provider version we support.

---

## Findings

### P0 - Critical

- **[client.py:5](client.py:5)** The new receipt check rejects every save from the released provider, after that provider has already written the values
  - Profile: python · Checklist: security-checklist.md (Data Integrity) / code-quality-checklist.md (Error Handling)
  - Triggered by: content: `.py` extension
  - The README says every client increment must work with the provider at tag `eval-release`, including ordinary saves while `enhanced_settings` is false. That provider (`git show eval-release:provider/settings.py`) stores the settings and returns only `{"ok": True}`. It never sends `"applied"`. The new check `response.get("applied") is not True` runs for every save, so every save now raises `RuntimeError`. The values are already stored when it does, so the caller is told the save failed when it actually succeeded. That contradicts the README's definition of success ("values were applied and the caller sees success").
  - Confirmed by running it against the tag's provider source:
    ```
    RAISED: Provider did not acknowledge applied settings | storage after: {'w': {'label': 'blue'}}
    ```
  - Confidence: 98%. I checked the provider at the tag and reproduced the failure. The only open question would be whether some other provider is supported, and the README names `eval-release` as the supported one.
  - Suggested fix: only require the receipt when the new behaviour is turned on, and leave the ordinary path exactly as it was. For example:
    ```python
    request = {"settings": values}
    if enhanced_settings:
        request["require_receipt"] = True
    response = send(workspace_id, request)
    if not response.get("ok"):
        raise RuntimeError("Settings save failed")
    if enhanced_settings and response.get("applied") is not True:
        raise RuntimeError("Provider did not acknowledge applied settings")
    ```
    Even with this gate, turning `enhanced_settings` on against the released provider would still fail after a write. That is acceptable only while the enhanced UI is off by default and Task 2 hasn't shipped. If you'd rather avoid that case too, accept a missing `applied` field and reject only an explicit `applied: False`.

### P1 - High

- **[tests/test_client.py:8](tests/test_client.py:8)** The test was changed to match the new code, which hides the incompatibility
  - Profile: generic · Checklist: —
  - Triggered by: —
  - The fake `send` used to return `{"ok": True}`, which is what the released provider actually returns. It was changed to `{"ok": True, "applied": True}`, a response no provider in this repo's supported set sends. So the test passes (`Ran 1 test … OK`) while real saves fail.
  - Confidence: 95%. The diff shows the old fake matched the released response exactly.
  - Suggested fix: keep a test whose fake returns exactly `{"ok": True}` and assert the ordinary save succeeds. Add enhanced-path tests for `applied: True` (success), a missing `applied` (failure), and `applied: False` (failure). Also assert that `require_receipt` is sent only when `enhanced_settings=True`.

### P2 - Medium

- **[client.py:2](client.py:2)** `require_receipt` is sent unconditionally, and nothing in the client uses the `enhanced_settings` flag to change behaviour
  - Profile: python · Checklist: solid-checklist.md (OCP)
  - Triggered by: content: `.py` extension
  - The released provider ignores the extra key, so it does no harm today. But the protocol change isn't tied to the feature flag the design names, so it can't be switched off. The P0 fix above covers this too.
  - Confidence: 80%. It's harmless now and only matters for keeping the rollout controllable.

### P3 - Low

(none)

---

## Removal/Iteration Plan
Not applicable. Nothing is being removed.

## Additional Suggestions
- Before merging any client increment, run it against `git show eval-release:provider/settings.py`, as I did above. A small test helper that loads the tagged provider would make this automatic.
- Capy had no earlier `kk:review-findings` or `kk:lang-idioms` entries, so the knowledge base was empty. I saved the P0 pattern as `kk:review-findings`: protocol changes not gated by the flag, plus fakes that use the new response shape.

---

## Next Steps

I found 3 issues (P0: 1, P1: 1, P2: 1, P3: 0).

The fixes I recommend:
1. **P0**: Require the receipt only when `enhanced_settings` is on, so ordinary saves work with the `eval-release` provider again.
2. **P1**: Bring back the released-provider response in the test and add the enhanced-path tests listed above.
3. **P2**: Send `require_receipt` only when `enhanced_settings` is on (fixed along with item 1).

Nothing to keep as-is. I'm confident none of these are false positives.

**How would you like to proceed?**

1. **Fix all**: I'll implement all the suggested fixes
2. **Fix P0/P1 only**: Address the critical and high-priority issues
3. **Fix specific items**: Tell me which issues to fix
4. **No changes**: Review complete, no implementation needed
