I loaded the `/kk:review-code` instructions and stopped before investigation. No subject files were opened, nothing was changed, and I didn't run git status, diff selection or `capy_search`.

**`printenv TOOLBOX_PLUGIN_ROOT`** returned `/tmp/fr-advisory-actors-20261017/binding-claude-candidate/plugins/kk`. That matches the plugin root the helper reported.

**Instructions I read** (directly from the plugin):
- Entry point: `skills/review-code/SKILL.md` and `packet-preparation.md`
- Process and shared/common method: `review-process.md`, `shared-capy-knowledge-protocol.md`, `shared-profile-detection.md`, `shared-review-scope-protocol.md`, `shared-change-context.md`, `functional-review.md`
- Detection rules for all eight Known profiles: `profiles/{go,python,java,js_ts,kotlin,k8s,k8s-operator,skill-md}/DETECTION.md`. All reads succeeded.

**Deviation from the normal flow:** I ran the helper (`prepare_instructions.py bootstrap`), but it writes its packet files to `/tmp/kk-review-instructions-c413ove4/`. That's outside both the workspace and the plugin. So I didn't read those files and used the skill's documented direct-read fallback instead. The source list and hashes the helper reported match the files I read. The packet directory is still on disk, created by the helper. The preparation gate is closed: no diff selected, no profiles detected, no checklists loaded.

**`kk:code-reviewer` agent:** it read only instruction files, opened no subject files, ran no searches and produced no findings. It listed these paths:
- **Required by its agent definition:**
  - `skills/_shared/change-context.md`
  - `skills/review-code/functional-review.md`
  - `skills/_shared/review-scope-protocol.md`
  - `skills/_shared/capy-knowledge-protocol.md`
- **Entry point:** `skills/review-code/SKILL.md`
- **Could not read:** none.

The agent read from `skills/_shared/`, and I read the `review-code/shared-*.md` names. Those names are symlinks to the `_shared/` files, and the SHA-256 hashes match, so we both loaded the same text.

The `cd` in that hash check moved the shell's working directory to `plugins/kk/skills`. Nothing else changed.
