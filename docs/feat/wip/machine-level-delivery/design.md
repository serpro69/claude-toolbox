# Machine-level delivery: retire template sync

> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)
> Status: draft — not yet reviewed
> Created: 2026-11-18

## Problem and outcome

claude-toolbox reaches consumer repositories through two channels. The `kk` plugins deliver skills, agents and the Claude permission guard. Everything else is copied into each repository by template sync: the Claude settings baseline, behavioural instructions, statusline scripts, and the whole Codex tree (config, hooks, guard runtime, rules, sub-agents).

Every copy needs a person to refresh it. A release that touches synced configuration is not delivered until someone runs sync in every repository, and the plugin half is a separate manual update on every machine. Releasing a version does not get adopters onto it.

The outcome is that configuration stops being copied into repositories. One adopter-run command per machine brings every repository on that machine to a release, validated before it takes effect, with a way back.

How might we make a toolbox release reach every adopter's terminal sessions, with the same experience, configuration and protections they get today, without anyone running a sync or editing config, and without a bad release locking everyone out?

## Size and lifetime

- **Cadence:** 72 tags since 2026-02-01, 59 of them stable, roughly two a week and ongoing.
- **Maintainer footprint:** seven synced repositories on one machine. Each config-touching release is seven syncs plus two plugin updates.
- **External footprint:** 155 stars, 30 forks, and the repository is a GitHub template. The number of repositories created from it is unknown.
- **Mechanism being replaced:** `.claude/toolbox/scripts/template-sync.sh`, about 2,650 lines with four migrations, a three-way settings merge and a self-handoff.

This is a recurring cost on a long-lived project. It justifies a real mechanism; it does not justify a compiled binary or a package channel.

## Success measures

1. **Per release:** an adopter gets the new version in every repository on a machine by running one upgrade on that machine. There are no per-repository steps and no config edits.
2. **Per new repository:** a repository on a set-up machine needs no toolbox step. Capy's own per-repository setup is outside this measure.
3. **Per new machine:** one install command, with no hand-edited settings.
4. **Parity:** every adopter-facing item in today's template has a named home or an explicit decision to drop it. See the [parity ledger](#parity-ledger).
5. **Bad release:** a broken guard or rules file is caught on the adopter's machine before it takes effect, and the adopter can return to the previous release offline.
6. **Upgrade churn:** adopters are told when a release exists and decide when to upgrade.

## Constraints

