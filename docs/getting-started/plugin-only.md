# Plugin-Only Setup

Already have a project? Install just the plugin to get all 16 workflow and utility skills.

## Claude Code

```
claude plugin marketplace add serpro69/claude-toolbox
claude plugin install kk@claude-toolbox
```

Skills are available as `/kk:(skill-name)` (annotated with `(kk)` in the slash command menu). The Claude plugin also includes commands, sub-agents and the permission guard. The guard protects secrets, destructive operations and configuration on Bash, file tools and capy execution tools without needing template settings or configuration files.

Use Claude Code 2.1.295+, Bash, `jq` and Python 3.8+. Guard failures block matched calls, including reads; repair a missing interpreter rather than expecting the hook to skip it. See [Guard Configuration](../user-guide/configuration.md#guard-configuration) for project additions and user exceptions. Disabling hooks removes plugin-only protection because this installation mode has no native settings baseline.

For launchers, native permission settings and machine-wide updates, use [Install kk](template-setup.md). Configure [MCP servers](../user-guide/mcp-servers.md) separately.

## Codex

```bash
codex plugin marketplace add serpro69/claude-toolbox
codex plugin add kk@claude-toolbox
```

The Codex plugin includes skills and language-specific profile content (review checklists, implementation gotchas, etc.). See [kodex-plugin](https://github.com/serpro69/claude-toolbox/tree/master/kodex-plugin) for details.

To install the separate permission guard from a marketplace revision that includes it, run `codex plugin add kk-guard@claude-toolbox`. Review its three `PreToolUse` handlers in `/hooks`. The guard reads project policy from the session workspace.

[Machine installation](template-setup.md) also supplies the named Codex profile, owned sub-agent files and optional account-wide rules.

For MCP servers (Context7, Pal), see [Codex MCP Setup](../user-guide/mcp-servers.md#codex).

## Upgrading

Use the vendor’s marketplace update commands for the Git installation. In Claude Code, refresh the marketplace with `claude plugin marketplace update claude-toolbox`, update `kk@claude-toolbox` with `claude plugin update kk@claude-toolbox`, and start a fresh session. In Codex, review changed guard handlers in `/hooks` before using a new session. Managed installations use `kk upgrade`.

## What's Included

The plugin gives you:

- **16 workflow and utility skills** — `/kk:design`, `/kk:implement`, `/kk:review-code`, `/kk:clarify-docs`, etc.
- **Language profiles** — Go, Java, JS/TS, Kotlin, Kubernetes, Python
- **Commands** — isolated variants for code review, CoVe and spec review
- **Hooks** — permission checks for Claude Code and, with the separate guard plugin, for Codex
- **Sub-agents** — independent reviewers (Claude Code only)

## What's Not Included

- MCP server configuration (Context7, Pal, Capy)
- Native permission-settings baseline and statusline (the Claude guard's runtime baseline is included)
- The `kk` launchers, offline rollback and owned Codex agent files

For the full setup, [install kk on your machine](template-setup.md).
