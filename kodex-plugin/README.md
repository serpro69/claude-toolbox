# kk — Codex Plugin

Development workflow skills generated from [klaude-plugin/](../klaude-plugin/) (the Claude Code source of truth).

## Installation

```bash
codex plugin marketplace add serpro69/claude-toolbox
```

Then open `/plugins` in the Codex TUI, select the **Claude Toolbox** marketplace, and install `kk`.

> **Note:** Sparse checkout is not supported. The full repository must be cloned.

## Available Skills

| Skill | Description |
|-------|-------------|
| `chain-of-verification` | Apply CoVe prompting for self-verified accuracy |
| `dependency-handling` | Look up dependencies before writing calls |
| `design` | Turn ideas into design docs and implementation plans |
| `document` | Document changes after implementation |
| `implement` | Execute tasks from plans or standalone changes |
| `merge-docs` | Merge competing design docs into one |
| `review-code` | Code review with SOLID methodology |
| `review-design` | Review design docs for completeness and soundness |
| `review-spec` | Compare implementation against design docs |
| `test` | Write and run tests |

## Updating

```bash
codex plugin marketplace upgrade claude-toolbox
```

## How It Works

Skills are authored once in `klaude-plugin/skills/` and generated into this directory by `cmd/generate-kodex/`. The generation tool resolves `${CLAUDE_PLUGIN_ROOT}` references and copies auxiliary files. Run `make generate-kodex` after editing source skills to regenerate.

## Troubleshooting

- **Skills not appearing:** Ensure the plugin is installed via the marketplace browser, not manually copied.
- **Profile paths not resolving:** Profiles only work when the full toolbox repo is checked out (local development). Marketplace-only installs don't have access to `klaude-plugin/profiles/` — skills still function, but without language-specific review checklists.
- **Stale output:** Run `make generate-kodex` and check `git diff kodex-plugin/` to see if regeneration is needed.
