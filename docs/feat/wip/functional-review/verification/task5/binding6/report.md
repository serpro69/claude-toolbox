Probe complete. All instruction files for the isolated `/kk:review-code` workflow loaded, plus the `code-reviewer` agent definition. No repository source/diff was inspected and no reviewers were spawned.

## Hook-exported plugin root

`printenv TOOLBOX_PLUGIN_ROOT` →
```
/private/tmp/fr-task5-actors-x3akibin/binding6/plugins/kk
```
This is the actual hook-exported root. Skill base dir is its child: `…/plugins/kk/skills/review-code`.

## Loaded locations

**Skill entry**
- `plugins/kk/skills/review-code/SKILL.md` (loaded via Skill invocation)

**Isolated workflow**
- `plugins/kk/skills/review-code/review-isolated.md`

**Shared / common instructions** (the full Step 1 load set referenced by the isolated workflow, all resolved under the skill base dir):
- `plugins/kk/skills/review-code/shared-capy-knowledge-protocol.md`
- `plugins/kk/skills/review-code/shared-profile-detection.md`
- `plugins/kk/skills/review-code/shared-review-scope-protocol.md`
- `plugins/kk/skills/review-code/shared-change-context.md`
- `plugins/kk/skills/review-code/functional-review.md`
- `plugins/kk/skills/review-code/shared-pal-codereview-invocation.md`

**Agent definition (read from the hook-exported root)**
- `plugins/kk/agents/code-reviewer.md` — frontmatter `name: code-reviewer`, `model: claude-opus-4-8[1m]`, tools: Read, Grep, Glob, `mcp__capy__capy_search`

## Notes on path-resolution consistency

One wrinkle worth flagging: the instruction files reference the plugin tree under **two different naming conventions**, which could cause load failures if followed literally:

- Hook-exported root and actual on-disk layout use `plugins/kk/…` with flat `skills/review-code/shared-*.md` files.
- `review-isolated.md` and `shared-profile-detection.md` reference files via `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/…` and `profiles/<profile>/review-code/index.md` (not yet read — routing-only, out of scope for this probe).
- `code-reviewer.md` (the agent) instead references `klaude-plugin/skills/_shared/change-context.md`, `klaude-plugin/skills/review-code/functional-review.md`, `klaude-plugin/skills/_shared/review-scope-protocol.md`, `klaude-plugin/skills/_shared/capy-knowledge-protocol.md` — a `klaude-plugin/` prefix and a `_shared/` subdir that do **not** exist at the resolved root (actual files are flat `shared-*.md` under `skills/review-code/`). The agent would need to map these legacy `_shared/…` references onto the actual `plugins/kk/skills/review-code/shared-*.md` files.

Stopping here as instructed — no reviewers spawned, no profile checklists loaded, no diff/source read.
