Probe complete. All instruction content loaded successfully; no repository source, diff, or review findings were inspected or produced, and no reviewers were spawned.

## Hook-exported plugin root
`printenv TOOLBOX_PLUGIN_ROOT` →
```
/private/tmp/fr-task5-actors-x3akibin/binding7/plugins/kk
```

## Loaded locations

**Skill entry (via Skill tool)**
- `plugins/kk/skills/review-code/SKILL.md` (base dir: `.../plugins/kk/skills/review-code`)

**Isolated workflow**
- `plugins/kk/skills/review-code/review-isolated.md`

**Shared / common instructions** (all referenced by review-isolated.md Step 1, read from the skill dir)
- `plugins/kk/skills/review-code/shared-capy-knowledge-protocol.md`
- `plugins/kk/skills/review-code/shared-profile-detection.md`
- `plugins/kk/skills/review-code/shared-review-scope-protocol.md`
- `plugins/kk/skills/review-code/shared-change-context.md`
- `plugins/kk/skills/review-code/functional-review.md`
- `plugins/kk/skills/review-code/shared-pal-codereview-invocation.md`

**Agent definition (read from the hook-exported root)**
- `plugins/kk/agents/code-reviewer.md` — `name: code-reviewer`, `model: claude-opus-4-8[1m]`, tools: Read, Grep, Glob, `mcp__capy__capy_search`

## Notes on path consistency
- Root resolution is consistent: the skill base dir's parent-of-`skills/` equals the hook-exported `TOOLBOX_PLUGIN_ROOT`.
- **Cross-reference drift worth flagging:** several loaded files point at a `klaude-plugin/skills/_shared/...` layout that does not match the actual on-disk layout (shared files live flat in `skills/review-code/`, agent lives in `agents/`):
  - `agents/code-reviewer.md` §1 instructs reading `klaude-plugin/skills/_shared/change-context.md`, `.../_shared/review-scope-protocol.md`, `.../_shared/capy-knowledge-protocol.md`, and `klaude-plugin/skills/review-code/functional-review.md`.
  - `shared-review-scope-protocol.md` references `klaude-plugin/skills/_shared/review-scope-protocol.md`.
  - These are the `_shared/` naming of the same four common files that actually exist as `shared-*.md` under `skills/review-code/`. A dispatched sub-agent following those literal paths would fail its load gate unless it maps `_shared/<x>.md` → `skills/review-code/shared-<x>.md`.

Stopping here as instructed — no reviewers spawned.
