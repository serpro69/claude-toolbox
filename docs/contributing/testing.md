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
| `test-guard.sh` | Python engine tests: glob/path semantics, shell parsing, configuration layers, patches, capy inputs and corpus replay |
| `test-hooks.sh` | Full guard wrapper transport, plugin-only protection, fail-closed cases, capy-wrapper degradation, Read/Bash p95 latency |
| `test-generate-guard.sh` | Generated settings/rules/docs, output stability, per-rule examples and invalid-marker rejection |
| `test-codex-hooks.sh` | Bash/patch/MCP adapter delegation, failure denial, protected-files advisory and per-event capy handoff |
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
The [retained functional-review utilities](https://github.com/serpro69/claude-toolbox/blob/master/scripts/functional-review-evals/README.md)
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
- `make generate-guard` must leave `.claude/settings.json`, `.codex/rules/`, `.codex/scripts/guard/` and `docs/user-guide/configuration.md` clean (`git diff --exit-code`)
- `make plugin-graph` must pass (Go tests + `validate` exits 0 against `klaude-plugin/`)
- Go tests must pass (`go test ./...`)

## Permission Guard Verification

Run the engine and wrapper separately when diagnosing a failure:

```bash
bash test/test-guard.sh
bash test/test-hooks.sh
bash test/test-codex-hooks.sh
bash test/test-generate-guard.sh
```

`test/guard/test_guard.py` imports the engine and replays `test/fixtures/guard/corpus.jsonl`. Rows carry expected decisions/categories, optional cwd/project roots and per-row configuration fixtures. They use a synthetic home and project; submitted commands are never executed. `KK_GUARD_TEST_PYTHON` selects the engine test interpreter. The Python floor is 3.8, with actual local runs on 3.9.6/macOS and 3.10.12/Linux; the 3.8 syntax check does not replace a 3.8 runtime run.

The wrapper suite times 100 Read calls and every active Bash corpus row, including process startup, validation and cleanup. It always reports both p95 values when the timing probes run. Targets are 30 ms for file tools and 50 ms for Bash; local gates fail at 60/100 ms respectively when `CI` is unset. With `CI` present, timing is reported without enforcement. A CI-mode pass is not evidence that a local latency target passed.

The 2026-10-26 macOS arm64 run with the default Apple Python 3.9.6 measured **76.62 ms Read / 76.00 ms Bash** outside the agent sandbox: the Read gate failed and both targets were missed. The performance requirement remains open before feature completion; limits were not relaxed. See the [permission-guard evidence](https://github.com/serpro69/claude-toolbox/blob/master/docs/feat/wip/permission-guard/design.md#16-assumptions) for all attempts and prerequisites.

A later wrapper optimization on the same host prefers an existing Homebrew Python, skips unused site startup and avoids subprocesses for empty output. That run measured **40.92 ms Read / 42.13 ms Bash**, passing both unchanged local gates and the Bash target. A second pass imports the engine through a small launcher so Python can reuse compiled bytecode: the unchanged benchmark measured **37.27 → 31.10 ms Read / 42.50 → 34.75 ms Bash** against its immediate predecessor. The 30 ms Read target remains open. Earlier measurements remain historical evidence.

Launcher tests cover policy reloads between calls, unavailable caches, import isolation, source updates and loader failures. Cold starts and unwritable cache directories compile source. Apple Python 3.9.6 disables cache writes by default; its functional tests pass, with the corrupt-cache test explicitly skipped. The speedup was measured with Homebrew Python 3.15.1 and does not establish timing on other runtimes or hosts.

Payload tests establish adapter contracts, not installed hook activation. Live probes must record versions, actual hook inputs/results and benign controls. The Claude bypass probe uses a disposable project outside temporary roots so `rm -rf ./scratch` is not intentionally exempt. Use synthetic files and an absent `.env`, never real credentials. The recorded Claude 2.1.296 probe denied both destructive and secrets access under bypass mode. The Codex 0.164.0 probe verified relative patch paths against cwd with explicit inline hooks; ordinary project-hook discovery was not established and still needs a visible startup/patch-hook check.

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
