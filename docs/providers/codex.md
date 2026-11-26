# Codex

[Install kk](../getting-started/install.md) with Codex on your `PATH`, then review folder and hook trust in plain `codex` before launching your first `kk codex` session. The managed marketplace provides two plugins. `kk@agentstakk-local` supplies workflow skills and profiles. `kk-guard@agentstakk-local` supplies the guard adapters and runtime, with its own version and trust history. For a Git-marketplace installation, use [plugin-only setup](../getting-started/plugin-only.md).

## Permission guard

Start plain `codex`, open `/hooks`, and review the three managed PreToolUse handlers (Bash, Edit/Write and capy execution). Exit and start a fresh `kk codex` session. Run `kk status --live` for a scratch-session check. A skills-only upgrade reuses the installed guard when its content is unchanged.

For example, the stable v0.26.0 release shipped skills version `0.26.0` and guard version `0.26.0-rc.4`. The guard bundle had the same contents as the previously reviewed version, so it kept its version and could reuse that trust.

**Two open-session cases need attention.** Close Codex sessions before confirming a guard-changing upgrade or rollback. An open session can lose protection across the change. Review the replacement hooks and start a fresh session before resuming work. Also close sessions opened in a legacy repository before kk was installed and reviewed: they depend on repository scripts that migration removes. [Migrate a template repository](../user-guide/template-sync.md)

For `exec` and `review`, the launcher reads trust and enablement for the selected workspace, using the configuration flags of the run that follows in the same order. Missing, modified, disabled or untrusted handlers block a batch launch, including when one of your own `-c` flags is the cause. Batch launches also require a verifiable local workspace. They refuse a named profile (`-p`/`--profile`, including the former `-p kk`), `--ignore-user-config` and `--trust` before any session starts, because the check cannot reproduce what those change. An interactive launch can select a named profile; kk then passes none of its settings. If the vendor lacks the trust-reading method, review the hooks and run `kk apply` interactively to acknowledge that review. The recorded state is `unverified`, and batch launches warn. `kk migrate` also requires an attributable live denial.

## Configuration files

| Location | Purpose |
| --- | --- |
| `$CODEX_HOME/agents/kk-*.toml` | Owned sub-agent definitions |
| `$CODEX_HOME/rules/kk.rules` | Optional account-wide native forbids |
| Project `.codex/config.toml`, `.codex/hooks.json`, `AGENTS.md` | Adopter-owned settings, hooks and instructions |
| `${XDG_CONFIG_HOME:-$HOME/.config}/kk/config.json` | Machine overrides. Run `kk apply` after edits. |

`CODEX_HOME` defaults to `~/.codex`. kk writes no Codex configuration file: `config.toml` stays yours, and Codex saves your interactive choices there. Bare Codex gets none of kk’s settings. The user-scope guard plugin can still run there once trusted. Toolbox checks for collisions before creating owned files. `kk codex` refuses to start under a `CODEX_HOME` other than the one its settings were applied to, unless you name a profile.

## Launch settings

`kk codex` runs plain `codex` and puts the active release’s settings in front of your arguments as `-c` flags. Before each launch it asks Codex which settings your account, the repository and your command line already set, and passes only what the table allows.

| kk passes | Values | Unless |
| --- | --- | --- |
| Defaults | `model`, `model_reasoning_effort`, `model_context_window`, `model_auto_compact_token_limit`, `project_doc_max_bytes`, `agents.max_concurrent_threads_per_session`, `agents.max_depth`, and under `tui`: `status_line`, `terminal_title`, `effects.starfield` and `animations` | The setting has a value anywhere else: `config.toml`, a trusted repository’s `.codex/config.toml` or a `-c` flag. Or you switched the default off in `codex.defaults`. |
| Your choices | The behavioral instructions (`developer_instructions`), the `codex.optIn` approval and sandbox values, and everything in `codex.settings` | A trusted repository sets the same setting. |

A default therefore ranks below `config.toml`. Your choices rank above `config.toml` and below a trusted repository, so existing project sandbox and approval settings still win after migration, and so do a repository’s own `developer_instructions`. Your own `-c` flags come after kk’s and win for the same setting. A table you pass, such as `-c 'tui={…}'`, replaces kk’s whole table for that key.

