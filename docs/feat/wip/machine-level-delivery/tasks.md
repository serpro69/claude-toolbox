# Tasks: Machine-level delivery

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending — revised after the [design review](./review-design.md); see the [resolution](./review-resolution.md)
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
- [ ] 1.3 Re-add the unchanged guard plugin, then the guard plugin at a new version with a changed script, each with a session open; then install it once under a digest-stamped version string → verify: record whether the cache directory is replaced, which outcome the open session shows (assumption 2), and which stamped form Codex accepts as a version and cache directory name (assumption 13)
- [ ] 1.4 Probe trust scope across two repositories, the hook's launch directory against the payload directory, and a Git-URL marketplace source → verify: results recorded for assumptions 3, 4 and 10
- [ ] 1.5 Find how to read hook trust from outside a session (app-server `hooks/list`, then persisted hook state), then disable the trusted hook and read again → verify: the request and response are recorded, with whether a disabled hook shows as disabled, whether the answer depends on the workspace, and how long one read takes; or the absence of a usable mechanism is recorded (assumption 7)
- [ ] 1.6 Probe profile precedence against user and trusted project config with every baseline key, user-level sub-agents, and an MCP-tool matcher from a plugin hook → verify: results recorded for assumptions 5 and 6
- [ ] 1.7 In a scratch repository, trust a project hook that runs a script from the repository, open a session, delete the script and send a guarded command → verify: record whether the call proceeds unguarded, is blocked or errors (assumption 12)
- [ ] 1.8 Write the results to `verification/task-1/` with tool versions, and update `design.md` Assumptions and any section a result contradicts

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
- [ ] 3.1 Create `kk/bin/kk` (entry point: resolve the toolbox home, read the active release, the rollback target and the per-tool phase with `jq`, run the rollback target's CLI for `rollback` and the active release's otherwise, under isolated Python) and `kk/payload.json` (layout version and required directories)
- [ ] 3.2 Create the state module in `kk/lib/`: one active release, per-tool state, rollback target, candidate phase, the time each release stopped being active, the installed-paths record, atomic writes, and the exclusive writer lock on `$KK_HOME/lock` → verify: a failed rename leaves the previous state file intact; a second writer exits at once and changes nothing
- [ ] 3.3 Create the payload module: fetch from a tag archive or a local checkout, extract only payload directories, reject absolute paths, parent traversal and escaping symlinks → verify: crafted archives are rejected; the plugin's relative symlinks survive
- [ ] 3.4 Create `kk/selftest/guard-cases.json` and the validation module: payload completeness, guard self-test against the candidate engine, one event through the Claude guard handler as the staged `hooks/hooks.json` registers it, `claude plugin validate` → verify: a candidate with a broken engine fails and the state file is unchanged; so does one whose hook registration names a script missing from the payload
- [ ] 3.5 Create Claude activation: write the local marketplace manifest, add the marketplace, install the plugin at user scope, verify the load path through `claude plugin list --json`; stop without replacing anything when `~/.local/bin/kk` exists and is not in the installed-paths record
- [ ] 3.6 Add `kk upgrade` for the first-install path, `kk status`, and `install.sh` at the repository root; running the installer again after an interrupted first install resumes from the journaled phase or starts over
- [ ] 3.7 Add `test/kk/` and `test/test-kk.sh` with stub vendor CLIs covering first install, an interrupted first install completed by a second installer run, failed validation, a colliding symlink and two overlapping writers → verify: the suite passes under isolated Python 3.8 syntax checks

