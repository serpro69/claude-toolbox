## Review Summary (Isolated Mode, degraded)

**Reviewers:** only the `code-reviewer` sub-agent ran. The `pal codereview` reviewer didn't run because no `pal` tool exists in this session.
**Other limits:** Bash is denied here, so I couldn't capture the staged diff text or run the tests. The reviewer worked from the current files plus `git diff --cached --stat`: `payload.py` (1 line changed) and `tests/test_payload.py` (new, 11 lines). The old version of `payload.py:2` is unknown. It most likely just lacked `.strip()`.
**Profile:** python (security, SOLID, code-quality and removal-plan checklists applied)

### Code Reviewer Findings

**P0 / P1:** none.

- **`payload.py:2`: `None` or a non-string name now crashes before the request is sent.** P2, 60% confidence.
  - `save(transport, None)` raises `AttributeError` inside `build_payload`, so `transport.put` is never called.
  - If the old code passed the value through unchanged, `None` used to go out as JSON `null`, which is a common way to clear a field.
  - No caller in this repo passes `None`, so this only matters if code outside the repo does.
  - Fix: pass `None` through on purpose, or reject it with a clear `TypeError`, and add a test for whichever you choose.

- **`payload.py:2`: a name that is only spaces now becomes `""`.** P2, 65% confidence.
  - `tests/test_client.py:21-24` treats `{"display_name": ""}` as a valid body, so typing only spaces now sends the same thing as clearing the name.
  - If the `/settings` server reads `""` as "clear", an accidental few spaces erases the user's name with no error.
  - Fix: decide whether whitespace-only input should be rejected or treated as a clear, and test it.

- **`tests/test_payload.py:6-11`: the new tests only cover the normal cases.** P3.
  - Missing cases: `""`, whitespace-only, `None`, tabs/newlines and non-breaking spaces (which Python's `strip()` does remove).
  - Fix: add these as `subTest` cases.

- **`client.py:4-5`: no client-level test checks that trimming reaches the request.** P3.
  - Fix: add a test that `save(t, "  Ada  ")` sends `{"display_name": "Ada"}`.

**Author context:** I didn't write this change, so I have no design reasoning to add. I read `client.py` and `tests/test_client.py` myself and they match the reviewer's description. `save()` is the only caller in this repo.

**Indexing:** no P0/P1 findings, so there was nothing to save to the review-findings knowledge base.

### Is it ready to deploy?

**Probably yes, but not confirmed.**
- **What looks fine:** nothing blocks it. Traced by hand, all four tests (two new, two existing client tests) should pass, and the only caller in this repo keeps working.
- **What wasn't checked:** the tests weren't actually run, the real diff wasn't seen, and the second reviewer didn't run.
- **The real risk:** what happens to a name that is `None` or only spaces. Whether those cause a crash or erase a name depends on code outside this repo and on how the server treats `""` and `null`.

Before deploying I'd:
1. Run `python3 -m unittest discover -s tests`.
2. Run `git diff --cached payload.py` to confirm what the old line 2 was.
3. Decide how `None` and whitespace-only names should behave, and add tests for both.

### Next Steps

There are 4 findings, all from the one reviewer that ran: 2 P2 and 2 P3. I recommend fixing all four. None of them looks like a false positive.

**How would you like to proceed?**
1. **Fix all:** I'll handle `None` and whitespace-only names (tell me which behavior you want) and add the missing tests.
2. **Fix high severity only:** there are no P0/P1 findings, so this would mean the two P2 items.
3. **Fix specific items:** tell me which ones.
4. **No changes:** the review is done.

To get the full two-reviewer review, allow Bash and make `pal` available, then re-run `/kk:review-code:isolated`.
