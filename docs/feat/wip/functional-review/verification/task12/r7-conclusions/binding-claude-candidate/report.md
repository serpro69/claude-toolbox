All the instructions loaded, and I stopped before any investigation. `payload.py`, `tests/test_payload.py` and the diff were never opened.

**Plugin root:** `printenv TOOLBOX_PLUGIN_ROOT` returned `/tmp/fr-r7-conclusions-20261013/binding-claude-candidate/plugins/kk`. That matches the root the preparation helper resolved.

**What I read myself:**
- **Entry point:** `skills/review-code/SKILL.md`, then `packet-preparation.md`.
- **Process:** `review-process.md`, the 11-step workflow.
- **Shared and method files:** `shared-capy-knowledge-protocol.md`, `shared-profile-detection.md`, `shared-review-scope-protocol.md`, `shared-change-context.md` and `functional-review.md`, all in `skills/review-code/`.
- **Detection rules:** the `DETECTION.md` file for each of the eight known profiles (go, python, java, js_ts, kotlin, k8s, k8s-operator, skill-md). I read them but didn't apply them, so no profiles were detected.

**What the code-reviewer agent read:** it confirmed it opened no subject files and found nothing missing.
- `skills/_shared/change-context.md`
- `skills/review-code/functional-review.md`
- `skills/_shared/review-scope-protocol.md`
- `skills/_shared/capy-knowledge-protocol.md`
- `skills/review-code/SKILL.md`

**Points to note:**
1. **Files written outside the workspace.** The `bootstrap` helper wrote its packets to `/tmp/kk-review-instructions-fym9sbja/`, which is outside both the workspace and the plugin. I didn't read them and used the skill's direct-read fallback instead, which loads the same files from the plugin. The helper's design always writes there, so a fully contained run would need a different temp location or the fallback from the start.
2. **Two copies of the shared files.** The agent definition names the `skills/_shared/` versions, while `SKILL.md` and I used the `shared-*.md` copies inside `skills/review-code/`. The main session and the agent may therefore be working from different text. I didn't compare the two sets because that wasn't part of this probe.
3. **Agent definition paths.** The agent definition refers to these files as `klaude-plugin/skills/...`. The agent mapped that to `skills/...` under the plugin root on its own.
