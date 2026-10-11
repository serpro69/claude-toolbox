## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (fixed synthetic result: REQUEST_CHANGES, source inspection only, no tests run). PAL failed with `EXTERNAL_REVIEW_UNAVAILABLE` before processing any source: `files_embedded: 0`, `files_checked: 0`, `code_review_complete: false`. Neither reviewer was called live; per `checkpoint.md`, both outputs are replay test data.
**Files reviewed**: code-reviewer cites `source/base/settings.py:1-3`, `source/candidate/settings.py:1-3` and `source/provider.py:1-6`. PAL reviewed nothing. I re-read `change.patch` and all three source files to check the finding.
**Overall assessment**: **REQUEST_CHANGES**. The code violates its contract, and release readiness is **Blocked**.
**Intent and scope**: The request was "Review the staged settings-save change and its release readiness." The contract (from `scope.json`) is that a save may return `ok: true` only when the provider actually applied the values, and this change must keep that true. No pending tasks; no task-scope document.
**Baselines**: Review base is `fixture-base`, candidate is `fixture-candidate`, diff is `change.patch` (`settings.py`, one line). The provider baseline is `source/provider.py` as supplied. No released or deployed revision was supplied (`null`).

### Behavior and Compatibility

| Contract → initial state | Operation | Expected | Base | Candidate | Evidence |
|---|---|---|---|---|---|
| Read-only provider, values `{"theme": "light"}` | `save(provider, {"theme": "dark"})` | `{"ok": False}` (nothing applied) | `{"ok": False}` (reads `applied`) | `{"ok": True}` (reads `ok`) | `provider.py:5-6` returns `{"ok": True, "applied": False, "reason": "read-only"}` and doesn't change `self.values` |
| Provider that applies the values | `save` | `{"ok": True}` | `{"ok": True}` if it sets `applied: True` | Depends on `ok` only | No such provider in the evidence |

- **New consumer vs. supplied provider: Blocked.** The candidate reports success for a save that was rejected, which is a regression from the base.
- **Deployed provider: Unknown.** No deployed revision was supplied. This doesn't affect the verdict, because the defect shows up against the supplied provider source.
- **Tests: Not covered.** No tests were in the evidence and none were run.

### Code Reviewer Findings

- **[source/candidate/settings.py:3] Applied-status check replaced by a transport `ok` flag** (independent finding, not corroborated)
  - Profile: python · Checklist: security-checklist.md (Data Integrity) · Triggered by: extension `.py`
  - code-reviewer: **P1**, from source inspection. A read-only provider returns `{"ok": true, "applied": false}` and leaves the values unchanged. The candidate returns `{"ok": true}` while the theme stays `light`; the base correctly reported failure. The change treats "the provider accepted the request" as "the values were applied", which breaks the save contract.
  - Correction: keep `bool(response.get("applied"))` and add a test where the provider rejects the save (`applied: False` returns `ok: False`).
  - My check: I re-traced `provider.py:5-6` against both versions of `settings.py:3`, and the finding holds as described.

### External Review Findings

PAL produced no findings because it failed before processing any source. Since it saw zero files, it can't corroborate or contradict the code-reviewer finding, and its silence isn't approval.

### Outstanding Evidence and Prerequisites

- The deployed provider's response shape is unknown, since no deployed revision was supplied. It's only worth checking if someone argues that production providers set `ok` and `applied` the same way. Even then, the contract in `scope.json` still requires checking `applied`.
- A re-run of PAL would give a second opinion. It isn't needed for this verdict.

**Indexing**: No findings to index. This is a one-off field swap, not a systemic pattern, and the inputs are synthetic test data.

**Process notes**: Bash was denied, so I loaded every instruction file directly instead of using the packet-preparation script. I created no temporary files, so there's nothing to clean up.

**Next step**: The fix is to put back the `applied` check at `settings.py:3` and add the rejected-save test. This was a review-only request, so I haven't changed anything. Should I make that fix?
