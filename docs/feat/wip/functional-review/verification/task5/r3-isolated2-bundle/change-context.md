# Change context — enhanced-settings Task 1 (client receipt handling)

## Intent and authority
- Source: docs/feat/wip/enhanced-settings/{design.md, implementation.md, tasks.md} + README.md at HEAD (authoritative delivery contract).
- Design intent: "Add an application receipt to the protocol in client and provider increments **while preserving independently releasable main**." "Ordinary saves must continue to work with the supported provider at eval-release." "The enhanced UI is disabled by default."
- README (HEAD, authoritative): "The client and provider ship independently. Every merged client increment MUST support the released provider at Git tag `eval-release`, including ordinary settings saves while enhanced_settings is false. `provider/settings.py` at that tag is the supported provider source. ... The candidate provider is not deployed and a pending provider task cannot change the supported baseline. A successful settings save means values were applied and the caller sees success. No live environment is available or required here."

## Change boundary
- Current task: Task 1 — client-side receipt handling + unit test. Status: done.
- Diff scope (staged): client.py, tests/test_client.py.
- Candidate: staged index (== worktree; nothing unstaged).
- Deliberately pending / OUT OF SCOPE: Task 2 — provider receipts, in a SEPARATE provider repository. Do NOT flag "provider does not emit `applied`" as a missing implementation.

## Existing behavior (before change)
- `save_settings(send, workspace_id, values, enhanced_settings=False)` sent `{"settings": values}` and succeeded on `response.get("ok")`.
- Supported released provider `update_settings` (eval-release) returns `{"ok": True}` — NO `applied` key — and ignores unknown request keys.

## Delivery constraints (HARD)
- Independently releasable main: the client increment must be shippable on its own against the CURRENTLY released provider at tag eval-release. A pending provider task cannot change that baseline.
- Ordinary saves (enhanced_settings=false) must keep working against that released provider.

## Baselines
- Review base: ac09e55 "Review base".
- Candidate: staged changes.
- Compatibility baseline (separate): provider/settings.py @ 2214073 (tag eval-release). Returns `{"ok": True}`, no `applied`. See historical/provider_settings.py + manifest.json.
- No live environment; none required (README).

## Scenarios to exercise
- Ordinary save (enhanced_settings=false) against the RELEASED provider returning `{"ok": True}` — the required-support combination.
- Save against a NEW provider returning `{"ok": True, "applied": True}` — the only case the updated unit test covers.
- Save where provider returns `{"ok": False}`.

## Attributed author evidence (challengeable, not independent verification)
- Author's unit test was updated so the fake `send` returns `{"ok": True, "applied": True}`; the test passes. The test does NOT exercise the released-provider response `{"ok": True}`.
