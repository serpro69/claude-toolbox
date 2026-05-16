# Plugin-Only Setup

Install just the kk plugin — no template, no configuration changes. Works with any existing project.

## Claude Code

```
/plugin install kk@claude-toolbox
```

All skills appear as `/skill-name` in the slash command menu (annotated with `(kk)`). No additional configuration needed.

## Codex

```bash
codex plugin marketplace add serpro69/claude-toolbox
```

!!! note "Codex limitations"
    Plugin-only installs provide skills and profile content only — hooks, sub-agents, rules, and project config require [template setup](template-setup.md) or [adopting into an existing repo](adopting.md).

## What's Included

The plugin gives you:

- **10 workflow skills** — `/kk:design`, `/kk:implement`, `/kk:review-code`, etc.
- **Language profiles** — Go, Java, JS/TS, Kotlin, Kubernetes, Python
- **Commands** — isolated variants for code review, CoVe, spec review, design review

## What's Not Included

- MCP server configuration (Context7, Pal, Capy)
- Permission baselines and hooks
- Statusline themes
- Template sync infrastructure

For the full setup, use [Template Setup](template-setup.md) or [Adopt into Existing Repos](adopting.md).
