## Review Summary (Isolated Mode)

**Is it ready to deploy?** Not yet. For normal string input the trimming change is correct. Two things are unconfirmed, and each could break a real flow:

1. **`None` now crashes the save.** The old `build_payload` sent `None` through as `{"display_name": None}`. Now `client.save(transport, None)` raises `AttributeError` before any request is made.
2. **Whitespace-only names now become `""`.** Nobody has confirmed that the server's PUT /settings handler accepts `""`.

**Reviewers**: one independent reviewer (`kk:code-reviewer`) ran and completed. The second, external reviewer (PAL) could not run because its server failed to connect. **So none of the findings below are corroborated by a second reviewer.**

**Files reviewed**: the reviewer read the staged diff, `payload.py`, `tests/test_payload.py`, and the unchanged `client.py`, `tests/test_client.py` and `README.md`. I read the same files.

**Overall assessment**: **COMMENT** on the code. **Deploy readiness: Unknown.**

**Intent and scope**: there is no spec or task document, so the intent is inferred: trim spaces around `display_name` before PUT /settings. I reviewed the staged changes only. There are no unstaged changes, so the working copy matches what is staged.

**Baselines**: review base is HEAD `57664d8`, compared against the staged state. No deployed revision of the client or the server was available.

### Behavior and Compatibility

The only caller of `build_payload` in the repo is `client.py:5`, inside `save`. The client keeps no state, so the change only affects the request body.

| Input | Before | After | Evidence |
|---|---|---|---|
| `"  Ada  "` | sent unchanged | `"Ada"` | new test, passes |
| `"Ada Lovelace"`, `"Ada"`, `""` | sent unchanged | same as before | tests, pass |
| `"   "` (whitespace only) | `"   "` | `""` | reasoning from the code, no test |
| tabs, newlines or non-breaking spaces around the name | kept | stripped | reasoning from the code, no test |
| `None` or any non-string | sent as-is | `AttributeError`, no request sent | reasoning from the code, no test |
| retry | same body | same body (stripping twice gives the same result) | reasoning from the code |

- **Non-empty strings, old and new clients side by side, rollback:** Supported compared with `57664d8`.
- **Callers passing `None` or non-strings:** Unknown. Callers outside this repo aren't available.
- **Server receiving `""` from whitespace-only names:** Unknown. The server source isn't in this repo, and local Git history has only the single commit `57664d8`.
- **Security:** Not applicable. This is a pure transform with no input/output.

**Tests:** I ran `python3 -B -m unittest discover -s tests` myself and all 4 tests passed. The reviewer did not run anything and relied on reading the code.

### Code Reviewer Findings

- **[payload.py:2] P2: `build_payload`/`save` now crash on `None` and other non-string input.** Profile: python · Checklist: code-quality-checklist.md · Triggered by: `.py` extension
  - **How it happens:** `save(transport, None)` calls `None.strip()`. The old code sent `{"display_name": None}`. The new code raises `AttributeError` and the update never goes out.
  - **Confidence:** 80%. The behavior change is certain. Whether any caller actually passes `None` is unknown; if one does, this becomes P1 and should block the change.
  - **Suggested fix:** decide what `None` should mean.
    - To keep the old behavior: `display_name.strip() if isinstance(display_name, str) else display_name`.
    - To reject it: raise a clear `TypeError`.
    - Either way, add a test for `None`.

- **[tests/test_payload.py:7-11] P3: whitespace-only names now turn into `""`, and no test covers it.** Profile: python · Checklist: code-quality-checklist.md
  - **Why it matters:** this is probably the intended behavior. But if the server rejects `""` or reads it as "clear the name", users who submit only spaces get a different result than before.
  - **Confidence:** 70%. It depends on how the server behaves.
  - **Suggested fix:** add a test for `"   "` (and perhaps `"\tAda\n"`), and confirm the server accepts `""`.

### Outstanding Evidence and Prerequisites

The reviewer requested two pieces of evidence. Neither exists in this repository or its Git history:

1. **The server's PUT /settings handler:** how it handles `""`, `null` and spaces around the name. This decides the P3 and whether `None` was ever a supported way to clear the name.
2. **Code outside this repo that calls `client.save` or `build_payload`:** whether any of it passes `None`. This decides whether the P2 becomes a blocking P1.

Neither prerequisite has an owner or a place where it is tracked yet.

No findings to index (nothing rated P0 or P1 in the knowledge base). The staged diff I wrote for the review is kept at `/tmp/kk-review-code-settings-payload/` until the two open requests are settled.

### Next steps

Do you want me to make the `None` handling explicit and add tests for `None` and whitespace-only names? It's a two-line code change plus about three tests. Separately, someone with access to the server needs to confirm how PUT /settings treats an empty `display_name`.
