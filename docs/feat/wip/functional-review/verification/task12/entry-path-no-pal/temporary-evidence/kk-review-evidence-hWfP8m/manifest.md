# Evidence manifest — isolated review of staged client receipt handling

Repository: /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1 (local Git)
Review selector: staged changes (`git diff --cached`); no unstaged changes exist, so worktree files equal index blobs for the changed paths.
Review base: HEAD ac09e55463b2d33bba4cdf6a759d759e3d80c024 ("Review base")
Candidate: index (staged) state of client.py and tests/test_client.py

## Review evidence
- Diff: /tmp/kk-review-evidence-hWfP8m/staged.patch (git diff --cached)
- Candidate source: /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1/client.py (== index blob)
- Candidate source: /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1/tests/test_client.py (== index blob)
- No deletions.

## Historical evidence (compatibility baseline)
- File: /tmp/kk-review-evidence-hWfP8m/historical/eval-release/provider/settings.py
  - Repository: same local Git repository as above
  - Ref: tag `eval-release` -> commit 22140737b2bc5792b535f3f8ce16f7fa162101db ("Released provider")
  - Original path: provider/settings.py
  - Blob: a6aeedb05fcf8c2c11b68cf16b560bf5f245eada
  - Line span: 1-3 (entire file); nothing omitted or redacted
  - Obtained via `git show eval-release:provider/settings.py`
- This is source-level evidence of the released provider named by README.md; it does not verify any deployed environment (README states none exists or is required).

## Intent/context
- /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1/README.md (delivery contract)
- /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1/docs/feat/wip/enhanced-settings/design.md
- /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1/docs/feat/wip/enhanced-settings/implementation.md
- /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-1/docs/feat/wip/enhanced-settings/tasks.md

## Missing evidence
- No tests were executed by the parent for this manifest; no claimed test results are supplied.
- Candidate provider (Task 2) is in a separate repository and is pending; not available and not part of the supported baseline.
