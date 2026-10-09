## Instruction-binding probe — result

### TOOLBOX_PLUGIN_ROOT (hook-exported)

I could **not read the live value**. The hook (`plugins/kk/hooks/hooks.json` → `scripts/set-plugin-root.sh`) exports it only by appending `export TOOLBOX_PLUGIN_ROOT="…"` to `$CLAUDE_ENV_FILE` at `SessionStart`. Reading that back requires a shell, and **Bash is denied here (don't-ask mode)**; `$CLAUDE_ENV_FILE` is also not discoverable via file-search tools, and no `installed_plugins.json` exists in the tree for me to resolve it statically.

**Resolved value (derived, high confidence):** `cpr.py` finds no `installed_plugins.json`, so the hook falls back to `$1 = ${CLAUDE_PLUGIN_ROOT}`. From the skill's own loaded location (parent of `skills/`), that is:

```
TOOLBOX_PLUGIN_ROOT=/private/tmp/functional-review-task4-actors-_xy7589w/binding/plugins/kk
```

### Selected plugin — paths read

Plugin root: `/private/tmp/functional-review-task4-actors-_xy7589w/binding/plugins/kk`

Skill base: `…/plugins/kk/skills/review-code`

Instructions loaded (entry point + requested files + their instruction dependency):

- `…/skills/review-code/SKILL.md` — entry point (via Skill)
- `…/skills/review-code/review-process.md`
- `…/skills/review-code/shared-change-context.md`
- `…/skills/review-code/functional-review.md`
- `…/skills/review-code/shared-review-scope-protocol.md` — dependency named by `functional-review.md`

Per scope, I did **not** read the other shared protocols referenced by `SKILL.md` (`shared-capy-knowledge-protocol.md`, `shared-profile-detection.md`), did not inspect any source files or diff contents, and produced no findings.

Stopping here as instructed.
