## Review Summary (Isolated Mode)

**Verdict: REQUEST_CHANGES.** Your increment can't merge to main by itself. With the released provider, every ordinary settings save now fails, even though the settings were actually applied.

**Reviewers**: code-reviewer finished. PAL **failed**: no PAL tools exist in this session, so there was no external review and nothing is corroborated.
**Files reviewed**: The reviewer and I read all of `client.py`, `tests/test_client.py`, the staged diff, the README and the feature docs. We also read the released provider `provider/settings.py` at `eval-release`. I extracted it from local Git and checked it matches blob `a6aeedb`.
**Intent and scope**: Task 1, client receipt handling (done). Task 2, provider receipts, is pending and was not treated as missing. I reviewed staged changes only; nothing is unstaged.
**Baselines**: The review base is HEAD `ac09e55` and the candidate is the staged version. The compatibility baseline is the tag `eval-release` (`2214073`). It is source only; the README says no live environment exists.

### Behavior and Compatibility

| Scenario | Result |
|---|---|
| New client with the released provider, ordinary save (`enhanced_settings=False`) | **Blocked.** The provider saves the settings and returns `{"ok": True}` with no `applied` key, so `client.py:5` raises. |
| Same save with `enhanced_settings=True` | **Blocked.** The receipt check ignores the flag. |
| A retry after that error | Each retry writes the same values and raises again. Nothing is corrupted, but the caller always sees failure. |
| Extra `require_receipt` key sent to the released provider | Supported: the provider only reads `request["settings"]`. |
| Provider returns `ok: False`, or `applied: False` | Both raise as expected (source reasoning only). Neither case has a test. |
| New client with the future Task 2 provider | Unknown: that provider's source isn't available. Only the test fake covers it. |

These results come from reading the code. I didn't run any tests.

### Code Reviewer Findings

- **P1 · [client.py:5] The receipt check breaks every ordinary save against the `eval-release` provider**
  - Profile: python · Checklist: code-quality-checklist.md · Triggered by: `.py` extension
  - **What fails:** `response.get("applied") is not True` is true when the key is missing. So every save against the released provider raises "Provider did not acknowledge applied settings", even though the settings were applied.
  - **Requirement broken:** The README and design doc require that each client increment supports `eval-release`. The README also says a pending provider task can't change that baseline.
  - **Confidence:** 97%. The whole client and provider were read, and the failing path has no other branches. It was not executed.
  - **Suggested fix:** At `eval-release`, `ok: True` is only returned after the settings are stored, so a missing `applied` key can safely count as "applied". Reject only an explicit non-`True` value:
    ```python
    if "applied" in response and response["applied"] is not True:
        raise RuntimeError("Provider did not acknowledge applied settings")
    ```
    The alternative is a capability handshake, which Task 2 would also have to implement.

- **P2 · [tests/test_client.py:8] The tests only use the future provider response**
  - The fake provider was changed from the released response `{"ok": True}` to `{"ok": True, "applied": True}`. That's why the regression above still passes the tests.
  - **Missing tests:**
    - the released-provider response `{"ok": True}`;
    - `applied: False` raising an error;
    - `ok: False` raising an error (this gap already existed);
    - a check that the request sends `require_receipt` and passes the settings unchanged.
  - **Confidence:** 92%.

### External Review Findings
None, because PAL was unavailable.

### Outstanding Evidence and Prerequisites
- **Merge blocker:** the P1 needs a fix, or you need to explicitly change the supported baseline or accept an exception.
- **Unknown future contract:** the design docs don't define the receipt format (`require_receipt`, and `applied` being exactly the boolean `True`). Task 2 needs it written down to match the client.

I indexed this mismatch between a new client requirement and the released provider as a reusable pattern under `kk:review-findings`.

This was a review only, so I haven't changed any files. Do you want me to apply the P1 fix and add the missing tests? I've kept the temporary evidence in `/tmp/kk-review-evidence-hWfP8m` for that follow-up and will delete it once we're done.
