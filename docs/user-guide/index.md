# User Guide

Learn how to use Agentstakk's features effectively.

## Core Concepts

| Topic | Description |
|-------|-------------|
| [Skills](skills.md) | Workflow and utility skills, commands and examples |
| [Profiles](profiles.md) | Per-domain content for Go, Java, JS/TS, Kotlin, K8s, K8s Operator, Python, and agent-skill authoring |
| [MCP Servers](mcp-servers.md) | Context7, Pal, and Capy — the knowledge stack |
| [Configuration](configuration.md) | Settings, permissions, statusline, and hooks |
| [Template migration](template-sync.md) | Previewing sync and retirement of a legacy repository |

## The Pipeline

```
/kk:design → /kk:review-design → /kk:implement → /kk:review-code → /kk:test → /kk:document
```

Each skill produces artifacts the next one consumes. See [Skills](skills.md) for the full breakdown.
