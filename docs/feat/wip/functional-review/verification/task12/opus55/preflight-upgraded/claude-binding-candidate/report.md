The instructions are loaded and I stopped before reviewing anything. I didn't read `cleanup.py` or any other subject file, didn't check the diff, didn't search capy, and didn't edit anything.

**SessionStart root:** `printenv TOOLBOX_PLUGIN_ROOT` returned `/tmp/fr-opus55-actors-20261011/claude-binding-candidate-upgraded/plugins/kk`. That matches the directory the skill loaded from, so the root is set correctly.

**What I read myself (all in full):**
- The skill entry point, `SKILL.md`, which loaded when I invoked `/kk:review-code`.
- `packet-preparation.md`, then `review-process.md`, `shared-capy-knowledge-protocol.md`, `shared-profile-detection.md`, `shared-review-scope-protocol.md`, `shared-change-context.md` and `functional-review.md`, all under `plugins/kk/skills/review-code/`.
- The detection file for each of the eight known profiles: `plugins/kk/profiles/{go,python,java,js_ts,kotlin,k8s,k8s-operator,skill-md}/DETECTION.md`.

**The preparation helper wrote outside the allowed area.** The skill's helper script (`scripts/prepare_instructions.py bootstrap`) ran and packaged those same 15 files. But it wrote the packaged copies to `/tmp/kk-review-instructions-hjqbdaln/part-01..06.md`, which is outside both the workspace and the plugin. Running it is what created that folder. I didn't read those files; I used the skill's direct-read fallback and read the original plugin files instead. The helper reported that the instruction-loading checkpoint was "NOT ESTABLISHED" because the packaged copies were never read. If your workflow expects those copies to be read, this is a mismatch to fix.

**The `kk:code-reviewer` agent** read only instructions and opened no subject files. It reported these paths, all read in full:
- **Required by its agent definition:** `plugins/kk/skills/_shared/change-context.md`, `plugins/kk/skills/review-code/functional-review.md`, `plugins/kk/skills/_shared/review-scope-protocol.md` and `plugins/kk/skills/_shared/capy-knowledge-protocol.md`.
- **Read because I asked:** `plugins/kk/skills/review-code/SKILL.md`. It isn't part of the agent's required set.
- **No profile checklists:** none were passed to it, so it loaded none.

**The agent and the skill point to different copies of three files.** Its definition points to the `skills/_shared/` versions, while the skill links to the `skills/review-code/shared-*.md` versions. So the agent and I read different files for change context, review scope and the capy protocol. I tried to compare the two sets, but the shell command was denied, so I don't know whether their contents match.

Steps 2 onward (choosing the diff, matching profiles, loading checklists and reviewing) were deliberately not run.
