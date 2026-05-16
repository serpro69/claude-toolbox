# Overview

Tools like Claude Code and Codex are powerful on their own, but LLMs don't know your development workflow. claude-toolbox started as a way to streamline configurations across projects without copy-paste. Over time, recurring patterns evolved into skills and agents.

## What You Get

**A minimal, opinionated configuration** — sensible permission baselines, a rich statusline, MCP server wiring, and sync infrastructure to keep it all up to date across your projects. Think of it as a dotfiles repo for Claude Code and Codex.

**A structured development pipeline** — 10 workflow skills with explicit multi-language support that take you from idea through design, implementation, code review, testing, to documentation, with persistent knowledge that carries across sessions.

```
/design → /review-design → /implement → /review-code → /test → /document
```

## Features at a Glance

- **10 workflow skills** — a complete development pipeline invoked as `/kk:<skill-name>`, with many skills integrated with each other
- **Multi-language support** — precise and distinct instructions from design, to implementation, to testing, to review for: Go, Java, JS/TS, Kotlin, Kubernetes, and Python
- **Multi-model code review** — independent reviewers using sub-agents and external models (Gemini, etc.)
- **Persistent knowledge base** — findings, decisions, and conventions that survive across sessions via Capy
- **Up-to-date library docs** — always-current documentation lookup via Context7
- **Battle-tested configuration** — permissions, statusline themes, hooks, sensible defaults

## Requirements

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — the AI coding assistant this toolbox extends
- **[npm](https://www.npmjs.com/package/npm)** — used by some MCP server installations
- **[uv](https://docs.astral.sh/uv/)** — Python package runner for Pal MCP server
- **[jq](https://jqlang.github.io/jq/)** — JSON processor, required for template-cleanup

### API Keys

- [Context7](https://context7.com/) API key — for library documentation lookups
- Gemini API key for [Pal](https://github.com/serpro69/pal-mcp-server) (or [any other provider](https://github.com/serpro69/pal-mcp-server/blob/main/docs/getting-started.md)) — for multi-model code review
