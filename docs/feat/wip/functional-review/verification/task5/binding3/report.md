Probe complete. No repository source, diff, or review findings were inspected or produced, and no reviewers were spawned.

## Hook-exported root
`printenv TOOLBOX_PLUGIN_ROOT` → `/private/tmp/fr-task5-actors-x3akibin/binding3/plugins/kk`

## Loaded locations

**Skill entry (via `/kk:review-code`)**
- `…/plugins/kk/skills/review-code/SKILL.md`

**Isolated workflow**
- `…/plugins/kk/skills/review-code/review-isolated.md`

**Shared/common instructions referenced by the isolated workflow's Step 1** (all under `…/plugins/kk/skills/review-code/`)
- `shared-capy-knowledge-protocol.md`
- `shared-profile-detection.md`
- `shared-review-scope-protocol.md`
- `shared-change-context.md`
- `functional-review.md`
- `shared-pal-codereview-invocation.md`

**Code-reviewer agent definition (read from the hook-exported root)**
- `…/plugins/kk/agents/code-reviewer.md` — frontmatter: `name: code-reviewer`, `model: claude-opus-4-8[1m]`, tools `Read, Grep, Glob, mcp__capy__capy_search`

## Notes on path references inside the loaded instructions
- The isolated workflow resolves the plugin root as the **parent of `skills/`** — here `…/plugins/kk` — matching the hook-exported `TOOLBOX_PLUGIN_ROOT`.
- Several files use a `${TOOLBOX_PLUGIN_ROOT}/…` token and a `klaude-plugin/skills/_shared/…` convention for the shared files; in this installation those resolve to the concrete `…/plugins/kk/skills/review-code/shared-*.md` files listed above (the agent definition points sub-agents to read from the injected absolute `## Plugin Root`, since it has no shell).

Stopping here as instructed — no reviewers spawned.