- `klaude-plugin/` stays the canonical source. Codex artifacts stay generated, with CI freshness checks.
- The guard keeps one rules declaration, fails closed on errors, and secrets stay non-loosenable.
- Plugin content references nothing outside the plugin tree.
- Toolbox writes only files it owns outright. The one-time [migration](#legacy-coexistence-and-migration) is the single exception.
- Vendor trust controls (Codex hook trust, Claude workspace trust) are worked with, never bypassed.
- Capy's per-repository setup stays capy's. Toolbox hooks keep yielding HTTP routing to capy's hooks when those are registered.
- Runtime dependencies stay `bash`, `python3` (3.8 or newer, standard library only), `jq` and `git`.
- macOS and Linux. Native Windows stays unsupported.
- `docs/feat/done/**` and the historical `dirs_to_remove` list in the sync script's plugin migration are not edited.

## Accepted decisions

| Decision | Rationale |
|---|---|
| Toolbox stops being a template | A per-repository copy always waits for a person |
| It does not become an orchestrator | Different job; the maintainer's fleet needs are met by tmux |
| A script CLI named `kk`, in a toolbox-owned directory, published from the same tag as the plugins | It must survive a bad plugin release and own recovery; a compiled binary and package channel add nothing needed |
| Validation happens at upgrade time, before activation | By launch time the vendor has already activated the plugin for every session, wrapped or not |
| Plugins install from a local marketplace that points at an immutable release directory | Activation and rollback are offline and use exactly the validated bytes |
| The Codex guard is its own plugin, untouched by skills-only releases | Codex fingerprints the whole plugin bundle for hook trust; a combined plugin would need re-review on every skill change |
| Launchers are thin: `kk codex` uses a Codex profile, `kk claude` passes a settings layer | No merge into user-owned files, no lag |
| Launcher values yield to anything the user or project set | Claude's flag layer outranks user, project and local settings |
| `Skill(kk:*)` is pre-approved by default, with opt-out | The workflow chains skills; documented as standing authorisation for model-initiated skill calls, including future skills |
| Default allow list is `Skill(kk:*)` and a read grant on the active release directory; `Bash(mkdir:*)` and `WebSearch` are opt-in; shell-read grants are dropped | Claude already permits `cat`, `grep`, `ls` and `sort` inside the working directory; outside it they are a blanket grant |
| Guard-changing Codex upgrades ask for confirmation, default no | An open session may lose enforcement; open sessions cannot be detected reliably |
| A launch notice announces newer releases, default on with opt-out | A manual command nobody is reminded to run recreates the original problem |
| Existing repositories migrate once with `kk migrate` | Legacy files cannot be retired by upgrading alone |

## Evidence and provenance

Probes ran on 2026-11-18 against Claude Code 2.1.296 and Codex CLI 0.169.0 in scratch directories. Three kinds of evidence back the design, and the difference matters when a claim is load-bearing.

**Observed in a probe**

- Claude: a model set only in a `--settings` file was used in place of the user-level model. Allow lists merged across the flag and project layers. `env` merged per variable with the flag layer winning.
- Claude: project `permissions.allow` entries are ignored in an untrusted workspace, even with `-p`.
- Claude: with no allow rules, `cat`, `grep`, `ls` and `sort` on files inside the working directory run without approval; `mkdir` and reads outside it do not.
- Codex: hooks bundled in a plugin with the legacy `.codex-plugin/plugin.json` manifest ran from the CLI. `SessionStart` ran; `PreToolUse` on `Bash` allowed and denied through exit 2 with a reason on stderr; the `Edit|Write` matcher intercepted `apply_patch`. `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` pointed at the plugin cache.
- Codex: a new plugin hook from a local marketplace was skipped without the trust bypass, and `codex exec` printed nothing about it.
- Codex: every `*.rules` file in `$CODEX_HOME/rules/` loaded; `forbidden` in one file beat `allow` in another; an invalid file made `codex exec` exit with "Error loading rules".
- Codex: a profile file `$CODEX_HOME/kk.config.toml` selected with `--profile kk` put its `developer_instructions` into the model-visible prompt as a developer message.

**Documented by the vendor**

- Claude settings precedence: managed, then `--settings`, then local, project, user. Lists merge.
- Claude: a plugin manifest has no field for permissions, env, model or statusline; a plugin-root `CLAUDE.md` is not loaded; a plugin `bin/` is on `PATH` only inside sessions.
- Claude: a plugin from a local-path marketplace loads in place, and refresh is skipped for local sources. `--plugin-dir` silently replaces a same-named installed plugin. Earlier cached versions are kept for 14 days.
- Claude: `claude plugin list --json` always reports `installPath`. `claude plugin validate` checks a plugin directory.
- Claude: `managed-settings.d/` fragments apply to the terminal, the IDE extensions and the desktop app's Code tab.
- Codex: `codex plugin add --json` reports `installedPath`. The cache layout is `plugins/cache/<marketplace>/<plugin>/<version>/`. Sub-agents load from `~/.codex/agents/`.

**Read from Codex source at `rust-v0.169.0`, not probed**

- Upgrading a plugin deletes older cached versions. A same-version reinstall also moves the existing directory aside.
- Plugin hook trust fingerprints the plugin bundle; a project hook is hashed by its declaration only. The plugin hook identity contains no repository path.
- Codex verifies the bundle before running a hook command. If the bundle is gone, the tool call proceeds.
- The hook process starts in the session's directory, while the payload carries the tool's working directory.
- On a rules parse failure the app-server path continues with an empty policy and a warning. The interactive TUI shows a "Hooks need review" prompt at startup.

The source-read claims shaped two decisions (the separate guard plugin and the confirmation on guard upgrades) and are the first [verification tasks](#verification).

The direction was pressure-tested in four turns with Codex on `gpt-6.2-astra`, which rejected the first proposal (a launcher shipped inside the plugin and validated at launch) and agreed with this one. It left one recorded disagreement: it would make `Skill(kk:*)` opt-in.

## Architecture

### Components

```
release tag
  ├─ klaude-plugin/     Claude plugin: skills, agents, guard hooks, instructions, statusline
  ├─ kodex-plugin/      Codex skills plugin (generated)
  ├─ kodex-guard/       Codex guard plugin: adapters, hooks, engine copy
  └─ kk/                CLI code, baseline declaration, self-test cases

adopter machine
  $KK_HOME/                         toolbox-owned
    bin/kk                          stable entry point
    state.json                      activation state
    releases/<version>/             immutable payloads
    .claude-plugin/marketplace.json local Claude marketplace
    .agents/plugins/marketplace.json  local Codex marketplace
  $CODEX_HOME/kk.config.toml        toolbox-owned Codex profile
  $CODEX_HOME/rules/kk.rules        toolbox-owned native forbids
  $CODEX_HOME/agents/kk-*.toml      toolbox-owned sub-agents
  <config dir>/kk/config.json       adopter-owned overrides
```

`$KK_HOME` defaults to `${XDG_DATA_HOME:-~/.local/share}/kk`. The override file lives at `${XDG_CONFIG_HOME:-~/.config}/kk/config.json`. `~/.local/bin/kk` is a symlink to `$KK_HOME/bin/kk`.

### Release payload

A release is the four directories above, taken from the tag. `kk` fetches the tag archive from the upstream repository, extracts only those directories into a staging directory, and never executes anything from a payload before validating it.

Two sources are supported: a tag on the upstream repository, and a local checkout given by path. The local source serves tests and lets the maintainer run unreleased work. The upstream repository is configurable so forks work.

Release directories are immutable once activated. `kk` keeps the active release, the previous one, and any release activated in the last 14 days, because a running session keeps reading the directory it started with.

### The `kk` command

| Command | Purpose |
|---|---|
| `kk upgrade` | Fetch, validate and activate a release. Also the first install. `--check` only reports whether a newer release exists |
| `kk rollback` | Re-activate the previous release, offline |
| `kk status` | Show the active release, per-tool state, pending review and mixed-install findings. `--live` runs one guarded action per tool |
| `kk claude`, `kk codex` | Start the vendor CLI with the toolbox layer |
| `kk migrate` | One-time retirement of legacy template files in the current repository |

The entry point `$KK_HOME/bin/kk` is deliberately small. It reads the state file and dispatches to the code of a release. `rollback`, `status` and the resumption of an interrupted upgrade always run from the last release that reached *ready*, never from a candidate. This is what lets recovery work when a candidate's own code is broken.

A one-line installer script at the repository root downloads the latest stable release and runs its `kk upgrade`.

### Activation state

State is tracked per tool, because an adopter may have only one vendor CLI.

| State | Meaning | Launcher behaviour |
|---|---|---|
| *staged* | Candidate fetched and validated; nothing on the machine has changed | Launches the active release |
| *activating* | Vendor installs or owned files are being written | `kk codex` refuses; `kk claude` warns |
| *awaiting review* | Activated, but Codex hooks changed and are not yet trusted | `kk codex` starts interactive sessions so the adopter can review, and refuses `codex exec` |
| *ready* | Activated and verified | Normal |

The state file records the active release, the previous release and any pending candidate with its phase. Every write to it and to an owned file is a write to a temporary file followed by a rename.

### Upgrade flow

1. **Fetch and stage.** Download the candidate, extract it to a staging directory, check the payload is complete and that its manifest versions agree.
2. **Validate, with nothing activated.**
   - Run the candidate guard against the self-test cases shipped in the payload, under the machine's own Python. This catches an engine that cannot run here.
   - Run `claude plugin validate` on the candidate Claude plugin.
   - Run `codex execpolicy check` over the candidate `kk.rules` together with every rules file that will remain in `$CODEX_HOME/rules/`, excluding the `kk.rules` being replaced. Check that a known forbidden command is forbidden.
3. **Confirm, when the guard changes.** If the candidate's Codex guard plugin version differs from the installed one, state that open Codex sessions may continue without the guard, and proceed only on confirmation. The default is no, including in non-interactive runs.
4. **Activate.** Record *activating*, then:
   - move the staged directory into `releases/`;
   - point both local marketplaces at it;
   - on first install, add the marketplaces and install the plugins at user scope;
   - re-add the Codex skills plugin; re-add the Codex guard plugin only when its version changed;
   - write the Codex profile, the rules file and the sub-agent files, removing owned sub-agent files the release no longer ships.
5. **Verify.** Compare the bytes at the path each vendor reports with the release. Read Codex hook trust; if the guard hooks are not trusted, record *awaiting review* and tell the adopter to review them with `/hooks`.
6. **Ready.** Record the release as active and the former one as previous, and replace the entry point if it changed.

A skills-only release leaves the Codex guard plugin alone: same plugin ID, same version, same cache directory. That is what keeps an open Codex session enforcing through it, and it applies to rollback as well.

### Rollback and interrupted upgrades

`kk rollback` repeats activation and verification with the previous release directory. It needs no network, because both vendors install from the local marketplace.

An upgrade interrupted in *activating* leaves a mixed installation. The next `kk` command reports it and offers two ways out: resume the upgrade, or roll back. `kk codex` refuses to start until one of them completes.

Rollback counts as recovery only once verification passes for the restored guard, including Codex trust.

### Launching Claude

`kk claude` composes one settings layer and starts `claude --settings <layer>` with the adopter's arguments. The layer contains:

- **Preferences** from the baseline (model, effort level, environment variables, statusline). Each key and each environment variable is left out when the user, project or local settings file already sets it. Those files are JSON, so the launcher can read them.
- **The native secret denies**, projected from the release's guard rules. Denies only tighten, so they are always included.
- **The default allow entries:** `Skill(kk:*)` and a read grant on the active release directory.
- **Disablement of the Git-marketplace copy** of the plugin, so a wrapped session in an unmigrated repository loads exactly one `kk` plugin.
- **The adopter's overrides**, applied last.

The statusline entry points at the script inside the active release. A session keeps the release it started with, so its hooks, its statusline and its read grant stay consistent across an upgrade.

If the adopter passes their own `--settings`, the launcher passes everything through unchanged and says so.

### Launching Codex

`kk codex` starts `codex --profile kk` with the adopter's arguments. The profile is `$CODEX_HOME/kk.config.toml`, written at upgrade from the baseline and the adopter's overrides. It carries the Codex defaults and the behavioural instructions as developer instructions.

The profile ranks above the base user config and below trusted project config. A repository's deliberate choice, such as an approval policy, therefore wins over the toolbox default; a value in `~/.codex/config.toml` does not. Adopters who want a different value put it in the override file. This asymmetry with Claude is a documented consequence of not parsing TOML under Python 3.8.

Before a `codex exec` run the launcher checks the recorded review state and refuses while hooks await review, because Codex would skip them without saying so.

### Overrides

The override file is the adopter's. It can:

- set or replace Claude settings keys, or name a settings file of the adopter's own to layer on top;
- set Codex profile keys;
- switch off individual defaults, including `Skill(kk:*)`, the statusline and the launch notice;
- switch on the opt-in grants `Bash(mkdir:*)` and `WebSearch`.

Codex overrides are written as JSON and serialised into the profile, so the launcher never needs to read TOML.

### Update notice

`kk claude` and `kk codex` print one line when a newer stable release exists. The check runs in the background, is cached for a day, prints only to an interactive terminal, and stays silent when offline. It can be switched off.

### Plugins

**Claude plugin (`klaude-plugin/`).** It keeps the guard hooks. It gains three things:

- The behavioural instructions as a plugin file, injected at `SessionStart`. The hook skips injection when the repository still has the legacy `.claude/CLAUDE.extra.md`, so an unmigrated repository does not receive two copies. Stepping aside is safe here because instructions are not a protection.
- The statusline scripts.
- A simpler plugin-root export: when the hook's own script sits under `$KK_HOME/releases/`, its parent directory is the plugin root. The existing resolver remains only for plugin-only installs.

**Codex skills plugin (`kodex-plugin/`).** Unchanged: generated skills and profiles, no hooks.

**Codex guard plugin (`kodex-guard/`).** New. It holds the three adapters, their hook registrations and a generated copy of the guard engine. Its version changes only in a release that changes its contents. Its hooks are the Codex enforcement boundary and need the adopter's review once per machine, then again whenever the bundle changes.

There is no Codex `SessionStart` hook. Instructions ride the profile, which avoids a hook whose trust every instruction edit would invalidate.

### Guard changes

- **Workspace anchoring.** The Codex adapters anchor policy to the session workspace: the git top level of the directory the hook process starts in, or that directory itself outside a repository. The payload's working directory is used only to resolve tool operands. Today's adapters derive the root from their own location, which would point into the plugin cache.
- **Self-protection.** The protected-path list gains the toolbox home, the override file, the owned files under `$CODEX_HOME`, and Codex's plugin cache. The rules format already supports a path token for the temp directory; these paths use the same mechanism.
- **Denial contract.** Unchanged: exit 2 with a reason on stderr, and adapter failures deny.
- **Capy.** The Bash adapter keeps its legacy HTTP routing and keeps yielding it when capy's own hook is registered in the workspace's `.codex/hooks.json`.

### Baseline declaration and generation

The baseline is data in `kk/baseline/`: Claude preferences and default grants, Codex profile keys, and the Codex bootstrap text. The behavioural instructions have one source, the plugin file, which the Codex profile also reads from the release.

Generated artifacts move with their consumers:

| Artifact | Today | After |
|---|---|---|
| Claude secret denies | `.claude/settings.json` | `kk/baseline/claude/deny.json` |
| Codex native forbids | `.codex/rules/default.rules` | `kk/baseline/codex/kk.rules` |
| Guard engine copy | `.codex/scripts/guard/` | `kodex-guard/scripts/guard/` |
| Codex sub-agents | `.codex/agents/*.toml` | `kk/baseline/codex/agents/*.toml` |

During the transition the generators write both sets, so template sync keeps working until it is retired.

### Install modes

- **Managed by `kk`.** The mode this design is about.
- **Plugin-only.** Installing from the Git marketplace keeps working for people who do not want `kk`. They get skills and the Claude guard with vendor-managed updates, and no launcher layer.
- **Mixed.** A machine with both is ambiguous about which hooks are active. `kk status` reports it, `kk` offers to remove the user-scope Git-marketplace installs through the vendor CLIs, and a tool does not reach *ready* while its active hooks are ambiguous.

The local marketplace is named `toolbox`, distinct from the Git marketplace `claude-toolbox`, so the two can be told apart.

### Legacy coexistence and migration

A repository still on the template keeps working after the machine moves to `kk`:

- **Both guards run.** The legacy project guard and the plugin guard both fire. Nothing steps aside, because a disabled or untrusted legacy entry would otherwise leave no guard running.
- **Duplicates persist.** The old rules file stays in force, and Codex sessions receive the instructions twice. These go stale but do not break.

`kk migrate` retires the legacy files in one repository:

- It refuses unless `kk` is *ready* on the machine for the tools the repository uses.
- It shows the full diff, applies only on confirmation, and leaves the result uncommitted.
- It removes only what matches known release contents. Hook registrations are compared one handler at a time by exact command string; a file the adopter edited is reported and left alone.
- It removes the Git-marketplace plugin enablement and the committed deny list, and the sync infrastructure itself. The adopter can decline individual parts.
- The diff states the team-wide effect: the change is committed, so a collaborator without `kk` loses the Codex guard and the deny list in that repository, and installing `kk` alone does not restore native denies to unwrapped Claude sessions.

The removal logic lives in one final release of the sync script, which already fetches the template at a repository's recorded version, applies its substitutions, and separates toolbox entries from downstream ones. Its three-way settings merge removes exactly what the template added once the upstream side is empty. `kk migrate` is a wrapper: it checks readiness, runs that script in preview mode, asks, then runs it for real. The retirement release is pinned by tag, so the script can later be deleted from the default branch.

### Retiring the template

After the retirement release, this repository stops being a template: the template flag, the cleanup workflow and the sync workflow go, the generators stop writing the legacy targets, and the repository's own `.claude/` and `.codex/` shrink to what an adopter's would hold. The repository then uses `kk` itself.

### Release safety

- **CI gate.** The guard engine suite, the `kk` tests and the self-test cases run in CI and block a release. Today no workflow runs the engine suite.
- **Stable by default.** `kk upgrade` and the launch notice consider stable tags only. Pre-releases need an explicit version.
- **Local validation.** The upgrade flow validates the candidate on the adopter's machine before activation.
- **Installation-level check.** `kk status --live` runs one non-interactive session per tool that attempts a guarded read of a decoy file and expects the guard's own denial text. CI cannot tell whether a vendor invoked the installed handler; this can.

## Protection guarantee

- The hook guard is the enforcement, for both tools.
- On Codex it requires the adopter's hook review. Until then a non-interactive run is unguarded apart from the native forbids, as it is today per repository. `kk` refuses such runs while it knows review is pending.
- A Codex session open during a guard upgrade may lose enforcement. The adopter is told and must confirm.
- Wrapped Claude sessions also carry the native secret denies.
- Unwrapped Claude sessions (IDE extension, desktop app, bare `claude`) have the hook guard only.

## Parity ledger

| Today | After | Status |
|---|---|---|
| Skills, agents, commands, profiles | Plugins | Unchanged |
| Claude guard hooks | Claude plugin | Unchanged |
| Codex guard hooks and runtime | Codex guard plugin | Moved |
| Codex native forbids | Owned rules file | Moved |
| Codex sub-agents | Owned agent files | Moved |
| Codex config defaults | Codex profile | Moved; outranks user config, yields to project config |
| Claude native secret denies | Launcher layer | Kept in wrapped sessions; **lost in unwrapped sessions** |
| Claude model, effort, env | Launcher layer | Kept in wrapped sessions; yields to user values |
| Statusline and themes | Plugin scripts plus launcher layer | Kept in wrapped sessions |
| Behavioural instructions, Claude | Plugin `SessionStart` | Kept everywhere the plugin loads |
| Behavioural instructions, Codex | Codex profile | Kept in wrapped sessions |
| `Skill(kk:*)`, read of plugin files | Launcher layer | Kept, with opt-out |
| `Bash(mkdir:*)`, `WebSearch` | Override file | **Opt-in** |
| `cat`, `grep`, `ls`, `sort` grants | — | **Dropped** |
| Temp-directory read for reviewers | PAL's Claude client routed through `kk` | Changed; one documented setting |
| Per-project manifest variables | Override file, or the repository's own settings | Changed |
| Version pinning, preview | `kk upgrade` with a version; *staged* state | Changed |
| Review of config changes by pull request | — | **Dropped**; the adopter reviews the release, not a diff |
| Per-repository `.claude/CLAUDE.<name>.md` extras injected into Codex | — | **Dropped**, pending the [open question](#open-questions) |
| Capy guidance injected when capy's hooks are absent | — | **Dropped**, pending the [open question](#open-questions) |

## Verification

Three demonstrations gate the retirement of template sync:

1. A Codex session opened before a skills-only upgrade still denies a guarded action afterwards, with the denial attributed to the guard.
2. An upgrade interrupted during activation is rolled back offline to a guard that the vendor runs and trusts.
3. A legacy repository migrates without a moment in which no guard is active, and the migration diff shows the team-wide effect.

Deterministic behaviour is covered by tests: layer composition, per-key yielding, profile serialisation, the state machine, payload extraction safety, and the adapters. Vendor behaviour is covered by recorded probes, which are evidence about one version and are labelled with it. A probe that cannot run limits the claim; it is neither a pass nor a failure.

## Assumptions

Each is a bet the design depends on, with the check that would confirm or break it.

1. A separate Codex guard plugin keeps its trust and stays loaded when only the skills plugin is re-added. This is the central promise; demonstration 1 tests it.
2. An open Codex session loses the guard after a guard-plugin upgrade. If a probe shows it stays guarded or blocks all guarded calls until restart, the confirmation becomes unnecessary or becomes a restart notice.
3. One Codex hook review covers every repository on the machine.
4. Codex starts the hook process in the session's directory and puts the tool's directory in the payload.
5. `codex --profile kk` ranks below trusted project config, and the profile accepts every baseline key.
6. Codex loads sub-agents from `$CODEX_HOME/agents/`, and the capy MCP matcher works from a plugin hook.
7. Codex hook trust can be read from outside a session. If it cannot, *awaiting review* ends on the adopter's acknowledgement instead.
8. Claude loads a local-marketplace plugin in place from the release directory, picks up a re-pointed marketplace at the next session start, and runs hook scripts from that directory.
9. Claude honours the statusline and the deny list from `--settings`, including in an untrusted workspace, and a `false` for a plugin ID in the flag layer disables a project-enabled plugin.
10. A Git-marketplace source behaves like the local one for Codex hook trust. The probe used a local source only.
11. The tag archive can be fetched and extracted with the Python 3.8 standard library, including the plugin's symlinks.

## Open questions

These are choices made while writing this document that the maintainer has not confirmed.

1. **Codex loses per-repository instruction extras.** Today's Codex `SessionStart` hook injects every `.claude/CLAUDE.<name>.md` in the repository. A machine-level profile cannot. The alternative is a `SessionStart` hook in the guard plugin whose script is stable and reads instruction text from the workspace, at the cost of putting non-guard behaviour in the trusted bundle.
2. **Capy's legacy guidance injection goes with that hook.** Capy 0.17.1 and later register their own hooks. Is requiring that version acceptable?
3. **Migration is hosted in the final sync release.** The alternative is new removal logic inside `kk`, which would have to reproduce the sync script's fetch and substitution to compare files exactly.
4. **Names and locations:** the command `kk`, the marketplace `toolbox`, the home under `~/.local/share/kk`, the override file under `~/.config/kk`.
5. **The Codex profile outranks `~/.codex/config.toml`,** including for `approval_policy` and `sandbox_mode`. The alternative is to leave security-relevant keys out of the baseline.

## Not Doing

- **Orchestrator or fleet features.** tmux covers this.
- **A Go binary or package-manager distribution.** A script CLI from the same tag is enough.
- **Built-in unattended upgrades.** A scheduler line running `kk upgrade` covers it.
- **Full parity for IDE, desktop, cloud and CI sessions.** They get the hook guard only.
- **Merging into user-owned config.** The migration is the only exception.
- **General shell-read allow grants.**
- **Reliable detection of open Codex sessions.**
- **A `kk uninstall` command.** Removal is documented as manual steps.
- **Native Windows, a per-repository stub for teammates, and changes to capy's setup.**

## Rejected Alternatives

- **Launcher inside the plugin behind a shim.** Validation ran after the vendor had activated the plugin, the launcher shared the plugin's fate, and it needed a resolver to find vendor cache paths.
- **Standalone Go CLI with an embedded baseline.** Its independence from the plugin is kept; the binary and the package channel are not needed for it.
- **Shell functions in the rc file.** They only govern callers that invoke them.
- **One combined Codex plugin.** Any skill change would force a fresh guard review.
- **`-c` overrides for the Codex baseline.** They overrule project config; the profile does not.
- **Plugin hooks stepping aside for legacy hooks.** A disabled legacy entry would leave no guard running.
- **A Git marketplace pinned to a tag.** It is not offline and does not guarantee the validated bytes.
- **A `SessionStart` hook that writes user-level config.** It applies one session late and needs a merge into user-owned files.
- **Keeping template sync, or becoming an orchestrator app.**

## Future improvements

- **System-level deny fragment.** An opt-in `managed-settings.d/` fragment would restore the native secret denies to every Claude surface on a machine. It needs administrator rights.
- **VS Code through `kk`.** The extension's `claudeProcessWrapper` setting may allow wrapped VS Code sessions. It needs a probe.
- **A reviewer-private evidence grant.** A read grant scoped to one review's bundle, in place of routing PAL's client through `kk`.
