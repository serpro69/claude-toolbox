# Changelog

## v0.26.0 · Agentstakk

Released November 23, 2026. The project moved from `serpro69/claude-toolbox` to `serpro69/agentstakk`. The workflow plugin and skill prefix keep the name `kk`. This release adds the `kk` command for installation-wide upgrades, provider launchers and offline rollback. [Release notes](https://github.com/serpro69/agentstakk/releases/tag/v0.26.0)

- **Template users** install kk on each machine. In each repository with `.github/template-state.json`, `kk migrate` previews a sync to the last full template and then previews removal of the template files. Repositories still using a sync script older than v0.21.0 must pin ordinary sync to `v0.26.0-rc.4` until migration. [Migration guide](../user-guide/template-sync.md)
- **Plugin-only users** switch from `kk@claude-toolbox` to `kk@agentstakk` in their provider’s marketplace. Machine installs register their own plugins under `agentstakk-local`. [Plugin-only switch](../getting-started/plugin-only.md#switch-an-existing-git-marketplace-installation)
- **Upstream clones and bookmarks** can use the new repository and Pages URLs. [Rename details](../getting-started/template-setup.md#move-an-existing-installation-to-agentstakk)

See [all releases](https://github.com/serpro69/agentstakk/releases) for the full history.
