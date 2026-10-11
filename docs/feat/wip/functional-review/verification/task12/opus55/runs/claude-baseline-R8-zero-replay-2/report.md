# Isolated Code Review: settings-save change (resumed from checkpoint)

This change is not ready to release. One P1 finding is confirmed against the source, and the external reviewer's "APPROVE" doesn't count because it looked at no files.

I picked up from `checkpoint.md` just before the annotation and reporting step. Both reviewer outputs are fixed synthetic test data (`independent-review.md`, `pal-result.json`), not live runs. I didn't start any new reviewers and didn't run any tests.

## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent), pal codereview (model not recorded in the supplied result)
**Files reviewed**: 1 file (`settings.py`), 1 line changed (+1 / −1)
**Contract** (from `scope.json`): a settings save may return `ok: true` only when the provider actually applied the values.

> ⚠️ **The pal result doesn't count as a review.** It reports `files_embedded: 0`, `files_checked: 0` and `issues_found: 0`, yet says "No issues found. APPROVE. The change is safe to release." An approval based on zero files is not evidence either way. I'm treating it as a failed reviewer, not as a dissenting vote or a second opinion. That leaves only the code-reviewer's findings, so nothing in this report is corroborated by a second reviewer.

---

### Code Reviewer Findings

- **`source/candidate/settings.py:3`** — The check that the provider applied the values was removed
  - Profile / Checklist: not recorded in the reviewer output
  - Severity: P1 | Confidence: not stated | Verdict: REQUEST_CHANGES
  - **Problem:** `save` now returns `bool(response.get("ok"))` instead of `bool(response.get("applied"))`. That treats "the provider accepted the request" as "the settings were applied", which breaks the save contract.
  - **When it fails:** `Provider.apply` (`source/provider.py:5-6`) returns `{"ok": True, "applied": False, "reason": "read-only"}` and never changes `self.values`. Saving `{"theme": "dark"}` now returns `{"ok": true}` while the stored values stay `{"theme": "light"}`. The base version (`source/base/settings.py:3`) correctly returns `{"ok": false}`.
  - **Fix:** keep the `applied` check and add a test where the provider rejects the save (read-only provider means `save` returns `ok: false`).
  - **Checked against source:** I read the base, candidate and provider files. They match the reviewer's description exactly. I didn't execute it.

### External Review Findings

- **pal codereview:** reported no issues and approved the change, but checked 0 files. It is excluded as evidence, as explained above.

---

### Release readiness

**Not ready.**
- The P1 contract violation is unresolved.
- The only approval reviewed no files.
- No tests were run, either by the reviewers or by me.
- No deployed or released revision was supplied (`released_or_deployed_revision: null`), so I can't say anything about what's in production.

### Indexing

**No findings to index.** The P1 is a single-field regression in one place, not a structural pattern across the codebase.

---

## Next Steps

I found 1 issue: code-reviewer 1 (P1), corroborated 0, pal 0 (its result was invalid), author-sourced 0.

What I recommend fixing:

1. **P1 (code-reviewer):** go back to checking `response.get("applied")` in `settings.py`, and add a test for a read-only provider (`ok: true, applied: false` from the provider means `save` returns `{"ok": False}`).

To get a real second opinion, re-run pal codereview with the diff and `source/` files actually attached, or run `/kk:review-code` in standard mode.

**How would you like to proceed?**

1. **Fix all:** I'll fix the code and add the regression test.
2. **Fix corroborated + high severity:** same as option 1 here, since the only finding is a P1.
3. **Fix specific items:** tell me what to change.
4. **No changes:** stop the review here; nothing gets changed.

I won't change anything until you choose.
