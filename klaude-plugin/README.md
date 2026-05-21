# kk — Claude Code Plugin

[![Documentation](https://img.shields.io/badge/docs-serpro69.github.io%2Fclaude--toolbox-blue?style=for-the-badge)](https://serpro69.github.io/claude-toolbox/latest/user-guide/skills/)

A development workflow plugin for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that gives your AI assistant a structured pipeline — from idea through design, implementation, code review, testing, to documentation. Part of the [claude-toolbox](https://github.com/serpro69/claude-toolbox) project.

Why `kk`? I have `jj` and `kk` mappings in nvim to go back to normal mode, and it seemed like a low-conflict/easy-to-type option for a plugin-prefixed skill names. We can also pretend it's an acronym for "klaude kode", if you need a better reason for the plugin naming.

## Installation

```
/plugin install kk@claude-toolbox
```

All skills appear as `/skill-name` in the slash command menu (annotated with `(kk)`). No additional configuration needed.

## What's Included

- **10 workflow skills** — `/kk:design` → `/kk:review-design` → `/kk:implement` → `/kk:review-code` → `/kk:test` → `/kk:document`, plus utilities
- **Commands** — isolated variants for code review, CoVe, spec review, design review
- **Hooks** — Bash validation (blocks commands touching sensitive paths)
- **Profiles** — per-domain content (Go, Java, JS/TS, Kotlin, K8s, Python) with review checklists, implementation gotchas, design prompts, test validators, and doc rubrics

See the [Skills](https://serpro69.github.io/claude-toolbox/latest/user-guide/skills/) and [Profiles](https://serpro69.github.io/claude-toolbox/latest/user-guide/profiles/) documentation for details.
