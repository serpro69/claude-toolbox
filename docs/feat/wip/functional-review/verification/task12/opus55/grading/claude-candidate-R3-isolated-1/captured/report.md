## Isolated review summary

**Verdict: REQUEST_CHANGES.** The code is not safe to merge as it stands. Ordinary saves with `enhanced_settings=False` probably fail against the released provider, which breaks the README's requirement that each client release works with the provider at `eval-release`.

**Coverage limits:**
- **One reviewer, not two.** The PAL MCP server failed to connect, so the external review never ran. Every finding comes from the `kk:code-reviewer` sub-agent alone, and nothing is corroborated.
- **No shell.** Bash was denied, so there's no staged diff, no copy of the old client at HEAD (`ac09e55`), and no provider source from the release tag. Both reviewers read the two candidate files in full. I assumed they match what's staged, because the starting git status showed no unstaged changes.
- **No tests were run.**

**What was reviewed:** Task 1 (client receipt handling) from `docs/feat/wip/enhanced-settings`. Task 2 (provider receipts) is pending and out of scope. The `python` profile applied and all four of its checklists were loaded.

**Baselines:** The review base is HEAD `ac09e55`, compared against the staged files. Compatibility is judged against tag `eval-release`, which is commit `22140737` ("Released provider"). The provider file at that tag couldn't be read.

### Behavior and compatibility

| Case | Expected | What the candidate does | Conclusion |
|---|---|---|---|
| Released provider, flag off, ordinary save | Caller sees success | Raises `RuntimeError` unless the response has `applied: True` (`client.py:5-6`) | **Blocked** by the documented contract; not confirmed from provider source |
| Released provider rejects the new `require_receipt` request key | Success | Save fails at `client.py:3` | **Unknown** |
| Future provider that sends receipts, `applied: True` | Success | Success; this is the only tested case | **Supported** for this one case |
| Provider returns `ok: False` or `applied: False` | Error | Raises | Correct from reading the code; untested |
| Does the flag protect anything? | Default-off flag keeps old behavior | `enhanced_settings` is only echoed in the return value | **Blocked**: the flag gates nothing |
| Persistence, migration | — | Stateless function | Not applicable |

### Findings (code-reviewer only)

**P1: `client.py:2-6`: ordinary saves now require a receipt the released provider likely doesn't send**
- **Where it fails:** every call sends `require_receipt: True` and raises unless `response.get("applied") is True`, regardless of `enhanced_settings`.
- **Why the provider likely lacks it:** the design says the receipt is being *added* in client and provider increments, the provider half is pending, and the README says a pending provider task can't change the supported baseline.
- **Consequence:** with the released provider, saves the provider reports as `ok` (likely already applied) come back to the caller as failures, and retries fail the same way. The one test fakes `{"ok": True, "applied": True}`, so it repeats the implementation's assumption.
- **Confidence: 75%.** The client side is certain from the code. The provider side is inferred from the docs, not read from source.
- **Suggested fix:**
  - Reject only an explicit `applied: False`.
  - Treat a missing `applied` alongside `ok: True` as the old-style success, provided the released provider's `ok` already means "applied".
  - Send `require_receipt` only behind a flag or a capability check, unless the released provider is shown to ignore unknown keys.
  - Add a test using the released response shape with the flag off.
- **If released `ok` does not mean "applied":** the two README requirements conflict, and that's a decision for you rather than something the client code can settle.

**P2: `tests/test_client.py:6-10`: the new behavior has no tests**
- There's only a happy-path test. Nothing covers a missing or false `applied`, `ok: False`, the request payload, or `enhanced_settings=True`.
- Confidence: 90%.

**Out of scope, not flagged:** `is True` would reject non-boolean truthy receipts (e.g. `1`), but that only matters if Task 2 picks a different shape. `response.get` would crash on a `None` response; the baseline behavior there is unknown.

### Outstanding evidence

1. **The released provider's response** (`provider/settings.py` at `22140737`). This would confirm or withdraw the P1: which keys a successful save returns, whether `ok` means applied, and whether unknown request keys are accepted. Running `git show eval-release:provider/settings.py` would settle it, but I couldn't run git in this session.
2. **The pre-change client and tests at `ac09e55`, plus `git diff --cached`.** This only decides whether this change introduced the problem; release stays blocked either way.
3. **Release readiness is Blocked** until the client handles a response without a receipt, or you explicitly change the supported baseline. Merging Task 2 doesn't fix it.

**Indexing:** the P1 pattern (a new response field made mandatory before the provider ships it, behind a flag that gates nothing) is now in the knowledge base as `kk:review-findings`.

**Clean-up:** none needed; no temporary files were created.

### Next steps (each needs your OK)
- Run the two `git show` commands yourself or allow Bash, and I'll settle evidence items 1–2 with the reviewer.
- Apply the P1 fix and the P2 tests.
- Record the open evidence items under an **Execution context** entry for Task 1 in `docs/feat/wip/enhanced-settings/tasks.md`, as the reviewer suggested.
