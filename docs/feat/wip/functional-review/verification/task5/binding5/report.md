Probe complete. All instruction-loading targets were read; no repository source, diff, or findings were touched, and no reviewers were spawned.

## Hook-exported root

`printenv TOOLBOX_PLUGIN_ROOT` →

```
/private/tmp/fr-task5-actors-x3akibin/binding5/plugins/kk
```

## Skill entry (loaded via Skill tool)

- `…/kk/skills/review-code/SKILL.md` — `/kk:review-code`, base dir `…/plugins/kk/skills/review-code`

## Isolated workflow

- `…/kk/skills/review-code/review-isolated.md` — the 10-step isolated-mode workflow (referenced from SKILL.md §Review Modes → Isolated Mode)

## Shared / common instructions (per isolated workflow Step 1)

All resolved under `…/kk/skills/review-code/`:

- `shared-capy-knowledge-protocol.md`
- `shared-profile-detection.md`
- `shared-review-scope-protocol.md`
- `shared-change-context.md`
- `functional-review.md` (common functional method)
- `shared-pal-codereview-invocation.md` (Reviewer B / PAL branch)

## Code-reviewer agent definition (from exported root)

- `…/kk/agents/code-reviewer.md` — `subagent_type: kk:code-reviewer`, `model: claude-opus-4-8[1m]`, tools: Read, Grep, Glob, `mcp__capy__capy_search`

## Notes observed during load (not acted on)

- The agent definition and shared protocols reference some paths under a `klaude-plugin/skills/_shared/…` layout (e.g. `_shared/change-context.md`, `_shared/review-scope-protocol.md`), whereas the actual on-disk skill files are flat under `skills/review-code/` with `shared-*` prefixes. I did **not** resolve or chase those `_shared/` references — flagging the naming divergence only.
- Co-located agents in the same `agents/` dir: `architecture-reviewer.md`, `design-reviewer.md`, `eval-grader.md`, `profile-resolver.md`, `spec-reviewer.md` (not loaded).

Stopping here — no profile detection, no diff/source reads, no reviewer sub-agents spawned.
