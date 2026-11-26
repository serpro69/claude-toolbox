---
description: Migrate this project from Task Master MCP to native markdown-based task tracking.
---

Migrate this project from Task Master MCP to native markdown-based task tracking.

## Pre-flight checks

Before doing anything, verify that Task Master artifacts actually exist in this project. If none of the following exist, inform the user that there's nothing to migrate and stop:

- `.taskmaster/` directory
- `.claude/commands/tm/` directory
- `.claude/agents/task-orchestrator.md`, `.claude/agents/task-executor.md`, or `.claude/agents/task-checker.md`
- `task-master-ai` entries in `.claude/settings.json` (allow or deny lists)
- Task Master sections in `CLAUDE.md` (look for "Task Master" headings or `@./.taskmaster/CLAUDE.md`)

## Step 1: Port pending tasks

Use the Task Master MCP tool `mcp__task-master-ai__get_tasks` with `status: "pending"` and `withSubtasks: true` to fetch all pending tasks. If the MCP server is not connected, fall back to reading `.taskmaster/tasks/tasks.json` directly.

Also check for tasks in other non-terminal statuses (`in-progress`, `blocked`, `deferred`, `review`) by calling `get_tasks` without a status filter and filtering out `done` and `cancelled`.

For each feature/group with pending tasks:

1. Create `/docs/feat/wip/[feature]/tasks.md` following the format in `../../skills/design/example-tasks.md`
2. Map Task Master statuses: `pending` → `pending`, `in-progress` → `in-progress`, `blocked` → `blocked`, `deferred` → `blocked` (note the reason), `review` → `in-progress`
3. Preserve task descriptions, subtasks, dependencies, and any implementation notes
4. Skip tasks with status `done` or `cancelled`
5. Show the user what was ported and ask for confirmation before proceeding

If all tasks are `done`, inform the user and proceed to Step 2.

## Step 2: Clean up Task Master files

Remove the following files and directories. List what you're about to delete and confirm with the user first:

- `.taskmaster/` directory (entire tree)
- `.claude/commands/tm/` directory (entire tree)
- `.claude/TM_COMMANDS_GUIDE.md`
- `.claude/agents/task-orchestrator.md`
- `.claude/agents/task-executor.md`
- `.claude/agents/task-checker.md`

## Step 3: Update settings.json

Remove from `.claude/settings.json`:

- **Allow list:** all `mcp__task-master-ai__*` entries
- **Deny list:** `Bash(task-master:*)` entry

## Step 4: Update CLAUDE.md

Remove from `CLAUDE.md`:

- Any "Task Master" sections (architecture references, integration guide, slash command docs)
- The `@./.taskmaster/CLAUDE.md` import line and surrounding section
- File management rules referencing `tasks.json` or `config.json`
- References to Task Master commands in context management

Do NOT remove sections about Serena, Claude Code, skills, or other non-TM content.

## Step 5: Update template-state.json

If `.github/template-state.json` exists, remove these variables from the `variables` object:

- `TM_CUSTOM_SYSTEM_PROMPT`
- `TM_APPEND_SYSTEM_PROMPT`
- `TM_PERMISSION_MODE`

## Step 6: Update legacy sync clients

Skip this step when the project has no `.github/template-state.json`. For a project that still uses template sync, update its client before the next sync so old Task Master settings do not return. Use the `upstream_repo` from its manifest and the last full template tag, `v0.26.0-rc.4`. Fetch `.github/workflows/template-sync.yml`, `.claude/toolbox/scripts/template-sync.sh`, and its sibling `semver-compare.sh` from that same tag into a temporary directory. Fetch all three successfully before replacing the corresponding project files, preserve exclusions, and keep the scripts executable. If a fork lacks that tag, report the missing source and leave the client intact.

## Step 7: Update MCP config

Remind the user to manually remove the `task-master-ai` entry from their `~/.claude.json` `mcpServers` config (we cannot modify user-level config).

## Step 8: Summary

Show a summary of what was done:

- Number of tasks ported (if any) and where they were saved
- Files and directories removed
- Config files updated
- Manual action needed (MCP config in ~/.claude.json)

Suggest the user run `/clear` after migration to reset context, since the permission config has changed.
