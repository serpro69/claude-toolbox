# Task 1 loading verification

This page records Task 1. For the subsequent frozen fixtures, captured baselines
and remaining Codex handoff gate, see [Task 2 verification](task2/README.md).

Task 1 loading checks are **complete**. Both providers loaded the selected
filtered baseline in separate baseline/candidate-probe locations. Named reviewer
children read the selected instructions and retrieved their run-local Capy marker.
These are launch probes; no measured behavioral baseline or candidate has run.

## Captured evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Immutable baseline and filtered bundles | PASS: 1,271 source files; 836 excluded; 435 retained (Claude 223, Codex 206, generated agents 6) | [Identity](evidence/baseline/identity.json), [source manifest](evidence/baseline/source-manifest.json), [exclusions](evidence/baseline/exclusions.json), [retained manifest](evidence/baseline/retained-manifest.json) |
| Candidate loading location | Prepared with a second identical baseline copy; no behavioral candidate | Same archive/retained hashes; separate controller snapshot and actor directories |
| Fresh knowledge stores | PASS: A and B start empty, index/search work, foreign markers absent, vault unavailable | [Summary](evidence/state-probe/summary.json), [A events](evidence/state-probe/state-a.json), [B events](evidence/state-probe/state-b.json) |
| Claude entry points, hook root and named child | PASS in both locations after login refresh: registered skill invocation, supporting/implement instruction reads, kk:code-reviewer dispatch and child read/search results | [Baseline](evidence/claude-refreshed-baseline.json), [candidate location](evidence/claude-refreshed-candidate.json) |
| Codex installed caches and project agents | PASS: each cache has the expected 206 files; each project has the expected six agent definitions | Verification commands below |
| Codex effective skill catalog | PASS after trust and explicit peer disablement; initial mixed attempt retained as invalid | [Trusted catalogs](evidence/codex-catalog-trusted.json), [invalid attempt](evidence/codex-catalog-untrusted.json) |
| Codex registered skill reads | PASS in both loading locations; actual tool outputs contain selected SKILL.md, review-process.md, shared-profile-detection.md and project role TOML | [Baseline events](evidence/codex-baseline.json), [candidate-location events](evidence/codex-candidate.json) |
| Instantiated Codex role | PASS in both locations: persisted parent/child records expose named-role dispatch, parent linkage, effective model/effort, exact public role bytes, child instruction reads and marker retrieval | [Baseline](evidence/codex-persist-baseline.json), [candidate location](evidence/codex-persist-candidate.json) |
| Final workspace/config identity | PASS: all four worktrees clean, identical initial README hash, explicit per-run Capy paths; post-run bundle/cache and six-role manifests match | [Runner configs](evidence/completed-run-configs.json), [post-run scan results](evidence/completed-manifest-checks.json) |
| Launch and cleanup record | Exact completed prompts/options retained; probe-owned trust, caches and marketplaces removed | [Launches](evidence/completed-launches.json), [cleanup](evidence/completed-cleanup.json) |

The bundles contain no retained evaluator paths or escaping/dangling links. This
is a path-based packaging scan, not a claim that actors cannot read arbitrary
host files. No measured evaluation has run. The successful loading probes are
bounded checks; earlier authentication failures, the initial mixed catalog and
the incomplete ephemeral child trace do not count as passes. Captured source
reads accessed selected instructions and project role files; no grading-material
read appears. One Codex parent listed sibling filenames while locating project
instructions; it read no sibling file contents. No OS-wide read confinement is
claimed. Controller/oracle paths were absent from actor catalogs and prompts.

## Reproduce packaging and state checks

Run from the toolbox root with Python 3.9+ and installed Git/Capy. Allocate fresh
controller and actor directories under `/private/tmp` with `mktemp -d`; use
task-specific variables `fr_controller` and `fr_actors`. Do not reuse workspaces.
For example, after setting those variables:

```bash
python3 -B docs/feat/wip/functional-review/verification/prepare-bundles.py build . c2d28c9e3064a0a71a0e5ac3748a9616c794eb61 "$fr_controller/baseline"
python3 -B docs/feat/wip/functional-review/verification/prepare-bundles.py build . c2d28c9e3064a0a71a0e5ac3748a9616c794eb61 "$fr_controller/candidate-probe"
python3 -B docs/feat/wip/functional-review/verification/probe_state.py "$fr_actors" "$fr_controller/state-probe"
python3 -B -m unittest discover -s docs/feat/wip/functional-review/verification -p 'test_controller.py' -v
```

`prepare-runtime.py PROVIDER SNAPSHOT WORKSPACE MARKETPLACE` prepares a fresh
Git workspace, filtered plugin copy, local Capy config and provider metadata.
Use `claude` or `codex`; snapshot is the controller's baseline/candidate-probe
directory. Marketplace names must distinguish revision and side. Pass repeated
`--disable-plugin kk@OTHER-MARKETPLACE` for every other visible kk installation
(the normal `kk@claude-toolbox` is disabled by default). Preparation
does not establish trust, install a plugin, authenticate, or launch a model.
Never expose the controller snapshot or this verification directory to an actor.

