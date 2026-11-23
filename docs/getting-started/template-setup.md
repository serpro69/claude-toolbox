# Install kk on your machine

Install once per user account. You can then start Claude Code or Codex in any repository with the same toolbox release. New projects need no toolbox files.

## Install

On macOS or Linux, use Bash, Git, `jq`, Python 3.8 or later, and a signed-in Claude Code CLI with plugin support (2.1.295 or later). Install Codex first if you also want its managed profile and plugins. The installer validates the release and registers its local marketplace with each supported CLI it finds. Claude Code is required for this installer.

From a toolbox checkout that contains `install.sh`, run the following from its root. This works before the first machine release is published.

```bash
./install.sh --local .
```

Once the first stable machine release (`v0.26.0`) is published, you can install the latest stable version without a checkout:

```bash
curl -fsSL https://raw.githubusercontent.com/serpro69/claude-toolbox/master/install.sh | bash
```

For a reproducible install, fetch `install.sh` from the chosen tag and pass `--version TAG` to it. For a pre-release, name the full candidate tag rather than selecting the latest stable release.

Put `~/.local/bin` on your shell’s `PATH`. For example, run `export PATH="$HOME/.local/bin:$PATH"` and add that line to your shell profile for future terminals. The installer creates the `kk` entry point there. By default releases live in `${XDG_DATA_HOME:-$HOME/.local/share}/kk`. Set `KK_HOME` before installation to choose another directory. If the first install is interrupted, rerun the installer to resume.

## Verify and launch

```bash
kk status
kk claude
```

For Codex, start **plain `codex` without `--profile`** in your project. Review the folder’s trust prompt and the three `kk-guard@toolbox` handlers in `/hooks`. Exit Codex. These decisions are now in your account configuration. Use `kk codex` for daily sessions. When a new project needs a folder trust decision, make it in plain `codex` there first. If Codex reports that it cannot read hook trust, run `kk apply` interactively and acknowledge the review. That vendor state is recorded as `unverified`. Run `kk status --live` from your terminal. It starts short vendor sessions in scratch workspaces and checks for a denial from each managed guard. It needs working vendor authentication.

If you already installed plugins from the Git marketplace, `kk status` lists the copies and their scopes. `kk status --remove-mixed` offers to remove user-scope Git copies with a managed counterpart. Review project-owned registrations in their repository. [Existing repositories](adopting.md)

## Update and recover

```bash
kk upgrade                      # latest stable machine release
kk upgrade --version v0.26.0    # choose a published machine release
kk upgrade --local .            # use the current toolbox checkout
kk status
kk rollback                     # restore the recorded target offline
```

After an interrupted upgrade, `kk status` gives the resume or rollback command. Save the recovery command printed during an upgrade. It invokes the retained release’s own dispatcher, so it also works if the newly active command is damaged. Restart long-running sessions within 14 days after their release is superseded.

Next, [try the workflow](quickstart.md), [configure your launchers](../user-guide/configuration.md), or [migrate a legacy repository](../user-guide/template-sync.md).
