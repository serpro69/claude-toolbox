# Codex

Codex (OpenAI) is supported as a secondary provider. Skills are generated from the canonical `klaude-plugin/` source via the `generate-kodex` tool.

## Setup

1. Install [Codex](https://openai.com/index/codex/)
2. Install the plugin: `codex plugin marketplace add serpro69/claude-toolbox`
3. Configure [MCP servers](../user-guide/mcp-servers.md#codex) at the user level

## Configuration Files

| File | Purpose |
|------|---------|
| `.codex/config.toml` | Main configuration; `capy setup --platform codex` registers capy's MCP server here, template sync preserves it |
| `.codex/hooks.json` | Session-start and pre-tool-use hooks; `capy setup --platform codex` registers capy's hooks here too, template sync preserves them |
| `.codex/rules/default.rules` | Starlark permission rules |
| `.codex/scripts/session-start.sh` | Behavioral instructions (session startup), plus capy guidance until capy's hooks take over |
| `.codex/scripts/pretooluse-bash.sh` | File-path denylist on shell commands, plus HTTP routing until capy's hooks take over |
| `.codex/scripts/guard/` | Generated shared permission-guard engine, declaration and license; adapter wiring is pending |
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

### Template sync and capy's entries

Template sync does not own capy's registration. The template ships no `[mcp_servers]` table in `config.toml` and only toolbox's own entries in `hooks.json`; on every sync the downstream copies of both files are merged rather than replaced:

- `config.toml`: toolbox substitutes `model` and `approval_policy` from the manifest, then keeps every `mcp_servers.*` entry the project has that the template does not ship. A server the template does ship wins by name. Existing explicit server tables whose values are unchanged are preserved byte-for-byte, including comments, ordering, quoting, nested tables, and whitespace. Only changed or repaired registrations are rendered as new explicit root-level tables, which `capy setup` can update.
- `hooks.json`: toolbox owns every entry whose command runs a script under `.codex/scripts/`, and those come from the template verbatim, so a toolbox entry that changed or was removed upstream does not linger. Every other entry the project has (capy's `capy codex-launch` hooks, hand-added hooks) is appended after toolbox's entries for its event.
- `.codex/capy-owner`: a built-in sync exclusion, never reported as deleted or removed. Capy refuses to regenerate a lost marker, so keep it committed alongside `hooks.json` and `config.toml` as capy's setup instructs.

The merge is stateless and derived from the project's files on every run. If either downstream file fails to parse, sync warns and falls back to the template copy for that file, which drops capy's entries; rerun `capy setup --platform codex` after fixing the file.

Older syncs could append an inline `mcp_servers = { ... }` assignment after `[tui]`, making it part of the TUI settings instead of a root-level registration. Sync now recovers those misplaced servers into root-level tables. If `capy setup` has already added a valid root-level entry, that whole entry takes precedence over the misplaced copy. Applying sync removes the stray TUI assignment; no manual cleanup is needed.

Sync does not run `capy setup`. Preserving existing table text avoids formatting churn when alternating setup and sync. Table extraction uses Python 3's standard library; `yq` validates the extracted registrations and the complete merged MCP map before the candidate file is accepted.

### Shared guard support for capy execution

The shared permission-guard engine recognizes `capy_execute`, `capy_execute_file`, and `capy_batch_execute` under any MCP server name. It checks shell code like Bash, other-language code with its literal-path/write-call scans, and each batch command independently. An execute-file input receives the secrets Read check before its processing code is inspected.

Capy execution defaults to the project root. A supplied cwd is absolute or project-relative; it does not change the project identity or the anchor for `capy_execute_file.path`. The file input always remains project-root-relative. Path parameters are literal, without shell-variable or tilde expansion.

The generated engine is present under `.codex/scripts/guard/`, but the template does not yet wire toolbox's MCP adapter to it. Engine support alone therefore does not enforce toolbox's capy policy on Codex. Capy's own registered hooks remain independent and unchanged.

## Known Limitations

!!! warning "Current limitations"

    - **Plugin-only installs** provide skills and profile content only — hooks, sub-agents, rules, and project config require [template setup](../getting-started/template-setup.md) or [adopting into an existing repo](../getting-started/adopting.md).
    - **Toolbox PreToolUse hooks** are only wired for Bash commands. The shared engine supports capy execution payloads, but its MCP adapter and the `apply_patch` adapter are not yet wired. See [ADR 0005](../adr/0005-codex-hook-enforcement-gap.md) for the hook-enforcement background.
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
