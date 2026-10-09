Probe complete. All instructions loaded; no repository source/diff inspected, no review findings produced, no reviewers spawned.

## Hook-exported root

`printenv TOOLBOX_PLUGIN_ROOT` →
```
/private/tmp/fr-task5-actors-x3akibin/binding4/plugins/kk
```

## Loaded locations

**Skill entry (via Skill tool)**
- `plugins/kk/skills/review-code/SKILL.md` — review-code skill body + base dir

**Isolated workflow**
- `plugins/kk/skills/review-code/review-isolated.md` — the `/kk:review-code:isolated` 10-step workflow

**Shared / common instructions** (all referenced by the isolated workflow's Step 1, read from the skill dir)
- `plugins/kk/skills/review-code/shared-capy-knowledge-protocol.md`
- `plugins/kk/skills/review-code/shared-profile-detection.md`
- `plugins/kk/skills/review-code/shared-review-scope-protocol.md`
- `plugins/kk/skills/review-code/shared-change-context.md`
- `plugins/kk/skills/review-code/functional-review.md`
- `plugins/kk/skills/review-code/shared-pal-codereview-invocation.md`

**Code-reviewer agent (from the hook-exported root)**
- `plugins/kk/agents/code-reviewer.md` — `name: code-reviewer`, `model: claude-opus-4-8[1m]`, tools: Read, Grep, Glob, mcp__capy__capy_search

## Notes on path resolution

- The skill's own base dir and the shared files resolve under `…/kk/skills/review-code/`, while the agent definition resolves under the hook root at `…/kk/agents/`. Both branches land under the same `TOOLBOX_PLUGIN_ROOT` (`…/binding4/plugins/kk`), confirming the skill-location-derived root (parent of `skills/`) matches the hook-exported value.
- One cross-reference discrepancy worth flagging: the loaded files use two different layouts for the shared instructions. The isolated workflow and SKILL.md reference them as flat siblings in `skills/review-code/` (e.g. `shared-change-context.md`), whereas `agents/code-reviewer.md` §1 and `shared-pal-codereview-invocation.md` reference a `skills/_shared/` layout (e.g. `klaude-plugin/skills/_shared/change-context.md`, `skills/_shared/review-scope-protocol.md`). The actual on-disk files that exist are the flat `shared-*.md` siblings I loaded; the `_shared/` paths are the agent-payload-relative form the spawning workflow is expected to expand to absolute paths before dispatch.

Stopping here as instructed — no reviewers spawned.
