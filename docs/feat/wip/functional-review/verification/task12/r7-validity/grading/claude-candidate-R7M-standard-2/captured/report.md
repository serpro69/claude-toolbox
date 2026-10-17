## Code Review Summary

**Files reviewed**: 2 files (`client.py`, `tests/test_client.py`), 10 lines added and 1 removed, staged
**Overall assessment**: **COMMENT**. I found no defects in the code. Whether it's ready to deploy is **Unknown**: it depends on which provider protocol version the target environment runs, and nothing in the repo shows that.
**Intent and scope**: The requirements come from `README.md` and `protocol.md`. This increment adds `clear_name(transport)`, which removes the explicit label so the account default is used. An empty label doesn't count as clearing. The operation has no activation flag, and `save` must not change. There are no `docs/feat/wip` task documents, so no task scope applies.
**Baselines**: The review base is `022431b` ("Review base", the only commit, no tags). The candidate is the staged index; the worktree matches it exactly. There is no release or deployed baseline in the repo.

## Behavior and Compatibility

| Contract | Scenario | Expected | Candidate | Evidence |
| --- | --- | --- | --- | --- |
| README: `save` unchanged | `save(t, "Ada")`, `save(t, "")` | Same request, response returned as-is | Not touched by the diff; tests pass | Source and tests run |
| README: clear ≠ empty label | `clear_name(t)` | `PUT /settings {"display_name": null}` | Sends `None` and returns the transport response | Source and `test_clear_name` |
| protocol v2: `null` | clear against a v2 provider | Label removed, default used | Correct request | Source only; no provider in repo |
| protocol v1: `null` | clear against a v1 provider | HTTP 422, stored value unchanged | Transport raises and the error reaches the caller; no data changes | Source and protocol doc; not run |
| Exceptions are passed through | transport raises | Error reaches the caller | No try/except in `clear_name` | Source |

**Compatibility:**
- **Existing `save` flow**: Supported. It isn't touched and its tests pass.
- **New client with a v2 provider**: Supported, based on the source and the request-recording test.
- **New client with a v1 provider**: Blocked for that combination. The README says `clear_name` "can be called immediately after the client is deployed" with no flag, so every call will fail with 422. It fails safely: the error is visible and the stored value doesn't change. No client-side fix is possible, because sending `""` is ruled out and the protocol has no way to detect the version.
- **Target deployment's provider version**: **Unknown**. `protocol.md` says its version table is "not a record of which version a deployment runs." Before deploying, someone needs to confirm that every environment the client will reach runs provider v2.
- **Rollback**: Supported. Removing `clear_name` affects only callers of the new function.

**Evidence limits:**
- I ran `python3 -B -m unittest discover -s tests -v` and all 3 tests passed. That was on Python 3.15 only; 3.9 wasn't run, although the change uses no newer syntax.
- `MemoryTransport` only records requests. It doesn't model the provider, so no test covers the v1 422 path or confirms that the real transport encodes `None` as JSON `null`. The production transport isn't in the repo.
- The knowledge base was empty, so there were no past findings or language idioms to compare against.
- As you asked, I didn't deploy anything or check environment health.

---

## Findings

### P0 - Critical
(none)

### P1 - High
(none)

### P2 - Medium
(none)

### P3 - Low
(none)

I applied the Python security, SOLID, code-quality and removal checklists along with the general review steps. None of them flagged anything for a two-line function that passes the transport response straight through.

---

## Release prerequisites (not code defects)

1. **Confirm provider v2 is deployed** in every environment this client will call, before deploying the client. Until then, release readiness stays Unknown, and any environment on v1 is blocked.
2. **Record the dependency in `README.md`.** It currently says the operation can be called immediately after deploy without mentioning that this requires provider v2.

**Indexing**: No findings to index (no P0/P1).

I recommend no code changes. The remaining work is the provider-version check and the README note above.
