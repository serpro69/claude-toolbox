# Testing

## Running Tests

Run all test suites:

Use the project tools on your normal PATH. The structure checks need Python 3.11+
(`tomllib`) or the documented `tomli` fallback; template suites need Mike Farah's
`yq` as well as `jq`. When selecting another Python installation, prepend its
directory instead of replacing PATH and hiding existing tools.

```bash
for test in test/test-*.sh; do $test; done
```

Run a single suite:

```bash
./test/test-plugin-structure.sh
```

## Test Suites

| Suite | What it covers |
|-------|----------------|
| `test-plugin-structure.sh` | Plugin/marketplace manifests, skills, commands, hooks, profiles, cross-references, kodex-plugin generated output validation |
| `test-codex-structure.sh` | Codex marketplace, config.toml, hooks.json, agent TOMLs, Starlark rules, scripts, AGENTS.md |
| `test-template-sync.sh` | CLI parsing, manifest validation, variable substitution, settings merge, plugin migration, sync exclusions, self-update handoff |
| `test-template-cleanup.sh` | Manifest generation, variable capture, git tag/SHA detection |
| `test-claude-extra.sh` | CLAUDE.extra.md headings, CLAUDE.md imports of behavioral and AGENTS.md project instructions, compare_files detection, auto-import |
| `test-manifest-jq.sh` | JSON generation patterns, special character handling, schema validation, round-trip |
| `test-semver-compare.sh` | Semver comparison logic used by release workflows |
| `test-cpr.sh` | Claude Plugin Root resolver — exact/fuzzy matching, project-path resolution cascade (project → user → last-installed), install-path validation, env var precedence, error handling |
| `test-hooks.sh` | Hook script validation (Bash denylist patterns, capy HTTP interception) |
| `test-codex-hooks.sh` | Codex hook scripts — `session-start.sh` and `pretooluse-bash.sh` with and without capy's own Codex hooks registered in `hooks.json` (legacy injection/denials, per-event handoff to capy, denylist and provider/extras preservation) |
| `test-review-eval-staging.sh` | Fresh before/after/history and legacy fixture staging, path safety and evaluator-material exclusion |
| `test-review-instructions.sh` | Instruction-packet source completeness, routing inputs and path boundaries; does not establish actor compliance |
| `test-functional-review-tools.sh` | Extracted bundle/capture/receipt/grading utilities and archive inventory; runs from a temporary copy without historical evidence, using Python 3.11+ |

## Test Infrastructure

Tests use shared utilities from `test/helpers.sh`:

- `log_section`, `log_test` — structured output
- `assert_equals`, `assert_contains`, `assert_file_exists` — assertion helpers
- `log_pass`, `log_fail`, `log_skip` — result reporting
- `print_summary` — final pass/fail count

Test fixtures live in `test/fixtures/`.
The [retained functional-review utilities](../../scripts/functional-review-evals/README.md)
own small synthetic fixtures within their tests. Set `FUNCTIONAL_REVIEW_PYTHON`
to an explicit Python 3.11+ interpreter when the default `python3` is older.
Codex hook cases derive from `toolbox-only-hooks.json`, so the legacy case stays
independent of Capy registrations in the developer's live `.codex/hooks.json`.

## Writing Tests

Follow [proportionate verification](https://github.com/serpro69/claude-toolbox/blob/master/klaude-plugin/skills/_shared/verification-policy.md)
when choosing coverage and acceptance criteria; [ADR 0010](../adr/0010-proportionate-verification.md)
records the rationale. Deterministic tests protect software contracts. Agent
evaluations measure semantic outcomes with variability and evidence limits;
each assertion is not automatically a release gate. Keep required repository
checks, and expand verification only for a concrete risk or unresolved decision.

- Add tests to the appropriate existing suite when possible
- New suites follow the same pattern: source `helpers.sh`, use `log_section`/`log_test`/`assert_*`, end with `print_summary`
- Structure tests check file existence and content invariants, not runtime behavior
- The bidirectional index invariant (every link in `index.md` resolves, every `.md` in a phase dir is referenced) is enforced in `test-plugin-structure.sh` — adding profile content automatically gets tested

## Go Tests

The Go tools under `cmd/` ship unit and integration tests:

```bash
go test ./cmd/generate-kodex/...   # Codex generation tool
go test ./cmd/plugin-graph/...     # plugin dependency-graph analyzer
```

`cmd/generate-kodex` tests also run as part of `make generate-kodex`.

`cmd/plugin-graph` tests run via `make plugin-graph`, which additionally runs
`go run ./cmd/plugin-graph --root klaude-plugin/ validate` against the real
plugin — a structural-health gate that exits non-zero on broken markdown/template
links or orphaned content. It complements `test-plugin-structure.sh`'s
bidirectional index invariant: the structure test enforces profile `index.md`
completeness, while `plugin-graph validate` catches broken links and orphans
across the whole plugin. See [Architecture › Plugin Graph Analysis](architecture.md).

## Validation Before Release

- Every `test/test-*.sh` suite must pass
- `make generate-kodex` must leave `kodex-plugin/` and `.codex/agents/` clean (`git diff --exit-code`)
- `make plugin-graph` must pass (Go tests + `validate` exits 0 against `klaude-plugin/`)
- Go tests must pass (`go test ./...`)

## Agent evaluation

Skill evals live under each canonical `klaude-plugin/skills/<skill>/evals/`
directory. A scenario contains `eval.json`, subject files under `test-files/`
and optional grader-only expected results under `oracle/`. Regenerate the Codex
copies with `make generate-kodex`.

The [review harness](https://github.com/serpro69/claude-toolbox/blob/master/klaude-plugin/skills/review-code/evals/_harness/HARNESS.md)
describes component grading and full-workflow capture. Its `setup.sh` stages flat
fixtures, complete `before/` and `after/` snapshots, and optional local Git history
into fresh destinations. Use a workspace outside any `SKILL.md` ancestor so the
host skill does not activate a profile on unrelated fixtures. Stage only subject
files; keep assertions, oracles, grading controls and results outside actor inputs
and filtered plugin bundles. Deliberately broken eval/template links must remain.

Run ordinary skill prompts against declared immutable instructions and fresh
fixture/knowledge state. For targeted changes, compare with the immediate
predecessor under matching conditions. Capture observable tool results,
reviewer handoffs, initial/final files and final reports; do not substitute private
reasoning or final self-attestation for execution. Never include credentials.
Workflow grading uses sealed evidence; component grading uses the supplied
output text. Calibrate the chosen grader against meaningful positive, negative
and missing-evidence examples before making comparative claims.

Keep PASS/FAIL/PARTIAL observations separate from adoption. A material wrong
verdict matters differently from optional advice, a missing endpoint name or an
unavailable external reviewer. Retain all attempts and disclose sample size,
runtime/configuration differences and missing coverage. Synthetic external-review
replays test reporting, not live integration. Expand measurement only for a
concrete uncertainty that could change the decision; structural tests do not
establish model reliability.

The [functional-review summary](https://github.com/serpro69/claude-toolbox/blob/master/docs/feat/wip/functional-review/verification-summary.md)
records the retained comparisons, current acceptance and known limits. Detailed
captures remain in the feature's evidence tree until the human-owned release
archive is verified.
