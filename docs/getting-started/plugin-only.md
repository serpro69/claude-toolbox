# Plugin-only setup

Use the public `agentstakk` marketplace to add the workflow skills to your existing Claude Code or Codex configuration. Start sessions with the provider’s own CLI. For the `kk claude` and `kk codex` launchers, use the [machine installer](install.md). If you already have `kk@claude-toolbox`, follow the [marketplace switch](#switch-an-existing-git-marketplace-installation).

## Claude Code

With Claude Code 2.1.295 or later, Bash, `jq` and Python 3.9+ installed, run the following in your terminal.

```bash
claude plugin marketplace add serpro69/agentstakk
claude plugin install kk@agentstakk
```

Start a fresh `claude` session and invoke a skill such as `/kk:design`. The plugin also includes slash commands, sub-agents and a permission guard. The guard requires hooks to be enabled. A failing guard blocks matched operations. [Guard configuration](../user-guide/configuration.md#guard-configuration)

## Codex

```bash
codex plugin marketplace add serpro69/agentstakk
codex plugin add kk@agentstakk
```

Start `codex` and invoke a skill such as `$kk:design`. To add the permission guard, run `codex plugin add kk-guard@agentstakk`, open plain `codex` and review its three handlers in `/hooks`. The guard reads project policy from the session workspace.

The Codex plugin does not include the reviewer sub-agents. `$kk:review-architecture`, the isolated modes of `$kk:review-code`, `$kk:review-design` and `$kk:review-spec`, and the review step of `$kk:implement` delegate to them. The [machine installation](install.md) installs them as `$CODEX_HOME/agents/kk-*.toml`.

## Switch an existing Git-marketplace installation

In v0.25.x the public plugin was `kk@claude-toolbox`. Its replacement is `kk@agentstakk`. The repository rename changes the download address, but the provider still knows your installation by its old marketplace ID.

1. **Find the old installation.** Run `claude plugin list --json` or `codex plugin list --json`. For Claude, note whether the scope is user, project or local. Project settings may enable the plugin for teammates or CI.
2. **Install the replacement.** Use the [Claude Code](#claude-code) or [Codex](#codex) commands above. The Claude examples use the default user scope. For a project or local registration, use the corresponding `--scope` on the Claude commands in that project. Update any project-owned marketplace declaration and plugin enablement together in their original scope. For a Codex guard, complete the hook review before removing an older guard.
3. **Remove the old plugin.** For a Claude user installation, run `claude plugin uninstall --scope user --keep-data kk@claude-toolbox`. For Codex, run `codex plugin remove kk@claude-toolbox`. Remove any other old plugin only if the inventory shows it is yours and you have replaced it.
4. **Retire the old registration.** Once no other installation or scope uses it, run `claude plugin marketplace remove --scope user claude-toolbox` for a Claude user registration or `codex plugin marketplace remove claude-toolbox` for Codex. Start a fresh session and check the plugin list and, if enabled, the guard in `/hooks`.

If you are adopting machine-managed kk instead, the installer registers `agentstakk-local` for you. Use `kk status` to identify duplicate plugins after installation. [Machine installation and verification](install.md#verify-and-launch)

### Codex warns that the marketplace name does not match

> Codex could not update marketplace `claude-toolbox`: upgraded marketplace name `agentstakk` does not match configured marketplace `claude-toolbox`

Codex tried to refresh the old public Git marketplace, and the repository now advertises the new name. A marketplace registration can survive removal of its last plugin, including cleanup with `kk status --remove-mixed`.

Run `codex plugin marketplace list` and `codex plugin list` from the same project and Codex home that showed the warning. If the old marketplace still supplies plugins you use, complete the switch above. Once no plugin or project uses the old registration, remove it with `codex plugin marketplace remove claude-toolbox`. Keep `agentstakk-local` for a machine installation. If `claude-toolbox` is already absent, there is nothing to remove in that scope. Check a fresh Codex session for the warning.

## Upgrading

- **Claude Code.** Run `claude plugin marketplace update agentstakk`, then `claude plugin update kk@agentstakk` and start a fresh session.
- **Codex.** Run `codex plugin marketplace upgrade agentstakk` to refresh the Git marketplace. Use `/plugins` to check the installed plugin version. Review changed guard handlers in `/hooks` before starting a new session.

## What's included

Both plugins include the workflow skills and language profiles. Claude also includes the commands, reviewers and guard described above. Codex provides its guard as a separate plugin and has no reviewer sub-agents. [Skill reference](../user-guide/skills.md)

## What's not included

Configure [MCP servers](../user-guide/mcp-servers.md) separately. The [machine installation](install.md) supplies the kk launchers, Claude’s native permission settings and statusline, Codex launch settings and reviewer files, optional account-wide Codex rules, and offline rollback.
