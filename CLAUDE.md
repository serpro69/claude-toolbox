# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a starter template repository providing a complete development environment for Claude Code with pre-configured MCP servers and tools. It is a **configuration-only repository** with no application code.

## Architecture

Two integrated MCP server configurations:

1. **Claude Code** (`.claude/`): Project settings (`settings.json`), skills, agents, and custom commands
2. **Serena** (`.serena/`): Semantic code analysis via LSP — language detection, gitignore integration, tool exclusions (`project.yml`)

For API keys and MCP server setup, see the "MCP Server Configuration" section in `README.md`.

## Project Rules

- `.claude/` is a symlink to `.github/templates/claude/`

## Testing

Tests for the template-sync feature are in `test/`. Run with:

```bash
for test in test/test-*.sh; do $test; done
```

Tests use shared utilities from `test/helpers.sh`. See that file for available assertions and helpers.

## Troubleshooting

See `README.md` for detailed troubleshooting of MCP connection issues, Serena language detection, and template sync problems.

# Extra Instructions

@import .claude/CLAUDE.extra.md
