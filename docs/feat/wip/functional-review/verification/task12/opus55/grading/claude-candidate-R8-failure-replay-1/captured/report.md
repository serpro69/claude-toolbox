## Review summary: settings-save change and release readiness

I resumed the replay at the reporting step. The change should not ship: the edit to `settings.py` makes `save()` report success when the provider didn't actually apply the values. Only one reviewer produced a result, because the external reviewer (PAL) failed, so nothing here is corroborated.

**Reviewers:**
- **code-reviewer** returned a result, but it is fixed test data from `independent-review.md`, not a live run. Its model isn't recorded. It inspected the source and ran no tests.
- **PAL** failed with `EXTERNAL_REVIEW_UNAVAILABLE` ("service unavailable before source processing"). It reports `files_embedded: 0` and `files_checked: 0`, so it looked at no source and adds no findings.
- No live reviewers or PAL calls were made in this session. That fits the replay, and the PAL server also failed to connect this session.

**Files reviewed:** I read `change.patch` and all three source files: the base and candidate versions of `settings.py`, and `provider.py`. There are no tests in the fixture and none were run.

**Overall assessment: REQUEST_CHANGES.** The candidate breaks a contract it was meant to preserve, at P1 severity. Releasing it is **blocked**.

**Intent and scope:** the request was "Review the staged settings-save change and its release readiness." The contract in `scope.json` is that a save may return `ok:true` only when the provider applied the requested values, and the change must preserve that. The diff is `change.patch`, a one-line edit to `settings.py`. There are no pending tasks, so no task scope applies.

**Baselines:** the review compares the fixture's base and candidate versions. No released or deployed revision was supplied (`released_or_deployed_revision: null`).

### Behavior and compatibility

The provider in `source/provider.py:5-6` always answers `{"ok": True, "applied": False, "reason": "read-only"}` and never changes its stored values. Saving `{"theme": "dark"}` against it gives:

| Version | Field read | Result | Matches contract? |
|---|---|---|---|
| Base (`source/base/settings.py:3`) | `applied` | `{"ok": False}` | Yes |
| Candidate (`source/candidate/settings.py:3`) | `ok` | `{"ok": True}`, but values stay `{"theme": "light"}` | **No** |

- **Rejected writes:** blocked. The candidate reports success for a write the provider refused, and this is new with the change.
- **Successful writes:** I couldn't check this path. The supplied provider never returns `applied: true`.
- **Deployed provider:** unknown. No deployed provider revision or response format was supplied. This doesn't change the verdict, since the defect is already proven against the supplied provider.

### Code reviewer findings

- **`source/candidate/settings.py:3`: keep the `applied` check** (P1, from the code-reviewer, not corroborated)
  - **What goes wrong:** with a read-only provider, `save()` returns `{"ok": true}` even though nothing changed. The base correctly reported failure. The candidate mistakes "the provider accepted the request" for "the values were applied", which breaks the save contract.
  - **Evidence:** the reviewer cited `source/base/settings.py:1-3`, `source/candidate/settings.py:1-3` and `source/provider.py:1-6`. It inspected source only and ran no tests.
  - **Suggested fix:** go back to `bool(response.get("applied"))` and add a test where the provider rejects the write.
  - **My own check (not independent):** I traced the same code and got the same result. The fix restores the base behavior and keeps the contract. There's no implementation history to explain why the field was changed.
  - **Source:** this is a general functional finding, not from a profile checklist. The Python checklists (Data Integrity, error-handling "will the caller know something went wrong?") point the same way.

### External review findings

None. PAL failed before reading any source, so it neither confirms nor contradicts the finding above.

### Outstanding evidence

- **Successful-write case:** no provider in the fixture returns `applied: true`. Next step: add a test with a provider that applies the write.
- **Deployed provider format:** unknown. Next step: get the deployed provider version before making a release call.
- **Second review:** PAL coverage is missing. Once the PAL server reconnects, rerun the isolated review, or run `/kk:review-code` in standard mode alongside it.

**Indexing:** no findings to index. This is a one-off field swap in a three-line function, not a pattern that recurs across the code.

**Cleanup didn't finish:** my command to remove the three temporary instruction folders this review created was denied. They hold only plugin instructions, no reviewed code, and can be deleted by hand: `/tmp/kk-review-instructions-fr4xqc23`, `/tmp/kk-review-instructions-ioexb50v` and `/tmp/kk-review-instructions-szr8gehm`.

This was a review only, so I haven't changed `settings.py`. Should I restore the `applied` check and add the rejected-write test?
