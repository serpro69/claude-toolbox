# Claude Code

Claude Code is the primary provider for claude-toolbox. All skills, agents, and configuration are authored for Claude Code first.

## Setup

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. Install the plugin: `/plugin install kk@claude-toolbox`
3. Configure [MCP servers](../user-guide/mcp-servers.md) in `~/.claude.json`

## Configuration Files

| File | Purpose |
|------|---------|
| `.claude/settings.json` | Generated secrets deny baseline, allowed commands, settings |
| `.claude/kk-guard.json` | Optional project additions to the permission guard; never replaced by sync |
| `~/.claude/kk-guard.json` | User-owned, project-scoped destructive/self-modification exceptions |
| `CLAUDE.md` | Project instructions (checked into repo) |
| `.claude/CLAUDE.extra.md` | Behavioral instructions |
| `klaude-plugin/` | Skills, commands, agents, hooks, profiles |

## Features

- **Full plugin support** — skills appear as `/skill-name` with `(kk)` annotation
- **Sub-agents** — `klaude-plugin/agents/*.md` for independent reviewers
- **Hooks** — `PreToolUse` guard on Bash, file tools and capy execution tools; secrets, destructive operations and protected configuration
- **Statusline** — rich terminal display with multiple themes
- **Template sync** — full support for upstream updates
- **MCP servers** — Context7, Pal, Capy pre-wired

## Permission Guard

The plugin enforces its shipped baseline without template settings or guard config files. It covers `Bash`, `Read`, `Grep`, `Glob`, `Edit`, `Write`, `NotebookEdit`, and capy's three execution tools. Template installations additionally receive generated `Read(...)` secrets deny rules as a native fallback. Logs, build output, dependencies and `.env.example` are readable under the baseline.

Use Claude Code 2.1.295+ with Bash, `jq` and Python 3.8+. The wrapper denies when it cannot evaluate a call, and the hook registration blocks failures/timeouts. Destructive rules apply in bypass mode too. Turning hooks off removes destructive and self-modification protection; plugin-only installations also lose the hook's secrets protection.

Project config can tighten protection; only the user's config can loosen destructive rules or permit settings edits. See [Guard Configuration](../user-guide/configuration.md#guard-configuration) for examples, including the `disable_selfmod` entry needed when an agent edits settings. Secrets remain protected; search-result contents and dynamically constructed interpreter paths are outside complete coverage.

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
