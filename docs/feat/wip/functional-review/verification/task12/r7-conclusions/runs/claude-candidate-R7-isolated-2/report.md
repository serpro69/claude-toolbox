**The change is not deploy-ready yet. Nothing in the code needs to change, but whether it's safe to ship depends on the `/settings` server, and that code isn't in this repo.** The change itself is correct for normal names: one P3 note, no blockers. The review verdict is **COMMENT** rather than APPROVE because the deploy question can't be answered from this repo alone.

## Review Summary (Isolated Mode)

- **Reviewers:** one of the two ran. The independent code-reviewer agent (Opus 5.5) completed. The external PAL reviewer is not available in this session, so it never ran and none of the findings are confirmed by a second reviewer.
- **What was reviewed:** the staged changes against `HEAD` 57664d8. That covers `payload.py`, where `build_payload` now calls `display_name.strip()`, and the new `tests/test_payload.py`. The reviewer also read the unchanged caller `client.py`, its tests, the README and the previous version of `payload.py`. I took the files to review from the staged copy, not the working folder.
- **Purpose of the change:** there's no spec or commit message. From the diff and tests, the intent appears to be: trim spaces at the start and end of the display name before sending it to the server, and keep spaces inside the name.
- **Review setup:** only the `python` checklists applied (security, SOLID, code quality, removal), and all four were used.
- **Tests:** I ran `python3 -B -m unittest discover -s tests` and all 4 tests pass. The staged files and the working folder are identical, so this result applies to the staged change.

## How behavior changes

| Input | Before | After | Tested? |
|---|---|---|---|
| `"  Ada  "` | sent unchanged | `"Ada"` | yes |
| `"Ada Lovelace"` | unchanged | unchanged | yes |
| `"Ada"`, `""` via `save` | unchanged | unchanged | yes (existing tests) |
| `"   "` (only spaces) | `"   "` | `""` | no |
| Tabs, newlines, non-breaking spaces at the ends | sent unchanged | trimmed | no |
| `None` or a number | sent to the server | crashes in the client before any request is sent | no |

What this means for shipping:
- **Sending normal text names: fine.** For any text name, the new client sends a value the old client could already send. Rolling back is also safe, because the client stores nothing.
- **What the server does with `""` from a spaces-only name: unknown.** It might clear the name, reject the request, or store the empty value.
- **Callers outside this repo that pass `None`: unknown.**
- **Ready to deploy: unknown.** I found no server code, deploy config, tags, remotes or other history: the repo has a single commit.

## Code Reviewer Findings

- **P3 — `payload.py:2`: `build_payload` now quietly accepts only text.** If a caller passes `None` (for example, to clear the name) or a number, it now crashes with `AttributeError` before anything is sent. Before, the value went straight to the server. Nothing documents the function as text-only, and no caller in this repo passes `None`, so it's not shown that this case actually happens.
  - Confidence: 60%. The behavior change is certain; whether it matters depends on how the server and outside callers use `None`.
  - Possible fix: either keep `None` working (`display_name if display_name is None else display_name.strip()`), or declare `display_name: str` and add a test for that rule.

## What still needs checking before deploy

1. **The `/settings` server's rules for `display_name`, at the version that's actually deployed.** What do `""` and `null` mean, and does the server already trim spaces? Spaces-only input now arrives as `""`, so this answer decides whether the new behavior is safe.
2. **Outside callers of `save` and `build_payload`.** Does any of them pass `None` or another non-text value? If so, the P3 above should be treated as more serious.
3. **Which version and environment you're deploying to.**

If the server treats `""` sensibly and nothing passes `None`, the change is fine to ship as it is.

## Cleanup

Shell permissions blocked the cleanup command, so these temporary folders are still there. You can delete them:
- `/tmp/kk-review-code-bSstlp`
- `/tmp/kk-review-instructions-1me69sog`
- `/tmp/kk-review-instructions-uu2bvfqv`
- `/tmp/kk-review-instructions-zohcdzyc`
