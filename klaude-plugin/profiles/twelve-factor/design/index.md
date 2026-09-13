# 12-Factor App — design artifacts

Consumed by the `/kk:design` skill when the `twelve-factor` profile is active. Both files are always-loaded (the design phase has no diff to predicate on). Both carry co-activation rules so overlapping factors are asked and documented once when a domain profile such as `k8s` is also active.

## Always load

- [questions.md](questions.md) — refinement-question pool, one cluster per design-relevant factor: config, backing services, build/release/run, statelessness, concurrency, disposability, dev/prod parity, admin processes, port binding and logs, codebase/dependencies. Opens with the skip-if-already-answered and defer-to-domain-profile rules.
- [sections.md](sections.md) — four grouped required sections for the design document (config & backing services; process model & concurrency; release & disposability; parity & observability) plus the codebase/dependencies preamble, the omit-none / justify-N/A rule, and the co-active merge / cross-reference rule.
