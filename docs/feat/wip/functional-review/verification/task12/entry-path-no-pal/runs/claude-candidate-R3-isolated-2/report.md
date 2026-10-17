## Review Summary (Isolated Mode)

**Verdict: REQUEST_CHANGES.** The staged change breaks every ordinary settings save against the provider at `eval-release`. Your README says each client increment must support that provider.

- **Reviewers:** the `kk:code-reviewer` sub-agent completed. The PAL external reviewer could not run because no PAL tools are available in this session. So there is no second opinion, and nothing below is corroborated.
- **Files reviewed:** the staged `client.py` and `tests/test_client.py` (your working copy matches what's staged), `provider/settings.py` from `eval-release`, the README and the enhanced-settings design, implementation and task docs. The knowledge base was empty.
- **Scope:** task 1 (client receipt handling) only. Task 2 (provider receipts) is pending and was not treated as missing.
- **Baselines:** compared against the current commit (`ac09e55`) and, separately, `eval-release` (`2214073`). That second comparison is source-only; no deployed environment was checked, and the README says none is needed.

### Behavior and compatibility
| Scenario | Result |
|---|---|
| Ordinary save (`enhanced_settings=False`) against the `eval-release` provider | **Blocked.** The provider stores the values and returns `{"ok": True}`. The client then raises because `applied` is missing. This is new with this change. |
| Retrying after that false failure | **Blocked.** The provider rewrites the same values and the client raises again. Nothing ever recovers. |
| Old provider receiving the new `require_receipt` key | **Supported.** The provider only reads `request["settings"]` and ignores the extra key. |
| A receipt-aware provider returning `applied: True` | **Supported**, but only against the test's fake provider. |
| Does the `enhanced_settings` flag protect ordinary saves? | **No.** The flag doesn't control either the receipt request or the check. |
| Provider from task 2 | **Not applicable.** It's pending, not deployed, and can't change the supported baseline. |

I ran `python3 -B -m unittest discover -s tests` and the 1 test passed. That test's fake provider now returns `applied: True`, so it doesn't exercise the released provider's response.

### Code Reviewer Findings

**P1: `client.py:5-6`: the new receipt check breaks every ordinary save against the supported provider**
- **Trigger:** any `save_settings(...)` call that reaches the `eval-release` `update_settings`, which returns only `{"ok": True}`.
- **Expected:** success. README lines 4–6 make this a hard delivery requirement, and line 9 says an applied save must show the caller success.
- **Actual:** the values are written, then the client raises `RuntimeError("Provider did not acknowledge applied settings")` because `None is not True`.
- **Confidence:** 95%. The provider is 3 lines and the client logic is deterministic. The only gap is that the real `send` transport isn't in this checkout.
- **Suggested fix:** read the receipt tolerantly and fail only on an explicit `applied is False`. A missing `applied` means an older provider, whose `ok: True` already means the values were stored. Requiring `applied is True` should wait until the README names a receipt-emitting provider release as the baseline.
- I confirmed this against the `eval-release` source myself.

**P2: `tests/test_client.py:8`: the only test no longer covers the released provider's response**
- Before this change, the fake provider returned exactly what `eval-release` returns. Now it returns `applied: True`, which is why the P1 went unnoticed.
- No test covers a missing `applied`, `applied: False` or `ok: False`.
- **Suggested fix:** add a fake that behaves like `eval-release` (stores the settings, returns `{"ok": True}`) and assert success. Also add tests that `applied: False` and `ok: False` raise.
- Confidence: 90%.

### Outstanding evidence and prerequisites
- **Areas not covered:** the real `send` transport (assumed to pass the provider's response through unchanged) and task 2's exact receipt format. That includes whether it always sends `applied` and whether it uses a strict boolean. Neither changes the verdict.
- **Untracked follow-up:** once the README's supported baseline moves to a provider that emits receipts, the check can be tightened to strict. That isn't recorded in `tasks.md` yet.
- **Indexing:** I saved the "strict check on a field only an unreleased provider sends" pattern to the knowledge base as `kk:review-findings`.

### Next steps
This was review-only, so I haven't edited anything. I can:
1. Apply the tolerant receipt check in `client.py` and add the missing tests.
2. Add the strict-receipt follow-up to the execution context in `tasks.md`.

Temporary evidence in `/tmp/kk-evidence-CaLRxy/` and the instruction files in `/tmp/kk-review-instructions-*` are kept for any follow-up. I'll delete them once you decide.
