The review is finished. This is the report, then my deploy assessment.

## Review Summary (Isolated Mode, partial)

**Reviewers:** code-reviewer (Claude sub-agent) only. The external `pal` reviewer couldn't run because the `pal` MCP server failed to connect, so there are no corroborated or external findings.
**Files reviewed:** `payload.py` (modified) and `tests/test_payload.py` (new), about 13 lines. Bash was denied, so I couldn't capture `git diff --cached` and the reviewer never saw the HEAD version of `payload.py`. From the staged content, the change looks like it only adds `.strip()` to `display_name`.
**Profile:** python, using all four checklists (triggered by the `.py` extension).

### Code Reviewer Findings

- **`payload.py:2`: Whitespace-only names now become `""` and are still sent.** P2, 80% confidence.
  - `"   "`, `"\t\n"` and `"\u3000"` all become `{"display_name": ""}`, and `save()` sends that to `/settings`.
  - If the server reads `""` as "clear the name", typing spaces now silently erases it.
  - **Fix:** decide whether blank input is rejected or means "clear", and add a test that pins it.
- **`payload.py:2`: `None` or other non-`str` input now raises `AttributeError`.** P2, 65% confidence.
  - If the old code passed values through unchanged, `save(t, None)` used to send JSON `null` and now crashes.
  - `bytes` still gets through, so the function has no consistent type contract.
  - **Fix:** either check for `str` and raise `TypeError`, or handle `None` explicitly. Add type hints.
- **`tests/test_payload.py:7-11`: Tests cover only the easy case.** P2, 90% confidence.
  - Nothing tests whitespace-only input, `None`, tabs or newlines, Unicode whitespace, or trimming through `save()`.
  - Nothing proves the request body is actually trimmed.
- **`payload.py:2`: `str.strip()` handles Unicode inconsistently.** P3, 70% confidence.
  - It removes NBSP and U+3000 but not zero-width space or BOM. A `"\u200b"` name survives and looks blank, and the client and server may disagree on what counts as blank.

**Author context:** none to add. I didn't write this change and have no notes from implementing it.

**Indexing:** nothing to index, since there are no P0/P1 findings.

## Is it ready to deploy?

**No.** There are no blocking bugs: for ordinary string input the change is correct, and existing callers and tests stay consistent. But:

1. **The change creates two input contracts that nobody has decided.** One is what blank names mean. The other is whether `None` is still accepted. Either could be a user-visible regression depending on how the server behaves.
2. **The checks before deploying didn't happen.** I couldn't confirm the staged diff, couldn't run `python3 -B -m unittest discover -s tests`, and only one of the two reviewers ran.

To get it deployable:
- Decide the blank-name and `None` behavior.
- Add the missing tests.
- Run the suite.
- Optionally, re-run this review once `pal` is connected, so the findings get a second opinion.

## Next Steps

There are 4 findings, all from the code reviewer. I recommend fixing all of them:

1. P2: Define and enforce the blank-name behavior.
2. P2: Define the `None`/non-`str` behavior and add type hints.
3. P2: Add tests for the cases above, including `save(t, "  Ada  ")`.
4. P3: Pin the Unicode whitespace behavior with a test, and decide whether zero-width characters should also be stripped.

**How would you like to proceed?**
1. **Fix all:** I'll implement all four fixes. Tell me first whether blank names should be rejected or mean "clear", and whether `None` should be rejected or mean "unset".
2. **Fix high severity:** I'll fix the three P2 items.
3. **Fix specific items:** tell me which ones.
4. **No changes:** the review is complete.
