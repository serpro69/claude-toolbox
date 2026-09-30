# Task 4 checks

Date: 2026-09-29. The operative change clarifies caller-only output links and adds
evaluation coverage; no dependency or skill description changed.

- `make generate-kodex`: PASS, including generator tests, 184 plugin-structure
  assertions and 29 Codex-structure assertions. The first sandbox attempt could
  not write `.codex/agents`; the authorized rerun succeeded. Logs preserve both.
- `make plugin-graph`: PASS, no broken edges or orphans. The existing cycle
  warning remains advisory; intentionally partial fixture links are unchanged.
- All nine shell suites ran: eight PASS. Schema tests initially hit the sandboxed
  uv cache; authorized reruns passed. Process-local Git signing was disabled for
  disposable test repositories. Python 3.12 was selected through a temporary PATH
  shim because the default Python lacks TOML support.
- `test/test-hooks.sh`: two pre-existing failures, unchanged from earlier tasks:
  `node_modules` and `.log` are expected to be denied but the hook omits them.
  The repository-maintainer follow-up in [verification.md](../../verification.md#follow-up-outside-task-1)
  still owns resolution. This is not a fully green repository suite.
- Shared instructions: initially 999 whitespace-delimited words; 1,000 after the
  PR-increment correction. No additional mandatory linked instructions. Dependency
  lookup is N/A.
- All 20 feature eval definitions (87 assertions) and 14 reader oracles parse;
  assertion IDs are sequential, every declared fixture resolves, each oracle has
  five questions, and all `baseline_defects` values are arrays.
  The runtime PR source's three resolver assertions pass; the source-disagreement
  example passes and prints `{'new_lookup': 20, 'old_order': 15}`. These source
  checks support the oracles; they do not substitute for editor/reader evaluations.
- `kustomize build` on the consumer fixture: PASS, empty resource output as
  intended. `kubeconform` is unavailable, so schema validation is skipped; install
  it with `brew install kubeconform` or
  `go install github.com/yannh/kubeconform/cmd/kubeconform@latest` to enable that
  check. No workload, Helm chart or policy-engine marker is introduced.

Final generation after the instruction and oracle corrections passes all generator and
structure checks. Repeated generation produces identical sorted generated-file
checksums: aggregate SHA-256
`e07856c30abd76d76654b7f22a72b4b594f54b78169ee08d49a706b1d66bc0b5`.
Final graph validation passes. The final full shell rerun again passes eight of
nine suites, with only the same two hook assertions failing.

Independent source review and behavioral grading are complete; see
[review.md](review.md) and the group run records. A direct check of 22 authored
reports resolves all 782 local links. Strict whitespace checks cover
authored source, fixtures and summary docs; immutable run evidence preserves its
runtime formatting, including terminal blank lines in consumed requests, so its
hashes and raw traces remain consistent. Task 5's release verification stays pending.

## Tooling follow-up outside Task 4

Owner: repository maintainer. A PreToolUse hook blocked a benign evaluation
request under `agent-instruction-target/` before the editor could read it, because
the path matched a denied `target/` substring. The blocked attempt is retained
under `local/agent-instruction-target/blocked-attempt-1/`; a fresh run uses a wholly
restaged fixture with a neutral directory name and identical subject bytes.
Hook policy is outside this editorial task. Next step: inspect the build-directory
deny matcher, constrain any unintended substring match to the intended path
component, and add a regression for a benign suffix such as this fixture directory
without weakening intended build-directory restrictions.
