## Code review summary

**Files reviewed:** 2 files, 12 lines added and 1 removed (`payload.py`, `tests/test_payload.py`)
**Overall assessment:** **COMMENT.** The code is correct for string input and I found no defects. Whether it's safe to deploy depends on two facts about callers and the server that this repo can't answer.
**Intent and scope:** The repo has no spec or task docs, so the intent is my reading of the diff: trim leading and trailing whitespace from `display_name` before `PUT /settings`. I reviewed the staged diff only; there were no unstaged changes. The README contract is just "Python 3.9+, standard library only."
**Baselines:** I compared commit `57664d8` ("Review base") with the staged files. I don't know which revision is currently deployed, so this isn't a comparison against production.

## Behavior and compatibility

| Scenario | Before | After | Evidence |
|---|---|---|---|
| `save(t, "Ada")` | `{"display_name": "Ada"}` | same | `test_client.test_save` passes |
| `save(t, "")` | `""` | `""` | `test_client.test_empty_name` passes |
| `"  Ada  "` | `"  Ada  "` | `"Ada"` | new test passes |
| `"Ada Lovelace"` | unchanged | unchanged, inner space kept | new test passes |
| `"   "` (only spaces) | `"   "` | `""` | read from source, no test |
| `"Ada\u00a0"`, tabs, newlines | kept | stripped (`str.strip()` removes all Unicode whitespace) | read from source, no test |
| `None` or a non-string | passed through as-is | **raises `AttributeError`** before the request is sent | read from source, no test |

- **Payload shape (client vs. server):** Supported. It's still the same key with a string value, and the client is the only file that builds it.
- **Callers inside this repo:** Supported. `client.save` is the only caller of `build_payload` and always forwards its argument.
- **Callers outside this repo passing `None`:** Unknown. If anything calls `save(transport, None)`, for example to clear the name, it used to send `null` and now crashes. Nothing in the repo shows this happens, so it isn't a defect. Before deploying, check whether `save` callers can pass `None`.
- **Server handling of a whitespace-only name:** Unknown. A name of only spaces now arrives as `""`. `test_empty_name` shows `""` is a value the client already sends, but I can't tell what the server does with it (reject it, store it, or treat it as "clear the name"). Confirm that turning whitespace-only into empty is what you want.
- **Rollback:** Supported. It's a client-only change with no stored state.

**Tests:** `python3 -B -m unittest discover -s tests -v` ran 4 tests and all passed. The working tree matches the staged files, so those results apply to what's staged.

**Coverage limits:**
- My command to run boundary inputs (`None`, `"   "`, NBSP) was denied by the permission mode. Those three rows come from reading the source and how `str.strip()` works, not from running them.
- I had no access to the server or to any deployment.
- The capy knowledge base is empty, so there were no past findings or language idioms to check against.

## Findings

**P0, P1, P2, P3:** none.

**Instructions applied:**
- The standard review method.
- The Python profile, which matched on the `.py` extension. I applied its security, SOLID, code-quality and removal checklists. Nothing applied: there's no injection, secret handling, concurrency or I/O risk, and nothing to remove.

No findings to index.

## Ready to deploy?

**The code is ready. Whether to deploy depends on two things only you can confirm:**
1. Nothing outside this repo calls `save(..., None)`.
2. Sending `""` for a whitespace-only name is acceptable to the server and is what you intend.

If both hold, it's safe to deploy and no changes are needed. If either doesn't, say which and I'll suggest the matching guard (for example, passing `None` through unchanged) plus a test that pins the behavior.
