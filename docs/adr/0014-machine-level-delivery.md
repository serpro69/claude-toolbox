# ADR 0014: Deliver the toolbox per machine

## Status

Accepted, 2026-11-23. Template retirement follows the tagged pilot and publication of the stable retirement release.

## Context

With template sync, each repository carried copies of provider settings, scripts and guard registrations. Updating several repositories meant reviewing similar pull requests, and an operating guard could depend on both the repository copy and the independently updated plugin. A shared Git marketplace alone delivers skills but cannot supply all launcher settings, owned agent files or offline recovery. A repository can also serve collaborators, CI and cloud sessions with different installations.

## Decision

Install one versioned toolbox release per user account. The installer stages and validates the payload before activation. A local marketplace named `toolbox` distinguishes the managed installation from the `claude-toolbox` Git marketplace. Claude loads the active plugin in place. Codex caches its skills and guard as separate plugins, so changing skills alone can preserve the reviewed guard. Record the active release, rollback target, pending operation and owned files under the toolbox home. Serialize writers and dispatch rollback through the retained release. [Installer](https://github.com/serpro69/claude-toolbox/blob/master/install.sh) · [Lifecycle](https://github.com/serpro69/claude-toolbox/blob/master/kk/lib/cli.py) · [State and retention](https://github.com/serpro69/claude-toolbox/blob/master/kk/lib/state.py)

Keep preferences and permissions at their appropriate scope. `kk claude` builds a settings layer for each launch. `kk codex` selects a named profile, with explicit opt-ins for approval and sandbox defaults and for account-wide native forbids. User overrides and repository instructions remain adopter-owned. Keep plugin-only installation available through the vendors. [Claude launcher](https://github.com/serpro69/claude-toolbox/blob/master/kk/lib/claude_launch.py) · [Codex profile](https://github.com/serpro69/claude-toolbox/blob/master/kk/lib/codex_profile.py) · [Codex launcher](https://github.com/serpro69/claude-toolbox/blob/master/kk/lib/codex_launch.py)

Retire an existing template only through an explicit, two-step migration. First verify the replacement guard in the repository and attribute a denial to the installed guard in a scratch workspace. Then preview and confirm sync to the retirement release and removal against its rendered template. The adopter reviews and commits the resulting diff. A later compatibility script at the old sync path directs supported clients to migration. [Migration command](https://github.com/serpro69/claude-toolbox/blob/master/kk/lib/migrate.py) · [Migration guide](../user-guide/template-sync.md)

## Consequences

One upgrade serves all repositories on the machine. A retained release can restore a broken activation offline. Running sessions have a 14-day supported lifetime after their release is superseded. Guard-changing Codex upgrades and rollbacks can still require hook review and a fresh session. Activation and effective protection in a specific workspace are separate observations.

The launcher supplies Claude’s native denies only to wrapped processes. Migrated repositories can lose committed plugin enablement for teammates, cloud sessions or CI without their own installation. Codex’s optional native rules affect every repository using the account. The migration report makes those choices visible before the change is shared. [Configuration](../user-guide/configuration.md) · [Patch and release procedure](../contributing/architecture.md#retirement-script-maintenance)
