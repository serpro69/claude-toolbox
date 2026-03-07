# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a starter template repository providing a complete development environment for Claude Code with pre-configured MCP servers and tools. It is a **configuration-only repository** with no application code.

## Architecture

Three integrated MCP server configurations:

1. **Claude Code** (`.claude/`): Permission allowlist/denylist (`settings.local.json`), 50+ Task Master slash commands (`commands/tm/`), command reference (`TM_COMMANDS_GUIDE.md`)
2. **Serena** (`.serena/`): Semantic code analysis via LSP — language detection, gitignore integration, tool exclusions (`project.yml`)
3. **Task Master** (`.taskmaster/`): AI-powered task management — model config (`config.json`), integration guide (`CLAUDE.md`), PRD template (`templates/example_prd.txt`)

For API keys and MCP server setup, see the "MCP Server Configuration" section in `README.md`.

## Claude-Code Behavioral Instructions

### Exploration Phase

Always explore on your own to gain complete understanding. Only delegate to exploration agents if the user explicitly requests it.
<!-- Why: Claude tends to first spawn exploration agents,
     and then re-reads all the files on its own...
     resulting in double token consumption -->

## Serena Best Practices

Serena provides semantic code analysis — use it efficiently:

### Intelligent Code Reading Strategy

1. **Start with overview**: Use `get_symbols_overview` to see top-level structure
2. **Target specific symbols**: Use `find_symbol` with `include_body=true` only for symbols you need to understand or edit
3. **Pattern search**: Use `search_for_pattern` for flexible regex-based discovery
4. **Reference tracking**: Use `find_referencing_symbols` to understand usage
5. **Read full files only as a last resort** when symbolic tools cannot provide what you need

### Symbol Navigation

Symbols are identified by `name_path` and `relative_path`:

- Top-level: `ClassName` or `function_name`
- Methods: `ClassName/method_name`
- Nested: `OuterClass/InnerClass/method`
- Python constructors: `ClassName/__init__`

### Efficiency Principles

- Read symbol bodies only when you need to understand or edit them
- Use `depth` parameter to get method lists without bodies: `find_symbol("Foo", depth=1, include_body=False)`
- Track which symbols you've read and reuse that context
- Use symbolic tools before reading full files

## Task Master Integration

Task Master is the primary workflow orchestration system. Always prefer MCP tools over CLI commands — the permission configuration enforces this by denying `Bash(task-master:*)`.

### Slash Command Structure

Commands are organized under `/project:tm/[category]/[action]`:

- Setup: `/project:tm/setup/quick-install`, `/project:tm/init/quick`
- Daily: `/project:tm/next`, `/project:tm/list`, `/project:tm/show <id>`
- Status: `/project:tm/set-status/to-{done|in-progress|review|pending|deferred|cancelled} <id>`
- Analysis: `/project:tm/analyze-complexity`, `/project:tm/expand <id>`
- Workflows: `/project:tm/workflows/smart-flow`, `/project:tm/workflows/auto-implement`

### Working with Tasks

1. Parse requirements: `/project:tm/parse-prd .taskmaster/docs/prd.txt`
2. Analyze complexity: `/project:tm/analyze-complexity --research`
3. Expand tasks: `/project:tm/expand/all`
4. Get next task: `/project:tm/next`
5. Update progress: Use MCP `update_subtask` to log implementation notes
6. Complete: `/project:tm/set-status/to-done <id>`

See `.taskmaster/CLAUDE.md` for the complete 400+ line Task Master integration guide.

## Project Rules

### File Management

- **Edit `tasks.json` only via Task Master commands** — use MCP tools or slash commands
- **Edit `config.json` only via** `/project:tm/models/setup`
- Task markdown files in `.taskmaster/tasks/*.md` are auto-generated

### Permission Configuration

See `.claude/settings.local.json` for the full tool allowlist/denylist.

### Context Management

- Use `/clear` between different tasks to reset context
- This CLAUDE.md is automatically loaded
- Task Master commands pull task context on demand

### Git Integration

- Serena respects `.gitignore` by default
- Use conventional commits with task IDs: `feat: implement JWT auth (task 1.2)`

### Template Sync

- `.github/template-state.json` tracks template version and configuration variables
- Use Actions → Template Sync to pull upstream configuration updates
- Always review PR changes before merging to preserve local customizations
- Sync preserves project-specific values (name, language, prompts) via manifest variables
- User-scoped files like `.taskmaster/tasks/`, `.taskmaster/docs/`, and `.taskmaster/reports/` are never modified

### Sync Exclusions

- Add `sync_exclusions` array to `.github/template-state.json` to prevent specific paths from being synced
- Patterns use glob syntax (e.g., `.claude/commands/cove/*`)
- See README.md "Configuring Sync Exclusions" section for details

## Testing

Tests for the template-sync feature are in `test/`. Run with:

```bash
for test in test/test-*.sh; do $test; done
```

Tests use shared utilities from `test/helpers.sh`. See that file for available assertions and helpers.

## Troubleshooting

See `README.md` for detailed troubleshooting of MCP connection issues, Task Master AI failures, Serena language detection, and template sync problems.

## Task Master AI Instructions

**IMPORTANT!!! Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**

@./.taskmaster/CLAUDE.md
