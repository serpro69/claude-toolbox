# Migrate a template repository

Use this guide if your project contains `.github/template-state.json` from claude-toolbox. In v0.25.x, template sync delivered settings and guard scripts as files committed to each project. Starting with v0.26.0, each user installs Agentstakk once. The team then runs `kk migrate` once per repository and decides which changes to commit. If you only installed `kk@claude-toolbox`, use the [plugin-only switch](../getting-started/plugin-only.md#switch-an-existing-git-marketplace-installation).

## Before you begin

1. **Prepare the machines.** Each person who relies on the repository’s guards should [install kk and verify the guards](../getting-started/install.md). If the project includes `.codex/`, the machine running the migration needs the managed Codex guard as well as folder and hook trust reviewed in plain `codex`. Close Codex sessions opened before that guard was installed and reviewed.
2. **Check what the team needs to keep.** Review `git status`. Save edits to synced files or list their paths in the manifest’s `sync_exclusions`. Check whether CI, cloud sessions or teammates depend on committed plugin settings before retiring them. [Effects on the team](#what-changes-for-the-team)
3. **Check the migration tools.** Put Bash 4 or newer (including on macOS), `curl` and Mike Farah’s `yq` on `PATH`, alongside the tools required by the installer. The command downloads the retirement scripts and contacts the providers for a live guard check.

## Preview, sync and retire

From the repository’s working tree, run the following command.

```bash
kk migrate
```

You can migrate directly from v0.25.x. Leave `serpro69/claude-toolbox` or `serpro69/claude-starter-kit` in the manifest. kk resolves those names to Agentstakk. Each kk release pins the full legacy template and its matching cleanup scripts to one Git tag. Plain `kk migrate` downloads both automatically. Run `kk migrate --help` to see the tag your installation uses.

If you use a fork, its manifest upstream must match the source of your kk installation. If a Git `insteadOf` rule routes the old and new names to different mirrors, align the rule before retrying.

Before changing files, kk checks the managed guard in this repository for each provider it finds and verifies a guard denial in a scratch workspace. After you confirm that you want to continue, it shows two previews.

1. **Sync to the last full template.** Read the preview before confirming. Like any sync, this step overwrites edits to synced files. Migration preserves adopter-owned settings and hooks during the merge, including custom deny entries. Files under `sync_exclusions` stay untouched. An up-to-date repository skips the sync confirmation.
2. **Retire the legacy files.** The second preview compares the repository with that same tag’s rendered template. It lists matching files and toolbox entries to remove, custom or excluded files to keep, and the effect on collaborators. Decline this step to leave the repository synced with its legacy guard in place. Rerunning `kk migrate` previews the remaining work.

Inspect `git diff` and `git status` before committing. Check project-owned commands and instruction imports for references to files listed as removed. If you keep a plugin registration for CI, keep its marketplace definition and any files it needs. Run `kk status --live` again from the migrated project to verify the guards, then share the diff with your team. Future machine updates use `kk upgrade`.

Migration keeps the legacy scripts together when you exclude `.codex/hooks.json` or a retained handler names the `.codex/scripts` directory. If your hook delegates to a separate program that depends on those scripts, exclude the script directory explicitly. Excluding an absent provider directory keeps it absent during migration sync.

### If the guard check stops before the first preview

- **Codex plugin inventory timed out.** Run `codex plugin list --json` from the same terminal. If it finishes and lists the managed plugins, retry `kk status --live` and `kk migrate`. If Codex itself reports an error, resolve that error first. A successful listing alone checks installation. The live check also verifies that the guard actually runs.
- **kk cannot verify the managed Codex profile.** A preference such as `service_tier` saved in the generated profile can cause this even when the hooks are trusted. Preserve any intended preferences in the machine overrides before running `kk apply`, then retry. [Recover a changed Codex profile](../providers/codex.md#recover-a-changed-managed-profile)

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

For maintenance of a repository still using the old updater, the versioned reference covers sync exclusions, GitHub Actions credentials and settings merges. [Legacy template-sync reference at v0.25.4](https://github.com/serpro69/agentstakk/blob/v0.25.4/docs/user-guide/template-sync.md)

Use Git to revert a committed repository migration. `kk rollback` restores a retained release on one machine. [Machine updates and recovery](../getting-started/install.md#update-and-recover)
