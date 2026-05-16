# Configuration

claude-toolbox provides opinionated defaults for permissions, statusline, hooks, and project settings.

## Settings

Configuration lives in `.claude/settings.json` (Claude Code) and `.codex/config.toml` (Codex).

### Recommended Claude Code Settings

Run `/config` in Claude Code to review and customize. Key settings:

```
- Theme: dark
- Notifications: enabled
- Auto-compact: enabled (on context limit)
- Verbose tool calls: disabled
```

### Permission Baselines

The template ships with a tuned permission set:

- **Read-only tools** — always allowed (file reads, glob, grep, git status)
- **Write tools** — allowed for project files (edit, write)
- **Bash commands** — allowed for safe patterns (git, npm, go, make, python, etc.)
- **Blocked patterns** — `.env`, `.git/`, `node_modules`, `build/`, `dist/`, `venv/`

Customize in `.claude/settings.json` under `permissions.allow` and `permissions.deny`.

## Hooks

The plugin ships one hook:

| Hook | Trigger | Description |
|------|---------|-------------|
| Bash validation | `PreToolUse` on `Bash` | Blocks commands touching `.env`, `.git/`, `node_modules`, `build/`, `dist/`, `venv/`, and other sensitive paths |

## Statusline

The statusline shows useful context at the bottom of your terminal: git branch, model, token usage, and more. Multiple themes are available.

## Project Instructions

- `CLAUDE.md` — project-specific instructions for Claude Code (checked into the repo)
- `.claude/CLAUDE.extra.md` — behavioral instructions (independent thinking, fail-loud, assumptions)
- `AGENTS.md` — equivalent instructions for Codex
