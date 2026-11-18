# Implementing machine-level delivery

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: draft — not yet reviewed

## Repository context

Read this section first if you have not worked in this repository.

- **Canonical source and generators.** `klaude-plugin/` is hand-authored. `make generate-kodex` (a Go tool in `cmd/generate-kodex/`, driven by `scripts/kodex-generate-manifest.yml`) produces `kodex-plugin/` and `.codex/agents/`. `make generate-guard` (`scripts/generate-guard.sh`) projects `klaude-plugin/scripts/guard/guard-rules.json` into several targets and copies the guard engine. CI rejects stale generated output (`.github/workflows/generated-check.yml`). Never edit a generated copy.
- **The guard.** `klaude-plugin/scripts/guard/guard.sh` picks an interpreter and runs `run-guard.py` under isolated Python (`python3 -I`), which loads the adjacent `guard.py` by absolute path. The engine is standard library only and stays within Python 3.8 syntax. A denial is exit 2 with a reason on stderr; any failure denies. Policy is anchored by `KK_GUARD_PROJECT_ROOT`; project additions come from `<root>/.claude/kk-guard.json`.
- **Codex adapters today.** `.codex/scripts/pretooluse-{bash,patch,mcp}.sh` are hand-authored and registered in `.codex/hooks.json`. They derive the project root from their own location. `.codex/scripts/session-start.sh` injects instructions.
- **Template sync today.** `.claude/toolbox/scripts/template-sync.sh` fetches the template at a version, applies substitutions from `.github/template-state.json`, compares, and applies. It has a migration pattern (`needs_*` / `run_*` pairs gated on `APPLY_MODE`), a three-way settings merge with a fetched base, and a hook filter that separates toolbox entries from downstream ones.
- **Tests.** Shell suites are `test/test-*.sh` and share `test/helpers.sh`. Python suites run through a thin shell wrapper under isolated Python (see `test/test-guard.sh` and `test/guard/test_guard.py`).
- **Vendor versions.** The design's evidence is from Claude Code 2.1.296 and Codex CLI 0.169.0. Record the versions with every probe.

Two conventions apply to all new `kk` code:

- **Python 3.8, standard library only, run isolated.** Follow the guard's loader pattern for importing sibling modules; isolated mode does not put the script's directory on the import path.
- **Vendor CLIs are stubbed in tests.** Put fake `claude` and `codex` executables first on `PATH`; they record their arguments and print canned JSON. Live vendor behaviour belongs in recorded probes, not in the test suites.

Record probe evidence under `docs/feat/wip/machine-level-delivery/verification/`, one directory per task, with the tool versions, the commands and the observed output.

The work is ordered so that the two probe tasks run first. Either can change the design; do not start the tasks that depend on them until their results are recorded and the design is updated.

## Codex vendor probes

