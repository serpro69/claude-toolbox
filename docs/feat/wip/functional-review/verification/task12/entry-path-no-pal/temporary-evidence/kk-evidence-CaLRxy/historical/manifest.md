# Historical evidence provenance

Repository: /tmp/fr-entry-path-no-pal-20261011/claude-candidate-R3-isolated-2 (local Git)

| Item | Value |
| --- | --- |
| Role | Named supported provider baseline (README: "provider/settings.py at that tag is the supported provider source") |
| Ref | `eval-release` (lightweight tag) |
| Full revision | 22140737b2bc5792b535f3f8ce16f7fa162101db |
| Original path | provider/settings.py |
| Blob | a6aeedb05fcf8c2c11b68cf16b560bf5f245eada |
| Line span | 1-3 (entire file) |
| Omitted/redacted | none |
| Materialized copy | /tmp/kk-evidence-CaLRxy/historical/eval-release/provider/settings.py (copied verbatim from `git show eval-release:provider/settings.py`) |

Source-level tag comparison only; deployed state is not verified (README: no live environment available or required).

# Candidate identity

- Selector: staged changes (index); no unstaged changes exist.
- Review base: HEAD ac09e55463b2d33bba4cdf6a759d759e3d80c024 ("Review base"), parent of nothing else besides eval-release 2214073.
- Staged blobs: client.py 910e877 (base d6ddf4b), tests/test_client.py f1dfc4f (base 39ea461).
- Worktree files for client.py and tests/test_client.py are identical to the index (`git diff --stat` empty), so the in-repo paths are the candidate source.
- provider/settings.py exists at eval-release but not at HEAD (moved out of this checkout after release, per README).
