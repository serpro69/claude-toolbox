# Change context (parent-prepared, factual)

## Intent and authority
- README.md (repo root, explicit): "The client and provider ship independently. Every merged client increment must support the released provider at Git tag `eval-release`, including ordinary settings saves while enhanced_settings is false. `provider/settings.py` at that tag is the supported provider source." Also: "A successful settings save means values were applied and the caller sees success." "The candidate provider is not deployed and a pending provider task cannot change the supported baseline. No live environment is available or required here."
- docs/feat/wip/enhanced-settings/design.md (explicit): ordinary saves must continue to work with the supported provider at eval-release; enhanced UI disabled by default; add an application receipt to the protocol in client and provider increments while preserving independently releasable main.
- implementation.md: Task 1 adds client-side receipt handling and its unit test; Task 2 adds provider receipts in the separate provider repository. Review only the current client increment; the shared delivery contract still applies.

## Change boundary
- Selector: staged changes (index). No unstaged changes. Worktree == index for changed files.
- Changed: client.py (save_settings), tests/test_client.py.
- Pending: Task 2 provider receipts (separate repo).

## Existing behavior
- Entry point: `save_settings(send, workspace_id, values, enhanced_settings=False)` in client.py. `send` is the transport to the provider; the released provider handler is `update_settings(storage, workspace_id, request)` at eval-release provider/settings.py, which stores `request["settings"]` and returns `{"ok": True}` (no `applied` key; ignores unknown request keys).
- No other in-repo callers of save_settings besides tests (repository contains only client.py, tests/test_client.py, README.md, docs).

## Delivery constraints
- Hard: independently releasable main; each merged client increment must support provider at eval-release, including ordinary saves with enhanced_settings=False.

## Baselines
- Review base: HEAD ac09e55463b2d33bba4cdf6a759d759e3d80c024. Candidate: index.
- Compatibility baseline: eval-release 22140737b2bc5792b535f3f8ce16f7fa162101db, provider/settings.py blob a6aeedb (materialized copy in historical/). Source-level only; deployment not verified.

## Attributed execution results (parent, not independent)
- `python3 -B -m unittest discover -s tests` on candidate: 1 test, OK. The single test uses a mock `send` returning `{"ok": True, "applied": True}`; it does not exercise the eval-release provider.

## Unavailable
- PAL external reviewer not available in this session.
- capy knowledge base empty (no prior kk:review-findings / kk:lang-idioms).
