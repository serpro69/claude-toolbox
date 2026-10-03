# Try It

After setup, try the core workflow:

For an optional conversation first, use `/kk:brainstorm` to explore a technical idea or decision. The interview adapts to what you need to decide and ends with a chat-only recap of decisions, rationale, and open assumptions. It creates no files and does not start another workflow automatically. Request `/kk:design` when you want written planning.

1. **Write a plan.** Type `/kk:design` and describe a feature you want to build. Claude will ask refinement questions and confirm decisions, then produce design docs, an implementation plan, and a task list in `docs/feat/wip/`.

2. **Review the design.** Run `/kk:review-design your-feature` to catch gaps before writing code.

3. **Build it.** Type `/kk:implement` — Claude executes the task list with code review checkpoints between batches.

4. **Review the code.** `/kk:review-code` checks for SOLID violations, security risks, and quality issues. Use `/kk:review-code:isolated` for independent sub-agent reviewers with zero authorship bias.

This is the core loop. See the [kk plugin README](https://github.com/serpro69/claude-toolbox/tree/master/klaude-plugin) for all available skills and the full workflow pipeline.

## What Just Happened?

The planning and implementation loop passes artifacts between skills. Optional brainstorming supplies conversation context:

| Skill | Input | Output |
|-------|-------|--------|
| `/kk:brainstorm` (optional) | A technical idea or decision | Chat recap; no files |
| `/kk:design` | Your idea, optionally with a brainstorm recap | `design.md`, `implementation.md`, `tasks.md` |
| `/kk:review-design` | Design docs | Review findings, gap analysis |
| `/kk:implement` | Task list | Code changes, review checkpoints |
| `/kk:review-code` | Git diff | Findings, fix suggestions |
| `/kk:test` | Code changes | Test files, coverage report |
| `/kk:document` | All of the above | Updated `architecture.md`, ADRs |

## Next Steps

- [Skills](../user-guide/skills.md) — learn what each skill does in detail
- [Profiles](../user-guide/profiles.md) — understand language-specific behavior
- [Configuration](../user-guide/configuration.md) — customize for your workflow
