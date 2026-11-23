# Changelog

Release notes are published on the [GitHub Releases page](https://github.com/serpro69/agentstakk/releases).

## Unreleased · Agentstakk

The GitHub repository moved from `serpro69/claude-toolbox` to `serpro69/agentstakk`. Update your upstream Git remote, installer URLs and Pages bookmarks. The CLI is still `kk`. The release resolver accepts saved canonical repository names and keeps explicitly selected forks separate.

**If your repository uses a sync script older than `v0.21.0`, pin ordinary sync to `v0.26.0-rc.4` until you migrate.** Use `--version v0.26.0-rc.4` locally or enter `v0.26.0-rc.4` in the sync workflow’s version field. RC4 is the last full template and the default source for `kk migrate`. [Migration guide](../user-guide/template-sync.md#ordinary-sync-and-the-retirement-boundary)

The public and machine-managed marketplace IDs for `v0.26.0` are `agentstakk` and `agentstakk-local`. Pilot users retire their user-scope `@toolbox` registrations before resuming the staged upgrade and review `kk-guard@agentstakk-local` in plain Codex. Follow the same vendor cleanup in reverse before rolling back to RC4. [Machine upgrade and remote change](../getting-started/template-setup.md#move-an-existing-installation-to-agentstakk) · [Plugin-only switch](../getting-started/plugin-only.md#switch-an-existing-git-marketplace-installation)
