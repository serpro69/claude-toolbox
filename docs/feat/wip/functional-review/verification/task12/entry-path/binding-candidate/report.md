I loaded the instructions for the isolated code review and stopped before investigating anything. I did not open `client.py`, `tests/test_client.py`, any diff or git status, and I did not run detection or load any profile checklists.

**Plugin root:** `printenv TOOLBOX_PLUGIN_ROOT` returned `/tmp/fr-entry-path-20261011/binding-candidate/plugins/kk`. All the paths below are under it.

**What I read (Step 1, all reads succeeded):**
- Entry point: `skills/review-code/SKILL.md`
- Workflow: `skills/review-code/review-isolated.md`
- Loading procedure: `skills/review-code/packet-preparation.md`
- Shared protocols:
  - `skills/review-code/shared-capy-knowledge-protocol.md`
  - `skills/review-code/shared-profile-detection.md`
  - `skills/review-code/shared-review-scope-protocol.md`
  - `skills/review-code/shared-change-context.md`
  - `skills/review-code/shared-pal-codereview-invocation.md`
- Common method: `skills/review-code/functional-review.md`

I read these files directly instead of running the packaging script `prepare_instructions.py`. Later in the session Bash was blocked by "don't ask" mode, so the script couldn't be used either.

**What the `kk:code-reviewer` agent read** (it reported all five as successful, and it did not review anything):
1. `skills/_shared/change-context.md`
2. `skills/review-code/functional-review.md`
3. `skills/_shared/review-scope-protocol.md`
4. `skills/_shared/capy-knowledge-protocol.md`
5. `skills/review-code/SKILL.md`

It loaded no profile checklists because I didn't pass any.

**Two path issues to know about:**
- **The agent definition points at the wrong folder.** Its four required methodology paths start with `klaude-plugin/skills/...`, but this install lives under `plugins/kk/`. The agent found them only by remapping to `skills/...` under the root I gave it. `shared-profile-detection.md` has the same `klaude-plugin/profiles/` naming in its text, but its actual reads use `${TOOLBOX_PLUGIN_ROOT}`, so they resolve correctly.
- **The agent and I read the protocols from different files.** It used `skills/_shared/*`, while I used the `skills/review-code/shared-*` copies. Without Bash I couldn't compare hashes or check for symlinks. I read the three `_shared` files and they match the `review-code` copies line for line.

The next step would be Step 2 (working out which changes to review from filenames only). I didn't start it.
