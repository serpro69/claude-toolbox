## Code Review Summary

**Overall assessment:** COMMENT. The code is ready to approve. Whether it's ready to deploy is **Unknown**, because that depends on which protocol version the live provider runs, and nothing in the repo records that.

**Files reviewed:** 2 files, 10 insertions and 1 deletion (staged only; there were no unstaged changes).
- **Intent and scope:** I reviewed the change against `README.md` and `protocol.md`. `clear_name(transport)` should remove the explicit label so the account default is used. It must not behave like sending an empty label. It can be called as soon as the client is deployed, with no flag. `save` must stay unchanged. There are no task docs, so there's no task scope beyond this.
- **Baselines:** the review base is `022431b` and the candidate is the staged index. I didn't look at any released client or deployed provider, as you asked.
- **Profiles:** `python` matched both files, and all four of its checklists were loaded and applied. No other profiles matched.

## Behavior and compatibility

| Scenario | Expected (contract) | Candidate | Evidence |
| --- | --- | --- | --- |
| `save("Ada")` / `save("")` | Unchanged; response and exceptions passed through | Unchanged | Diff doesn't touch `save` (`client.py:1-2`); existing tests pass |
| `clear_name` against a **v2** provider | Sends `{"display_name": null}`; label removed; returns `{"ok": true}` | Sends `None` and returns the transport's response | `client.py:5-6`, `test_clear_name` |
| `clear_name` vs an empty label | Must not send `""` | Sends `None`, not `""` | Test asserts the `None` payload |
| `clear_name` against a **v1** provider | HTTP 422; stored value unchanged; transport raises | Exception passes through to the caller; nothing is corrupted | `protocol.md:9,14-15` (source only, not run) |
| Mixed v1/v2 provider instances, or provider rollback to v1 | — | Some or all `clear_name` calls fail with 422 errors; `save` is unaffected | Inferred from the protocol table |

**Compatibility conclusions**
- **New client with a v2 provider: Supported.** Checked against the protocol table. The local tests use a recording fake, not a provider.
- **New client with a v1 provider: Blocked for `clear_name`.** It fails safely and visibly, but the feature doesn't work. `save` is unaffected.
- **Deploy readiness: Unknown.** The README says the operation is callable right after the client deploys. So every provider instance it can reach must already run v2 and stay on v2, with no rollback to v1. `protocol.md:16-17` says the docs don't record which version a deployment runs, and I didn't check the environment.
- **Next step:** before deploying, confirm the provider is fully on v2 and that a rollback to v1 isn't planned.

**Evidence**
- I ran `python3 -B -m unittest discover -s tests -v` on Python 3.15.0, and all 3 tests passed. The worktree matched the index.
- The tests only check request shape and that the fake's response is passed through. They don't exercise a real provider or JSON encoding: I assumed the real transport turns `None` into JSON `null`, but I didn't verify it.
- I didn't verify the README's Python 3.9+ claim on 3.9, though the change uses no newer syntax.

## Findings

- **P0:** none.
- **P1:** none.
- **P2:** none.
- **P3:** none.

The python checklists turned up nothing: no injection, deserialization, shared state, error swallowing or SOLID issues in a one-line pass-through. The new function also follows the existing pattern: it borrows the transport, doesn't retry, and doesn't catch exceptions.

**Indexing:** there were no P0/P1 systemic findings to index. The `kk:review-findings` and `kk:lang-idioms` knowledge bases were empty.

**Summary**
- No code changes are recommended.
- Before deploying, confirm the provider fully serves protocol v2 and won't roll back to v1. If it's still on v1, every `clear_name` call will fail with an error, though stored labels won't be corrupted.
- I didn't deploy anything or check environment health.
