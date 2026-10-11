The probe is done. I stopped after Step 1 (loading the instructions), before scope resolution and investigation. I didn't read or change any subject files: no `client.py`, no `tests/`, no diff. I ran no `capy_search`, did no PAL work and made no findings.

**SessionStart root:** `printenv TOOLBOX_PLUGIN_ROOT` returned `/tmp/fr-entry-path-no-pal-20261011/binding-candidate/plugins/kk`.

**What I loaded.** I read the files directly instead of running the packet helper (`prepare_instructions.py bootstrap`). The helper is the preferred path in `packet-preparation.md`, so this is a departure from the workflow. All reads succeeded, and all paths are under `plugins/kk/skills/review-code/`:
- Command entry: `kk:review-code:isolated`, delivered through the Skill tool.
- Entry point: `SKILL.md`.
- Workflow: `review-isolated.md`.
- Shared protocols and common method: `packet-preparation.md`, `shared-capy-knowledge-protocol.md`, `shared-profile-detection.md`, `shared-review-scope-protocol.md`, `shared-change-context.md`, `functional-review.md`, `shared-pal-codereview-invocation.md`.

**Not loaded, because they need scope resolution first:** the eight Known-profile `DETECTION.md` files, the profile indexes and the checklists. The helper's `bootstrap` output would have included the `DETECTION.md` files, so a real run needs to read those before Step 3.

**`kk:code-reviewer` agent.** I gave it the plugin root. It read 7 files, all inside the plugin root, with no failures:
1. `skills/_shared/change-context.md` (required by its agent definition)
2. `skills/review-code/functional-review.md` (agent definition)
3. `skills/_shared/review-scope-protocol.md` (agent definition)
4. `skills/_shared/capy-knowledge-protocol.md` (agent definition)
5. `skills/review-code/SKILL.md` (asked for by this probe)
6. `skills/review-code/shared-change-context.md` (linked from `functional-review.md`)
7. `skills/review-code/shared-review-scope-protocol.md` (linked from `functional-review.md`)

**Things worth checking:**
- **Path mismatch:** the agent definition writes paths as `klaude-plugin/...`, but the installed root is `plugins/kk`. The agent used the definition's own rule (put `skills/...` under the supplied root), and all four required paths resolved.
- **Duplicate files:** the agent's methodology comes from `skills/_shared/*`, while the parent workflow lists `skills/review-code/shared-*`. Files 6 and 7 have the same text as files 1 and 3, but it couldn't tell whether they're symlinks or copies. Nobody checked whether the two capy protocol files match. This matters for Step 5, which requires the same criteria paths in both reviewers' manifests.
- **Shared detection file references the wrong root:** `shared-profile-detection.md` says profiles live under `klaude-plugin/profiles/<name>/`. Reads would actually go through `${TOOLBOX_PLUGIN_ROOT}/profiles/`, so it works, but the wording doesn't match this install.
