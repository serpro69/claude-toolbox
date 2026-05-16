# Providers

claude-toolbox supports two AI coding providers:

|                             | Claude Code                         | Codex (OpenAI)                                         |
| --------------------------- | ----------------------------------- | ------------------------------------------------------ |
| **Skills**                  | `klaude-plugin/` (authored)         | `kodex-plugin/` (generated)                            |
| **Sub-agents**              | `klaude-plugin/agents/*.md`         | `.codex/agents/*.toml` (generated)                     |
| **Project instructions**    | `CLAUDE.md`                         | `AGENTS.md`                                            |
| **Behavioral instructions** | `.claude/CLAUDE.extra.md`           | `.codex/scripts/session-start.sh`                      |
| **Config**                  | `.claude/settings.json`             | `.codex/config.toml`                                   |
| **Hooks**                   | `klaude-plugin/hooks/`              | `.codex/hooks.json`                                    |
| **Rules/Permissions**       | `.claude/settings.json`             | `.codex/rules/default.rules` (Starlark)                |
| **Plugin install**          | `/plugin install kk@claude-toolbox` | `codex plugin marketplace add serpro69/claude-toolbox`  |
| **Template sync**           | Full support                        | `.codex/` synced                                       |

`klaude-plugin/` is the canonical source of truth. The `generate-kodex` tool produces `kodex-plugin/` and `.codex/agents/` with all necessary transformations.

- [Claude Code](claude-code.md) — setup, features, and configuration details
- [Codex](codex.md) — setup, known limitations, and workarounds
