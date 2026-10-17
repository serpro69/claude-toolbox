I’m using `kk:review-code` for this instruction-loading probe. I’ll read its entry point and required methodology, and have an isolated `code-reviewer` report the instruction paths it reads. Both will stop before investigation.


The main-agent reads are complete: the entry point, common methodology, and all eight profile detection files from the selected installation. I used direct reads and stopped before diff selection. The isolated reviewer is finishing its instruction-path inventory.


Completed the instruction-loading probe and stopped before investigation. Spawned the named `code-reviewer` role with `fork_turns: "none"`.

The reviewer reported reading these paths relative to the selected plugin root, `/home/sergio/.codex/plugins/cache/fr-advisory-4b694214/kk/0.23.0`:

```text
skills/_shared/change-context.md
skills/_shared/review-scope-protocol.md
skills/_shared/capy-knowledge-protocol.md
skills/review-code/functional-review.md
skills/review-code/SKILL.md
skills/review-code/packet-preparation.md
skills/review-code/review-process.md
skills/review-code/shared-profile-detection.md
profiles/go/DETECTION.md
profiles/python/DETECTION.md
profiles/java/DETECTION.md
profiles/js_ts/DETECTION.md
profiles/kotlin/DETECTION.md
profiles/k8s/DETECTION.md
profiles/k8s-operator/DETECTION.md
profiles/skill-md/DETECTION.md
```

I also read the entry point and required common methodology directly. No subject files were inspected or modified, no review was performed, and all explicit file accesses stayed within the selected installation.
