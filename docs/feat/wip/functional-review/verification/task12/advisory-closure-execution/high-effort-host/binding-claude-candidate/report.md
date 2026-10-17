I loaded the `/kk:review-code` instructions and stopped before investigation. I didn't read, diff or search any subject files, and I made no edits.

**Plugin root check:** `printenv TOOLBOX_PLUGIN_ROOT` printed `/tmp/fr-advisory-high-effort-host-20261017/binding-claude-candidate/plugins/kk`. That matches where the skill actually loaded from (`plugins/kk/skills/review-code`).

**What I read directly**, all complete, all under `plugins/kk/skills/review-code/`:
- `SKILL.md` (the entry point, loaded by the skill call)
- `packet-preparation.md`
- `review-process.md`
- `shared-capy-knowledge-protocol.md`
- `shared-change-context.md`
- `functional-review.md`
- `shared-review-scope-protocol.md`
- `shared-profile-detection.md`

I didn't run the packet helper (`scripts/prepare_instructions.py bootstrap`), because you asked for exactly one shell command. Instead I used the skill's fallback of reading each file directly.

**What the `kk:code-reviewer` agent read** (5 files, all complete, no source or diff access, no findings):
1. `plugins/kk/skills/_shared/change-context.md` (required)
2. `plugins/kk/skills/review-code/functional-review.md` (required; the agent called this its core method)
3. `plugins/kk/skills/_shared/review-scope-protocol.md` (required)
4. `plugins/kk/skills/_shared/capy-knowledge-protocol.md` (required)
5. `plugins/kk/skills/review-code/SKILL.md` (the entry point you named)

Things to note from the agent run:
- **No separate SOLID file:** the agent says its definition has no SOLID methodology file. The SOLID, security, quality and removal guidance is written into the definition itself.
- **No `## Plugin Root` heading:** the agent definition expects the plugin root under that heading in the prompt. I didn't include it, so the agent used the absolute paths I gave it. A real isolated run should pass that heading.
- **Different shared file paths:** the agent loaded the shared protocols from `skills/_shared/*.md`, while the skill links to `skills/review-code/shared-*.md`. I didn't check whether they're the same files (copies or symlinks).

**Stopping point:** the next step would be step 2, picking the diff from `git status` and filenames. I haven't done it, and I haven't done any of the profile routing that comes after. That means I didn't read any of the 8 profile `DETECTION.md` files, so no checklists are loaded yet.
