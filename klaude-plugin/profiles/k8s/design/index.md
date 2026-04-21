# Kubernetes — design artifacts

Consumed by the `design` skill when the `k8s` profile is active. `questions.md` seeds the idea-refinement question pool during Step 3 of `idea-process.md` (and during continue-WIP refinement in `existing-task-process.md`). `sections.md` lists required sections the design document must cover when Step 5 produces `design.md`.

Both files are always-loaded whenever the `k8s` profile activates — the K8s design rubric is not diff-conditional because the design phase has no diff to predicate on. Continue-WIP sessions apply the same rubric; a design that was authored before the profile rubric existed should be audited against `sections.md` on resumption.

## Always load

- [questions.md](questions.md) — question bank for idea refinement: cluster topology, GitOps and delivery, secrets strategy, multi-tenancy, observability, reliability and rollback.
- [sections.md](sections.md) — required sections for the design document: cluster-compat matrix, resource budget, reliability posture, security posture, failure-mode narrative.
