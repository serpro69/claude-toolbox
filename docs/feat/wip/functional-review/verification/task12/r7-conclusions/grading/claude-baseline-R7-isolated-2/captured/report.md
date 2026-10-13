## Review Summary (Isolated Mode)

**Reviewers**: code-reviewer (Claude sub-agent). The `pal codereview` reviewer didn't run because the `pal` server isn't connected in this session, so nothing was corroborated by a second model.
**Files reviewed**: 2 files, 12 lines changed (`payload.py`, `tests/test_payload.py`)
**Profile**: python (security, SOLID, code-quality and removal-plan checklists)

The staged files are the settings client: `client.save()` sends `build_payload(display_name)` as a PUT to `/settings`. The change makes `build_payload` call `.strip()` on the name, and adds two unit tests.

**Tests:** I ran `python3 -B -m unittest discover -s tests` and all 4 tests pass, including the existing `test_save` and `test_empty_name`. There are no unstaged changes, so this tested exactly what is staged.

### Code Reviewer Findings

- **`payload.py:2`: `None` or other non-string names now crash instead of passing through.** P2, confidence 60%
  - Before, `save(t, None)` sent `{"display_name": None}`, which in a PUT body usually means "clear the field". Now it raises `AttributeError`. Nothing limits the input to `str`: no type hint, no docstring.
  - Nothing in this repo passes `None`, so it's only a regression if callers outside the repo do.
  - Fix: keep the old pass-through (`display_name.strip() if isinstance(display_name, str) else display_name`), or reject non-strings on purpose with a type hint and a clear `TypeError`. Add a `None` test either way.

- **`payload.py:2`: a name of only spaces now becomes `""`, and nothing tests or documents that.** P3, confidence 55%
  - `.strip()` also removes tabs, newlines and non-breaking spaces. That's probably fine, but it removes more than the test name "surrounding spaces" suggests.
  - Fix: add a test for whitespace-only input. If the server rejects empty names, also check the value after stripping.

- **`tests/test_client.py`: no client-level test shows the trimming reaches what gets sent.** P3, confidence 50%
  - Fix: add a test where `save(transport, "  Ada  ")` sends `{"display_name": "Ada"}`.

The security and SOLID checklists found nothing; this is a one-line function with no attack surface. Nothing is removed by the change, so the removal plan doesn't apply.

**Indexing:** there are no P0 or P1 findings, so nothing was added to the review-findings index.

---

## Is it ready to deploy?

**Probably yes, with one open question.** The change is correct for string input, it's tested, and the full suite passes. Whether it's safe depends on one thing I can't see from this repo: **does any caller of `client.save()` pass `None` (or another non-string) to clear the display name?**
- If names are always strings, it's fine to ship. The P3s are optional extra tests.
- If `None` is possible or you're not sure, I'd make the `isinstance` guard and a `None` test (about 3 lines) a condition of shipping. Otherwise those callers will hit an `AttributeError` at runtime.

Limits of this review: it had only one reviewer, I didn't check CI or deploy config, and nothing in the repo describes the server's rules for `""` or `null` names.

**How would you like to proceed?**
1. **Fix all**: add the `None` guard and tests for `None`, whitespace-only input and the client path.
2. **Fix the P2 only**: add the `None` guard and its test.
3. **Fix specific items**: tell me which ones.
4. **No changes**: names are always strings, so ship as is.
