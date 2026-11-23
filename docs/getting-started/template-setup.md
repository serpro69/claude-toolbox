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
curl -fsSL https://raw.githubusercontent.com/serpro69/agentstakk/master/install.sh | bash
```

For a reproducible install, fetch `install.sh` from the chosen tag and pass `--version TAG` to it. For a pre-release, name the full candidate tag rather than selecting the latest stable release.

Put `~/.local/bin` on your shell’s `PATH`. For example, run `export PATH="$HOME/.local/bin:$PATH"` and add that line to your shell profile for future terminals. The installer creates the `kk` entry point there. By default releases live in `${XDG_DATA_HOME:-$HOME/.local/share}/kk`. Set `KK_HOME` before installation to choose another directory. If the first install is interrupted, rerun the installer to resume.

## Move an existing installation to Agentstakk

After the hosted rename, update the Git remote of a clone that tracks the upstream repository. Keep a fork’s `origin` pointing to the fork. If the canonical remote is named `upstream`, use that name instead of `origin`.

```bash
git remote set-url origin https://github.com/serpro69/agentstakk.git
```

### RC4 marketplace switch

RC4 registered the directory `KK_HOME` as `toolbox` in both vendors. The renamed release registers that same directory as `agentstakk-local`. Keep your existing `KK_HOME`, Codex home, overrides and profile. Close old sessions and finish batches before removing their registrations. Start new sessions after checking the replacement.

1. Stage the published release with `KK_REPOSITORY=serpro69/agentstakk kk upgrade --version TAG`. Use the exact candidate or stable tag in a terminal. Confirm the guard identity change while the RC4 registrations are still installed. Declining leaves them active. While the pilot catalogs are registered, the new installer leaves the candidate staged and identifies the vendor to switch.
2. Inspect `claude plugin list --json`, `claude plugin marketplace list --json`, `codex plugin list --json` and `codex plugin marketplace list --json`. The pilot's local marketplace root should be your `KK_HOME`. The following commands apply to its user-scope plugins. Skip entries the vendor inventory shows as absent. Remove a marketplace only after checking that no other plugin or scope uses its registration. Leave project-owned enablement in its original scope. Skip the Codex commands on a Claude-only install. Run the Codex commands with the same `CODEX_HOME` used for installation. If kk identifies another recorded Codex home, inspect it separately.

    ```bash
    claude plugin uninstall --scope user --keep-data kk@toolbox
    claude plugin marketplace remove --scope user toolbox
    codex plugin remove kk@toolbox
    codex plugin remove kk-guard@toolbox
    codex plugin marketplace remove toolbox
    ```

3. Run `kk upgrade` to resume the same staged and confirmed release. In plain Codex, review the three `kk-guard@agentstakk-local` handlers in `/hooks`. Then run `kk apply` and `kk status --live`. The launcher reports pending review until Codex trusts the new identity. An old public plugin still enabled by a project will appear in status. Update that setting in its original scope.

If you stop after removing the pilot registrations while the new release is still **staged**, the RC4 catalogs still exist under `KK_HOME`. To stay on RC4, add that directory back with each vendor’s `plugin marketplace add` command and reinstall the user-scope `kk@toolbox` plugins and Codex’s `kk-guard@toolbox`. Check `kk status` and review any hooks the vendor requests. Once activation has started, use `kk upgrade` to resume. If you choose recovery instead, follow the cross-name cleanup below before invoking the printed rollback command. During an interrupted activation that command restores the still-active release, which can differ from the usual rollback target.

**Offline rollback across the rename.** Check the rollback target in `kk status`. To restore RC4, close sessions and use the five commands above with `agentstakk-local` in place of `toolbox` to remove the departing registrations. Then run `kk rollback`. RC4 runs its own installer and restores `@toolbox` from its retained files. Check both vendor inventories and plain Codex’s hook status before resuming work. RC4 cannot diagnose newer duplicate registrations. To return to a retained renamed release, remove the RC4 registrations as above and run `kk rollback` again when the renamed release is the recorded target. Review any handlers the vendor marks untrusted or modified. A live check requires an available model transport.

Legacy repository migration still uses the full template at `v0.26.0-rc.4`.

For a Git-marketplace installation, follow the [plugin-only switch](plugin-only.md#switch-an-existing-git-marketplace-installation).

## Verify and launch

```bash
kk status
kk claude
```

For Codex, start **plain `codex` without `--profile`** in your project. Review the folder’s trust prompt and the three managed `kk-guard` handlers in `/hooks` (`@toolbox` through RC4, `@agentstakk-local` in the renamed release). Exit Codex. These decisions are now in your account configuration. Use `kk codex` for daily sessions. When a new project needs a folder trust decision, make it in plain `codex` there first. If Codex reports that it cannot read hook trust, run `kk apply` interactively and acknowledge the review. That vendor state is recorded as `unverified`. Run `kk status --live` from your terminal. It starts short vendor sessions in scratch workspaces and checks for a denial from each managed guard. It needs working vendor authentication.

If you already installed plugins from the Git marketplace, `kk status` lists the copies and their scopes. `kk status --remove-mixed` offers to remove user-scope Git copies with a managed counterpart. Review project-owned registrations in their repository. [Existing repositories](adopting.md)

## Update and recover

```bash
kk upgrade                      # latest stable machine release
kk upgrade --check              # report availability without changing the installation
kk upgrade --version v0.26.0    # choose a published machine release
kk upgrade --local .            # use the current toolbox checkout
kk status
kk rollback                     # restore the recorded target offline
```

After an interrupted upgrade, `kk status` gives the resume or rollback command. Save the recovery command printed during an upgrade. It invokes the retained release’s own dispatcher, so it also works if the newly active command is damaged. Restart long-running sessions within 14 days after their release is superseded.

Managed Codex batch runs (`kk codex exec` and `kk codex review`) can run concurrently. Each holds its verified installation until the vendor process exits. If a batch is running, an upgrade can stage its release and asks you to retry activation afterward with `kk upgrade`. The same retry applies to `kk apply` and `kk rollback`. To cancel a supervised batch, use Ctrl-C in its terminal or send `SIGTERM`. Killing only the supervisor with `SIGKILL` can leave the vendor running. Interactive sessions continue to use the existing upgrade and hook-review behavior.

**Transition from the pilot releases.** Finish running batches before upgrading from or rolling back to `v0.26.0-rc.1` through `rc.3`. Those releases predate batch coordination. Check the rollback target in `kk status`. If it is a Claude-only pilot release and the departing release added Codex, its recovery code can leave the departing Codex plugins installed. Full batch coordination and automatic removal of those plugins apply when both releases contain the correction.

Next, [try the workflow](quickstart.md), [configure your launchers](../user-guide/configuration.md), or [migrate a legacy repository](../user-guide/template-sync.md).
