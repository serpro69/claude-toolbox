# Migrate a template repository

`kk migrate` retires the legacy toolbox files in one Git repository. Installing or upgrading kk on a machine leaves those files in place. Run the migration once per repository, after the people who rely on its protections have installed and verified the machine release. The result is an ordinary, uncommitted Git diff.

## Before you begin

1. Check for `.github/template-state.json` at the repository root. Review local changes with `git status`. Copy out edits to synced files that you want to keep, or add their paths to the manifest’s `sync_exclusions`.
2. [Install kk](../getting-started/template-setup.md). For Codex, open plain `codex` in this repository without a named profile, review folder trust and all three managed guard hooks in `/hooks`, then exit. Run `kk status --live` to check the installed guards. Migration also reads the effective guard configuration **in this repository** for each tool it uses. A scratch workspace prevents a legacy hook from supplying a misleading denial.
3. Close Codex sessions opened before kk was installed and its hooks reviewed. An older session may lose protection when its legacy scripts disappear. Sessions opened after the machine guard is ready can keep using it. The legacy sync script needs Bash 4 or newer (including on macOS). Put that `bash`, `curl` and Mike Farah’s `yq` on `PATH` for migration.

## Preview, sync and retire

From the repository, run:

```bash
kk migrate
```

The default retirement tag is `v0.26.0-rc.4`, the last full template. The sync script, its version helper and the template it renders all come from that tag. If you are still running the RC4 or earlier pilot CLI, use `kk migrate --retirement-version v0.26.0-rc.4` explicitly. The same option can select a future retirement maintenance tag.

1. **Sync to the retirement release.** Read the preview before confirming. Like any sync, this step overwrites edits to synced files. Migration preserves adopter-owned settings and hooks during the merge, including custom deny entries. Files under `sync_exclusions` stay untouched. An up-to-date repository skips the sync confirmation.
2. **Retire the legacy files.** The second preview compares the repository with that same tag’s rendered template. It lists matching files and toolbox entries to remove, custom or excluded files to keep, and the effect on collaborators. Decline this step to leave the repository synced with its legacy guard in place. Rerunning `kk migrate` previews the remaining work.

Inspect `git diff` and `git status` before committing. You can keep individual changes out of the migration commit, for example the project rules file or a plugin registration used by CI. Preserve the files or marketplace definitions that a retained registration needs.

Migration keeps the legacy scripts together when you exclude `.codex/hooks.json` or a retained handler names the `.codex/scripts` directory. If your hook delegates to a separate program that depends on those scripts, exclude the script directory explicitly. Excluding an absent provider directory keeps it absent during migration sync.

## What changes for the team

| Repository change | Effect after the commit |
| --- | --- |
| Legacy Codex guard registrations, scripts and native forbids are removed | Each machine needs a reviewed guard plugin. Native forbids return on machines that enable the account-wide rules file. |
| Committed plugin enablement and Git-marketplace registration are removed | Cloud sessions, fresh CI runners and collaborators without a machine install may lose the plugin. Provision those hosts or retain the relevant project configuration. |
| Template Claude deny entries and statusline are removed | `kk claude` supplies the native denies and statusline. Bare Claude, IDE and desktop sessions rely on loaded plugin hooks for the toolbox guard. |
| Project choices survive | The report lists adopter deny entries, hooks, non-default manifest choices, and the Codex `sandbox_mode`, `approval_policy` and `approvals_reviewer` settings. These three lines continue to take precedence in the project. Delete them yourself to hand those decisions to each machine. |
| Toolbox instruction imports and sync infrastructure are retired | An import whose customised or excluded target remains is kept. Add an `@path` line to the root `AGENTS.md` for each repository file you want `kk codex` to inject. [Codex instructions](../providers/codex.md#repository-instructions) |

## Ordinary sync and the retirement boundary

Ordinary local and CI syncs to the retirement release still update the legacy template and print migration guidance. Removal requires the separate retirement operation. **A repository using a sync script older than v0.21.0 must not sync past the retirement release.** Use the retirement release as the latest possible sync target until migration. From v0.21.0 onwards, the local script hands control to the target version’s script before applying project changes.

Use `--version v0.26.0-rc.4` locally or enter `v0.26.0-rc.4` in the workflow’s version field to sync to the last full template. If an older local updater reports a missing `semver-compare.sh`, run `kk migrate` for retirement. To continue ordinary sync, restore the helper from the same tag as the installed updater before retrying.

The default branch and releases after RC4 carry a small compatibility script at the old sync path. A supported old client hands control to it. It prints migration guidance, exits successfully and reports `has_changes=false` to CI, so the workflow opens no sync PR. Some clients can backfill their own manifest before handing over.

For maintenance of a repository still using the old updater, the versioned reference covers sync exclusions, GitHub Actions credentials and settings merges. [Legacy template-sync reference at v0.25.4](https://github.com/serpro69/claude-toolbox/blob/v0.25.4/docs/user-guide/template-sync.md)

A running session is supported for **14 days after its machine release is superseded**. Restart older sessions within that window. Use `kk rollback` to restore a retained machine release. Repository migration changes have their own history in Git.
