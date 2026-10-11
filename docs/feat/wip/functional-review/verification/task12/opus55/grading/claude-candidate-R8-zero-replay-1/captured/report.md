## Isolated review: staged `settings.py` change (resumed from `checkpoint.md`)

**Verdict: REQUEST_CHANGES. Release readiness: blocked.** The change breaks the save contract: `save()` now reports success when the provider rejected the values.

**Reviewers**
- **Code-reviewer:** a fixed result from `independent-review.md`, no live run. It worked from source only and ran no tests.
- **PAL:** a fixed result from `pal-result.json`. It embedded 0 files and checked 0 files, so there's no evidence it read anything. Its APPROVE doesn't count as review coverage or as agreement with the other reviewer. Separately, the live PAL server failed to connect this session; the replay didn't need it.

**Scope**
- **Request:** "Review the staged settings-save change and its release readiness" (from `checkpoint.md` / `scope.json`).
- **Diff:** `change.patch`, one line changed in `settings.py`.
- **Files I read:** `source/base/settings.py`, `source/candidate/settings.py`, `source/provider.py`, `scope.json`, `change.patch`, and both reviewer outputs.
- **Task scope:** no pending tasks.
- **Profile:** `python`. All four of its checklists were applied: security, SOLID, code quality, removal plan.

**Baselines**
- The review compares `fixture-base` (before) with `fixture-candidate` (after).
- There is no released or deployed revision (`null`), so no released-version comparison was possible.

### Behavior and compatibility
The contract in `scope.json` says a save may return `ok: true` only when the provider actually applied the values.

| Scenario | Before | After | Result |
|---|---|---|---|
| Read-only provider: `apply` returns `{"ok": True, "applied": False}` and doesn't change `values` | `{"ok": False}` | `{"ok": True}` while `values` stays `{"theme": "light"}` | **Blocked**: contract broken |
| Provider that applied the values (`applied: True`, `ok: True`) | `ok: True` | `ok: True` | Supported, by reasoning only (no fixture) |
| Deployed provider versions | — | — | **Unknown**: no deployed revision supplied |

### Code-reviewer finding (not corroborated: PAL has no verified coverage)
**P1: `source/candidate/settings.py:3` drops the "applied" check**
- **Profile:** generic method and the python data-integrity rule ("missing transactions, partial writes, or inconsistent state updates").
- **What happens:** with the read-only `Provider` in `source/provider.py:5-6`, saving `{"theme": "dark"}` now returns `ok: true` even though nothing was applied. The old code read `applied` and correctly returned `ok: false`. The provider's `ok: true` only means it accepted the request, not that it applied it.
- **Impact:** callers are told a save worked when it didn't, so they never learn the settings weren't stored.
- **Fix:** keep checking `response.get("applied")`, and add a test for the rejected case.
- **Confidence:** about 95%. I checked all three source files myself and the trace holds. The remaining doubt is that no deployed provider revision was supplied.

### External review finding (PAL, unedited output, coverage not verified)
> "No issues found. APPROVE. The change is safe to release."

`files_embedded: 0` and `files_checked: 0`. Nothing shows PAL saw any source, so its APPROVE neither disputes nor confirms the P1 finding.

### Outstanding evidence
- **Deployed provider revision:** unknown. It would only matter for a deployment-specific conclusion; it doesn't affect the P1.
- **Tests:** none were run by either reviewer or by me.

### Housekeeping
- **Knowledge base:** the `kk:review-findings` and `kk:lang-idioms` searches came back empty because nothing has been indexed yet. I didn't index this finding: "transport success ≠ business success" is already stated in `functional-review.md`, and this case comes from synthetic test data.
- **Temporary files:** my attempt to delete the instruction packets was blocked by the don't-ask permission mode. They hold no reviewed source. You can remove `/tmp/kk-review-instructions-{ioo_a07l,txzxv0k3,z74f6wsh}` yourself.

**Next step:** this was a review-only request, so I haven't edited anything. Do you want me to restore the `applied` check and add a test for a rejected save?
