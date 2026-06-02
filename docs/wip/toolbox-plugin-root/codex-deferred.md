# Codex `${TOOLBOX_PLUGIN_ROOT}` resolution — status & remaining work

Part of the `TOOLBOX_PLUGIN_ROOT` change (PR #132, branch `cpr`).

## Why this approach

Codex confirmed (via its own source — `codex-rs/.../skills/injection.rs`) that it does
**not** expand `${PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_ROOT}` inside `SKILL.md` or agent
markdown — those reach the model as literal text. Codex stores the skill's absolute path
(`path_to_skills_md`, pointing into `~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/`)
and instructs the model to resolve referenced paths **relative to the skill directory**.

So the Codex-native pattern is *relative paths from the skill dir* — exactly what the
generator's `plugin_root_resolve` transform produces (`replacement_base: "../.."`).
Renaming tokens to `${PLUGIN_ROOT}` was rejected: it would ship literal, unexpanded
tokens. `PLUGIN_ROOT` is only injected into **hook command** subprocesses, not prose.

## What is now done (this PR)

- `transforms.go` resolves both `${CLAUDE_PLUGIN_ROOT}` and `${TOOLBOX_PLUGIN_ROOT}` to
  `replacement_base`.
- `plugin_root_resolve` is now **`all_md`-scoped** (was `skill_md`), so aux/shared skill
  files (`review-*.md`, `idea-process.md`, `_shared/profile-detection.md`, …) resolve
  their plugin-root path refs to `../..`, not just `SKILL.md`.
- **Profile transforms decoupled** (`ProfilesConfig.Transforms`): profiles no longer get
  `plugin_root_resolve`, so `profiles/skill-md/*` keeps its *documentation* of the
  `${...PLUGIN_ROOT}` convention literal.
- Variable-**name** mentions in skill prose bare-formed (`$TOOLBOX_PLUGIN_ROOT`) or
  rephrased so the `all_md` resolve doesn't mangle them; true **path refs** stay brace.
- Guards in `test/test-plugin-structure.sh`: (a) no unresolved `${TOOLBOX_PLUGIN_ROOT}`
  brace literals in generated kodex skills; (b) **depth guard** — a brace plugin-root path
  ref below `skills/<name>/` or `skills/_shared/` fails the suite, because `../..` only
  points at the plugin root at exactly that depth.

## Known limitation

`replacement_base` is the fixed relative path `../..`. It is correct only for files two
levels under the plugin root (all current path-ref files qualify; the depth guard enforces
it). If a future deep aux file needs a plugin-root path ref, either relocate it or extend
the generator to compute a per-file relative base.

## Remaining — REQUIRES a live Codex session (PR's "test codex" item)

Static generation is correct on paper, but **no one has confirmed in a running Codex
session** that:

1. The model resolves `../../profiles/...` in a generated skill relative to the skill dir
   (cache path), not the project cwd.
2. Sub-agents (`.codex/agents/*.toml`) correctly use the injected `## Plugin Root` value /
   the `<kk-plugin-root>` preamble heuristic to open checklists.

Run the `/kk:review-code` flow + the eval harness under Codex and confirm profile/checklist
loads resolve before considering the Codex side closed.
