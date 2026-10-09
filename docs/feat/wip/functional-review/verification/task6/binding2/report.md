Probe complete. All requested instructions loaded; stopping before task/source investigation, edits, tests, or reviewer dispatch as instructed.

## What was loaded

**Skill entry point** — `plugins/kk/skills/implement/SKILL.md` (via `/kk:implement`). Establishes the mandatory ordering (instructions before action), two-mode selection, 5-step process, and Required Outputs.

**Both mode procedures:**
- `plan-mode.md` — triggered by a docs/feat/wip feature or task number; entry collects minimal task/file metadata only, records work under a task's **Execution context** in `tasks.md`.
- `standalone-mode.md` — bug fixes / issues / one-offs; entry collects request + candidate target filenames only, context stays conversational.

**Both shared files:**
- `shared-change-context.md` — the pre-edit factual record contract (Intent/authority, Change boundary, Existing behavior, Delivery constraints, Baselines, Scenarios/evidence) and producer/reviewer responsibilities.
- `shared-profile-detection.md` — single-source detection algorithm over the 8 known profiles (`go`, `python`, `java`, `js_ts`, `kotlin`, `k8s`, `k8s-operator`, `skill-md`); path→filename→content cost order, filename/content authority rule, ~16 KB content bound.

**Hook-exported root** — `printenv TOOLBOX_PLUGIN_ROOT` →
```
/private/tmp/fr-task6-controller-v7vbitoc/binding2/plugins/kk
```

**Code-reviewer agent definition** (from that same root) — `plugins/kk/agents/code-reviewer.md`. Independent reviewer, `model: claude-opus-4-8[1m]`, tools restricted to Read/Grep/Glob/`capy_search`; receives profiles pre-resolved by the parent, applies methodology-before-evidence ordering, and emits the P0–P3 findings contract.

No profile detection was run, no targets were investigated, and no reviewer was dispatched — those are the next phases, held per the probe's stop condition.