- **Model.** The four model values are sized for kk’s default model. kk passes none of those defaults when the session will use another model: `model` is set elsewhere, you set it in `codex.settings` or switched it off in `codex.defaults`, or you pass `-m`/`--model` or `--oss`. A `codex.settings` value for one of the other three still applies.
- **Sandbox and approval flags.** With `-s`/`--sandbox`, `-a`/`--ask-for-approval`, `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox` or `--yolo`, kk passes no approval or sandbox value, so your flag and your native settings decide.
- **Named profile.** `kk codex --profile <name>` passes your arguments through without kk’s settings or imports. `--profile kk` has no special meaning.
- **Lookup.** The check starts a short `codex app-server` process and sends `config/read` for the directory Codex starts in (`-C`, or the current one). It took 0.15–0.30 seconds with Codex 0.172.0 on the verification machine; a batch launch adds the guard’s trust read. If the lookup fails or takes more than 5 seconds, kk prints one line starting `kk: could not read Codex configuration origins` and passes none of the values above for that launch, so repository settings keep precedence. Approved imports still apply.
- **Visibility.** `codex.settings` values become part of the Codex command line, which other local users can usually read in the process list. kk rejects the credential-bearing tables `mcp_servers`, `model_providers` and `shell_environment_policy` there. Configure them in `config.toml`.

