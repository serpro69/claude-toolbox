# MCP Servers

MCP servers are configured at the user level (not in the repo) to keep API keys safe. These configs are generic enough to reuse across all your projects.

You don't need all servers to get started. Add them incrementally:

1. **Context7** (needs API key) — up-to-date library documentation and code examples
2. **Pal** (needs API key) — multi-model AI integration for code review, debugging, planning, and security audit
3. **Capy** (optional, auto-configured by bootstrap) — persistent knowledge base across sessions

## Claude Code

Add MCP servers to `~/.claude.json` under the `mcpServers` key:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"],
      "env": {
        "DEFAULT_MINIMUM_TOKENS": "10000",
        "CONTEXT7_API_KEY": "<your-key>"
      }
    },
    "pal": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/serpro69/pal-mcp-server",
        "pal-mcp-server"
      ],
      "env": {
        "GEMINI_API_KEY": "<your-key>"
      }
    }
  }
}
```

!!! tip "Capy"
    Install Capy with `brew install serpro69/tap/capy`. It auto-configures on first run — no manual MCP entry needed.

## Codex

```bash
# Context7
codex mcp add context7 -- npx -y @context7/mcp

# Pal
codex mcp add pal -- uvx --from 'git+https://github.com/serpro69/pal-mcp-server' pal-mcp-server
```

Set environment variables in your shell profile:

```bash
export CONTEXT7_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
```

## What Each Server Does

### Context7

Fetches current documentation for any library, framework, or SDK. Used by the **dependency-handling** skill to look up API signatures instead of guessing. Also available for ad-hoc queries: ask about any library and Context7 provides up-to-date docs.

### Pal

Multi-model AI integration. Powers the **review-code** skill's independent reviewer sub-agents — your code gets reviewed by Gemini (or other models) in addition to Claude, catching blind spots neither model would find alone. Also provides: `debug`, `planner`, `secaudit`, `testgen`, and more.

### Capy

Persistent knowledge base that survives across sessions. Indexes command output, web content, and curated knowledge for BM25 search. Protects your context window by keeping large outputs in sandboxed subprocesses.
