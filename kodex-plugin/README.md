# kk — Codex Plugin

[![Documentation](https://img.shields.io/badge/docs-serpro69.github.io%2Fclaude--toolbox-blue?style=for-the-badge)](https://serpro69.github.io/claude-toolbox/latest/providers/codex/)

Development workflow skills generated from [klaude-plugin/](../klaude-plugin/) (the Claude Code source of truth). Part of the [claude-toolbox](https://github.com/serpro69/claude-toolbox) project.

## Installation

```bash
codex plugin marketplace add serpro69/claude-toolbox
```

Then open `/plugins` in the Codex TUI, select the **Claude Toolbox** marketplace, and install `kk`.

## What's Included

- **10 workflow skills** — the same pipeline as the Claude Code plugin (`design` → `implement` → `review-code` → `test` → `document` and utilities)
- **Language-specific profiles** — review checklists, implementation gotchas, design prompts, test validators, and doc rubrics for Go, Java, JS/TS, Kotlin, Kubernetes, and Python

The plugin does **not** include hooks, sub-agents, Starlark rules, or project configuration. For the full Codex experience, use the [template setup](https://serpro69.github.io/claude-toolbox/latest/getting-started/template-setup/) or [adopt into an existing repo](https://serpro69.github.io/claude-toolbox/latest/getting-started/adopting/).

See the [Codex provider docs](https://serpro69.github.io/claude-toolbox/latest/providers/codex/) for configuration, known limitations, and the generation pipeline.
