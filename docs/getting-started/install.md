# Install kk on your machine

Install Agentstakk once per user account. Its `kk` command starts Claude Code or Codex with the same release in any project. If you used the claude-toolbox template, install and verify kk first, then migrate each repository when its team is ready.

## Install

On macOS or Linux, have Bash, Git, `curl`, `jq`, Python 3.8 or later, and a signed-in Claude Code CLI (2.1.295 or later) on your `PATH`. Claude Code is required for the machine installer. To include Codex, put its CLI on your `PATH` before installing. For Codex alone, use the [plugin-only setup](plugin-only.md#codex).

Run this from any directory to install the latest stable release.

```bash
curl -fsSL https://raw.githubusercontent.com/serpro69/agentstakk/master/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
kk status
```

Add the `export` line to your shell profile for future terminals. The installer creates `~/.local/bin/kk`, validates the downloaded release and registers its plugins at user scope in the `agentstakk-local` marketplace. Releases live under `${XDG_DATA_HOME:-$HOME/.local/share}/kk` by default. To choose another location, set `KK_HOME` before installation. If the first installation is interrupted, rerun the installer.

To pin a fresh installation to v0.26.0, select the same tag for both the installer and the payload.

```bash
curl -fsSL https://raw.githubusercontent.com/serpro69/agentstakk/v0.26.0/install.sh | bash -s -- --version v0.26.0
```

## Verify and launch

1. **If you use Codex**, open plain `codex` in your project without a named profile. Review folder trust and the three `kk-guard@agentstakk-local` handlers in `/hooks`, then exit. Plain Codex saves these decisions to your account. Use it for the first folder-trust decision in each new project too. If your Codex version cannot report hook trust, run `kk apply` interactively after reviewing the hooks. [Codex trust settings](../providers/codex.md#where-codex-saves-trust-decisions)
2. **If `kk status` lists an older Git-marketplace plugin**, check its scope. After reviewing the managed guard, run `kk status --remove-mixed` to review and confirm removal of user-scope duplicates. Handle project-owned registrations with the team that uses them.
3. **Check the guards.** Run `kk status --live` in your terminal with working vendor authentication. It starts a short session for each managed CLI and checks that its guard denies a test read.
4. **Start work.** In your project, run `kk claude` or `kk codex`. [Try the workflow](quickstart.md)

## Move an existing installation to Agentstakk

- **Repository created from claude-toolbox.** Look for `.github/template-state.json`. After installing kk, run `kk migrate` in that repository to preview the changes. The old upstream name in the manifest is recognized automatically. [Migrate a template repository](../user-guide/template-sync.md)
- **Plugin installed directly as `kk@claude-toolbox`.** To keep using the public plugin, switch its registration to `kk@agentstakk`. To adopt the machine launchers, follow the install and verification steps above. [Switch a Git-marketplace installation](plugin-only.md#switch-an-existing-git-marketplace-installation)
- **Clone of the Agentstakk project itself.** This is the source repository and has no template manifest. Skip `kk migrate` here. If its Git remote still points to `serpro69/claude-toolbox`, update that remote. [Contributor setup](../contributing/index.md#getting-started)

For versioned documentation bookmarks, replace `/claude-toolbox/` with `/agentstakk/` and keep the version and page path.

If Codex still warns about updating the old marketplace at startup, [check for a leftover `claude-toolbox` registration](plugin-only.md#codex-warns-that-the-marketplace-name-does-not-match).

## Update and recover

Run `kk upgrade --check` to check for a newer stable release. Use `kk upgrade` to install it, or `kk upgrade --version v0.26.0` to select a specific release. Future launches across your projects use the active release.

Before confirming an upgrade or rollback that changes the Codex guard, close open Codex sessions. Review the replacement hooks in plain Codex and start a fresh session. A running `kk codex exec` or `kk codex review` batch keeps its release until it exits. If kk stages an upgrade while a batch is running, retry `kk upgrade` after it finishes. For a deferred apply or rollback, retry the original command. To cancel a batch, use Ctrl-C or send `SIGTERM` to its supervisor. Killing the supervisor with `SIGKILL` can leave the vendor process running. Restart long-lived sessions within 14 days of their release being superseded.

Run `kk status` to see the active release, any unfinished operation and the rollback target. `kk rollback` restores the recorded target offline. Save the recovery command printed during upgrade. It uses the retained release’s dispatcher and can recover an installation even if the active dispatcher is damaged.

<a id="rc4-marketplace-switch"></a>

If an upgrade reports “RC4 marketplace switch,” or your rollback target is an early v0.26.0 pilot, follow the [tagged pilot upgrade and rollback instructions](https://github.com/serpro69/agentstakk/blob/v0.26.0/docs/getting-started/template-setup.md#rc4-marketplace-switch). This applies only to machine installations made with those pre-release builds.