The first state attempt found a local Git template without `.git/info`; the
helper now creates it explicitly. The second attempt expected a no-results
response, but Capy 0.16.7 returns an explicit empty-store tool error. The check
now verifies that exact empty-store response. The third attempt passed in new
workspaces. No failed workspace was reused.

## Actual 2026-10-08 locations and launch settings

- Controller: `/private/tmp/functional-review-controller-pQrivtyX` (source
  archives, original manifests and logs). These temporary copies may disappear;
  repository manifests and the immutable Git commit permit exact reconstruction.
- Actor parent: `/private/tmp/functional-review-actors-Mp4My8ao`.
- Passed final state probes: `final-state/state-a` and `final-state/state-b`
  beneath that parent; rerun after the independent review's Git-isolation fixes.
- Prepared runtime workspaces: `claude-baseline`, `claude-candidate-probe`,
  `codex-baseline`, `codex-candidate-probe` beneath that parent.
- Codex baseline marketplace: `fr-c2d28c9e-baseline`.
- Installed baseline copy:
  `/Users/sergio/.codex/plugins/cache/fr-c2d28c9e-baseline/kk/0.23.0`.
  `prepare-bundles.py verify CACHE CONTROLLER/baseline/retained-manifest.json kodex-plugin`
  returned PASS, 206 files. The candidate-probe cache passed the same check.
  Both project `.codex/agents` copies passed, six definitions each, against the
  `.codex/agents` manifest. The original `claude-toolbox` cache was not modified.
  Initial probe caches/registrations and both temporary trust tables were removed
  after capture; the paths describe the captured run, not a surviving installation.

Claude local loader arguments were `-p --model 'claude-opus-4-8[1m]' --effort high
--plugin-dir ./plugins/kk --setting-sources project,local --settings
.runner/settings.json --mcp-config .runner/mcp.json --strict-mcp-config
--no-session-persistence --permission-mode dontAsk --output-format stream-json
--verbose --include-hook-events`, plus a controller debug destination. Allowed
tools were Read/Glob/Grep/Skill, selected read-only Bash commands (`pwd`,
`printenv TOOLBOX_PLUGIN_ROOT`, `capy *`) and Capy search. The prompt requested
catalog identity, registered /kk:review-code entry loading, reads of
review-process.md/shared-profile-detection.md, and the hook root; it explicitly
stopped before review analysis. These are **loading-probe restrictions**, not
the full tool policy for measured implementation/review runs.

Environment removed CAPY_VAULT_KEY/CAPY_DB_KEY/CLAUDECODE, supplied the synthetic
database key, private CAPY_VAULT_PATH and XDG_CONFIG_HOME, and a run-specific
CPR_PLUGINS_FILE. CLAUDE_CONFIG_DIR pointed to `.runner/claude-config`, which
isolated personal skills/settings but had no login. No credentials were copied.
Catalog, hook and MCP initialization succeeded before authentication failed.
After explicit user approval, a fresh `claude-approved-baseline` workspace used
the existing login without CLAUDE_CONFIG_DIR. Debug evidence loaded zero personal
skills and only the filtered kk plugin. Authentication then failed with
“OAuth session expired and could not be refreshed”; no instruction-reading model
turn ran. `claude-approved-candidate` was prepared but not launched after this
provider-wide failure. Both failed attempts remain recorded in
[the initial loader trace](evidence/claude-loader.json) and
[the expired-login trace](evidence/claude-approved-baseline.json).

Codex used `plugin marketplace add`, then `plugin add`, for the unique filtered
baseline. The local `app-server --stdio` was queried through `initialize` and
`skills/list` with the probe cwd and forceReload. CLI overrides disabling the
ordinary kk and setting project trust did not yield an isolated effective
catalog. After user approval, temporary project trust was applied with
`config/value/write`; project TOML disabled the ordinary kk and peer probe
installation. Trusted `skills/list` responses contained only the selected kk.
CLI `-c` quoted dotted keys had produced literal quote characters in plugin IDs;
real project TOML avoided that erroneous override. No incorrect override was
persisted in the user configuration.

Both Codex probes then ran `codex --no-daemon exec --ephemeral --json -m
gpt-6-astra -c model_reasoning_effort=xhigh` with an identical prompt requesting
the registered /kk:review-code entry point, its two supporting files, and the
project code-reviewer definition; they stopped before analysis or edits. Actual
read outputs are retained. A supplementary role probe asked for a fresh
code-reviewer child, but the CLI stream exposed only a wait event without a
receiver ID and a final confirmation. That is insufficient dispatch evidence.
The main skill-read probes and supplementary role probe are separate checks;
no claim of a fresh behavioral-evaluation repetition is made for the latter.

