# Template Sync

If you created your project from the claude-toolbox template, you can pull future updates from upstream.

## How It Works

Template sync compares your repo against the upstream template at a specific version and applies changes. It's aware of your customizations and won't overwrite them blindly.

### What Gets Synced

| Component | Synced? | Notes |
|-----------|---------|-------|
| `.claude/settings.json` | Yes | Merged with your customizations |
| `CLAUDE.md` | Yes | Template sections updated, your additions preserved |
| `.codex/` | Yes | Full Codex config |
| `.github/scripts/` | Yes | Sync scripts themselves |
| `.github/workflows/` | Configurable | Workflow files synced if enabled |
| `klaude-plugin/` | No | Plugin updates come via plugin system |
| Project-specific files | No | Your code, docs, configs are untouched |

### Sync Exclusions

Files matching patterns in `.github/template-sync-exclude` are never touched by sync. One glob per line:

```
# Example exclusions
.claude/settings.local.json
custom-config.yml
```

## Using Template Sync

=== "GitHub Actions (recommended)"

    The `template-sync.yml` workflow runs on a schedule or manually via `workflow_dispatch`. It creates a PR with the changes for you to review.

=== "Local"

    ```bash
    /kk:template:sync --version v0.14.0
    ```

    Add `--dry-run` to preview changes without applying them.

    ```bash
    /kk:template:sync --version v0.14.0 --dry-run
    ```

## Prerequisites

- A `.github/template-state.json` file tracking the current template version
- The `template-sync.sh` script in `.github/scripts/`

## Merge Behavior

Sync creates a branch and PR. You review the changes, resolve any conflicts, and merge. The sync script is conservative — it prefers your local version when in doubt.
