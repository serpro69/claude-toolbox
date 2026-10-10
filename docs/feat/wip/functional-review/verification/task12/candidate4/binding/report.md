Probe complete. All four steps executed; no subject files were reviewed or modified.

## Probe results

**1. `/kk:review-code` invoked** — skill instructions loaded (entry point: `skills/review-code/SKILL.md`).

**2. SessionStart root** (`printenv TOOLBOX_PLUGIN_ROOT`):
```
/tmp/fr-task12-c4-binding/plugins/kk
```

**3. Entry point + required shared/methodology instructions read (main session):**
```
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/SKILL.md                          (entry point)
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/shared-capy-knowledge-protocol.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/shared-change-context.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/functional-review.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/shared-review-scope-protocol.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/shared-profile-detection.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/review-process.md
```

**4. `kk:code-reviewer` agent** (restricted to its required methodology + the plugin SKILL.md, no subject-file review) reported these instruction paths:
```
/tmp/fr-task12-c4-binding/plugins/kk/skills/_shared/change-context.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/functional-review.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/_shared/review-scope-protocol.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/_shared/capy-knowledge-protocol.md
/tmp/fr-task12-c4-binding/plugins/kk/skills/review-code/SKILL.md
```

## Binding observation worth noting

The two entry points resolve the **shared protocols from different directories**:

- **Main-session SKILL.md** links them as siblings inside `skills/review-code/` (e.g. `shared-change-context.md`, `shared-review-scope-protocol.md`, `shared-capy-knowledge-protocol.md`) — and those files exist and read successfully there.
- **The `kk:code-reviewer` agent** resolved its methodology from `skills/_shared/` (`change-context.md`, `review-scope-protocol.md`, `capy-knowledge-protocol.md`).

So the same logical protocols appear to be bound via two path conventions (`review-code/shared-*.md` vs `_shared/*.md`). Both resolved without error in this run, but it's a divergence in how the skill vs. the agent locate the shared instruction set — relevant if these are meant to be a single source of truth.

Stopped here as instructed: no diff investigation, no findings, no edits.
