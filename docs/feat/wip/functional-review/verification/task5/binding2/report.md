Probe complete. All instruction content loaded; no repository source or diff was inspected, and no reviewers were spawned.

## Hook-exported plugin root

`printenv TOOLBOX_PLUGIN_ROOT` →
```
/private/tmp/fr-task5-actors-x3akibin/binding2/plugins/kk
```

## Loaded locations

**Skill entry point** (via `/kk:review-code`)
- `plugins/kk/skills/review-code/SKILL.md`

**Isolated workflow**
- `plugins/kk/skills/review-code/review-isolated.md`

**Shared / common instructions referenced by the isolated workflow (Step 1)**
- `plugins/kk/skills/review-code/shared-capy-knowledge-protocol.md`
- `plugins/kk/skills/review-code/shared-profile-detection.md`
- `plugins/kk/skills/review-code/shared-review-scope-protocol.md`
- `plugins/kk/skills/review-code/shared-change-context.md`
- `plugins/kk/skills/review-code/functional-review.md`
- `plugins/kk/skills/review-code/shared-pal-codereview-invocation.md`

**Code-reviewer agent definition** (read from the hook-exported root)
- `plugins/kk/agents/code-reviewer.md` — frontmatter: `name: code-reviewer`, `model: claude-opus-4-8[1m]`, tools `Read, Grep, Glob, mcp__capy__capy_search`

## Notes on path-resolution observations

- The isolated workflow and the agent definition reference checklists/protocols under a `klaude-plugin/skills/_shared/...` and `${TOOLBOX_PLUGIN_ROOT}/profiles/...` naming convention, but the **actual on-disk layout** is flat files under `skills/review-code/` (e.g. `shared-change-context.md` rather than `_shared/change-context.md`). The resolved hook root (`.../plugins/kk`) is the correct base; the `_shared/` path tokens in the prose are legacy/logical references, not literal paths in this install.
- The agent definition expects the plugin root injected under a `## Plugin Root` heading (it has no shell and cannot resolve `TOOLBOX_PLUGIN_ROOT` itself).
- Sibling agent definitions also present under the root: `architecture-reviewer.md`, `design-reviewer.md`, `eval-grader.md`, `profile-resolver.md`, `spec-reviewer.md`.

Stopping here as instructed — no reviewers spawned, no findings produced.
