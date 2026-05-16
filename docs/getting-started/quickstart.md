# Try It

Run the full pipeline in under 5 minutes. Assumes you've installed the plugin ([Plugin-Only](plugin-only.md) or [Template Setup](template-setup.md)).

## 1. Design a Feature

```
/kk:design "add a health check endpoint"
```

This creates design docs, an implementation plan, and a task list in `docs/wip/`.

## 2. Implement It

```
/kk:implement "work on task 1"
```

Executes the first task with automatic code review checkpoints between batches.

## 3. Review the Code

```
/kk:review-code
```

Reviews your changes for SOLID violations, security risks, and code quality issues. Language-aware — automatically detects Go, Python, TypeScript, etc.

## 4. Test and Document

```
/kk:test
/kk:document
```

Generates tests following project conventions, then updates architecture docs and records any ADRs.

## What Just Happened?

Each skill produced artifacts the next one consumed:

| Skill | Input | Output |
|-------|-------|--------|
| `/design` | Your idea | `design.md`, `tasks.md` |
| `/implement` | Task list | Code changes, review checkpoints |
| `/review-code` | Git diff | Findings, fix suggestions |
| `/test` | Code changes | Test files, coverage report |
| `/document` | All of the above | Updated `ARCHITECTURE.md`, ADRs |

## Next Steps

- [Skills](../user-guide/skills.md) — learn what each skill does in detail
- [Profiles](../user-guide/profiles.md) — understand language-specific behavior
- [Configuration](../user-guide/configuration.md) — customize for your workflow
