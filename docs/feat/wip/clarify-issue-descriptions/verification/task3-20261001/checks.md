# Task 3 repository checks

Starting HEAD: `f516712109b59314e656a3e535e5a099110b28c9`, 2026-10-01.

The final operative procedure and complete candidate match byte-for-byte at
**1,297 words**, SHA256
`519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681`.
Each independently fits the unchanged **1,297-word ceiling**. There are no
mandatory procedure dependencies. The entry point/description remains unchanged:
616 words, 449 description characters, SHA256
`1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`.

The only operative change is the prepared 49-word missing-body/support/destination
paragraph. The pre-application record is in the
[budget decision](../budget/decision.md). Baseline editors for all five new cases
completed before application. No dependency, skill registration, description or
instruction dependency changes were needed. Existing entry-point safeguards
already cover immutable input captures and execution non-triggers.

All commands in [status.tsv](checks/status.tsv) exited **0**:

| Check | Evidence |
| --- | --- |
| Generation, including generator tests and both structure suites | [generate-kodex.txt](checks/generate-kodex.txt) |
| Graph tests and validation | [plugin-graph.txt](checks/plugin-graph.txt) |
| All Go packages | [go-test-all.txt](checks/go-test-all.txt) |
| Claude extras | [test-claude-extra.txt](checks/test-claude-extra.txt) |
| Codex structure | [test-codex-structure.txt](checks/test-codex-structure.txt) |
| Plugin-root resolver | [test-cpr.txt](checks/test-cpr.txt) |
| Hooks | [test-hooks.txt](checks/test-hooks.txt) |
| Manifest/schema | [test-manifest-jq.txt](checks/test-manifest-jq.txt) |
| Plugin structure | [test-plugin-structure.txt](checks/test-plugin-structure.txt) |
| Semver comparisons | [test-semver-compare.txt](checks/test-semver-compare.txt) |
| Template cleanup | [test-template-cleanup.txt](checks/test-template-cleanup.txt) |
| Template sync | [test-template-sync.txt](checks/test-template-sync.txt) |

All nine shell suites pass. The three network-dependent symbolic-ref cases
(`master`, `HEAD`, `latest`) **also pass** in this approved run; the earlier tasks'
skips do not apply here. Graph validation retains the existing cycle warning,
with no broken-edge/orphan failures. Intentionally partial eval links are untouched.

Generation idempotence passes: [before](checks/generated-before.json) and
[after](checks/generated-after.json) hashes are identical around the
[repeat generator](checks/generator-repeat.txt). The
[generated inspection](checks/generated-inspection.txt) verifies every changed
canonical/generated pair after the skill-prefix transform, both generated shared
copies, and unchanged agent definitions. New eval inputs are fixtures, not source
fixes; the Python examples retain their intentional missing feature/bug.

Static eval checks confirm 24 unique IDs, correctly numbered assertions, exact
new fixture manifests, valid JSON oracles outside `test-files/`, and parseable
Python fixtures without executing them. Checks use the already installed Python
3.12.11, a writable temporary Go cache, and command-local Git signing disablement
for temporary test repositories. Approved generation/cache access was used; no
dependency installation or global configuration change was required.

Structural checks do not establish editorial behavior. Behavioral evidence is
recorded separately by the independent editor/reader/grader sessions.
