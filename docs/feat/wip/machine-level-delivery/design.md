# Machine-level delivery: retire template sync

> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)
> Status: draft — revised after the [design review](review-design.md); see the [resolution](review-resolution.md)
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

1. **Per release:** an adopter gets the new version in every repository on a machine by running one upgrade on that machine. There are no per-repository steps and no config edits. For a repository still on the template this starts after its one-time [migration](#legacy-coexistence-and-migration); until then its committed settings keep outranking the machine defaults.
2. **Per new repository:** a repository on a set-up machine needs no toolbox step. Capy's own per-repository setup is outside this measure.
3. **Per new machine:** one install command, with no hand-edited settings.
4. **Parity:** every adopter-facing item in today's template has a named home or an explicit decision to drop it. See the [parity ledger](#parity-ledger).
5. **Bad release:** a broken guard or rules file is caught on the adopter's machine before it takes effect, and the adopter can return to the previous release offline, including when the new release's own command is broken.
6. **Upgrade churn:** adopters are told when a release exists and decide when to upgrade.

## Constraints

- `klaude-plugin/` stays the canonical source. Codex artifacts stay generated, with CI freshness checks.
- The guard keeps one rules declaration, fails closed on errors, and secrets stay non-loosenable.
- Plugin content references nothing outside the plugin tree.
- Toolbox writes only files it owns outright. Ownership means `kk` recorded installing that exact path; a filename or prefix that looks reserved does not establish it. The one-time [migration](#legacy-coexistence-and-migration) is the single exception.
- Vendor trust controls (Codex hook trust, Claude workspace trust) are worked with, never bypassed.
- Capy's per-repository setup stays capy's. Toolbox hooks keep yielding HTTP routing to capy's hooks when those are registered.
- Runtime dependencies stay `bash`, `python3` (3.8 or newer, standard library only), `jq` and `git`. The one-time migration also needs `curl` and Mike Farah's `yq`, as the sync script does today.
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
| The Codex guard is identified by its content, not its version string | A local checkout can change the bytes under an unchanged version, and identical bytes must not be reviewed twice |
| Rollback runs from the code of the release being restored | A release that reached *ready* must not be able to break the way back from itself |
| Codex native forbids are opt-in, off by default | In `$CODEX_HOME/rules/` they bind bare Codex in every repository and no project can loosen them |
| The Codex profile leaves approval and sandbox keys out by default | The profile outranks the machine owner's config and the launcher cannot yield to it per key |
| The adopter's own `--settings` is composed into the Claude layer, never passed through | Secrets stay non-loosenable in every wrapped session |
| A launch notice announces newer releases, default on with opt-out | A manual command nobody is reminded to run recreates the original problem |
| Existing repositories migrate once with `kk migrate` | Legacy files cannot be retired by upgrading alone |
| Retirement is a separate mode of the sync script; ordinary sync never retires, and later releases keep a tombstone at the script's path | Local sync and the downstream workflow both reach the apply path, and neither can check that a replacement guard is ready |
| Migration first syncs the repository to the retirement release, then removes against that one template | Every repository is compared with the same known template, rendered by the script that shipped with it, whatever version it was on |

## Evidence and provenance

Probes ran on 2026-11-18 against Claude Code 2.1.296 and Codex CLI 0.169.0 in scratch directories. Four kinds of evidence back the design, and the difference matters when a claim is load-bearing.

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
- A hook command that fails with any status other than 2 does not block the tool call.
- The hook process starts in the session's directory, while the payload carries the tool's working directory.
- On a rules parse failure the app-server path continues with an empty policy and a warning. The interactive TUI shows a "Hooks need review" prompt at startup.

The source-read claims shaped two decisions (the separate guard plugin and the confirmation on guard upgrades) and are the first [verification tasks](#verification).

**Read from this repository at `9c6bd133`**

- Sync: `--local` and the downstream workflow's `--apply` both reach `apply_changes`. Since v0.21.0 a run hands off to the target version's script before it changes anything other than its own manifest, where it may first rename the upstream repository and backfill default variables. The downstream workflow has fetched the target version's script before running since v0.5.0.
- Sync: the settings merge assigns the whole `permissions.deny` list from upstream and re-applies manifest-controlled keys after merging. The hook merge drops every downstream toolbox handler that upstream no longer has.
- The template's adopter defaults are no pinned Claude model and effort `high`. This repository's own `.claude/settings.json` pins a model and `xhigh`.
- The legacy Codex registrations run a script from the repository on every call.
- The guard's project secret patterns, such as `./**/.env`, are anchored at the session's workspace.
- The release and pre-release workflows call `.claude/toolbox/scripts/semver-compare.sh`.

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
    state.json                      activation state and installed paths
    lock                            writer lock
    releases/<version>/             immutable payloads, each with its own entry point
    .claude-plugin/marketplace.json local Claude marketplace
    .agents/plugins/marketplace.json  local Codex marketplace
  $CODEX_HOME/kk.config.toml        toolbox-owned Codex profile
  $CODEX_HOME/rules/kk.rules        toolbox-owned native forbids, only when switched on
  $CODEX_HOME/agents/kk-*.toml      toolbox-owned sub-agents
  <config dir>/kk/config.json       adopter-owned overrides
```

`$KK_HOME` defaults to `${XDG_DATA_HOME:-~/.local/share}/kk`. The override file lives at `${XDG_CONFIG_HOME:-~/.config}/kk/config.json`. `~/.local/bin/kk` is a symlink to `$KK_HOME/bin/kk`.

`$KK_HOME` is toolbox's alone. The symlink and the files under `$CODEX_HOME` sit in directories shared with the adopter, where a name such as `kk.rules` or a `kk-` prefix may already belong to someone else. The state file therefore records the exact path of every file `kk` installs outside `$KK_HOME`:

- Before activation, each destination is checked. A path that exists and is not in the record is a collision. `kk` names it, replaces nothing, and stops before anything on the machine changes.
- A path is recorded before it is written, so a run interrupted between the two does not meet its own file as a collision when it resumes.
- Pruning removes only recorded paths. It never matches by prefix, so an adopter's own `kk-notes.toml` in the agents directory is left alone.

### Release payload

A release is the four directories above, taken from the tag. `kk` fetches the tag archive from the upstream repository, extracts only those directories into a staging directory, and never executes anything from a payload before validating it.

Two sources are supported: a tag on the upstream repository, and a local checkout given by path. The local source serves tests and lets the maintainer run unreleased work. The upstream repository is configurable so forks work.

Release directories are immutable once activated. `kk` keeps the active release, the [rollback target](#activation-state), and any release that stopped being active in the last 14 days, because a running session keeps reading the directory it started with.

The 14 days run from the moment a release was superseded, not from its activation. A release can be active for a month and still have a session that started on it yesterday; deleting its directory would remove that session's hooks, and with them its guard. A session is supported for 14 days after its release was superseded and must be restarted after that.

### The `kk` command

| Command | Purpose |
|---|---|
| `kk upgrade` | Fetch, validate and activate a release. Also the first install. `--check` only reports whether a newer release exists |
| `kk rollback` | Re-activate the rollback target, offline |
| `kk status` | Show the active release, per-tool state, pending review and mixed-install findings. `--live` runs one guarded action per tool |
| `kk claude`, `kk codex` | Start the vendor CLI with the toolbox layer |
| `kk migrate` | One-time retirement of legacy template files in the current repository |

The entry point `$KK_HOME/bin/kk` is deliberately small. It reads the state file and dispatches to the code of a release. Which release depends on the command:

- **`rollback` runs from the release it restores.** After an interrupted upgrade that is the release still recorded as active, because the candidate never took over. Otherwise it is the rollback target. Either way that release's activation code has already activated it on this machine once, and nothing from the release being left is loaded. A release that reached *ready* therefore cannot break the way back from itself, even if its own dispatcher or rollback code is faulty.
- **Everything else runs from the active release,** including `status` and the resumption of an interrupted upgrade. A pending candidate's code runs only its own activation and verification. This is what lets recovery work when a candidate's own code is broken.

A promoted release may replace the stable entry point, so the entry point can be the broken part. Every release carries its own copy for that case: the adopter runs `$KK_HOME/releases/<version>/kk/bin/kk rollback` from the rollback target, and `kk upgrade` prints that command when it finishes. This path depends only on the target's directory and on the state file.

Running an older release's code for rollback means it reads a state file that a newer release wrote. The state file therefore carries a format version and changes only by addition: a release may add fields, but never renames or reinterprets the active release, the rollback target, the candidate and its phase, the per-tool states, the stop times or the installed-paths record. Code that rewrites the file keeps the fields it does not know. A release that has to break this raises the format version; its upgrade says before activation that earlier releases can no longer be rolled back to, and older code refuses a format version it does not know instead of guessing.

A one-line installer script at the repository root downloads the latest stable release and runs its `kk upgrade`. On a first install no release has reached *ready*, so the installer is also the recovery path: run again, it resumes from the journaled phase when the staged candidate is intact and starts over otherwise. Every activation step is safe to repeat.

### Activation state

One release is active for the whole machine, and both tools run it. A release becomes active once its files are in place and their bytes verify. What differs per tool after that is whether its guard is confirmed effective, so that is tracked per tool; an adopter may also have only one vendor CLI.

| State | Meaning | Launcher behaviour |
|---|---|---|
| *staged* | Candidate fetched and validated; nothing on the machine has changed | Launches the active release |
| *activating* | Vendor installs or owned files are being written | `kk codex` refuses; `kk claude` warns |
| *awaiting review* | Activated, but a Codex guard hook is untrusted or disabled | `kk codex` starts interactive sessions so the adopter can review, and refuses non-interactive runs |
| *unverified* | Activated; Codex hook trust cannot be read on this machine and the adopter acknowledged reviewing the hooks | `kk codex` starts; non-interactive runs print a one-line warning; `kk migrate` relies on the live check |
| *ready* | Activated and verified | Normal |

*Unverified* is never reported as *ready*. It exists only where [assumption 7](#assumptions) fails.

The state file records:

- the active release, and any pending candidate with its phase;
- the **rollback target**: the most recently active release, other than the active one, on which every installed tool reached *ready* (or *unverified*, on a machine where trust cannot be read). A release whose Codex guard never got past *awaiting review* is skipped. With A reviewed, B active and awaiting review, and then C activated, `kk rollback` from B or from C returns to A, the last release whose guard the adopter actually reviewed. When no retained release qualifies, the target is simply the release that was active before this one, and `kk rollback` says which tool's guard is not reviewed there. That is the normal case for an adopter who has Codex installed and never reviews its hooks; they still get a way back for Claude;
- when each retained release stopped being active;
- the paths installed outside `$KK_HOME`.

Every write to it and to an owned file is a write to a temporary file followed by a rename. That keeps each file readable but does not stop two commands from interleaving: a scheduled upgrade and a manual rollback could leave the marketplaces, the vendor installs and the state file describing different releases. `upgrade`, `rollback` and resumption therefore hold one exclusive lock on `$KK_HOME` for their whole run. A second writer exits at once and names the first. It is an operating-system file lock, released when its holder exits, so a crashed run leaves nothing stale. Launchers and `status` do not take it.

### Upgrade flow

The whole flow runs under the [writer lock](#activation-state).

1. **Fetch and stage.** Download the candidate, extract it to a staging directory, check the payload is complete and that its manifest versions agree. Two checks belong here because they need nothing but the staged files and the state file:
   - compute the candidate guard's [content identity](#plugins). A tagged candidate that carries the installed guard's version with different content fails here. A local checkout has its staged guard version set from the identity instead;
   - check every destination outside `$KK_HOME` for a [collision](#components).
2. **Validate, with nothing activated.**
   - Run the candidate guard against the self-test cases shipped in the payload, under the machine's own Python. This catches an engine that cannot run here.
   - Send a tool event through each guard handler the way the staged plugin registers it: take the handler command from the staged hook registration of the Claude plugin and of the Codex guard plugin, point the plugin-root variable at the staged directory, and expect a denial for a secret read and a pass for a harmless command. Calling the engine directly would miss a mispackaged adapter or a registration that names the wrong script.
   - Run `claude plugin validate` on the candidate Claude plugin.
   - When the [native forbids](#codex-native-forbids) are switched on, check the candidate `kk.rules` in two steps with `codex execpolicy check`. First on its own: every command the file is meant to forbid is forbidden. Then together with every rules file that will remain in `$CODEX_HOME/rules/`, excluding the `kk.rules` being replaced: the combined set still loads. Checked only together, an incomplete candidate could pass on a forbid that someone else's file supplies.

   These are local claims about the packaged guard. Whether the vendor trusts and calls the installed handler is established after activation.
3. **Confirm, when the guard changes.** If the candidate's Codex guard content identity differs from the installed one, state that open Codex sessions may continue without the guard, and proceed only on confirmation. The default is no, including in non-interactive runs.
4. **Activate.** Record *activating*, then:
   - move the staged directory into `releases/`;
   - point both local marketplaces at it;
   - on first install, add the marketplaces and install the plugins at user scope;
   - re-add the Codex skills plugin; re-add the Codex guard plugin only when its content identity changed;
   - write the Codex profile, the sub-agent files and, when switched on, the rules file, recording each path before writing it; remove recorded paths the release no longer ships.
5. **Verify.** Compare the bytes at the path each vendor reports with the release. Read trust and enablement for each Codex guard handler; if any is untrusted or disabled, the Codex state is *awaiting review* and the adopter is told to review the hooks with `/hooks`.
6. **Promote.** Record the release as active with each tool's state, stamp the superseded release with the time it stopped being active, recompute the rollback target, and replace the entry point if it changed.

A skills-only release leaves the Codex guard plugin alone: same plugin ID, same version, same cache directory. That is what keeps an open Codex session enforcing through it, and it applies to rollback as well.

### Rollback and interrupted upgrades

`kk rollback` repeats activation and verification with the [rollback target](#activation-state), running that release's own code. It needs no network, because both vendors install from the local marketplace, and it does not need the active release's command to work (see [the `kk` command](#the-kk-command)).

An upgrade interrupted in *activating* leaves a mixed installation. The next `kk` command reports it and offers two ways out: resume the upgrade, or roll back to the release that is still recorded as active, using that release's code. `kk codex` refuses to start until one of them completes. An interrupted first install has nothing to roll back to; re-running the installer completes it.

Rollback counts as recovery for a tool only once verification passes for that tool's restored guard, including Codex trust. Whether trust given to an earlier guard survives a later one being installed is [assumption 14](#assumptions); if it does not, a rollback across a guard change ends in *awaiting review* until the adopter reviews the hooks again.

### Launching Claude

`kk claude` composes one settings layer and starts `claude --settings <layer>` with the adopter's arguments. The layer contains:

- **Preferences** from the baseline (effort level, environment variables, statusline). The baseline pins no model, as the template's defaults do not. Each key and each environment variable is left out when the user, project or local settings file already sets it. Those files are JSON, so the launcher can read them.
- **The native secret denies**, projected from the release's guard rules. Denies only tighten, so they are always included, and nothing composed after them can take one out.
- **The default allow entries:** `Skill(kk:*)` and a read grant on the active release directory.
- **Disablement of the Git-marketplace copy** of the plugin, so a wrapped session in an unmigrated repository loads exactly one `kk` plugin.
- **The adopter's overrides**, applied last. They set or replace preference keys and add to permission lists.

The statusline entry points at the script inside the active release. A session keeps the release it started with, so its hooks, its statusline and its read grant stay consistent across an upgrade.

If the adopter passes their own `--settings`, a file or inline JSON, the launcher reads it and composes it as the top of the same layer under the same rule: its keys win, its permission entries are added, and the generated denies stay. A value that cannot be read or parsed stops the launch. There is no pass-through. A wrapped session always carries the denies; an adopter who wants Claude without the toolbox layer runs `claude` directly, which is an unwrapped session and is described as one.

### Launching Codex

`kk codex` starts `codex --profile kk` with the adopter's arguments. The profile is `$CODEX_HOME/kk.config.toml`, written at upgrade from the baseline and the adopter's overrides. It carries the Codex defaults and the behavioural instructions as developer instructions.

The profile ranks above the base user config and below trusted project config. A repository's deliberate choice therefore wins over the toolbox default; a value in `~/.codex/config.toml` does not. This asymmetry with Claude is a documented consequence of not parsing TOML under Python 3.8: the launcher cannot see what the machine owner set, so it cannot yield to it per key.

For that reason the baseline leaves out the keys that decide what Codex may do without asking: `approval_policy`, `approvals_reviewer` and `sandbox_mode`. A profile carrying them would loosen a stricter owner setting, or tighten a looser one, in every wrapped session without the owner having chosen it. They stay whatever the machine owner set. An adopter who wants the template's former `on-request` and `read-only` posture switches it on in the override file. The remaining keys (model, reasoning effort, context limits, instruction budget, TUI settings) still outrank the base user config, and adopters who want a different value put it in the override file.

Before a non-interactive run (`exec`, `review`) the launcher re-reads trust and enablement for the guard's handlers. It does not rely on the state recorded at upgrade, because the adopter can disable or un-trust a hook at any time afterwards. It refuses when a handler is untrusted or disabled, because Codex would skip it without saying so. In the *unverified* state it warns in one line and proceeds.

### Overrides

The override file is the adopter's. It can:

- set or replace Claude preference keys and add permission entries, or name a settings file of the adopter's own to layer on top;
- set Codex profile keys;
- switch off individual defaults, including `Skill(kk:*)`, the statusline and the launch notice;
- switch on the opt-in grants `Bash(mkdir:*)` and `WebSearch`;
- switch on the Codex [native forbids](#codex-native-forbids), and the Codex approval and sandbox defaults.

No override, and no settings file named in one, removes a generated secret deny.

Codex overrides are written as JSON and serialised into the profile, so the launcher never needs to read TOML.

### Update notice

`kk claude` and `kk codex` print one line when a newer stable release exists. The check runs in the background, is cached for a day, prints only to an interactive terminal, and stays silent when offline. It can be switched off.

### Plugins

**Claude plugin (`klaude-plugin/`).** It keeps the guard hooks. It gains three things:

- The behavioural instructions as a plugin file, injected at `SessionStart`. The hook skips injection when the repository still has the legacy `.claude/CLAUDE.extra.md`, so an unmigrated repository does not receive two copies. Stepping aside is safe here because instructions are not a protection.
- The statusline scripts.
- A simpler plugin-root export: when the hook's own script sits under `$KK_HOME/releases/`, its parent directory is the plugin root. The existing resolver remains only for plugin-only installs.

**Codex skills plugin (`kodex-plugin/`).** Unchanged: generated skills and profiles, no hooks.

**Codex guard plugin (`kodex-guard/`).** New. It holds the three adapters, their hook registrations and a generated copy of the guard engine. Its hooks are the Codex enforcement boundary and need the adopter's review once per machine, then again whenever the bundle changes.

The guard's *identity* is its content: a digest over the path, mode and bytes of every file in the bundle, leaving out the manifest's version field. `kk` uses that identity, not the version string, to decide whether to reinstall the guard, whether to ask for confirmation, and what a rollback must restore. Codex names the plugin's cache directory after the version, so version and content are kept in step by three rules:

- The release workflows give the guard a new version only when its identity differs from the nearest earlier tag, pre-release or stable. A release candidate and the stable release that follows it share one guard version when the bytes are the same, so candidates are not reviewed twice.
- For a local checkout, `kk` sets the staged copy's guard version from its identity: the installed guard's version when the identity matches the installed guard, and a digest stamp otherwise. An unchanged guard is then byte-identical to the installed one and is left alone, and edited guard code never reuses a published version.
- A tagged candidate whose guard carries the installed version with different content fails staging, before anything changes.

There is no Codex `SessionStart` hook. Instructions ride the profile, which avoids a hook whose trust every instruction edit would invalidate.

### Codex native forbids

`kk.rules` carries the generated native forbids: `rm`, `shred`, `sudo`, `su` and `doas`. Today they live in each templated repository, where a repository can exclude the file from sync and edit it. In `$CODEX_HOME/rules/` they would apply to every Codex session of the account: bare `codex`, repositories that never used the template, and repositories that had excluded the file. A forbid there cannot be loosened by a project's allow rule, and it has no temporary-directory exemption, so an ordinary `rm` is refused everywhere.

That is a wider effect than the per-repository file had, so it is the adopter's choice. The rules file is off by default and switched on in the override file. `kk upgrade` states the effect above when it first installs the file, and removes the file when the switch is turned off.

With the switch off, the hook guard is the only Codex protection on the machine. It already denies destructive commands, with the exemptions and user exceptions the forbids lack. What is given up is the backstop for a session whose hooks are not yet reviewed. A repository that wants to keep its own rules file declines that part of the [migration](#legacy-coexistence-and-migration).

### Guard changes

- **Workspace anchoring.** The Codex adapters anchor policy to the session workspace: the git top level of the directory the hook process starts in, or that directory itself outside a repository. The payload's working directory is used only to resolve tool operands. Today's adapters derive the root from their own location, which would point into the plugin cache.
- **Self-protection.** The protected-path list gains the toolbox home, the override file, the owned files under `$CODEX_HOME`, and Codex's plugin cache. The rules format already supports a path token for the temp directory; these paths use the same mechanism.
- **Denial contract.** Unchanged: exit 2 with a reason on stderr, and adapter failures deny.
- **Capy.** The Bash adapter keeps its legacy HTTP routing and keeps yielding it when capy's own hook is registered in the workspace's `.codex/hooks.json`.

### Baseline declaration and generation

The baseline is data in `kk/baseline/`: Claude preferences and default grants, Codex profile keys, the opt-in catalogue for both tools, and the Codex bootstrap text. The behavioural instructions have one source, the plugin file, which the Codex profile also reads from the release.

The Claude preferences are the template's adopter defaults, the values the template cleanup script renders when given no options: no pinned model and effort `high`. This repository's own `.claude/settings.json` pins a model and `xhigh`; those are the maintainer's settings and are not the baseline. The maintainer keeps them through the override file like any adopter.

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
- **Committed settings keep winning.** The repository's committed model, effort, statusline and Codex config still outrank the machine defaults, in wrapped sessions too. One upgrade per machine reaches such a repository only after it migrates.
- **Ordinary sync keeps working and never retires anything.** See [ordinary sync](#ordinary-sync-and-the-tombstone) below.

#### What `kk migrate` does

`kk migrate` retires the legacy files in one repository.

- **It checks that the replacement guard works now.** State recorded at upgrade is not enough: a hook can be disabled later, and *unverified* was never confirmed. For each tool the repository uses, it re-reads hook trust and enablement where they can be read, asking for this repository when the mechanism takes a workspace, and it runs the [live check](#release-safety). It refuses otherwise. The live check runs in a scratch workspace, not in the repository, for two reasons. In an unmigrated repository the legacy guard and the plugin guard both fire and print the same denial, so a denial seen there could not be credited to the installed handler. And the guard's secret patterns are anchored at the workspace, so the decoy has to sit inside the workspace the session starts in. What the scratch check cannot see is a setting that switches the plugin's hooks off for this one repository; the trust read covers that where Codex reports it per workspace.
- **It tells the adopter to close older Codex sessions first.** A Codex session in this repository that started before `kk` was installed and its hooks reviewed loaded only the legacy registration. That registration runs a script from the repository on every call. Once migration deletes the script, the hook fails and Codex lets the call through. Open sessions cannot be detected, so `kk migrate` states this and asks, default no. Sessions started after `kk` became *ready* loaded the plugin guard and stay guarded.
- **It works in two steps, each previewed and confirmed.** First it syncs the repository to the retirement release with an ordinary sync. Then it removes, comparing against that release's template. Declining the second step leaves a repository that is simply up to date and still guarded. The result is left uncommitted.
- It removes only what the [removal rules](#removal-rules) allow. The adopter can decline individual parts, for example to keep the repository's own Codex rules file, its Codex sandbox and approval settings, or the plugin enablement that a cloud session relies on.
- **The diff states the team-wide effect.** The change is committed, so it reaches everyone who uses the repository:
  - a collaborator without `kk` loses the Codex guard and the deny list in that repository;
  - a host with no `kk` install that relied on the committed plugin enablement, such as a cloud session or a fresh CI runner, no longer gets the plugin at all;
  - installing `kk` alone does not restore native denies to unwrapped Claude sessions;
  - the repository's Codex native forbids go, and return only on machines that switched on the account-wide rules file;
  - the repository's Codex sandbox, approval policy and approvals reviewer go with its config. Sessions there then follow each machine's own Codex config, which may be looser than the template's `read-only` and `on-request`. The report states this separately from the diff.

#### Removal rules

The removal logic lives in one final release of the sync script, as a separate mode. It compares the repository with one template only: the retirement release's own, rendered with the repository's manifest by the script that shipped with it. The sync step before it is what makes that enough. Comparing each repository with the template at whatever version it last synced would mean rendering old layouts, from before four migrations, with a script that never produced them.

**The sync step** is an ordinary sync to the retirement tag and behaves as one:

- It runs the script's existing migrations and three-way settings merge, so the repository ends up on the final template with its customisations merged as on any sync.
- It overwrites edits the adopter made to synced files, as every sync does. The preview lists them as modified. An adopter who wants to keep one copies it out or adds it to `sync_exclusions` before confirming.
- It differs from an ordinary sync in one respect. A normal sync replaces the whole deny list with the template's, which would drop a deny the adopter added before the removal step could see it. `kk migrate` asks the script to merge the deny list three-way like every other list, so the adopter's own entries survive the step.

**The removal step** does not use the settings merge at all. That merge re-applies the manifest-controlled keys after merging, so against an empty upstream it could not tell an adopter's choice from a template default. Removal compares each entry with the rendered template and only removes:

- **An entry equal to what the retirement template supplies is removed.** A deny entry the template does not ship stays. Hook registrations are compared one handler at a time by exact command string.
- **A file identical to the retirement template is removed.** After the sync step that is every synced file the adopter has not excluded. A file that still differs is reported and left alone.
- **A value chosen through a manifest variable is the adopter's.** The Claude model, effort and permission mode, and the Codex model and approval policy, are kept as the repository's own settings and listed in the report, unless the manifest holds no value or the script's built-in default. The report says they will keep outranking the machine defaults. The statusline choice is listed too, but its entry is removed because the script it points at is.
- **Anything under `sync_exclusions` is not touched,** by either step. The adopter took those files out of the template's hands.
- **If the template cannot be fetched, nothing is removed** and the run stops.

`kk migrate` is a wrapper around the two steps. It fetches the script and its helper file from the retirement tag into a temporary directory and runs them from there with the script's self-update switched off. It depends on neither the repository's own copy of the script nor the default branch. It checks for `curl` and `yq` first and says they are needed for this step only. The retirement tag is a constant in `kk`, with a command-line override so that the [pilot](#verification) can run against a release candidate.

#### Ordinary sync and the tombstone

Both ways of running an ordinary sync reach the script's apply path: `--local` on a developer's machine, and the downstream workflow's `--apply`, which opens a pull request. Neither can know whether a replacement guard works on anyone's machine. So removal is never a side effect of syncing:

- **Against the retirement release,** every existing mode behaves as it always has. The legacy installation is brought up to date and the run prints one notice that points at `kk migrate`. Only the separate retirement mode removes anything.
- **Against later releases,** the script's path holds a tombstone. Sync scripts since v0.21.0 hand over to the target version's script before they change anything but their own manifest, and the downstream workflow has fetched that script before running since v0.5.0. The tombstone explains the migration, changes nothing, and reports no changes in CI, so no pull request is opened.

The tombstone is why the script is not simply deleted after retirement. With no script to hand over to, an older script would carry on against the shrunken tree, and its own merges would strip the deny list and the legacy Codex guard registrations from a repository nobody had checked. A local run of a script older than v0.21.0 does not hand over and is not protected; the migration guide tells those adopters not to sync past the retirement release.

### Retiring the template

Retirement waits for the [pilot](#verification) of the tagged retirement release. After that release, this repository stops being a template: the template flag, the cleanup workflow and the sync workflow go, the sync script is replaced by its [tombstone](#ordinary-sync-and-the-tombstone), the generators stop writing the legacy targets, and the repository's own `.claude/` and `.codex/` shrink to what an adopter's would hold. The repository then uses `kk` itself.

### Release safety

- **CI gate.** The guard engine suite, the `kk` tests and the self-test cases run in CI and block a release. Today no workflow runs the engine suite.
- **Stable by default.** `kk upgrade` and the launch notice consider stable tags only. Pre-releases need an explicit version.
- **Local validation.** The upgrade flow validates the candidate on the adopter's machine before activation.
- **Installation-level check.** `kk status --live` runs one non-interactive session per tool that attempts a guarded read of a decoy file and expects the guard's own denial text. CI cannot tell whether a vendor invoked the installed handler; this can. `kk migrate` runs the same check before it removes anything.

## Protection guarantee

- The hook guard is the enforcement, for both tools, on a host where the plugin is installed, enabled and loaded. A user-level install does not reach a cloud session or a fresh CI runner; those have no toolbox guard unless the repository still enables the plugin for them.
- On Codex it requires the adopter's hook review. Until then a non-interactive run is unguarded. The native forbids cover it only on a machine that switched them on. `kk` refuses such runs when it reads a guard hook as untrusted or disabled.
- A Codex session open during a guard upgrade may lose enforcement. The adopter is told and must confirm.
- A Codex session opened before `kk` was installed loses its guard when its repository is migrated. The adopter is told to close such sessions and must confirm.
- Wrapped Claude sessions also carry the native secret denies, whatever settings file or override the adopter adds.
- Unwrapped Claude sessions (IDE extension, desktop app, bare `claude`) have the hook guard only.

## Parity ledger

| Today | After | Status |
|---|---|---|
| Skills, agents, commands, profiles | Plugins | Unchanged |
| Claude guard hooks | Claude plugin | Unchanged |
| Codex guard hooks and runtime | Codex guard plugin | Moved |
| Codex native forbids, per repository, with exclusion from sync as the way to change them | Owned rules file for the whole account | **Opt-in**. When on, it also binds bare Codex and unrelated repositories, and no project can loosen it. The per-repository control is replaced by one machine switch, or by keeping the repository's own file at migration |
| Codex sub-agents | Owned agent files | Moved |
| Codex model, reasoning effort, limits, TUI defaults | Codex profile | Moved; outranks user config, yields to project config |
| Codex approval policy, approvals reviewer, sandbox mode | Override file | **Opt-in**; the machine owner's config governs by default. Migration removes them from the repository unless the adopter declines that part, or chose the approval policy in the manifest |
| Claude native secret denies | Launcher layer | Kept in wrapped sessions, including with the adopter's own `--settings`; **lost in unwrapped sessions** |
| Claude effort, env | Launcher layer | Kept in wrapped sessions; yields to user values. The baseline is the template default, effort `high` |
| Claude model | — | Unchanged for default adopters, whose template pinned none. A model chosen in the manifest stays in the repository's settings at migration |
| Plugin enabled by committed project settings, reaching hosts with no local install | — | **Dropped** at migration unless the adopter declines that part |
| Statusline and themes | Plugin scripts plus launcher layer | Kept in wrapped sessions |
| Behavioural instructions, Claude | Plugin `SessionStart` | Kept everywhere the plugin loads |
| Behavioural instructions, Codex | Codex profile | Kept in wrapped sessions |
| `Skill(kk:*)`, read of plugin files | Launcher layer | Kept, with opt-out |
| `Bash(mkdir:*)`, `WebSearch` | Override file | **Opt-in** |
| `cat`, `grep`, `ls`, `sort` grants | — | **Dropped** |
| Temp-directory read for reviewers | PAL's Claude client entry runs `kk claude` and keeps the scoped temp-directory read grant it documents today | Changed; one documented client entry. `kk claude` supplies the read of the review criteria in the release directory. The review diff is written with `mktemp` outside it and still needs its own grant |
| Per-project manifest variables | Override file, or the repository's own settings | Changed; migration keeps non-default choices in the repository and reports them |
| Version pinning, preview | `kk upgrade` with a version; *staged* state | Changed |
| Review of config changes by pull request | — | **Dropped**; the adopter reviews the release, not a diff |
| Per-repository `.claude/CLAUDE.<name>.md` extras injected into Codex | — | **Dropped**, pending the [open question](#open-questions) |
| Capy guidance injected when capy's hooks are absent | — | **Dropped**, pending the [open question](#open-questions) |

## Verification

Four demonstrations gate the retirement of template sync:

1. A Codex session opened before a skills-only upgrade still denies a guarded action afterwards, with the denial attributed to the guard.
2. An upgrade interrupted during activation is rolled back offline to a guard that the vendor runs and trusts.
3. A legacy repository migrates without a moment in which no guard is active for any session started after `kk` became *ready*, and the migration diff shows the team-wide effect. The run includes a Codex session opened before `kk` was installed and records what happens to it.
4. A release is promoted, its own command is made unavailable, and the previous release is restored offline. Demonstration 2 covers a candidate that never became active; this covers the release that did.

**Pilot.** Scratch marker plugins settle vendor mechanics early, but they are not what adopters install. Before the template is retired, the tagged retirement payload is piloted on a machine set up from scratch and on one legacy repository. A release candidate tag is enough. The pilot repeats the demonstrations with the shipped adapters, marketplace names and migration entry points, observes every parity row marked kept or moved, and confirms that an ordinary sync against the candidate leaves the legacy guard intact. Retirement removes the generators and the template flag and is not cheaply undone, so the pilot comes first.

Deterministic behaviour is covered by tests: layer composition, per-key yielding, profile serialisation, the state machine, the writer lock, collision checks and record-based pruning, payload extraction safety, the adapters, the removal rules, and ordinary sync never retiring from either entry point. Vendor behaviour is covered by recorded probes, which are evidence about one version and are labelled with it. A probe that cannot run limits the claim; it is neither a pass nor a failure.

## Assumptions

Each is a bet the design depends on, with the check that would confirm or break it.

1. A separate Codex guard plugin keeps its trust and stays loaded when only the skills plugin is re-added. This is the central promise; demonstration 1 tests it.
2. An open Codex session loses the guard after a guard-plugin upgrade. If a probe shows it stays guarded or blocks all guarded calls until restart, the confirmation becomes unnecessary or becomes a restart notice.
3. One Codex hook review covers every repository on the machine.
4. Codex starts the hook process in the session's directory and puts the tool's directory in the payload.
5. `codex --profile kk` ranks below trusted project config, and the profile accepts every baseline key.
6. Codex loads sub-agents from `$CODEX_HOME/agents/`, and the capy MCP matcher works from a plugin hook.
7. Codex hook trust and per-hook enablement can be read from outside a session, quickly enough to do before each non-interactive launch, and the result reflects a hook the adopter disabled after trusting it. If it cannot be read, the adopter's acknowledgement moves the tool to *unverified*, never to *ready*.
8. Claude loads a local-marketplace plugin in place from the release directory, picks up a re-pointed marketplace at the next session start, and runs hook scripts from that directory.
9. Claude honours the statusline and the deny list from `--settings`, including in an untrusted workspace, and a `false` for a plugin ID in the flag layer disables a project-enabled plugin.
10. A Git-marketplace source behaves like the local one for Codex hook trust. The probe used a local source only.
11. The tag archive can be fetched and extracted with the Python 3.8 standard library, including the plugin's symlinks.
12. When the script behind a project hook disappears under an open Codex session, the hook fails and the call proceeds unguarded. This is read from source, not probed. If a probe shows the call is blocked instead, the warning before migration becomes a restart notice.
13. Codex accepts a digest-stamped version string as a plugin version and as a cache directory name. If it does not, local checkouts need another way to keep version and content in step.
14. Codex accepts re-adding an earlier version of a plugin over a later one, and trust given to a guard bundle is still there when the same bytes come back after another bundle was installed in between. Rollback depends on the first. If the second fails, a rollback across a guard change needs the adopter's review before it counts as recovery, and demonstrations 2 and 4 record that review.

## Open questions

These are choices made while writing this document that the maintainer has not confirmed.

1. **Codex loses per-repository instruction extras.** Today's Codex `SessionStart` hook injects every `.claude/CLAUDE.<name>.md` in the repository. A machine-level profile cannot. The alternative is a `SessionStart` hook in the guard plugin whose script is stable and reads instruction text from the workspace, at the cost of putting non-guard behaviour in the trusted bundle.
2. **Capy's legacy guidance injection goes with that hook.** Capy 0.17.1 and later register their own hooks. Is requiring that version acceptable?
3. **Migration is hosted in the final sync release,** as a separate mode that runs after a sync to that release. The alternative is new removal logic inside `kk`, which would have to reproduce the sync script's fetch and substitution to compare files exactly.
4. **Names and locations:** the command `kk`, the marketplace `toolbox`, the home under `~/.local/share/kk`, the override file under `~/.config/kk`.

Closed on 2026-11-18 by the maintainer: the Codex profile leaves `approval_policy`, `approvals_reviewer` and `sandbox_mode` out by default, and the Codex native forbids are opt-in. Both are recorded under [accepted decisions](#accepted-decisions).

## Not Doing

- **Orchestrator or fleet features.** tmux covers this.
- **A Go binary or package-manager distribution.** A script CLI from the same tag is enough.
- **Built-in unattended upgrades.** A scheduler line running `kk upgrade` covers it. The writer lock keeps it from interleaving with a manual command.
- **Full parity for IDE, desktop, cloud and CI sessions.** IDE and desktop sessions on a set-up machine get the hook guard only. Cloud sessions and fresh CI runners get nothing from a user-level install.
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
- **Retirement as one more sync migration.** Migrations run on every sync that applies, from a local run and from the downstream workflow, with no check that a replacement guard is ready.
- **Deleting the sync script after retirement.** Older scripts would then sync against the shrunken tree and strip the legacy guard themselves.
- **Reusing the three-way settings merge for the removal step.** It replaces the whole deny list and re-applies manifest-controlled keys, so it cannot remove only what the template added.
- **Removing against the template at each repository's recorded version.** The script has never rendered old template layouts, and a recorded branch name or short SHA cannot be fetched at all. Syncing to the retirement release first gives every repository the same base.
- **Running the migration's live check inside the repository.** Both guards fire there with the same denial text, and a decoy outside the workspace does not match the guard's secret patterns.
- **Rollback driven by the active release.** A fault in that release's dispatcher or rollback code would strand the machine with the previous release intact on disk.
- **Passing the adopter's `--settings` through unchanged.** A session the adopter thinks of as wrapped would start without the native denies.
- **Account-wide native forbids and approval or sandbox defaults for everyone.** They change what Codex does in repositories and sessions that never asked for toolbox.
- **Owning files by name or prefix.** A path in a shared directory may already be someone else's.

## Future improvements

- **System-level deny fragment.** An opt-in `managed-settings.d/` fragment would restore the native secret denies to every Claude surface on a machine. It needs administrator rights.
- **VS Code through `kk`.** The extension's `claudeProcessWrapper` setting may allow wrapped VS Code sessions. It needs a probe.
- **A reviewer-private evidence grant.** A read grant scoped to one review's bundle, in place of routing PAL's client through `kk`.
