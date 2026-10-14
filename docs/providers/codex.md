# Codex

Codex (OpenAI) is supported as a secondary provider. Skills are generated from the canonical `klaude-plugin/` source via the `generate-kodex` tool.

## Setup

1. Install [Codex](https://openai.com/index/codex/)
2. Install the plugin: `codex plugin marketplace add serpro69/claude-toolbox`
3. Configure [MCP servers](../user-guide/mcp-servers.md#codex) at the user level

## Configuration Files

| File | Purpose |
|------|---------|
| `.codex/config.toml` | Main configuration |
| `.codex/hooks.json` | Session-start and pre-tool-use hooks; `capy setup --platform codex` registers capy's hooks here too |
| `.codex/rules/default.rules` | Starlark permission rules |
| `.codex/scripts/session-start.sh` | Behavioral instructions (session startup), plus capy guidance until capy's hooks take over |
| `.codex/scripts/pretooluse-bash.sh` | File-path denylist on shell commands, plus HTTP routing until capy's hooks take over |
| `.codex/agents/*.toml` | Sub-agent definitions (generated) |
| `kodex-plugin/` | Skills (generated from `klaude-plugin/`) |
| `AGENTS.md` | Project instructions |

## Capy Hooks

Out of the box, toolbox's two Codex hooks stand in for capy: `session-start.sh` injects `.capy/AGENTS.md` into the session context, and `pretooluse-bash.sh` denies `curl`, `wget`, and inline HTTP calls so the model routes them through capy's MCP tools.

Capy v0.17.1 and later ships its own Codex hooks. Running `capy setup --platform codex` in the project registers them in `.codex/hooks.json` next to toolbox's entries. They deliver availability-aware guidance and HTTP routing (advisory by default, evidence-based redirects, a silent-download exception) that toolbox's unconditional deny would otherwise override. Toolbox detects those entries per event — a registered command that invokes `capy codex-launch` — and steps aside:

- `session-start.sh` replaces the `.capy/AGENTS.md` injection with a one-line note that capy's hooks own guidance and routing. Provider instructions and `.claude/CLAUDE.*.md` extras are still injected.
- `pretooluse-bash.sh` skips the HTTP denials. The file-path denylist (`.env`, `.terraform/`, `.git/`, …) always applies.

The check runs on every session start and every shell call, so there is no flag to flip and nothing to roll back. Remove capy's entries from `hooks.json` and the legacy behavior returns on the next session.

!!! warning "Remove capy's entries, don't disable them"

    Codex trusts hooks individually through `/hooks`, and capy's setup never changes trust. A capy entry that is present but disabled still makes toolbox step aside, so the project ends up with no capy guidance and no HTTP routing at all. To switch capy's Codex hooks off, delete its entries from `.codex/hooks.json`. After running setup, review and trust the new entries in `/hooks`; registration alone does not execute them.

!!! warning "Template sync overwrites `.codex/hooks.json`"

    Template sync copies the upstream `.codex/` tree over the project, which drops capy's registered entries and silently returns the project to the legacy path. Until sync merges that file, either rerun `capy setup --platform codex` after every sync, or add `.codex/hooks.json` to `sync_exclusions` in `.github/template-state.json` at the cost of no longer receiving toolbox hook updates. Tracked as a follow-up to [issue #170](https://github.com/serpro69/claude-toolbox/issues/170).

    The `.codex/capy-owner` installation marker is safe: it is a built-in sync exclusion, so sync never reports it as deleted or removes it. Capy refuses to regenerate a lost marker, so keep it committed alongside `hooks.json` and `config.toml` as capy's setup instructs.

## Known Limitations

!!! warning "Current limitations"

    - **Plugin-only installs** provide skills and profile content only — hooks, sub-agents, rules, and project config require [template setup](../getting-started/template-setup.md) or [adopting into an existing repo](../getting-started/adopting.md).
    - **PreToolUse hooks** are only wired for Bash commands. `apply_patch` and MCP tool hooks are documented in [ADR 0005](../adr/0005-codex-hook-enforcement-gap.md) but not yet implemented.
    - **MCP servers** (Context7, Pal) must be configured at the user level — they are not packaged in the plugin. See [Codex MCP Setup](../user-guide/mcp-servers.md#codex).

## Generation Pipeline

`klaude-plugin/` is the single source of truth. The generation tool:

1. Reads `klaude-plugin/` skills and agents
2. Applies Codex-specific transformations (resolves `${CLAUDE_PLUGIN_ROOT}`, injects headers)
3. Produces `kodex-plugin/` (skills) and `.codex/agents/*.toml` (sub-agents)

After editing skills in `klaude-plugin/`, regenerate with:

```bash
make generate-kodex
```

CI checks freshness via `make generate-kodex && git diff --exit-code kodex-plugin/ .codex/agents/`.
