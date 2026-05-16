# Claude Code

Claude Code is the primary provider for claude-toolbox. All skills, agents, and configuration are authored for Claude Code first.

## Setup

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. Install the plugin: `/plugin install kk@claude-toolbox`
3. Configure [MCP servers](../user-guide/mcp-servers.md) in `~/.claude.json`

## Configuration Files

| File | Purpose |
|------|---------|
| `.claude/settings.json` | Permissions, allowed commands, settings |
| `CLAUDE.md` | Project instructions (checked into repo) |
| `.claude/CLAUDE.extra.md` | Behavioral instructions |
| `klaude-plugin/` | Skills, commands, agents, hooks, profiles |

## Features

- **Full plugin support** — skills appear as `/skill-name` with `(kk)` annotation
- **Sub-agents** — `klaude-plugin/agents/*.md` for independent reviewers
- **Hooks** — `PreToolUse` Bash validation for path safety
- **Statusline** — rich terminal display with multiple themes
- **Template sync** — full support for upstream updates
- **MCP servers** — Context7, Pal, Capy pre-wired

## Skills Invocation

Skills are invoked via slash commands:

```
/kk:design "feature description"
/kk:implement "work on task 1"
/kk:review-code
```

Commands (skill variants) use the full path:

```
/kk:review-code:isolated
/kk:chain-of-verification:default "question"
```