An initial Codex model-run approval rejection cited private-data transmission.
Read-only GitHub checks then established that `serpro69/claude-toolbox` is public
and the exact baseline commit is published. The retry was approved using that
evidence; only byte-verified public instructions and synthetic context were
sent. This did not bypass a rejection or change the task's acceptance rules.

## Completed probes after login refresh

The user refreshed login on 2026-10-08. Fresh workspaces were prepared at
`claude-refreshed-baseline`, `claude-refreshed-candidate`,
`codex-persist-baseline` and `codex-persist-candidate` under the same actor parent.
All use unchanged c2d28c9e bytes. Codex marketplaces are
`fr-c2d28c9e-role-baseline` and `fr-c2d28c9e-role-candidate`; each project disables
the normal kk installation and the other probe. Both temporary projects were
trusted using the existing user authorization.
The [final host catalogs](evidence/codex-persist-catalog.json) each contain only
the selected kk installation.

Claude used the same arguments/environment above, with refreshed authentication,
`--forward-subagent-text` added, and permission for registered-agent dispatch and
Capy index/search. The exact identical prompt is retained in both new evidence
files. It requests registered /kk:review-code loading, supporting files,
/kk:implement entry/plan reads, the hook root, a synthetic Capy marker, and a
kk:code-reviewer child that reads/searches only those inputs. Both runs completed
without permission denials. Host catalogs selected only the filtered kk plugin;
the child tool events identify their actual parent Agent call.

Codex used the same main model and effort but **omitted `--ephemeral`** so the
runtime persisted parent and child records. Both prompts requested the registered
/kk:review-code entry, shared detection file, a Capy marker, and a named
code-reviewer child that reads/searches those inputs. The selected plugin was
derived from the registered catalog. The raw records establish:

- `spawn_agent` used `agent_type: code-reviewer` with `fork_turns: none`.
- Child session metadata names its parent thread, role and matching workspace.
- Child model/effort is `gpt-6.1-sol` / `xhigh`.
- Child developer-message ordinal 2, content block 1 contains the exact public
  `developer_instructions` parsed from that project's generated TOML. The
  extracted body hashes to `0920c4453e6ade733f6e29e0d7fab68290b2cf2f494106616612e59ce5ee2e01`
  on both sides. Only that public substring is retained, not other system text.
- Child calls read the selected cache's shared instruction and search the
  run-local Capy source; returned tool content contains `ambercapybara`.

Codex encrypts the parent dispatch's message field in persisted history. The
original ciphertext is retained alongside structural dispatch metadata; the
record does **not** claim a plaintext handoff capture. Task 1 binding is supported
by emitted role bytes and actual child calls/results. For later assertions about
exact handoff content, the controller must capture plaintext at submission or
through another supported trace surface; ciphertext alone cannot pass them.
Task 2/8 capture must preserve this distinction without weakening assertions.

All new trace exports omit private reasoning. Raw source-file hashes, event
ordinals, parent edges and public instruction outputs preserve provenance.
Post-run scans still match both 223-file Claude bundles, both 206-file Codex
caches and both six-definition agent directories. No probe workspace or knowledge
store may seed a measured run. Both temporary trust tables, plugins/caches and
marketplace registrations were removed after final checks; the normal plugin
configuration remains. [Cleanup responses](evidence/completed-cleanup.json)
record the scoped removals.

## Next task

Task 2 owns final seed fixtures, hashes, ordinary prompts and measured baseline
capture. Task 8 owns the concrete workflow grader. Candidate and grader identities
remain pending in the run contract until those artifacts exist. No acceptance
threshold or provider selection changed in resolving the loading gates.

## Verification

- Eight offline controller tests passed, including export attributes and
  inherited Git configuration/hook rejection.
- All nine existing `test/test-*.sh` suites passed, 626 assertions, with three
  existing template-sync skips. Initial manifest/cleanup runs failed because
  sandboxed `uv` cache writes and globally configured commit signing were
  unavailable. Reruns allowed cache access and set per-process Git
  `commit.gpgsign=false` for disposable fixtures; both passed. Global Git
  configuration was unchanged.
- Trailing-whitespace, blank-EOF and space-before-tab checks passed for staged
  and unstaged changes. Bare `git diff --cached --check` also enabled the user's
  global `indent-with-non-tab` rule and flagged normal Python/JSON space
  indentation. Verification used a per-command whitespace setting consistent
  with those formats; no global Git configuration or file indentation changed.
  No operative plugin file changed, so generation is not required for this
  controller-only slice.
- Independent /kk:review-code review approved the controller fixes; see
  [review record](review.md), including PAL's unverified source-coverage limit.
