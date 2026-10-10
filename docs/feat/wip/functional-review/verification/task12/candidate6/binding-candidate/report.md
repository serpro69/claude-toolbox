Probe complete. Here is the instruction-loading inventory.

## 1. Entry point + required instructions (main session)

**Entry point:** `kk:review-code` → `skills/review-code/SKILL.md` (loaded).

Loaded via the `packet-preparation.md` bootstrap sequence (helper ran, all 6 packet parts read in full through their `END PACKET PART` markers). Sources packaged, all bound under `skills/review-code/`:

| Instruction | Source path |
|---|---|
| Packet preparation | `skills/review-code/packet-preparation.md` |
| Process | `skills/review-code/review-process.md` |
| Capy knowledge protocol | `skills/review-code/shared-capy-knowledge-protocol.md` |
| Profile detection | `skills/review-code/shared-profile-detection.md` |
| Review-scope protocol | `skills/review-code/shared-review-scope-protocol.md` |
| Change context | `skills/review-code/shared-change-context.md` |
| Functional review (common method) | `skills/review-code/functional-review.md` |
| 8 Known-profile DETECTION.md | `profiles/{go,python,java,js_ts,kotlin,k8s,k8s-operator,skill-md}/DETECTION.md` |

Stopped here, before investigation — no diff selected, no profile routing against subject files, no subject review.

## 2. SessionStart root

`printenv TOOLBOX_PLUGIN_ROOT` → `/tmp/fr-task12-c6-binding-candidate-20261010/plugins/kk`

## 3. `kk:code-reviewer` agent — its required methodology + SKILL.md

The agent (read-only, given the plugin root, told not to touch subject files) reported reading:

- `…/plugins/kk/skills/_shared/change-context.md`
- `…/plugins/kk/skills/review-code/functional-review.md`
- `…/plugins/kk/skills/_shared/review-scope-protocol.md`
- `…/plugins/kk/skills/_shared/capy-knowledge-protocol.md`
- `…/plugins/kk/skills/review-code/SKILL.md`

## 4. Binding divergence worth flagging

The two entry points resolve the **same three shared protocols to different files**:

- **Main-session path** (SKILL.md / packet-preparation) binds them under `skills/review-code/` with `shared-` prefixes — e.g. `shared-change-context.md`, `shared-review-scope-protocol.md`, `shared-capy-knowledge-protocol.md`.
- **Agent path** (code-reviewer.md) binds them under `skills/_shared/` without the prefix — e.g. `_shared/change-context.md`, `_shared/review-scope-protocol.md`, `_shared/capy-knowledge-protocol.md`.

So there appear to be two parallel copies of change-context, review-scope, and capy-knowledge (the common functional-review method and SKILL.md are the shared, single-location files). The agent treated its `_shared/` copies as canonical and the `shared-*` names as "packet-resolver aliases." I did not verify byte-equivalence of the two copies — that would require reading instruction files beyond this probe's scope. If these two trees can drift, the main session and the code-reviewer subagent could be reviewing under different methodology text.

No subject files were read or modified; all access stayed within the workspace/plugin.
