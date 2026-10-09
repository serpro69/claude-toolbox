Probe complete. All requested instruction files loaded; stopping before task/source investigation, edits, tests, or reviewer dispatch as instructed.

## Instruction-loading probe report

### Files read (entry point + both modes + two shared protocols)
| File | Status |
|---|---|
| `skills/implement/SKILL.md` (entry point) | ✅ loaded via Skill |
| `skills/implement/plan-mode.md` | ✅ loaded |
| `skills/implement/standalone-mode.md` | ✅ loaded |
| `skills/implement/shared-change-context.md` | ✅ loaded |
| `skills/implement/shared-profile-detection.md` | ✅ loaded |

### Resolved `TOOLBOX_PLUGIN_ROOT`
```
/private/tmp/fr-task6-controller-v7vbitoc/binding/plugins/kk
```
**Resolution method:** The canonical path (shell `echo $TOOLBOX_PLUGIN_ROOT`) was **denied** — Bash is blocked in this environment's don't-ask mode. I resolved it structurally instead, which the detection procedure permits: the root is the directory whose children match the `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/` and `${TOOLBOX_PLUGIN_ROOT}/agents/` layout. Both `plugins/kk/profiles/*/DETECTION.md` and `plugins/kk/agents/*.md` sit directly under `plugins/kk`, confirming the root.

One consistency note worth flagging: `shared-profile-detection.md` line 6 refers to profiles as `klaude-plugin/profiles/<name>/`, while the algorithm body (lines 33, 61–64) and the SKILL use `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/`. On disk the real location is `plugins/kk/profiles/` — so `${TOOLBOX_PLUGIN_ROOT}` = `…/plugins/kk`, and the `klaude-plugin/` literal in line 6 is a stale/illustrative label, not the actual directory name. No `CLAUDE.md` exists in the tree to cross-check `§Profile Conventions`.

Also present on disk but **not** in the detection procedure's §Known profiles enumeration: `profiles/twelve-factor/` (the authoritative list names `go, python, java, js_ts, kotlin, k8s, k8s-operator, skill-md`). Per the procedure, profile discovery uses the explicit list only, so `twelve-factor` would not be detected regardless.

### code-reviewer agent definition (read from the same root)
`…/plugins/kk/agents/code-reviewer.md` — ✅ loaded. Key facts:
- **model:** `claude-opus-4-8[1m]`; **tools:** `Read, Grep, Glob, mcp__capy__capy_search` (no shell, no Git).
- Independent/no-authorship reviewer; receives plugin root under a `## Plugin Root` heading (cannot resolve env vars itself) and reads `skills/_shared/change-context.md`, `skills/review-code/functional-review.md`, `skills/_shared/review-scope-protocol.md`, `skills/_shared/capy-knowledge-protocol.md` beneath it.
- Does **not** re-detect profiles — consumes `(profile, checklist, triggered_by)` records from the parent. Enforces methodology-before-evidence ordering and the P0–P3 output contract.

**Stopped here** — no task selection, requirement/source reading, profile *content* loading, edits, tests, or reviewer dispatch performed.