Approval policy, approval reviewer and sandbox defaults are optional. The separate native-forbids opt-in affects every repository and bare session using this Codex home. [Override keys and effects](../user-guide/configuration.md#how-configuration-works)

`kk apply`, installation and upgrade check the settings with your Codex CLI before changing anything: Codex must accept them, and `config/read` must report each one under the name kk passes. A name Codex reports differently stops the command, for example:

```text
kk: Codex config/read does not report agents.max_threads under the name kk passes; it reported agents.max_concurrent_threads_per_session instead. Use the name Codex reports in codex.settings. For one of kk's own defaults, switch it off in codex.defaults and update kk
```

kk therefore needs a Codex CLI that has `config/read` and the `--no-daemon` flag; 0.172.0 is the verified version. Without them the command stops, with nothing changed, and tells you to update Codex:

```text
kk: kk checks setting names through Codex config/read, which failed: <reason>. Run the command again; if this Codex CLI has no config/read, update Codex
```

### Where Codex saves trust decisions

Codex saves interactive choices in the active configuration file. For plain `codex` and for `kk codex` that file is `$CODEX_HOME/config.toml`. With Codex 0.172.0, a `/model` switch, folder trust and a hook approval made inside a `kk codex` session were all written there, and the next `kk codex exec` ran with the saved model and passed its guard check without `kk apply`. Because kk’s model defaults yield to `config.toml`, a model you pick with `/model` stays in use until you change it. The exception is a `model` or `model_reasoning_effort` you set in `codex.settings`: whenever kk passes that value, it overrides the corresponding saved one.

Review the machine guard in plain `codex`, as kk’s messages say; a `kk codex` session saves the same decisions in the same place. A session started with a named profile is different: Codex saves its choices in that profile, where the batch guard check does not read them. Toolbox never copies a trust decision into another scope. Project restrictions still apply.

### Upgrade from a release with the managed profile

Releases through v0.26.1 launched `codex --profile kk` and owned `$CODEX_HOME/kk.config.toml`. Codex saved `/model` switches and hook approvals in that file, which then blocked batch launches. The upgrade removes the file and prints once:

```text
kk: removed the managed Codex profile <path>; kk codex now passes its settings as launch flags. A model or hook approval Codex saved in that profile no longer applies: choose it again in plain codex, or set it in config.toml.
```

kk copies nothing out of the removed file, because `config.toml` is yours. If the upgrade stops on your `codex.settings`, correct `${XDG_CONFIG_HOME:-$HOME/.config}/kk/config.json` and run it again:

- `configure mcp_servers in native Codex configuration` (also `model_providers` and `shell_environment_policy`): move the table to `config.toml`.
- `Codex config/read does not report … under the name kk passes`: rename the key to the name the message reports.
- `codex.settings key … is not a plain name`: write a dotted key as a nested JSON object.

`kk rollback` to v0.26.x restores that release’s profile and launcher. That release’s `kk apply` rejects a `codex.defaults` key as unknown, so remove the key from `config.json` while you stay on it.

## Repository instructions

Codex loads the root `AGENTS.md`. For an extra file to reach a wrapped session, add a repository-relative path on its own line outside a code fence, for example:

```text
@.claude/CLAUDE.team.md
@.capy/AGENTS.md
```

On an interactive launch, `kk codex` shows the eligible paths and sizes and asks once per repository and path list. A changed list requires a new decision. Approved imports are reread on launch and added to the toolbox’s developer instructions for that session, replacing any repository-level `developer_instructions` value. Without prior approval, non-interactive launches skip the imports. The wrapper expands one level of imports. Bare Codex does not expand these references. Missing, protected, oversized or outside-repository files are skipped with a diagnostic.

## Project instruction budget

kk passes `project_doc_max_bytes = 65536` for native project instructions unless your `config.toml` or the repository sets its own value. Set a different budget in `codex.settings` and run `kk apply`. The launcher separately limits its serialized import argument to 120 KiB including toolbox text and escaping.

## Removed Auto-review settings

Current Codex versions warn that `auto_review.experimental_policy_template`
and `auto_review.extra_policy` are ignored. The toolbox template no longer
ships the `[auto_review]` block that supplied these settings for Codex 0.164.0.
Check older template repositories for these obsolete entries. For an immediate
manual fix, remove those two keys and their complete multiline values from
`.codex/config.toml`; remove the table header too if it becomes empty.

The old block supplied a standing authorization for read-only external Claude
reviews. Removing ignored settings clears the warning; it does not restore
that authorization. kk’s approval and sandbox defaults are separate opt-ins.

Codex's warning directs additional Guardian rules to the top-level
`guardian_extra_policy` key in managed `requirements.toml`. On Linux and macOS,
the system file is `/etc/codex/requirements.toml`; project-local and user-local
`requirements.toml` files are not documented managed sources. See
[managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration#understand-policy-scope-and-precedence).
The machine installer leaves this system policy to administrators.
Any migration must retain the intended review scope and existing managed
requirements, then verify the effective policy in a fresh session.

`auto_review.policy` remains supported, but it **replaces the entire policy**.
Putting only the old authorization paragraph there would discard the other
policy rules. See [Auto-review configuration](https://learn.chatgpt.com/docs/sandboxing/auto-review#configuration).

If you use [pal](https://github.com/serpro69/pal-mcp-server) and rely on
[clink-based reviews](../user-guide/skills.md#isolated-reviews-and-external-models),
but they get blocked by the auto-review policy, the current recommended solution
is to add the following to your `/etc/codex/requirements.toml`:

```toml
guardian_extra_policy="""
## Pre-authorized external code reviews

For work requested by the user in the current project, PAL clink calls using
cli_name="claude", role="default", and allow_edits=false are authorized for
independent code and technical-document review. Treat Anthropic through the
configured Claude CLI as an approved recipient for this purpose.

This standing authorization covers successive tasks, revised snapshots,
review-fix follow-ups, and the source, diffs, tests, documentation, review
criteria, provenance metadata, and relevant local dependency source needed
for the review. Temporary review bundles containing those materials are
included. Do not require separate disclosure approval for each snapshot.

The request must instruct the reviewer to inspect files without modifying
project files or running tests, builds, or submitted code. Read-only inspection
commands are permitted. This authorization excludes credentials, secret files,
production data, unrelated personal information, and unrelated repositories.
Other destinations, clients, purposes, and actions remain subject to the normal
approval policy. Preserve all other safety rules and managed restrictions.
"""
```

## Capy hooks

Run `capy setup --platform codex` in a repository using capy and review its registrations in `/hooks`. Capy supplies guidance and HTTP routing through its own hooks. To load its written guidance in a wrapped session, you can also import `@.capy/AGENTS.md`. The machine guard checks supported capy execution calls independently. [Codex MCP setup](../user-guide/mcp-servers.md#codex)

## Known limitations

Guard coverage depends on the vendor loading the reviewed handlers for the current workspace. The registered channels are shell commands, intercepted patches and supported capy execution tools. MCP server registration is a separate setup step. [Codex file-access decision](../adr/0013-codex-file-access-through-hooked-tools.md)

**Shared background server.** Codex attaches an interactive session to a shared background server, except when the launch carries configuration flags or a named profile. A `kk codex` session with kk’s settings therefore runs in a server of its own, as it did with the managed profile. kk adds `--no-daemon` to such a launch so that Codex does not warn about this at every start. A session launch is one with no subcommand, a prompt, `resume` or `fork`. kk leaves the flag out for batch launches and every other subcommand, when it passes no settings, and when you pass `--remote` or `--no-daemon` yourself. `kk codex --profile <name>` gets neither kk’s settings nor the flag, so Codex shows its own warning for the profile.

**Managed configuration.** A value an administrator pins in the system `managed_config.toml` outranks command-line flags. kk’s default for that setting yields. One of your choices for it is passed without effect, and kk does not report this.

**Resumed sessions.** For `resume` and `fork`, kk looks up settings for the directory you start in. If the session belongs to another repository, kk does not see that repository’s values, so kk’s defaults and your choices can override them for the session. Imports are skipped for these launches. [Launch overrides decision](../adr/0015-codex-launch-overrides.md)

## Generation pipeline

Edit skills and agents in `klaude-plugin/` and run `make generate-kodex` to refresh the Codex plugin and agent definitions. The guard engine is projected by `make generate-guard`. [Contributor architecture](../contributing/architecture.md)
