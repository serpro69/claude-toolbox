# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a starter template repository providing a complete development environment for Claude Code with pre-configured MCP servers and tools. It is a **configuration-only repository** with no application code.

## Architecture

Three integrated components:

1. **Claude Code** (`.claude/`): Project settings (`settings.json`), statusline scripts, and sync infrastructure
2. **kk plugin** (`klaude-plugin/`): Skills, commands, hooks, and utility scripts — distributed via the Claude Code plugin system
3. **Serena** (`.serena/`): Semantic code analysis via LSP — language detection, gitignore integration, tool exclusions (`project.yml`)

For API keys and MCP server setup, see the "MCP Server Configuration" section in `README.md`.

## Testing

Tests for the template-sync feature are in `test/`. Run with:

```bash
for test in test/test-*.sh; do $test; done
```

Tests use shared utilities from `test/helpers.sh`. See that file for available assertions and helpers.

## Troubleshooting

See `README.md` for detailed troubleshooting of MCP connection issues, Serena language detection, and template sync problems.

## Skill & Command Naming Conventions

Applies when creating or renaming kk-plugin skills and commands.

### Skills

- **Imperative verbs over noun phrases.** `design` not `analysis-process`, `implement` not `implementation-process`. Drop filler suffixes like `-process`. Skills are invoked as `/skill-name` — shorter names are faster to type.
- **Self-documenting over acronyms.** `chain-of-verification` beats `cove`. If the name requires expansion to understand it, it's the wrong name.
- **Family prefixes for grouped skills.** When multiple skills do the same action on different targets, share a prefix: `review-design`, `review-spec`, `review-code`. Tab-completion, discoverability, and mental grouping all benefit.
- **Reference bare in prose.** Inside skill/command files, reference other skills without the `kk:` prefix (e.g., `` `review-code` `` not `` `kk:review-code` ``). The `kk:` prefix is for command invocations, not prose references.

### Commands

Commands live under `klaude-plugin/commands/<name>/`. For skills with standard + isolated modes:

- `default.md` — standard variant, invoked as `/kk:<name>:default`
- `isolated.md` — isolated sub-agent variant, invoked as `/kk:<name>:isolated`

Symmetric naming avoids stuttering (`/kk:cove:cove` → `/kk:chain-of-verification:default`).

### Agents

Agent names describe the **role**, not the skill that invokes them. `code-reviewer`, `design-reviewer`, `spec-reviewer` persist across skill renames. Don't rename agent files when renaming the skills that delegate to them.

### Shared instructions

Instructions referenced by more than one skill live in `klaude-plugin/skills/_shared/<name>.md` with a bare basename (e.g., `review-scope-protocol.md`, `pal-codereview-invocation.md`).

Each consuming skill gets a **per-skill symlink** at `klaude-plugin/skills/<skill>/shared-<name>.md` pointing to `../_shared/<name>.md`. Reasons:

- Markdown links inside a skill stay local — `[shared-foo.md](shared-foo.md)` resolves without `../` path traversal, which keeps links working when the skill is bundled/copied.
- The `shared-` prefix in the skill directory makes it obvious at a glance which files are shared vs skill-specific.
- Only symlink into skills that actually reference the file — don't blanket-symlink.

When adding a new shared instruction:

1. Create `klaude-plugin/skills/_shared/<name>.md` (bare basename, no `shared-` prefix on the source file).
2. In each consuming skill directory, run `ln -s ../_shared/<name>.md shared-<name>.md`.
3. Reference it in skill docs as `[shared-<name>.md](shared-<name>.md)`.
4. Agents (in `klaude-plugin/agents/`) can't use the per-skill symlink pattern — reference shared files by their repo-relative path: `klaude-plugin/skills/_shared/<name>.md`.

### When renaming

- Update `test/test-plugin-structure.sh` `EXPECTED_SKILLS` and `EXPECTED_COMMANDS`.
- **Don't touch `run_plugin_migration`'s `dirs_to_remove` in `.github/scripts/template-sync.sh`** — those are historical paths for cleaning up pre-v0.5.0 downstream projects. They must stay as the names that existed at migration time.
- Leave `docs/done/**` untouched — it's frozen history.
- Watch for substring collisions (e.g., a `design-review` → `review-design` rename will also hit the `design-reviewer` agent name via simple sed; hand-fix those).

# Extra Instructions

@.claude/CLAUDE.extra.md

# capy — MANDATORY routing rules

@.claude/capy/CLAUDE.md
