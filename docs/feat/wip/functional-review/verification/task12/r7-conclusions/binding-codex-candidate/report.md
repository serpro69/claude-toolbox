I’m loading `kk:review-code` and its required methodology for this probe, then stopping before investigation. I’ll also ask the named `code-reviewer` role, with no inherited conversation, to load its instructions and report the paths it read.

The entry point and all six bootstrap packet parts are loaded, including the common methodology and eight profile detection rules. I’ve stopped before diff selection or subject-file inspection; the isolated `code-reviewer` is finishing its instruction-path report.

Probe complete. Loaded `kk:review-code` and all six bootstrap instruction parts. Spawned the named `code-reviewer` role with `fork_turns="none"`; it confirmed complete reads and stopped before investigation.

The reviewer reported these paths relative to the [selected plugin root](/home/sergio/.codex/plugins/cache/fr-r7-bf873de6-20261013/kk/0.23.0):

```text
skills/review-code/SKILL.md
skills/review-code/functional-review.md
skills/review-code/packet-preparation.md
skills/review-code/review-process.md
skills/review-code/review-isolated.md
skills/_shared/change-context.md
skills/_shared/review-scope-protocol.md
skills/_shared/capy-knowledge-protocol.md
skills/_shared/profile-detection.md
skills/_shared/pal-codereview-invocation.md
profiles/go/DETECTION.md
profiles/python/DETECTION.md
profiles/java/DETECTION.md
profiles/js_ts/DETECTION.md
profiles/kotlin/DETECTION.md
profiles/k8s/DETECTION.md
profiles/k8s-operator/DETECTION.md
profiles/skill-md/DETECTION.md
```

No subject files were inspected or modified. No review, findings, tests, or external searches occurred. Instruction packets were created only inside the workspace.