## Task 4: Upgrade, rollback and recovery for Claude
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7, Task 8
- **Docs:** [implementation.md#kk-foundation](./implementation.md#kk-foundation), [design.md#rollback-and-interrupted-upgrades](./design.md#rollback-and-interrupted-upgrades)

### Subtasks
- [ ] 4.1 Implement the hand-off: fetch, staging and validation from the active release's code; activation and verification from the candidate's; rollback from the rollback target's code; status and resumption from the active release
- [ ] 4.2 Journal the candidate's phase before each activation step and implement resumption of an interrupted upgrade
- [ ] 4.3 Implement `kk rollback` to the rollback target, the recovery command `kk upgrade` prints, and pruning of releases that are not active, not the rollback target, and stopped being active more than 14 days ago
- [ ] 4.4 Extend the stub-based suite: upgrade, interruption at each activation step followed by resume and by rollback, pruning with a release that was active for a month and superseded yesterday → verify: after every interruption case `kk status` reports the mixed state and both ways out work; the month-old release is kept
- [ ] 4.5 Add the post-promotion case: promote a release, make its `kk/lib` unreadable, then break the stable entry point too → verify: the previous release is restored through the stable entry point in the first state and through the copy inside the rollback target in the second

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
- [ ] 6.1 Create `kk/baseline/claude.json`: preferences from the template's adopter defaults as `.github/scripts/template-cleanup.sh` renders them with no options (no `model` key, `effortLevel: high`), environment variables from `.claude/settings.json`, statusline path, default allow entries, opt-in catalogue; do not copy this repository's pinned model or `xhigh`
- [ ] 6.2 Add `kk/baseline/claude/deny.json` as a target in `scripts/generate-guard.sh` and in every freshness list
- [ ] 6.3 Implement layer composition: yield per key and per environment variable to the user, project and local settings; always include denies, which nothing composed later can remove; add default allows; disable the Git-marketplace plugin ID only where it is enabled
- [ ] 6.4 Implement the override file: schema, named settings file, default switches, opt-in grants; overrides set or replace preference keys and add to permission lists; a malformed file stops the launch with a message
- [ ] 6.5 Implement `kk claude` with `--print-layer`; when the adopter supplies `--settings` as a path or inline JSON, compose it as the top of the layer and pass the one composed file; stop the launch when it cannot be read or parsed
- [ ] 6.6 Unit tests for yielding, list composition, each override, the adopter's `--settings` in both forms with the denies intact, an override that tries to empty the deny list, and a malformed override → verify: on a real machine a wrapped session uses the baseline effort level when none is set and the user's when one is; with hooks disabled, a wrapped session started with the adopter's own `--settings` refuses to read a decoy secret

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
- [ ] 7.6 Add `kk/lib/guard_identity.py`, a standalone module: SHA-256 over the sorted path, mode and bytes of every file in a guard bundle, leaving out the manifest's `version` field → verify: bundles differing only in version share an identity; a one-byte change or a changed executable bit changes it

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
- [ ] 9.1 Create `kk/baseline/codex.json` from `.codex/config.toml` (no MCP entries; `approval_policy`, `approvals_reviewer` and `sandbox_mode` in the opt-in catalogue, not the defaults) and `kk/baseline/codex/bootstrap.md` from the tool-name mapping in `.codex/scripts/session-start.sh`
- [ ] 9.2 Make generated sub-agents available at `kk/baseline/codex/agents/` through the generator, with a freshness check; keep `.codex/agents/`
- [ ] 9.3 Write the JSON-to-TOML serialiser for the baseline's value shapes → verify: output parses back to the input where a TOML parser is available
- [ ] 9.4 Compose the profile from baseline keys, the opt-in keys the override file switched on, Codex overrides and developer instructions (behavioural instructions, bootstrap text, protected-files advisory)
- [ ] 9.5 Install owned files: the profile, the `kk-` sub-agent files, and the rules file only when the override file switches the native forbids on; check every destination against the installed-paths record at staging and stop on a collision; record each written path and prune by the record, never by prefix; remove the rules file when the switch is turned off; print the account-wide effect the first time the rules file is installed
- [ ] 9.6 Validate the rules file in two steps with `codex execpolicy check`: the candidate alone forbids every command it must, then the candidate with the remaining rules files still loads
- [ ] 9.7 Implement `kk codex`: add the profile, pass through when the adopter names one, refuse per the state table, treat `exec` and `review` as non-interactive; before a non-interactive run re-read trust and enablement of the guard's handlers, refuse when one is untrusted or disabled, and warn in one line when the state is *unverified*
- [ ] 9.8 Unit tests for composition with the opt-in keys off and on, serialisation, each refusal, a pre-existing `kk.config.toml` that stops the install untouched, an adopter's `kk-notes.toml` that survives pruning, and a candidate rules file missing a forbid another file supplies → verify: `codex --profile kk debug prompt-input` shows the instructions as a developer message

## Task 10: Codex activation, trust and rollback
- **Status:** pending
- **Depends on:** Task 7, Task 9
- **Size:** M
- **Can run in parallel with:** Task 6
- **Docs:** [implementation.md#codex-activation-and-trust](./implementation.md#codex-activation-and-trust), [design.md#activation-state](./design.md#activation-state)

### Subtasks
- [ ] 10.1 Write the local Codex marketplace manifest with both plugins; add the marketplace and plugins on first install; compare the tree at the reported install path with the release
- [ ] 10.2 At staging, compute the candidate guard's identity, stamp a local-checkout guard's version with the digest in the form Task 1 found, and fail when the candidate carries the installed version with a different identity; send one event through each staged Codex adapter as its `hooks/hooks.json` registers it; on upgrade re-add the skills plugin when its version differs and the guard plugin only when its identity differs
- [ ] 10.3 Implement the guard-change confirmation, keyed on identity, defaulting to no without a terminal
- [ ] 10.4 Implement trust tracking with the mechanism from Task 1: read trust and enablement per guard handler and record *awaiting review* while any is untrusted or disabled; without a mechanism, the adopter's acknowledgement gives *unverified*, never *ready*; surface both in `kk status`
- [ ] 10.5 Implement Codex rollback and resumption, including a guard that differs between the two releases; the rollback target skips a release whose guard never got past *awaiting review*
- [ ] 10.6 Stub-based tests for each activation path, a local checkout whose guard changed under an unchanged manifest version, and the mixed case: Codex *awaiting review* on B, C activated, `kk rollback` restores A with B still on disk
- [ ] 10.7 Record demonstration 2 in `verification/task-10/`: interrupt during activation, roll back offline, show a guarded action denied by the restored guard without a trust bypass
- [ ] 10.8 Record demonstration 4 in `verification/task-10/`: promote a release, make its `kk/lib` unavailable, restore the previous release offline through the entry point inside the rollback target, show a guarded action denied by the restored guard

## Task 11: Launch notice, mixed installs and live check
- **Status:** pending
- **Depends on:** Task 6, Task 10
- **Size:** M
- **Can run in parallel with:** Task 12, Task 13
- **Docs:** [implementation.md#notice-mixed-installs-and-live-check](./implementation.md#notice-mixed-installs-and-live-check), [design.md#install-modes](./design.md#install-modes)

### Subtasks
- [ ] 11.1 Implement the launch notice: background check, one-day cache, terminal-only output, silent offline, switchable off → verify: a launch with the network blocked is not delayed and prints nothing
- [ ] 11.2 Detect Git-marketplace installs of the plugin for both tools in `kk status`; offer removal of user-scope installs through the vendor CLIs after confirmation; block *ready* while active hooks are ambiguous
- [ ] 11.3 Implement `kk status --live` with a decoy secret in a scratch directory, callable with the session started in a given repository for `kk migrate` → verify: the output contains the guard's own denial text for each tool
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
- [ ] 12.3 Add the guard plugin version rule to `release.yml` and `pre-release.yml`, comparing identity from `kk/lib/guard_identity.py` with the nearest earlier tag of any kind → verify: a dry run on a skills-only change leaves `kodex-guard`'s manifest untouched; a release candidate with a guard change bumps it; the stable release that follows with the same bytes keeps the candidate's version

## Task 13: Retirement migration in the sync script
- **Status:** pending
- **Depends on:** Task 10
- **Size:** M
- **Can run in parallel with:** Task 11, Task 12
- **Docs:** [implementation.md#migration](./implementation.md#migration), [design.md#removal-rules](./design.md#removal-rules), [design.md#ordinary-sync-and-the-tombstone](./design.md#ordinary-sync-and-the-tombstone)

### Subtasks
- [ ] 13.1 Add a `--retire` mode to `.claude/toolbox/scripts/template-sync.sh` (`parse_arguments` and a separate path in `main`), previewing with `--dry-run`; do not add a `needs_*` / `run_*` migration and do not call the removal functions from `apply_changes`; every existing mode prints one notice naming `kk migrate` → verify: one fixture run through `--local`, a staged `--apply` and `--retire`; only `--retire` removes guard files or hook registrations
- [ ] 13.2 Remove toolbox hook handlers one at a time by exact command string against the template at the recorded version; drop emptied groups and events; keep all others
- [ ] 13.3 Remove template-added entries from the settings file and the Codex config by a removal-only comparison with the fetched base, without the three-way merge: deny entries only when the base has them; keep and report manifest-selected `model`, `effortLevel`, `permissions.defaultMode`, Codex `model` and `approval_policy` unless the manifest holds the built-in default; remove `statusLine` and report the choice; remove the Git-marketplace enablement and registration
- [ ] 13.4 Remove synced files identical to the template with substitutions applied; report and keep edited files; remove the two exact import lines; skip and list everything under `sync_exclusions`; remove the sync infrastructure last
- [ ] 13.5 When the base or the template at the recorded version cannot be fetched, remove only the Git-marketplace enablement and registration and list the rest for removal by hand
- [ ] 13.6 State the team-wide effect and the kept adopter choices in the report
- [ ] 13.7 Write the tombstone script (accepts every existing option, sources nothing, changes nothing, prints migration guidance, exits successfully, writes `has_changes=false` with `--ci`) and keep it beside the tests until Task 16 installs it → verify: the previous release's script run with `--local`, and with a staged `--apply`, against a fixture upstream holding the tombstone leaves the working tree byte-identical
- [ ] 13.8 Add fixtures and cases to `test/test-template-sync.sh`: capy hooks, an adopter hook, an edited synced file, a customised settings file, a deny entry the template never shipped, a manifest selecting a Claude model and a Codex approval policy, a file under `sync_exclusions`, an unfetchable recorded version → verify: every non-toolbox entry survives byte for byte

## Task 14: `kk migrate` and the migration demonstration
- **Status:** pending
- **Depends on:** Task 11, Task 13
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#migration](./implementation.md#migration), [design.md#verification](./design.md#verification)

### Subtasks
- [ ] 14.1 Implement the guard check in `kk migrate`: for each tool the repository uses, re-read trust and enablement where the mechanism exists and run the live check with the session started in the repository; refuse unless the guard's own denial is seen
- [ ] 14.2 Implement the rest of `kk migrate`: check for `curl` and Mike Farah's `yq` with a message that they are needed for this step only; warn about Codex sessions opened before `kk` was installed, worded from the Task 1 deleted-script result, and ask, default no; fetch `template-sync.sh` and `semver-compare.sh` from the retirement tag into a temporary directory; run with `TEMPLATE_SYNC_NO_HANDOFF=1` and `--retire --dry-run`, ask, run `--retire`; leave the changes uncommitted
- [ ] 14.3 Tests for the refusal when the trust read reports a disabled hook despite a recorded *ready*, when the tool is *unverified* and the live check fails, for a missing `yq`, and for each declined confirmation
- [ ] 14.4 Record demonstration 3 in `verification/task-14/` on one of the maintainer's repositories, with a Codex session opened before `kk` was installed: a guard is active at every point for sessions started after `kk` became ready, what the older session does is recorded, and the diff shows the team-wide effect

## Task 15: Documentation and ADR
- **Status:** pending
- **Depends on:** Task 11, Task 14
- **Size:** M
- **Can run in parallel with:** Task 18
- **Docs:** [implementation.md#documentation-and-adr](./implementation.md#documentation-and-adr), [design.md#parity-ledger](./design.md#parity-ledger)

### Subtasks
- [ ] 15.1 Write `docs/adr/0014-machine-level-delivery.md` and add it to the ADR table in `docs/contributing/architecture.md`
- [ ] 15.2 Rewrite `docs/getting-started/` around the install command; keep plugin-only as a mode; turn `docs/user-guide/template-sync.md` into a migration guide that covers ordinary sync never retiring, the tombstone, the 14-day supported session lifetime, and not syncing past the retirement release from a script older than v0.21.0
- [ ] 15.3 Update `docs/user-guide/configuration.md`: launcher layer, overrides, parity exceptions, `Skill(kk:*)` as standing authorisation including future skills, the two Codex opt-ins and the account-wide effect of the native forbids
- [ ] 15.4 Update `docs/providers/codex.md` (guard plugin, hook review, profile precedence, opt-in approval and sandbox defaults, opt-in native forbids, both open-session caveats) and `docs/providers/claude-code.md` (unwrapped-session exception; no coverage for cloud sessions and fresh CI runners from a user-level install)
- [ ] 15.5 Document PAL's Claude client entry in `docs/user-guide/mcp-servers.md`: it runs `kk claude` and keeps the scoped temp-directory read grant → verify: a review launched through the documented entry reads both its criteria and its diff
- [ ] 15.6 Update `README.md`, `AGENTS.md`, `docs/contributing/architecture.md`, `docs/contributing/testing.md`, the plugin READMEs and `mkdocs.yml` → verify: `make docs-build` succeeds

## Task 18: Pilot the tagged release
_Runs before Task 16. It was added after the design review and is numbered 18 so that existing references to Tasks 16 and 17 stay valid._
- **Status:** pending
- **Depends on:** Task 12, Task 14
- **Size:** S
- **Slicing:** Risk-First — retirement is not cheaply undone, and scratch plugins are not what adopters install
- **Can run in parallel with:** Task 15
- **Docs:** [implementation.md#pilot-the-tagged-release](./implementation.md#pilot-the-tagged-release), [design.md#verification](./design.md#verification)

### Subtasks
- [ ] 18.1 Tag a release candidate of the retirement release through the pre-release workflow
- [ ] 18.2 On a machine or user account with no toolbox state, run the installer at the candidate version → verify: every parity-ledger row marked kept or moved is observed, with both Codex opt-ins switched on and off
- [ ] 18.3 In one legacy repository, open a Codex session, then install and review the hooks, then run an ordinary `--local` sync against the candidate → verify: the legacy guard files and hook registrations are intact
- [ ] 18.4 Run `kk migrate` in that repository → verify: a new session is guarded throughout; what the older session does is recorded
- [ ] 18.5 Repeat demonstrations 1, 2 and 4 with the shipped guard plugin and the real marketplace names
- [ ] 18.6 Write the results to `verification/pilot/` with tool versions; fix and re-pilot with a new candidate anything the pilot contradicts before the stable retirement release is tagged

## Task 16: Retire the template in this repository
- **Status:** pending
- **Depends on:** Task 15, Task 18
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#retire-the-template](./implementation.md#retire-the-template), [design.md#retiring-the-template](./design.md#retiring-the-template)
- **Blocked until:** the pilot is recorded and the stable retirement release is tagged

### Subtasks
- [ ] 16.1 Replace the sync script with the tombstone from Task 13 and keep its test; remove `semver-compare.sh`, the sync workflow, the template cleanup script and workflow, the bootstrap script, the example state file and their tests
- [ ] 16.2 Remove the legacy generator targets and the transition copies (`.claude/CLAUDE.extra.md`, `.claude/toolbox/` except the tombstone, `.codex/scripts/`, `.codex/rules/default.rules`, `.codex/agents/`) and update every freshness list
- [ ] 16.3 Reduce this repository's `.claude/` and `.codex/` to an adopter's footprint and run it on `kk` → verify: all suites pass and a wrapped session in this repository shows the guard and the instructions
- [ ] 16.4 The maintainer turns off the repository's template flag

## Task 17: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 18
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 17.1 Run `/kk:test` for the shell and Python suites, the Go tool tests and generated-output freshness; confirm the four demonstrations and the pilot are recorded with tool versions; broaden if a probe contradicted the design after dependent tasks finished or a vendor release changed hook, plugin or settings behaviour
- [ ] 17.2 Confirm the pilot record covers every parity-ledger row marked kept or moved, and observe again any row touched by a change made after the pilot
- [ ] 17.3 Run `/kk:document` to update any remaining docs
- [ ] 17.4 Run `/kk:review-code` with bash and python as the language input
- [ ] 17.5 Run `/kk:review-spec` to verify the implementation matches the design and implementation docs
- [ ] 17.6 If any non-blocking items remain, ask the maintainer how to follow up, for example with GitHub issues
- [ ] 17.7 Move the feature docs from `docs/feat/wip/` to `docs/feat/done/` and update markdown references

## Dependency Graph

```
Task 1 ─┬─→ Task 7 ─┬─→ Task 10 ─┬─→ Task 11 ─→ Task 14 ─┬─→ Task 15 ─┬─→ Task 16 ─→ Task 17
        │           └─→ Task 12  └─→ Task 13 ─→ Task 14  └─→ Task 18 ─┘
        └─→ Task 9 ─→ Task 10
Task 2 ─→ Task 3 ─→ Task 4 ─┬─→ Task 9
                   │        └─→ Task 12 ─→ Task 18
                   └─→ Task 6 ─→ Task 11
Task 5 ─→ Task 6
Task 8 (independent) ─→ Task 17
```
