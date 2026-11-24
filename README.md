<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/images/lockup-dark.svg">
    <img src="docs/assets/images/lockup-light.svg" alt="Agentstakk" width="720">
  </picture>
</div>

# Agentstakk

[![GitHub Release](https://img.shields.io/github/v/release/serpro69/agentstakk?style=for-the-badge&color=D9683D)](https://github.com/serpro69/agentstakk/releases)
[![Mentioned in Awesome Claude Code](https://img.shields.io/badge/Awesome-Claude%20Code-fc60a8?style=for-the-badge&logo=awesomelists&logoColor=white)](https://github.com/hesreallyhim/awesome-claude-code)
[![Documentation](https://img.shields.io/badge/docs-serpro69.github.io%2Fagentstakk-blue?style=for-the-badge)](https://serpro69.github.io/agentstakk/)

> [!NOTE]
> **From `claude-toolbox` to `agentstakk`.** I started this project as a template for sharing Claude Code settings across my repositories. It now ships skills, hooks and workflows for both Claude Code and Codex through one `kk` installation. “Agentstakk” reads as “agent stack.” The Norwegian word *stakk* gives the name its double *k*, a nod to the `kk` command.
>
> If your project has `.github/template-state.json`, follow the [template migration guide](docs/user-guide/template-sync.md). If you installed `kk@claude-toolbox` directly and want to keep using the public plugin, follow the [marketplace switch](docs/getting-started/plugin-only.md#switch-an-existing-git-marketplace-installation).

<div align="center">
  <picture>
    <img width="1080" alt="Terminal view" src="https://github.com/user-attachments/assets/27ef7269-0153-47c0-b07d-ed6a9504a176" />
  </picture>
</div>

Agentstakk is a collection of "tools" for all your agentic workflows — pre-configured MCP servers, skills, sub-agents, commands, hooks, statuslines with themes, and more - everything you need for AI-powered development workflows, used and battle-tested daily on many of my own projects.

**Supported providers:** [Claude Code](https://serpro69.github.io/agentstakk/latest/providers/claude-code/) · [Codex](https://serpro69.github.io/agentstakk/latest/providers/codex/)

<div align="center">

## [Read the full documentation →](https://serpro69.github.io/agentstakk/latest/)

  <a href="https://serpro69.github.io/agentstakk/latest/">
    <img width="1080" alt="Docs landing page" src="https://github.com/user-attachments/assets/f6af0017-7f78-476b-8399-81eda8673d0a" />
  </a>

### [Or explore how Agentstakk was used in a real project →](https://serpro69.github.io/agentstakk/latest/explore/)

  <a href="https://serpro69.github.io/agentstakk/latest/explore/">
    <img width="1080" alt="Explore page" src="https://github.com/user-attachments/assets/1adbbaa6-579c-4f27-94b1-8515cfefc2ec" />
  </a>
</div>

---

> [!IMPORTANT]
> This project was created with the help of Claude-Code. Is it, however, always reviewed, tested, and reworked with a human-in-the-loop.
>
> No AI slop here. Purely AI-made skills are hot garbage, and that's putting it mildly.
>
> That said, if you have any problems with code that is written by AI - you've been warned. But, then again, why would you be interested in AI-related configs and skills in the first place... `¯\_(ツ)_/¯`

## Why Agentstakk?

Tools like Claude Code and Codex are powerful on their own, but LLMs don't know your development workflow. This project started as a way for me to streamline claude configurations across all my projects without needing to copy-paste things. With time, patterns and re-curring prompts evolved into skills and agents. Currently, Agentstakk gives you two things:

**A minimal, opinionated Claude Code and Codex configuration** — sensible permission baselines, a rich statusline, MCP server wiring, and a machine-level installation that updates them across projects. Think of it as a dotfiles repo for Claude Code and Codex.

**A structured development pipeline** — 16 workflow and utility skills with explicit multi-language support that take you from idea through design, implementation, code review, testing, to documentation, with persistent knowledge that carries across sessions.

```
/kk:design → /kk:review-design → /kk:implement → /kk:review-code → /kk:test → /kk:document
```

Out of the box you get:

- **16 workflow and utility skills** — a complete development pipeline invoked as `/kk:<skill-name>`, plus utilities such as `/kk:clarify-docs` for improving existing documentation, PR drafts and issue descriptions, and explicit `/kk:handoff` publication of task context to a secret GitHub gist.
- **Multi-language support** — precise and distinct instructions from design, to implementation, to testing, to review for: go, java, js/ts, kotlin, kubernetes, and python
- **Multi-model code review** — independent reviewers using sub-agents and external models (Gemini, etc.)
- **Persistent knowledge base** — findings, decisions, and conventions that survive across sessions via Capy
- **Up-to-date library docs** — always-current documentation lookup via Context7
- **Battle-tested configuration** — permissions, statusline themes, hooks, sensible defaults

## Install kk

On macOS or Linux, install the latest stable release once per user account. Have Claude Code 2.1.295 or later, Bash, Git, `curl`, `jq` and Python 3.8+ on your `PATH`. Include Codex on your `PATH` if you use it.

```bash
curl -fsSL https://raw.githubusercontent.com/serpro69/agentstakk/master/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
kk status
```

For Codex, open plain `codex` in your project first, review folder trust and the three managed guard handlers in `/hooks`, then exit. Run `kk status --live` to check your installed guards. Start sessions with `kk claude` or `kk codex`. [Installation and updates](docs/getting-started/install.md) · [Plugin-only setup](docs/getting-started/plugin-only.md)

## Try It

After setup, try the core workflow:

For an optional conversation first, use `/kk:brainstorm` to think through a technical idea. It adapts the interview to your next decision and ends with a chat recap of decisions, rationale, and open assumptions. It creates no files or automatic handoff; request `/kk:design` when you want written planning.

1. **Write a plan.** Type `/kk:design` and describe a feature you want to build. Claude will ask refinement questions and confirm decisions, then produce design docs, an implementation plan, and a task list in `docs/feat/wip/`.

2. **Review the design.** Run `/kk:review-design your-feature` to catch gaps before writing code.

3. **Build it.** Type `/kk:implement` — Claude establishes the task's behavior and compatibility constraints, implements it, and supplies current evidence to independent review. Standalone fixes also work without design documents.

4. **Review the code.** `/kk:review-code` traces intended behavior, unchanged callers and affected compatibility contracts alongside SOLID, security and quality checks. Use `/kk:review-code:isolated` for independent review without the implementation conversation: an internal reviewer plus external review through PAL, using an API model when one is configured and otherwise your installed CLIs from other vendors (see [isolated reviews](docs/user-guide/skills.md#isolated-reviews-and-external-models)).

Reviews distinguish current regressions from inherited issues and code support
from deployment readiness. Missing evidence stays explicit; green tests support
the paths exercised. Verification is proportionate to the change, while explicit
repository and release checks remain required. See
[functional review and implementation](docs/user-guide/skills.md#functional-review-and-implementation)
for examples and limits.

This is the core loop. See the [Skills documentation](https://serpro69.github.io/agentstakk/latest/user-guide/skills/) for all available skills and the full workflow pipeline.

To clarify a bug report or feature request, use `/kk:clarify-docs issue-draft.md`
or supply an issue URL or pasted description with a local destination. The skill
preserves evidence limits and produces a local draft; it does not publish or
implement the issue. See [issue-description examples](docs/user-guide/skills.md#clarify-an-issue-description)
for output selection and audience rules. Clarification remains optional.

## Examples

Examples of actual Claude Code workflows executed using this template's configs, skills, and tools: [examples/](./examples)

## Contributing

Contributions are welcome! See the [Contributing guide](https://serpro69.github.io/agentstakk/latest/contributing/) for guidelines, [Architecture](https://serpro69.github.io/agentstakk/latest/contributing/architecture/) for how components fit together, and [Testing](https://serpro69.github.io/agentstakk/latest/contributing/testing/) for test conventions.

## License

Copyright &copy; 2025 - present, [serpro69](https://github.com/serpro69)

Distributed under the Apache License 2.0.

See [`LICENSE.md`](https://github.com/serpro69/agentstakk/blob/master/LICENSE.md) file for more information.
