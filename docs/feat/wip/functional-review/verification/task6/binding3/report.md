Probe complete. All requested instruction reads are loaded; I stopped before any task/source investigation, edits, tests, or reviewer dispatch — as instructed.

## Instruction-loading checkpoint

**Entry point**
- `skills/implement/SKILL.md` — loaded via the `/kk:implement` skill invocation.

**Hook-exported root (observed, not echoed)**
- `printenv TOOLBOX_PLUGIN_ROOT` → `/private/tmp/fr-task6-controller-ytou6pam/binding3/plugins/kk`

**Both mode procedures**
- `skills/implement/plan-mode.md` — plan-mode entry/iteration/completion.
- `skills/implement/standalone-mode.md` — standalone entry procedure.

**Shared protocols**
- `skills/implement/shared-change-context.md` — change-context contract.
- `skills/implement/shared-profile-detection.md` — profile-detection procedure (8 known profiles: `go`, `python`, `java`, `js_ts`, `kotlin`, `k8s`, `k8s-operator`, `skill-md`).

**Agent definition (from the same hook-exported root)**
- `plugins/kk/agents/code-reviewer.md` — resolved under `${TOOLBOX_PLUGIN_ROOT}/agents/`; model `claude-opus-4-8[1m]`, tools restricted to Read/Grep/Glob/`mcp__capy__capy_search`.

**Unread required instructions:** none for this probe's scope.

**Deliberately not entered** (per your stop condition): mode determination/selection as an actual run, profile detection execution, dependency handling, requirement/source investigation, change-context establishment, edits, `/kk:test`, and `/kk:review-code` reviewer dispatch. No capy knowledge-protocol file was read since it was outside the enumerated scope you gave.