These settle the source-read claims in [Evidence and provenance](design.md#evidence-and-provenance). Use a scratch `CODEX_HOME` so the real one is untouched. Runs that need a model call need credentials in the scratch home; the maintainer copies them, the implementer does not.

An *open session* means one long-lived Codex process. A resumed `codex exec` starts a new process and reloads plugins, so it proves nothing here. Drive the interactive TUI in a tmux pane: send a prompt, change the installation from another shell, send a second prompt, capture the pane.

To attribute a denial to the guard, the probe hook writes a log line for every call it sees, and the session runs with a sandbox that would otherwise permit the action.

1. Build a scratch local marketplace with two plugins: one skills-only, one with a `PreToolUse` hook that denies a marker command. Install both and trust the hook. → verify: a marker command is denied and the hook log shows it.
2. With a session open, re-add only the skills plugin at a new version, then send a marker command in the open session. → verify: the hook log shows a new denial. This is [assumption 1](design.md#assumptions).
3. Re-add the unchanged guard plugin and check whether its cache directory was replaced. → verify: record whether the directory's identity changed; this decides whether `kk` must skip unchanged guards.
4. With a session open, re-add the guard plugin at a new version with a changed script, then send a marker command. → verify: record which of three outcomes occurs: denied by the old hook, executed unguarded, or blocked with an error. This is assumption 2.
5. Trust the hook in one scratch repository, then start a session in a second. → verify: the hook runs in the second without a new review (assumption 3).
6. Have the hook log its own working directory and the payload's, and run a command whose working directory differs from the session's. → verify: record both values (assumption 4).
7. Find a way to read hook trust from outside a session: the app-server's `hooks/list` method first, the persisted hook state second. → verify: record the exact request and response, or record that neither is usable (assumption 7).
8. Put a profile, a base user config and a trusted project config in conflict on one key, and load every baseline key in the profile. → verify: the project value wins and no key is rejected (assumption 5).
9. Place a sub-agent file in `$CODEX_HOME/agents/` and register a hook matcher for an MCP tool. → verify: the agent is available and the matcher fires (assumption 6).
10. Repeat step 1's trust check with the marketplace added from a Git URL. → verify: record any difference from the local source (assumption 10).

Update the design's Assumptions and affected sections with each result before closing the task.

## Claude vendor probes

These need a real logged-in configuration, because a scratch configuration directory has no credentials. Use a uniquely named scratch marketplace and plugin, and remove both afterwards. Get the maintainer's agreement before adding anything to the real configuration.

1. Add a local-path marketplace whose plugin entry points at a versioned subdirectory, install the plugin at user scope, and start a session. → verify: a hook in the plugin reports its script path and plugin root inside that subdirectory (assumption 8).
2. Re-point the marketplace entry at a second subdirectory while a session is open. → verify: the open session still uses the first; a new session uses the second.
3. In an untrusted scratch directory, pass a settings layer with a deny rule and a statusline. → verify: a matching read is denied with hooks disabled, and the statusline renders in an interactive session (assumption 9).
4. Enable a plugin in a trusted project's settings and set the same plugin ID to `false` in the settings layer. → verify: the plugin does not load.
5. Optional: set the VS Code extension's process wrapper to a script that adds a settings layer. → verify: record whether the layer applies.

## `kk` foundation

Deliver one complete path for Claude: a first install on a clean machine, an upgrade, a rollback and a status report.

**Files to create**

- `kk/bin/kk` — the stable entry point, a short shell script. It resolves the toolbox home, reads the active release from the state file, and runs that release's CLI under isolated Python. It contains no upgrade logic.
- `kk/lib/` — the CLI modules. Keep them few: state, payload, validation, Claude activation, command dispatch.
- `kk/payload.json` — the payload's layout version and the directories it must contain.
- `kk/selftest/guard-cases.json` — a small set of guard inputs with expected decisions, covering an allowed command, a secret read, a destructive command and a protected-path edit.
- `install.sh` at the repository root — downloads the latest stable release and runs its upgrade.
- `test/kk/` and `test/test-kk.sh` — the Python suite and its wrapper.

**Behaviour to implement**

1. Toolbox home resolution and the layout in [Components](design.md#components). Every write is a temporary file followed by a rename. → verify: an interrupted write never leaves a truncated state file (test by failing the rename).
2. Payload fetch from a tag archive and from a local checkout. Extract only the payload directories. Reject archive members with absolute paths, parent traversal, or symlinks that leave the payload; the plugin contains legitimate relative symlinks. → verify: a crafted archive with each kind of bad member is rejected; a real payload's symlinks survive.
3. A version for local-checkout payloads that cannot collide with a tag.
4. Validation with nothing activated: payload completeness, the guard self-test against the candidate engine, and `claude plugin validate`. → verify: a candidate with a syntax error in the engine fails validation and leaves the state file unchanged.
5. The state machine in [Activation state](design.md#activation-state), per tool, with the candidate's phase journaled before each activation step.
6. Claude activation: write the local marketplace manifest pointing at the release, add the marketplace and install the plugin on first install, then verify through `claude plugin list --json` that the plugin loads from the release directory. Marketplace plugin sources must start with `./`.
7. Hand-off: fetch, staging and validation run from the active release's code; activation and verification run from the candidate's. Rollback, status and resumption run from the last ready release.
8. `kk rollback`, `kk status`, and pruning of releases that are neither active, previous, nor activated in the last 14 days.

→ verify: with stub vendor CLIs, the suite covers first install, upgrade, failed validation, interruption at each activation step followed by resume and by rollback, and pruning.

## Claude plugin changes

1. Create `klaude-plugin/instructions/behavior.md` from `.claude/CLAUDE.extra.md` and make it the single source. Until the template is retired, `.claude/CLAUDE.extra.md` becomes a generated copy with a freshness check, so template sync keeps delivering it. → verify: `test/test-claude-extra.sh` still passes, and the copy is byte-identical.
2. Move the plugin-root override text from `.claude/toolbox/CLAUDE.md` into a plugin instruction file. It is injected only for plugin-only installs, where the stale-path problem exists.
3. Add a `SessionStart` hook script that emits the instructions as additional context. Register it for start, resume, clear and compaction so the instructions survive compaction. It skips the behavioural instructions when the project still has `.claude/CLAUDE.extra.md`, and honours the override file's instruction switch. → verify: with a fixture project that has the legacy file, the hook emits no behavioural instructions.
4. Move the statusline scripts into `klaude-plugin/statusline/`. The copies under `.claude/toolbox/scripts/` stay until retirement and are checked identical.
5. In `klaude-plugin/scripts/set-plugin-root.sh`, use the script's parent directory as the plugin root when it sits under the toolbox home's `releases/`; otherwise keep the resolver. → verify: `test/test-cpr.sh` passes and a new case covers the toolbox-home branch.
6. Run `make generate-kodex` and the structure tests. Plugin prose must not reference repository documents.

## Claude launch layer

1. Create `kk/baseline/claude.json`: preferences (model, effort level, environment variables), the statusline script's path relative to the release, the default allow entries with a placeholder for the release directory, and the opt-in catalogue. Take the current values from `.claude/settings.json`.
2. Add `kk/baseline/claude/deny.json` as a generator target in `scripts/generate-guard.sh`, alongside the existing settings target.
3. Implement layer composition as described in [Launching Claude](design.md#launching-claude). Read the user, project and local settings files; leave out each preference key and each environment variable they already set; always include the denies. Add the Git-marketplace disablement only when that plugin ID is enabled in one of those files.
4. Implement the override file: its schema, the named settings file, the default switches and the opt-in grants. An override file that fails validation stops the launch with a message naming the problem; it is never silently ignored.
5. `kk claude` writes the layer to a file under the toolbox home and replaces itself with `claude --settings <file>` plus the adopter's arguments. `--print-layer` shows the layer without launching. When the adopter passes `--settings`, pass everything through and say so.

→ verify: unit tests for yielding per key and per variable, list composition, each override, the pass-through, and a malformed override file. → verify: on a real machine, a wrapped session shows the baseline model when none is set and the user's model when one is.

## Codex guard plugin

1. Create `kodex-guard/` with a legacy-format manifest named `kk-guard`, `hooks/hooks.json`, and the three adapters ported from `.codex/scripts/`. Copy the matchers from `.codex/hooks.json`. Hook commands locate their scripts through the plugin-root variable Codex provides.
2. Change the adapters' anchoring per [Guard changes](design.md#guard-changes): policy root from the hook's launch directory, payload directory for operands only. The capy registration check reads the workspace's `.codex/hooks.json`. Use the result of the launch-directory probe.
3. Extend `scripts/generate-guard.sh` with three targets: the engine copy in `kodex-guard/scripts/guard/`, `kk/baseline/codex/kk.rules`, and the deny list above. Keep the legacy targets. Update every freshness list that names generated paths: the Makefile, `generated-check.yml`, `release.yml`, `test/test-generate-guard.sh` and the generated-files section of `AGENTS.md`.
4. Extend the guard's protected paths with the toolbox home, the override file, the owned files under the Codex home, and Codex's plugin cache. Add path tokens for the three home directories the way the temp-directory token works, with tests in `test/guard/test_guard.py`. Regenerate the documentation table.
5. Add a `kk-guard` entry to the repository's Codex marketplace manifest so plugin-only Codex users can install the guard too.
6. Port the adapter cases from `test/test-codex-hooks.sh` to the new adapters and add anchoring cases: launch directory in one repository, payload directory in another, policy from the first. Update `test/test-codex-structure.sh`.

→ verify: the ported suite passes against the new adapters; a live run from a subdirectory enforces a rule added in the workspace's `.claude/kk-guard.json`.

## Codex baseline and launch

1. Create `kk/baseline/codex.json` with the profile keys from `.codex/config.toml`, excluding MCP server entries, and `kk/baseline/codex/bootstrap.md` with the tool-name mapping from `session-start.sh`.
2. Make the generated sub-agent definitions available in the payload at `kk/baseline/codex/agents/`, keeping `.codex/agents/` until retirement. Prefer one more target in the generator over a copy step, and extend the freshness check either way.
3. Write a JSON-to-TOML serialiser for the value shapes the baseline uses: scalars, arrays, nested tables and one long multi-line string. → verify: where the interpreter has a TOML parser, the output parses back to the input; this mirrors the fallback in `test/test-codex-structure.sh`.
4. Compose the profile: baseline keys, the adopter's Codex overrides, and developer instructions built from the behavioural instructions, the bootstrap text and the protected-files advisory rendered from the guard rules.
5. Install owned files at upgrade: the profile, the rules file after the [validation in the upgrade flow](design.md#upgrade-flow), and the sub-agent files under an owned filename prefix, removing owned files the release no longer ships.
6. `kk codex` adds the profile and replaces itself with `codex`. It passes through when the adopter names a profile. It refuses on the states in [Activation state](design.md#activation-state), and treats `exec` and `review` as non-interactive.

→ verify: unit tests for composition, serialisation, pruning and each refusal; `codex --profile kk debug prompt-input` on a real machine shows the instructions as a developer message.

## Codex activation and trust

1. Write the local Codex marketplace manifest with both plugins, in the format of the repository's `.agents/plugins/marketplace.json`.
2. Activation: add the marketplace and both plugins on first install; afterwards re-add the skills plugin when its version differs and the guard plugin only when its version differs. Compare the tree at the reported install path with the release.
3. Guard-change confirmation per the [upgrade flow](design.md#upgrade-flow), defaulting to no without a terminal.
4. Trust tracking with the mechanism found in the probes. Record *awaiting review* until the guard hooks are trusted. If no mechanism exists, end the state on the adopter's explicit acknowledgement and say that it is unverified.
5. Rollback for Codex, including a guard that differs between the two releases, and resumption of an interrupted activation.
6. Record the second [demonstration](design.md#verification): interrupt an upgrade during activation, roll back with the network disabled, and show a guarded action denied by the restored guard without a trust bypass.

→ verify: stub-based tests for each activation path; the recorded demonstration.

## Notice, mixed installs and live check

1. The launch notice per [Update notice](design.md#update-notice). The check must never delay or fail a launch.
2. Mixed-install detection for both tools from the vendors' plugin listings, reported by `kk status`. Offer removal of user-scope Git-marketplace installs through the vendor CLIs after confirmation. A tool with ambiguous active hooks does not reach *ready*.
3. `kk status --live`: one non-interactive session per tool attempts to read a decoy secret in a scratch directory. → verify: the output contains the guard's own denial text, not a sandbox or native refusal.

## CI gate and release workflow

1. Run the guard engine suite, the `kk` suite, the Codex adapter suite and the self-test cases in CI on the oldest and newest Python the runners offer.
2. Make the release and pre-release workflows run that gate before tagging.
3. Guard plugin version rule: the release workflow sets `kodex-guard`'s version to the release version only when the directory's contents, apart from the version field, differ from the previous stable tag. → verify: a dry run on a skills-only change leaves the guard manifest untouched.

## Migration

The removal logic goes into the sync script as one more migration, following the existing `needs_*` / `run_*` pattern and its `APPLY_MODE` gating.

1. Add an upstream marker that identifies the retirement release, and a migration that runs only when the target version carries it.
2. Hook registrations: fetch the template's hooks file at the repository's recorded version and remove from the downstream file each handler whose command string equals a toolbox handler there. Drop groups and events that become empty. Leave every other handler. This replaces the group-level substring filter for this purpose.
3. Settings and Codex config: use the fetched base to remove entries equal to what the template added, and keep the adopter's. Remove the Git-marketplace plugin enablement and marketplace registration.
4. Files: remove synced files identical to the template at the recorded version with substitutions applied. Report edited files and keep them. Remove the two toolbox import lines from the project instructions file when they match exactly.
5. Remove the sync infrastructure last.
6. The report states the team-wide effect in the words of [Legacy coexistence and migration](design.md#legacy-coexistence-and-migration).
7. `kk migrate`: check readiness for the tools the repository uses, run the pinned retirement release of the script in preview mode, ask, run it for real, and leave the changes uncommitted. Fetch the pinned script when the repository's own copy cannot hand off.

→ verify: fixtures in `test/test-template-sync.sh` for a repository with capy's hooks, an adopter-added hook, an edited synced file and a customised settings file. → verify: record the third demonstration on one of the maintainer's repositories.

## Documentation and ADR

1. Record the decision as `docs/adr/0014-machine-level-delivery.md`, citing the operative files.
2. Rewrite getting-started around the install command, keep plugin-only as a documented mode, and turn the template-sync guide into a migration guide.
3. Update the configuration guide: the launcher layer, overrides, the parity exceptions from the [parity ledger](design.md#parity-ledger), and `Skill(kk:*)` described as standing authorisation for model-initiated skill calls, including future skills.
4. Update the provider pages: for Codex, the guard plugin, hook review, profile precedence and the open-session caveat; for Claude, the unwrapped-session exception.
5. Document routing PAL's Claude client through `kk` so a launched reviewer can read review evidence.
6. Update `README.md`, `AGENTS.md`, the architecture and testing pages, and the plugin READMEs. Run the docs build.

## Retire the template

Only after the retirement release is tagged and the three demonstrations are recorded.

1. Remove the sync script, its workflow, the template cleanup script and workflow, the bootstrap script and the example state file, with their tests.
2. Remove the legacy generator targets and the generated copies kept for the transition.
3. Reduce the repository's own `.claude/` and `.codex/` to what an adopter's would hold, and run the repository on `kk`.
4. The maintainer turns off the repository's template flag.

## Final verification

Sufficient evidence is: the shell and Python suites and the Go tool tests pass; generated output is fresh; the three demonstrations are recorded with tool versions; and every row of the parity ledger marked kept or moved has been observed on a machine set up from scratch. Broaden verification if a probe result contradicted the design after dependent tasks were finished, or if a vendor release during the work changes hook, plugin or settings behaviour.
