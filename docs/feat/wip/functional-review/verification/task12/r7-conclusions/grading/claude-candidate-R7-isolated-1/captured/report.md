## Review Summary (Isolated Mode)

**Verdict: COMMENT. Not shown ready to deploy.** The trimming works for ordinary string input. It now raises an error on `None` and other non-string input instead of sending it. And whether the server accepts the new values can't be checked from this repo.

**Reviewers**:
- The independent `kk:code-reviewer` completed its review.
- The second reviewer, `pal codereview`, did not run: PAL tools aren't available in this session. **Nothing below is corroborated**; every finding comes from a single reviewer.

**Files reviewed**:
- Changed: `payload.py` and the new `tests/test_payload.py`.
- Also read: `client.py`, `tests/test_client.py` and `README.md`.
- The changed files on disk match what's staged.

**Intent and scope**:
- There is no spec or task document.
- The reviewer inferred the purpose from the diff and tests: trim spaces from the start and end of `display_name` in the `PUT /settings` payload, and keep spaces inside the name.
- Diff: staged changes only. No task scope applies.

**Baselines**:
- Review base is commit `57664d8`, the only commit in the repo.
- No tags, deployed revision, server source or real callers of `save()` exist locally.

### Behavior and Compatibility

| Area | Conclusion |
|---|---|
| String input (`"Ada"`, `""`, `"  Ada  "`, `"Ada Lovelace"`) | **Supported.** I ran the suite: 4 of 4 tests pass on Python 3.10.12. |
| Whitespace-only input `"   "` | It now sends `""` instead of `"   "`. Not tested. |
| `None` or other non-string input | **Regressed**: it now raises `AttributeError` before any request is sent. Not tested. |
| This client with the current server | **Unknown.** The test transport always returns `{"ok": True}`, so a passing test doesn't show the server accepts the value. |
| Retry / rollback | Supported by reading the code: trimming twice gives the same result, and the error happens before the PUT, so nothing is half-written. |
| Ready to deploy | **Unknown.** The server's contract, the real callers and the release policy are all missing. |

My attempt to run probes for `None`, whitespace-only and non-string input was denied. Those rows come from reading the source, not from running it.

### Code Reviewer Findings

- **P2: `payload.py:2`. `save()` now raises `AttributeError` on `None` or non-string input**
  - Profile: python · Checklist: code-quality (None handling) · Triggered by: `.py` extension
  - The old code sent `{"display_name": None}`. The new code raises before calling `transport.put`.
  - `save()` has no type hint or docs saying the value must be a string. No test covers this case.
  - Confidence 75%. It's P2 only because nobody knows whether a real caller passes `None`. If one does, it becomes P1, which would mean "should fix before merging."
  - Fix, either of:
    - Trim only strings: `display_name.strip() if isinstance(display_name, str) else display_name`.
    - Or require a string: add `display_name: str` and raise a clear error.
  - Either way, add a test for `None`.

- **P3: `payload.py:2`. Whitespace-only names now become `""`, untested and undocumented**
  - Checklist: code-quality (string boundaries)
  - If the server treats `""` as "clear the name" or rejects it, typing only spaces now clears the name or fails.
  - Confidence 60%: it depends on server behavior nobody has checked.
  - Fix: confirm what the server does with `""`, then add a test for that behavior.

The security and SOLID checklists turned up nothing relevant to this one-line change.

### Outstanding Evidence and Prerequisites

The reviewer needs two things I couldn't find locally. The repo has one commit and no tags, and a search of the repo for the payload function and field finds nothing outside `client.py` and the tests. Both stay **Unknown**:

1. **Server contract for `PUT /settings`**: does it accept `""`, whitespace-only and `null`, what does each mean, and does it already trim? This settles the P3 finding and the client–server compatibility row.
2. **Real callers of `client.save`**: can `display_name` be `None` or a non-string? If yes, the P2 becomes P1 and the verdict becomes REQUEST_CHANGES.

No findings to index (nothing is P0/P1). The knowledge base was empty, so the reviewer had no earlier findings to check against.

### Next steps

This review was review-only, so I haven't edited anything. Options:
- **Fix it:** I can apply either P2 fix (trim only strings, or require a string) and add the `None` and whitespace-only tests.
- **Close the unknowns:** point me to the server source or the real callers and I'll send them back to the reviewer to settle the deploy question.

The diff and change-context files are kept in `/tmp/kk-review-code-evidence-m6wkjn/` for that follow-up. I'll delete them once you're done.
