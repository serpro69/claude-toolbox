## Review summary (isolated mode)

**Is it ready to deploy? Not yet.** I see nothing actually broken: the change works for normal text input and all 4 tests pass. But two behavior changes depend on how the `/settings` server handles values, and nothing in this repo tells us that.

**Verdict: COMMENT.** No blocking defects. Release readiness is **Unknown**.

**What ran:**
- **Independent reviewer:** the `kk:code-reviewer` agent, which had no access to this conversation, finished successfully. It read the diff, `payload.py`, `tests/test_payload.py`, `client.py`, `tests/test_client.py` and `README.md`.
- **Second reviewer (PAL):** did not run. Its server failed to connect this session, so no finding below is confirmed by two reviewers, and the result is less rigorous than a full isolated review.
- **Tests:** I ran `python3 -B -m unittest discover -s tests` on the staged code: 4 passed.

**Scope:** the staged changes only (there were no unstaged changes), compared against HEAD `57664d8`. There's no spec or task doc, so I inferred the purpose: trim spaces from the start and end of display names before `PUT /settings`. The Python checklists applied, and no other profiles matched.

### How behavior changes

| Input | Before | After | Covered by a test? |
|---|---|---|---|
| `"Ada"`, `""`, `"Ada Lovelace"` | unchanged | unchanged | yes |
| `"  Ada  "` | `"  Ada  "` | `"Ada"` | yes |
| `"   "` (only spaces) | sent as-is | `""` | no |
| Unicode spaces, e.g. a non-breaking space | sent as-is | removed | no |
| `None` or any non-text value | sent as `null` | crashes with `AttributeError`; nothing is sent | no |

- **Compatibility with the current server:** for text input, the new client sends nothing the old one couldn't already send, including `""`.
- **Server meaning of `""`, whitespace and `null`:** unknown.
- **Rollback:** safe. The change is client-only and has no migration.
- **Existing stored data:** names already saved with extra spaces stay as they are; only new saves are trimmed.

### Findings (from the independent reviewer)

**P2 · `payload.py:2`: `None` now crashes instead of being sent.** (confidence 55%)
- Before, `build_payload(None)` sent `{"display_name": null}`. Now `None.strip()` raises `AttributeError` and the request never goes out.
- If the API uses `null` to clear a name, that flow now breaks.
- No caller in this repo passes `None`, but `save` looks like a public function and callers outside the repo aren't visible.
- **Fix:** decide what `None` should mean and add a test for it. Either keep passing it through (`display_name.strip() if isinstance(display_name, str) else display_name`), or reject it on purpose with a type hint and a clear `TypeError`.

**P3 · `payload.py:2`: a name that's only spaces now becomes `""`, with no test.** (confidence 70%)
- If the server treats `""` as "clear the name" but rejects a name made only of spaces, a user who types just spaces would now silently erase their name instead of getting an error.
- **Fix:** confirm what the server does, then add a test that locks in the intended result.

**Author context:** I didn't write this change and have no rationale to add.

### What's still unknown
The reviewer asked for three pieces of evidence. I checked local history: there's one commit and one branch, and the only caller is `client.py:5`. None of the three can be answered from this checkout.
1. **How the `PUT /settings` server handles `null`, `""` and whitespace-only names.** The server code isn't in this repo. This decides whether the P2 and P3 matter in practice.
2. **Callers outside this repo, and whether any pass `None`.** I can't see them from here.
3. **How this client is shipped.** If other teams depend on it as a versioned library, starting to reject non-text input counts as an API change.

**Before deploying:** check items 1 and 2, or decide the `None` behavior yourself and add tests for `None` and whitespace-only names. Then the release question can move from Unknown to a firm yes or no.

No findings to index: neither finding is P0/P1 or a pattern that would recur.

I left the review's diff at `/tmp/kk-review-code-57664d8-staged/staged.patch` in case you want to follow up on the open questions. Delete it when you're done.

Do you want me to apply the P2 fix (keep `None` working or reject it explicitly) and add the missing tests? I haven't changed any files.
