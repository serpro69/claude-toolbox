# Claude Code

Claude Code is the primary provider for Agentstakk. All skills, agents, and configuration are authored for Claude Code first.

## Setup

[Install kk](../getting-started/install.md), then run `kk claude` in your project. For a vendor-managed plugin with your own settings, use the [plugin-only setup](../getting-started/plugin-only.md). Configure [MCP servers](../user-guide/mcp-servers.md) separately.

## Claude Code authentication and terms

`kk claude` starts the Claude Code executable you installed and passes a local settings file with `--settings`. Claude Code loads the toolbox skills and hooks through its plugin system. Sign in through Claude Code using your own account or your organization's configured provider. The launcher leaves authentication and billing with that provider. [Claude Code authentication](https://code.claude.com/docs/en/authentication) · [Claude Code plugins](https://code.claude.com/docs/en/plugins)

Anthropic’s published guidance allows end users to sign in to the unmodified Claude Code binary with their own subscription. Agentstakk uses that flow for local subscription use. It supplies settings and plugins while Claude Code handles sign-in with the provider and usage is billed under the user’s or organization’s agreement. Anthropic lists consumer terms for individual plans and commercial terms for Team, Enterprise and API use. Products or hosted services that run Claude Code have additional requirements, including preserving its sign-in methods and direct billing to each end user. [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance) · [Consumer terms](https://www.anthropic.com/legal/consumer-terms) · [Commercial terms](https://www.anthropic.com/legal/commercial-terms)

## Configuration files

| Location | Purpose |
| --- | --- |
| `$KK_HOME/releases/<release>/klaude-plugin/` | The active machine plugin, including skills, agents, commands, guard, behavioral instructions and statusline scripts |
| `${XDG_CONFIG_HOME:-$HOME/.config}/kk/config.json` | Personal launcher preferences and optional grants, read on the next launch |
| `.claude/settings.json` and `.claude/settings.local.json` | Team and personal project settings. Explicit preferences take precedence over toolbox defaults. |
| `CLAUDE.md` | Project instructions. Existing imports continue to work. |
| `.claude/kk-guard.json` and `~/.claude/kk-guard.json` | Project additions and machine-owner exceptions to the guard policy |

## Permission guard

The user-scope plugin `kk@agentstakk-local` supplies guard hooks wherever Claude loads and enables it. It checks shell calls, Claude file tools and the supported capy execution tools. Use Claude Code 2.1.295+ with Bash, `jq` and Python 3.9+. Start a fresh session after an upgrade. [Guard configuration](../user-guide/configuration.md#guard-configuration)

**Wrapped sessions** also receive the native secret deny list through `kk claude`, including when you supply your own `--settings`. They get the toolbox statusline in trusted interactive sessions with hooks enabled. Inspect the composed settings with `kk claude --print-layer`.

**Unwrapped sessions** such as bare `claude`, the IDE extension and the desktop app can load the plugin hooks. They do not receive the launcher’s native deny list or statusline. A user-level install on your machine does not reach cloud sessions or fresh CI runners. Provision the plugin on those hosts or retain the relevant committed enablement when migrating.

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
