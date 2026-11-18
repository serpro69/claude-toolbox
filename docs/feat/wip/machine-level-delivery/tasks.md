# Tasks: Machine-level delivery

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-11-18
> Not Doing: orchestrator features, Go binary or package-manager distribution, built-in unattended upgrades, full parity for IDE/desktop/cloud/CI sessions, merging into user-owned config (migration excepted), general shell-read grants, detection of open Codex sessions, `kk uninstall`, native Windows, per-repository teammate stub, changes to capy's setup, system-level deny fragment (future)

## Task 1: Codex vendor probes
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Slicing:** Risk-First — the central promise and four source-read claims are unprobed
- **Can run in parallel with:** Task 2, Task 5, Task 8
- **Docs:** [implementation.md#codex-vendor-probes](./implementation.md#codex-vendor-probes), [design.md#assumptions](./design.md#assumptions)

### Subtasks
- [ ] 1.1 Build a scratch local marketplace with a skills-only plugin and a guard-like plugin whose `PreToolUse` hook denies a marker command and logs every call; install into a scratch `CODEX_HOME` (the maintainer supplies credentials) → verify: a marker command is denied and logged
- [ ] 1.2 In a tmux-driven open TUI session, re-add only the skills plugin at a new version and send a marker command → verify: the hook log shows a new denial (assumption 1)
- [ ] 1.3 Re-add the unchanged guard plugin, then the guard plugin at a new version with a changed script, each with a session open → verify: record whether the cache directory is replaced and which outcome the open session shows (assumption 2)
- [ ] 1.4 Probe trust scope across two repositories, the hook's launch directory against the payload directory, and a Git-URL marketplace source → verify: results recorded for assumptions 3, 4 and 10
- [ ] 1.5 Find how to read hook trust from outside a session (app-server `hooks/list`, then persisted hook state) → verify: the request and response are recorded, or the absence of a usable mechanism is
- [ ] 1.6 Probe profile precedence against user and trusted project config with every baseline key, user-level sub-agents, and an MCP-tool matcher from a plugin hook → verify: results recorded for assumptions 5 and 6
- [ ] 1.7 Write the results to `verification/task-1/` with tool versions, and update `design.md` Assumptions and any section a result contradicts

## Task 2: Claude vendor probes
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Slicing:** Risk-First — activation depends on in-place loading from a local marketplace
- **Can run in parallel with:** Task 1, Task 5, Task 8
- **Docs:** [implementation.md#claude-vendor-probes](./implementation.md#claude-vendor-probes)

### Subtasks
- [ ] 2.1 With the maintainer's agreement, add a uniquely named local-path marketplace whose plugin entry points at a versioned subdirectory; install at user scope → verify: a plugin hook reports its script path and plugin root inside that subdirectory (assumption 8)
- [ ] 2.2 Re-point the marketplace entry at a second subdirectory with a session open → verify: the open session keeps the first, a new session uses the second
- [ ] 2.3 In an untrusted scratch directory pass a settings layer with a deny rule and a statusline; in a trusted project set a project-enabled plugin ID to `false` in the layer → verify: the read is denied with hooks disabled, the statusline renders, the plugin does not load (assumption 9)
- [ ] 2.4 Optional: route the VS Code extension through a wrapper that adds a settings layer → verify: record whether the layer applies
- [ ] 2.5 Remove the scratch marketplace and plugin; write results to `verification/task-2/` and update `design.md`

## Task 3: First install for Claude
- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7, Task 8
- **Docs:** [implementation.md#kk-foundation](./implementation.md#kk-foundation), [design.md#upgrade-flow](./design.md#upgrade-flow)

### Subtasks
- [ ] 3.1 Create `kk/bin/kk` (entry point: resolve the toolbox home, read the active release, run its CLI under isolated Python) and `kk/payload.json` (layout version and required directories)
- [ ] 3.2 Create the state module in `kk/lib/`: per-tool state, candidate phase, atomic writes → verify: a failed rename leaves the previous state file intact
- [ ] 3.3 Create the payload module: fetch from a tag archive or a local checkout, extract only payload directories, reject absolute paths, parent traversal and escaping symlinks → verify: crafted archives are rejected; the plugin's relative symlinks survive
- [ ] 3.4 Create `kk/selftest/guard-cases.json` and the validation module: payload completeness, guard self-test against the candidate engine, `claude plugin validate` → verify: a candidate with a broken engine fails and the state file is unchanged
- [ ] 3.5 Create Claude activation: write the local marketplace manifest, add the marketplace, install the plugin at user scope, verify the load path through `claude plugin list --json`
- [ ] 3.6 Add `kk upgrade` for the first-install path, `kk status`, and `install.sh` at the repository root
- [ ] 3.7 Add `test/kk/` and `test/test-kk.sh` with stub vendor CLIs covering first install and failed validation → verify: the suite passes under isolated Python 3.8 syntax checks

## Task 4: Upgrade, rollback and recovery for Claude
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7, Task 8
- **Docs:** [implementation.md#kk-foundation](./implementation.md#kk-foundation), [design.md#rollback-and-interrupted-upgrades](./design.md#rollback-and-interrupted-upgrades)

### Subtasks
- [ ] 4.1 Implement the hand-off: fetch, staging and validation from the active release's code; activation and verification from the candidate's; rollback, status and resumption from the last ready release
- [ ] 4.2 Journal the candidate's phase before each activation step and implement resumption of an interrupted upgrade
- [ ] 4.3 Implement `kk rollback` and pruning of releases that are neither active, previous, nor activated in the last 14 days
- [ ] 4.4 Extend the stub-based suite: upgrade, interruption at each activation step followed by resume and by rollback, pruning → verify: after every interruption case `kk status` reports the mixed state and both ways out work

## Task 5: Claude plugin instructions, statusline and plugin root
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 7, Task 8
- **Docs:** [implementation.md#claude-plugin-changes](./implementation.md#claude-plugin-changes), [design.md#plugins](./design.md#plugins)

### Subtasks
- [ ] 5.1 Create `klaude-plugin/instructions/behavior.md` from `.claude/CLAUDE.extra.md`; make the latter a generated copy with a freshness check → verify: `test/test-claude-extra.sh` passes and the copy is byte-identical
- [ ] 5.2 Move the plugin-root override text from `.claude/toolbox/CLAUDE.md` into a plugin instruction file used only for plugin-only installs
- [ ] 5.3 Add a `SessionStart` hook script and its registration in `klaude-plugin/hooks/hooks.json` for start, resume, clear and compaction; skip behavioural instructions when the project has `.claude/CLAUDE.extra.md`; honour the override file's switch → verify: `test/test-hooks.sh` covers both the legacy-file and the clean-project fixture
- [ ] 5.4 Move the statusline scripts to `klaude-plugin/statusline/`; keep the `.claude/toolbox/scripts/` copies identical until retirement
- [ ] 5.5 In `klaude-plugin/scripts/set-plugin-root.sh`, use the script's parent directory when it sits under the toolbox home's `releases/` → verify: `test/test-cpr.sh` passes with a new case for that branch
- [ ] 5.6 Run `make generate-kodex` and `test/test-plugin-structure.sh`

## Task 6: Claude launch layer and overrides
- **Status:** pending
- **Depends on:** Task 3, Task 5
- **Size:** M
- **Can run in parallel with:** Task 7, Task 8, Task 9
- **Docs:** [implementation.md#claude-launch-layer](./implementation.md#claude-launch-layer), [design.md#launching-claude](./design.md#launching-claude)

### Subtasks
- [ ] 6.1 Create `kk/baseline/claude.json` from the current `.claude/settings.json` values: preferences, statusline path, default allow entries, opt-in catalogue
- [ ] 6.2 Add `kk/baseline/claude/deny.json` as a target in `scripts/generate-guard.sh` and in every freshness list
- [ ] 6.3 Implement layer composition: yield per key and per environment variable to the user, project and local settings; always include denies; add default allows; disable the Git-marketplace plugin ID only where it is enabled
- [ ] 6.4 Implement the override file: schema, named settings file, default switches, opt-in grants; a malformed file stops the launch with a message
- [ ] 6.5 Implement `kk claude` with `--print-layer` and the pass-through when the adopter supplies `--settings`
- [ ] 6.6 Unit tests for yielding, list composition, each override, pass-through and a malformed override → verify: on a real machine a wrapped session uses the baseline model when none is set and the user's model when one is

## Task 7: Codex guard plugin with workspace anchoring
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 3, Task 4, Task 5, Task 6, Task 8
- **Docs:** [implementation.md#codex-guard-plugin](./implementation.md#codex-guard-plugin), [design.md#guard-changes](./design.md#guard-changes)

### Subtasks
- [ ] 7.1 Create `kodex-guard/` with a manifest named `kk-guard`, `hooks/hooks.json` with the matchers from `.codex/hooks.json`, and the three adapters ported from `.codex/scripts/`
- [ ] 7.2 Anchor policy to the hook's launch directory (git top level, else the directory); use the payload directory for operands only; read the capy registration from the workspace
- [ ] 7.3 Add the engine copy `kodex-guard/scripts/guard/` and `kk/baseline/codex/kk.rules` as targets in `scripts/generate-guard.sh`; update the Makefile, `generated-check.yml`, `release.yml`, `test/test-generate-guard.sh` and the generated-files text in `AGENTS.md`
- [ ] 7.4 Add a `kk-guard` entry to `.agents/plugins/marketplace.json`
- [ ] 7.5 Port the adapter cases in `test/test-codex-hooks.sh` to the new adapters and add cross-repository anchoring cases; update `test/test-codex-structure.sh` → verify: a live run from a subdirectory enforces a rule from the workspace's `.claude/kk-guard.json`

## Task 8: Protect toolbox-owned paths in the guard
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 7
- **Docs:** [implementation.md#codex-guard-plugin](./implementation.md#codex-guard-plugin), [design.md#guard-changes](./design.md#guard-changes)

### Subtasks
- [ ] 8.1 Add path tokens for the toolbox home, the override directory and the Codex home to `klaude-plugin/scripts/guard/guard.py`, following the temp-directory token
- [ ] 8.2 Add the toolbox home, the override file, the owned files under the Codex home and Codex's plugin cache to `selfmod` in `guard-rules.json`
- [ ] 8.3 Add cases to `test/guard/test_guard.py` for each new path, including a non-default home → verify: an agent edit to each path is denied and a read is not
- [ ] 8.4 Run `make generate-guard` and confirm the documentation table updates

## Task 9: Codex baseline, owned files and `kk codex`
- **Status:** pending
- **Depends on:** Task 1, Task 4
- **Size:** M
- **Can run in parallel with:** Task 6, Task 7, Task 8
- **Docs:** [implementation.md#codex-baseline-and-launch](./implementation.md#codex-baseline-and-launch), [design.md#launching-codex](./design.md#launching-codex)

### Subtasks
- [ ] 9.1 Create `kk/baseline/codex.json` from `.codex/config.toml` (no MCP entries) and `kk/baseline/codex/bootstrap.md` from the tool-name mapping in `.codex/scripts/session-start.sh`
- [ ] 9.2 Make generated sub-agents available at `kk/baseline/codex/agents/` through the generator, with a freshness check; keep `.codex/agents/`
- [ ] 9.3 Write the JSON-to-TOML serialiser for the baseline's value shapes → verify: output parses back to the input where a TOML parser is available
- [ ] 9.4 Compose the profile from baseline keys, Codex overrides and developer instructions (behavioural instructions, bootstrap text, protected-files advisory)
- [ ] 9.5 Install owned files: the profile, the rules file after `codex execpolicy check` over the remaining rules set, and prefixed sub-agent files with pruning
- [ ] 9.6 Implement `kk codex`: add the profile, pass through when the adopter names one, refuse per the state table, treat `exec` and `review` as non-interactive
- [ ] 9.7 Unit tests for composition, serialisation, pruning and each refusal → verify: `codex --profile kk debug prompt-input` shows the instructions as a developer message

## Task 10: Codex activation, trust and rollback
- **Status:** pending
- **Depends on:** Task 7, Task 9
- **Size:** M
- **Can run in parallel with:** Task 6
- **Docs:** [implementation.md#codex-activation-and-trust](./implementation.md#codex-activation-and-trust), [design.md#activation-state](./design.md#activation-state)

### Subtasks
- [ ] 10.1 Write the local Codex marketplace manifest with both plugins; add the marketplace and plugins on first install; compare the tree at the reported install path with the release
- [ ] 10.2 On upgrade re-add the skills plugin when its version differs and the guard plugin only when its version differs
- [ ] 10.3 Implement the guard-change confirmation, defaulting to no without a terminal
- [ ] 10.4 Implement trust tracking with the mechanism from Task 1, or explicit acknowledgement labelled unverified; record *awaiting review* and surface it in `kk status`
- [ ] 10.5 Implement Codex rollback and resumption, including a guard that differs between the two releases
- [ ] 10.6 Stub-based tests for each activation path
- [ ] 10.7 Record demonstration 2 in `verification/task-10/`: interrupt during activation, roll back offline, show a guarded action denied by the restored guard without a trust bypass

## Task 11: Launch notice, mixed installs and live check
- **Status:** pending
- **Depends on:** Task 6, Task 10
- **Size:** M
- **Can run in parallel with:** Task 12, Task 13
- **Docs:** [implementation.md#notice-mixed-installs-and-live-check](./implementation.md#notice-mixed-installs-and-live-check), [design.md#install-modes](./design.md#install-modes)

### Subtasks
- [ ] 11.1 Implement the launch notice: background check, one-day cache, terminal-only output, silent offline, switchable off → verify: a launch with the network blocked is not delayed and prints nothing
- [ ] 11.2 Detect Git-marketplace installs of the plugin for both tools in `kk status`; offer removal of user-scope installs through the vendor CLIs after confirmation; block *ready* while active hooks are ambiguous
- [ ] 11.3 Implement `kk status --live` with a decoy secret in a scratch directory → verify: the output contains the guard's own denial text for each tool
- [ ] 11.4 Tests for the cache, the terminal check and mixed-install detection

## Task 12: CI gate and release workflow
- **Status:** pending
- **Depends on:** Task 4, Task 7
- **Size:** S
- **Can run in parallel with:** Task 9, Task 10, Task 11
- **Docs:** [implementation.md#ci-gate-and-release-workflow](./implementation.md#ci-gate-and-release-workflow), [design.md#release-safety](./design.md#release-safety)

### Subtasks
- [ ] 12.1 Add a CI job running the guard engine suite, the `kk` suite, the Codex adapter suite and the self-test cases on the oldest and newest available Python
- [ ] 12.2 Make `release.yml` and `pre-release.yml` run that gate before tagging
- [ ] 12.3 Add the guard plugin version rule to the release workflow → verify: a dry run on a skills-only change leaves `kodex-guard`'s manifest untouched; a guard change bumps it

## Task 13: Retirement migration in the sync script
- **Status:** pending
- **Depends on:** Task 10
- **Size:** M
- **Can run in parallel with:** Task 11, Task 12
- **Docs:** [implementation.md#migration](./implementation.md#migration), [design.md#legacy-coexistence-and-migration](./design.md#legacy-coexistence-and-migration)

### Subtasks
- [ ] 13.1 Add an upstream retirement marker and a `needs_*` / `run_*` migration pair in `.claude/toolbox/scripts/template-sync.sh`, gated on `APPLY_MODE`
- [ ] 13.2 Remove toolbox hook handlers one at a time by exact command string against the template at the recorded version; drop emptied groups and events; keep all others
- [ ] 13.3 Remove template-added entries from the settings file and the Codex config using the fetched base, including the Git-marketplace enablement; keep the adopter's entries
- [ ] 13.4 Remove synced files identical to the template with substitutions applied; report and keep edited files; remove the two exact import lines; remove the sync infrastructure last
- [ ] 13.5 State the team-wide effect in the report
- [ ] 13.6 Add fixtures and cases to `test/test-template-sync.sh`: capy hooks, an adopter hook, an edited synced file, a customised settings file → verify: every non-toolbox entry survives byte for byte

## Task 14: `kk migrate` and the migration demonstration
- **Status:** pending
- **Depends on:** Task 11, Task 13
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#migration](./implementation.md#migration), [design.md#verification](./design.md#verification)

### Subtasks
- [ ] 14.1 Implement `kk migrate`: readiness check for the tools the repository uses, pinned retirement version, preview, confirmation, apply, changes left uncommitted; fetch the pinned script when the local copy cannot hand off
- [ ] 14.2 Tests for the refusal when `kk` is not ready and for a declined confirmation
- [ ] 14.3 Record demonstration 3 in `verification/task-14/` on one of the maintainer's repositories: a guard is active at every point, and the diff shows the team-wide effect

## Task 15: Documentation and ADR
- **Status:** pending
- **Depends on:** Task 11, Task 14
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#documentation-and-adr](./implementation.md#documentation-and-adr), [design.md#parity-ledger](./design.md#parity-ledger)

### Subtasks
- [ ] 15.1 Write `docs/adr/0014-machine-level-delivery.md` and add it to the ADR table in `docs/contributing/architecture.md`
- [ ] 15.2 Rewrite `docs/getting-started/` around the install command; keep plugin-only as a mode; turn `docs/user-guide/template-sync.md` into a migration guide
- [ ] 15.3 Update `docs/user-guide/configuration.md`: launcher layer, overrides, parity exceptions, `Skill(kk:*)` as standing authorisation including future skills
- [ ] 15.4 Update `docs/providers/codex.md` (guard plugin, hook review, profile precedence, open-session caveat) and `docs/providers/claude-code.md` (unwrapped-session exception)
- [ ] 15.5 Document routing PAL's Claude client through `kk` in `docs/user-guide/mcp-servers.md`
- [ ] 15.6 Update `README.md`, `AGENTS.md`, `docs/contributing/architecture.md`, `docs/contributing/testing.md`, the plugin READMEs and `mkdocs.yml` → verify: `make docs-build` succeeds

## Task 16: Retire the template in this repository
- **Status:** pending
- **Depends on:** Task 14, Task 15
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#retire-the-template](./implementation.md#retire-the-template), [design.md#retiring-the-template](./design.md#retiring-the-template)
- **Blocked until:** the retirement release is tagged and demonstrations 1 to 3 are recorded

### Subtasks
- [ ] 16.1 Remove the sync script and workflow, the template cleanup script and workflow, the bootstrap script, the example state file and their tests
- [ ] 16.2 Remove the legacy generator targets and the transition copies (`.claude/CLAUDE.extra.md`, `.claude/toolbox/`, `.codex/scripts/`, `.codex/rules/default.rules`, `.codex/agents/`) and update every freshness list
- [ ] 16.3 Reduce this repository's `.claude/` and `.codex/` to an adopter's footprint and run it on `kk` → verify: all suites pass and a wrapped session in this repository shows the guard and the instructions
- [ ] 16.4 The maintainer turns off the repository's template flag

## Task 17: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 17.1 Run `/kk:test` for the shell and Python suites, the Go tool tests and generated-output freshness; confirm the three demonstrations are recorded with tool versions; broaden if a probe contradicted the design after dependent tasks finished or a vendor release changed hook, plugin or settings behaviour
- [ ] 17.2 Observe every parity-ledger row marked kept or moved on a machine set up from scratch
- [ ] 17.3 Run `/kk:document` to update any remaining docs
- [ ] 17.4 Run `/kk:review-code` with bash and python as the language input
- [ ] 17.5 Run `/kk:review-spec` to verify the implementation matches the design and implementation docs
- [ ] 17.6 If any non-blocking items remain, ask the maintainer how to follow up, for example with GitHub issues
- [ ] 17.7 Move the feature docs from `docs/feat/wip/` to `docs/feat/done/` and update markdown references

## Dependency Graph

```
Task 1 ─┬─→ Task 7 ─┬─────────────→ Task 10 ─┬─→ Task 11 ─┬─→ Task 14 ─→ Task 15 ─→ Task 16 ─→ Task 17
        │           └─→ Task 12              │            │        ↑
        └─→ Task 9 ─────────────────→ Task 10 └─→ Task 13 ─────────┘
Task 2 ─→ Task 3 ─→ Task 4 ─┬─→ Task 9
                   │        └─→ Task 12
                   └─→ Task 6 ─→ Task 11
Task 5 ─→ Task 6
Task 8 (independent) ───────────────────────────────────────────────────────────────────────→ Task 17
```
