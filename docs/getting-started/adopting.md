# Use kk in an existing repository

[Install kk](template-setup.md) once. In your project, run `kk claude` or `kk codex`. Keep versioned team instructions in `CLAUDE.md` and `AGENTS.md`, project restrictions in `.claude/kk-guard.json`, and your personal launcher preferences in the [machine override file](../user-guide/configuration.md#how-configuration-works).

## Repositories created from the toolbox template

Look for `.github/template-state.json`. Its presence identifies a repository managed by template sync. Installing kk leaves the repository files in place. Team members can install and verify kk before anyone commits changes.

When the team is ready, follow the [migration guide](../user-guide/template-sync.md). `kk migrate` verifies the guard for each tool the repository uses, previews an ordinary sync to the retirement release, then previews removal. You decide separately whether to apply each step. Review the uncommitted diff with collaborators, particularly if CI or cloud sessions depend on the committed plugin settings.

## Repositories using plugins directly

The [plugin-only setup](plugin-only.md) remains available. When moving to the managed installation, `kk status` reports Git-marketplace copies. Check the scope before removing one. A project-scoped registration may also serve other developers or CI.
