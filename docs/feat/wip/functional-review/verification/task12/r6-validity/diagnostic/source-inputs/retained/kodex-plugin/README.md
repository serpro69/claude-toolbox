# kk — Codex Plugin

[![Documentation](https://img.shields.io/badge/docs-serpro69.github.io%2Fclaude--toolbox-blue?style=for-the-badge)](https://serpro69.github.io/claude-toolbox/latest/providers/codex/)

Development workflow skills generated from [klaude-plugin/](../klaude-plugin/) (the Claude Code source of truth). Part of the [claude-toolbox](https://github.com/serpro69/claude-toolbox) project.

## Installation

```bash
codex plugin marketplace add serpro69/claude-toolbox
```

Then open `/plugins` in the Codex TUI, select the **Claude Toolbox** marketplace, and install `kk`.

## What's Included

- **15 workflow and utility skills** — the same pipeline as the Claude Code plugin (`$kk:design` → `$kk:review-design` → `$kk:implement` → `$kk:review-code` → `$kk:test` → `$kk:document`, plus utilities)
- **Language-specific profiles** — review checklists, implementation gotchas, design prompts, test validators, and doc rubrics for Go, Java, JS/TS, Kotlin, Kubernetes, and Python

The plugin does **not** include hooks, sub-agents, Starlark rules, or project configuration. For the full Codex experience, use the [template setup](https://serpro69.github.io/claude-toolbox/latest/getting-started/template-setup/) or [adopt into an existing repo](https://serpro69.github.io/claude-toolbox/latest/getting-started/adopting/).

Use `$kk:brainstorm` for an optional conversation about a technical idea or decision. It asks one question at a time, adapts to the clarity you need, and ends with a chat-only recap of decisions, rationale, and open assumptions. Request `$kk:design` when you want written design documents, an implementation plan, and tasks; brainstorming creates no files and does not start that workflow automatically.

See the [Codex provider docs](https://serpro69.github.io/claude-toolbox/latest/providers/codex/) for configuration, known limitations, and the generation pipeline.
