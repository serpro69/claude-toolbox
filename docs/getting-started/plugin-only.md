# Plugin-Only Setup

Already have a project? Install just the plugin to get all 15 workflow and utility skills.

## Claude Code

```
claude plugin marketplace add serpro69/claude-toolbox
claude plugin install kk@claude-toolbox
```

Skills are available as `/kk:(skill-name)` (annotated with `(kk)` in the slash command menu). The Claude plugin also includes commands, sub-agents and the permission guard. The guard protects secrets, destructive operations and configuration on Bash, file tools and capy execution tools without needing template settings or configuration files.

Use Claude Code 2.1.295+, Bash, `jq` and Python 3.8+. Guard failures block matched calls, including reads; repair a missing interpreter rather than expecting the hook to skip it. See [Guard Configuration](../user-guide/configuration.md#guard-configuration) for project additions and user exceptions. Disabling hooks removes plugin-only protection because this installation mode has no native settings baseline.

!!! tip
    Want the full configuration too (settings, statusline, sync infrastructure)? See [Adopting into Existing Repositories](adopting.md).
    For MCP servers, see [MCP Server Configuration](../user-guide/mcp-servers.md).

## Codex

```bash
codex plugin marketplace add serpro69/claude-toolbox
```

The Codex plugin includes skills and language-specific profile content (review checklists, implementation gotchas, etc.). See [kodex-plugin](https://github.com/serpro69/claude-toolbox/tree/master/kodex-plugin) for details.

!!! note "Codex limitations"
    The Codex plugin provides **skills and profiles only** — it does not include hooks, sub-agents, Starlark rules, or project configuration. For the full Codex experience (SessionStart/PreToolUse hooks, sub-agents, config, rules), use the [template setup](template-setup.md) or [adopt into an existing repo](adopting.md).

For MCP servers (Context7, Pal), see [Codex MCP Setup](../user-guide/mcp-servers.md#codex).

## What's Included

The plugin gives you:

- **15 workflow and utility skills** — `/kk:design`, `/kk:implement`, `/kk:review-code`, `/kk:clarify-docs`, etc.
- **Language profiles** — Go, Java, JS/TS, Kotlin, Kubernetes, Python
- **Commands** — isolated variants for code review, CoVe and spec review
- **Hooks** — secrets, destructive-operation and configuration protection across the supported tool channels (Claude Code only)
- **Sub-agents** — independent reviewers (Claude Code only)

## What's Not Included

- MCP server configuration (Context7, Pal, Capy)
- Native permission-settings baseline and statusline (the Claude guard's runtime baseline is included)
- Template sync infrastructure

For the full setup, use [Template Setup](template-setup.md) or [Adopt into Existing Repos](adopting.md).
