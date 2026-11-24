# Codex

[Install kk](../getting-started/install.md) with Codex on your `PATH`, then review folder and hook trust in plain `codex` before launching your first `kk codex` session. The managed marketplace provides two plugins. `kk@agentstakk-local` supplies workflow skills and profiles. `kk-guard@agentstakk-local` supplies the guard adapters and runtime, with its own version and trust history. For a Git-marketplace installation, use [plugin-only setup](../getting-started/plugin-only.md).

## Permission guard

Start plain `codex` without `--profile`, open `/hooks`, and review the three managed PreToolUse handlers (Bash, Edit/Write and capy execution). Exit and start a fresh `kk codex` session. Run `kk status --live` for a scratch-session check. A skills-only upgrade reuses the installed guard when its content is unchanged.

For example, the stable v0.26.0 release shipped skills version `0.26.0` and guard version `0.26.0-rc.4`. The guard bundle had the same contents as the previously reviewed version, so it kept its version and could reuse that trust.

**Two open-session cases need attention.** Close Codex sessions before confirming a guard-changing upgrade or rollback. An open session can lose protection across the change. Review the replacement hooks and start a fresh session before resuming work. Also close sessions opened in a legacy repository before kk was installed and reviewed: they depend on repository scripts that migration removes. [Migrate a template repository](../user-guide/template-sync.md)

For `exec` and `review`, the launcher reads trust and enablement for the selected workspace. Missing, modified, disabled or untrusted handlers block a batch launch. Batch launches also require a verifiable local workspace and the managed profile. Use plain Codex for account-wide hook review. An interactive launch can also select another named profile. If the vendor lacks the trust-reading method, review the hooks and run `kk apply` interactively to acknowledge that review. The recorded state is `unverified`, and batch launches warn. `kk migrate` also requires an attributable live denial.

## Configuration files

| Location | Purpose |
| --- | --- |
| `$CODEX_HOME/kk.config.toml` | Named profile selected by `kk codex` |
| `$CODEX_HOME/agents/kk-*.toml` | Owned sub-agent definitions |
| `$CODEX_HOME/rules/kk.rules` | Optional account-wide native forbids |
| Project `.codex/config.toml`, `.codex/hooks.json`, `AGENTS.md` | Adopter-owned settings, hooks and instructions |
| `${XDG_CONFIG_HOME:-$HOME/.config}/kk/config.json` | Machine overrides. Run `kk apply` after edits. |

`CODEX_HOME` defaults to `~/.codex`. The managed profile supplies model and reasoning defaults, TUI settings and behavioral instructions. Precedence is base user settings, selected profile, trusted project settings, then explicit CLI flags. Bare Codex uses its normal profile selection. The user-scope guard plugin can still run there once trusted. Toolbox checks for collisions before creating owned files.

Approval policy, approval reviewer and sandbox defaults are optional. The separate native-forbids opt-in affects every repository and bare session using this Codex home. Existing project sandbox and approval settings still win after migration. [Override keys and effects](../user-guide/configuration.md#how-configuration-works)

### Where Codex saves trust decisions

Codex 0.171.0 saves interactive hook and folder trust in the active configuration file. Plain `codex` saves those choices in `$CODEX_HOME/config.toml`; `kk codex` selects the generated `$CODEX_HOME/kk.config.toml`. Use plain Codex for machine guard review, including after a guard change, and for the first folder trust decision in each repository. Project restrictions still apply.

If you already made a decision in the wrapped session, exit it and open plain `codex` in the same directory. Confirm the folder and hook choices you actually intend at account scope. Then run `kk apply` to regenerate the owned profile and `kk status --live` to verify. Regeneration replaces profile-local edits. Toolbox never copies a trust decision into another scope. Codex also writes display counters for model tips when its TUI opens. The launcher accepts those counters while continuing to verify the generated settings before batch runs.

### Recover a changed managed profile

If a batch run or `kk migrate` reports that kk cannot verify the managed profile, check that you are using the `CODEX_HOME` where kk was installed. Review `kk.config.toml` in that directory for preferences you want to keep. `kk apply` rebuilds this file from the release defaults and your machine overrides.

For example, to keep the `default` service tier for kk sessions, set `service_tier` to `"default"` under `codex.settings` in `${XDG_CONFIG_HOME:-$HOME/.config}/kk/config.json`. Omit that key to inherit the account preference. Make any folder or hook trust decisions in plain `codex`. Run `kk apply`, then `kk status --live` to verify the result. [Machine overrides](../user-guide/configuration.md#how-configuration-works)

## Repository instructions

Codex loads the root `AGENTS.md`. For an extra file to reach a wrapped session, add a repository-relative path on its own line outside a code fence, for example:

```text
@.claude/CLAUDE.team.md
@.capy/AGENTS.md
```

On an interactive launch, `kk codex` shows the eligible paths and sizes and asks once per repository and path list. A changed list requires a new decision. Approved imports are reread on launch and added to the toolbox’s developer instructions for that session, replacing any repository-level `developer_instructions` value. Without prior approval, non-interactive launches skip the imports. The wrapper expands one level of imports. Bare Codex does not expand these references. Missing, protected, oversized or outside-repository files are skipped with a diagnostic.

## Project instruction budget

The managed profile sets `project_doc_max_bytes = 65536` for native project instructions. Set a different budget in `codex.settings` and run `kk apply`. The launcher separately limits its serialized import argument to 120 KiB including toolbox text and escaping.

## Removed Auto-review settings

Current Codex versions warn that `auto_review.experimental_policy_template`
and `auto_review.extra_policy` are ignored. The toolbox template no longer
ships the `[auto_review]` block that supplied these settings for Codex 0.164.0.
Check older template repositories for these obsolete entries. For an immediate
manual fix, remove those two keys and their complete multiline values from
`.codex/config.toml`; remove the table header too if it becomes empty.

The old block supplied a standing authorization for read-only external Claude
reviews. Removing ignored settings clears the warning; it does not restore
that authorization. Approval and sandbox defaults in the machine profile are separate opt-ins.

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

## Generation pipeline

Edit skills and agents in `klaude-plugin/` and run `make generate-kodex` to refresh the Codex plugin and agent definitions. The guard engine is projected by `make generate-guard`. [Contributor architecture](../contributing/architecture.md)
