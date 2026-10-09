Probe complete. No repository source, diff, or review findings were inspected, and no reviewers were spawned.

## Hook-exported plugin root

`printenv TOOLBOX_PLUGIN_ROOT` →
```
/private/tmp/fr-task5-actors-x3akibin/binding/plugins/kk
```

## Loaded locations

**Skill entry + isolated workflow** (base: `plugins/kk/skills/review-code/`)
| # | File | Role |
|---|------|------|
| 1 | `SKILL.md` | Skill entry (loaded via Skill invocation) |
| 2 | `review-isolated.md` | Isolated-mode workflow (7 steps) |

**Shared / common instructions** referenced by the isolated workflow's Step 1 — all present and read (base: same `skills/review-code/` dir, flat `shared-*` naming):
| # | File |
|---|------|
| 3 | `shared-capy-knowledge-protocol.md` |
| 4 | `shared-profile-detection.md` |
| 5 | `shared-review-scope-protocol.md` |
| 6 | `shared-change-context.md` |
| 7 | `functional-review.md` |
| 8 | `shared-pal-codereview-invocation.md` |

**Agent definition** (from the hook-exported root):
| # | File | Notes |
|---|------|-------|
| 9 | `plugins/kk/agents/code-reviewer.md` | `name: code-reviewer`, `model: claude-opus-4-8[1m]`, tools: Read/Grep/Glob/`mcp__capy__capy_search` |

Sibling agents also present in `plugins/kk/agents/`: `architecture-reviewer`, `design-reviewer`, `eval-grader`, `profile-resolver`, `spec-reviewer`.

## Observations worth flagging

1. **Path-scheme divergence (potential load hazard).** The isolated workflow and `SKILL.md` reference shared files by their actual on-disk names — flat, `shared-`-prefixed, co-located in `skills/review-code/`. But the **code-reviewer agent definition** (`code-reviewer.md:54`, `:26`) instructs the sub-agent to read `klaude-plugin/skills/_shared/change-context.md`, `skills/_shared/review-scope-protocol.md`, `skills/_shared/capy-knowledge-protocol.md`, etc. That `_shared/` subdirectory layout does **not** match what exists here. A spawned reviewer following its own definition literally would hit ENOENT on the methodology files — which, per its own Step 1 ("If any instruction read fails, stop and surface the error"), keeps the gate closed. The parent workflow mitigates this by expanding and injecting **absolute** checklist/instruction paths before dispatch (`review-isolated.md:59`, `:68`), so in practice the agent should receive resolved paths rather than relying on its hardcoded relatives.

2. **Root-token handling is consistent.** Both the workflow (`review-isolated.md:22`, `:59`) and the agent def (`code-reviewer.md:28`) agree the sub-agent has no shell and must use the injected `## Plugin Root` absolute path, never `${TOOLBOX_PLUGIN_ROOT}` — matching the hook-exported value above.

Stopping here as instructed — no reviewers spawned.
