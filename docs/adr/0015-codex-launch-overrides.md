# ADR 0015: Pass Codex settings as launch flags

## Status

Accepted, 2026-11-26. Supersedes the statement in [ADR 0014](0014-machine-level-delivery.md) that `kk codex` selects a named profile. The rest of ADR 0014 stands. Evidence below is from Codex CLI 0.172.0 on Linux.

## Context

Since ADR 0014, `kk codex` launched `codex --profile kk`, and kk owned the profile file `$CODEX_HOME/kk.config.toml`. Codex treats the selected profile as the place to save interactive choices: `/model` rewrites `model` and `model_reasoning_effort` there, and a hook approval adds a `[hooks.state]` table. Batch launches (`exec`, `review`, `kk status --live`, the `kk migrate` live check) refused unless the file matched the generated profile byte for byte. A routine `/model` switch therefore broke every later batch launch, often days later in another repository, and `kk apply` repaired it by discarding the choice. [Issue #206](https://github.com/serpro69/agentstakk/issues/206)

The byte comparison could not simply be relaxed. The guard’s trust read runs `codex app-server`, which refuses `--profile`, so it saw the plain account’s hook state while the run that followed loaded the profile. The comparison was the only guarantee that the profile changed no hook state between the check and the run. A profile-held `enabled = false` for a guard handler would otherwise have passed.

The cause was ownership: kk treated a file that Codex writes to as its own. Three constraints shaped the replacement. kk supports Python 3.8, which has no TOML parser. Applying and launching kk’s settings writes nothing into repositories, which stay adopter-owned (ADR 0014), and the adopter’s `config.toml` is not kk’s to write. Offline rollback to an older release must keep working.

Probes established what Codex offers instead. They used a scratch `CODEX_HOME` unless the row says otherwise:

| Probe | Result |
| --- | --- |
| `codex --profile kk app-server` | Refused: `--profile` only applies to runtime commands |
| `-c model=…` against a trusted project’s `.codex/config.toml` | The flag wins (origin `sessionFlags`) |
| `config/read` with `cwd` on `app-server` | Returns the effective configuration and, per setting, the layer that set it (`user`, `project`, `sessionFlags`, …). Unset settings have no origin. |
| Names in `config/read` | Canonical, not as written: `agents.max_threads` is reported as `agents.max_concurrent_threads_per_session`. Arrays are reported per element. An empty array has no origin. |
| Two `-c` flags for one table | A later inline table replaces an earlier flag for the same key. A dotted key inside quotes is split and silently ignored. |
| `-c` before `exec` and after it | One ordered list. `app-server` given the same flags in the same order reports the same result. |
| `exec --ignore-user-config`, `exec --trust` | Change configuration or trust for the run. `app-server` accepts neither. |
| System `managed_config.toml` (the maintainer’s `~/.codex` and a scratch home) | Outranks `-c` (origin `legacyManagedConfigTomlFromFile`) |
| Interactive choices in a session launched with `-c` flags and no profile (the maintainer’s `~/.codex`) | `/model`, folder trust and hook approvals are saved to `config.toml` |

## Decision

`kk codex` runs plain `codex` and passes the active release’s saved settings as `-c` flags in front of the caller’s arguments. kk no longer writes a Codex configuration file. It emits one flag per top-level key, with tables as one inline table, because a second table would replace the first and dotted paths are unreliable. [Launcher](https://github.com/serpro69/agentstakk/blob/master/kk/lib/codex_launch.py) · [Settings and validation](https://github.com/serpro69/agentstakk/blob/master/kk/lib/codex_profile.py)

Before each launch kk reads `config/read` for the starting directory with the caller’s own configuration flags, and decides per setting. [App-server client](https://github.com/serpro69/agentstakk/blob/master/kk/lib/codex_app.py)

- **Release defaults** (model and its three sizing values, the project instruction budget, sub-agent limits, TUI settings) are passed only when no layer sets them, so `config.toml`, a trusted repository and the command line all win. The four model values are dropped together when the session will not use kk’s default model. The new `codex.defaults` switches a default off.
- **Explicit values** (the behavioral instructions, the `codex.optIn` approval and sandbox values, `codex.settings`) keep the profile’s old precedence: they beat `config.toml` and yield to a trusted repository. A dedicated sandbox or approval flag from the caller drops kk’s approval and sandbox values.
- **If the lookup fails**, kk passes neither class and says so in one line. It cannot tell what a repository set, and omitting its values keeps repository precedence safe. Approved instruction imports still apply.

A batch launch computes the same flags, then runs the trust read with **the configuration flags of the final command in their final order**: kk’s flags followed by the caller’s. The read and the run share `CODEX_HOME`, working directory and that flag sequence, which replaces the byte comparison. A batch launch refuses what the read cannot reproduce: any named profile, `--ignore-user-config` and `--trust`. [Trust read](https://github.com/serpro69/agentstakk/blob/master/kk/lib/codex_trust.py)

`kk apply`, installation and upgrade validate the settings with the installed Codex before publishing anything. Codex must accept all candidate flags, and `config/read` must report every setting under the name kk passes, from any layer. This catches an aliased `codex.settings` key or a vendor rename, which would otherwise never yield to another layer. A failed `config/read` stops the command; the check is not skipped.

An explicit `--profile <name>` on an interactive launch is a pass-through without kk’s settings or imports. `--profile kk` has no special meaning.

An upgrade from a release that owned the profile removes the file and prints one notice. kk copies nothing out of it into `config.toml`.

Session launches that carry kk’s flags also pass `--no-daemon`. Codex runs a session with configuration flags in its own server instead of the shared background one and warns at every start; the profile had the same effect ([#205](https://github.com/serpro69/agentstakk/issues/205)). The flag only silences the warning. kk leaves it out for batch launches and other subcommands, when it passes no flags, and when the caller gives `--remote` or `--no-daemon`. A launch with a named profile gets neither kk’s flags nor `--no-daemon`.

Rejected: tolerating model keys and `[hooks.state]` in the byte comparison (unsafe, as above); parsing the profile and replaying its hook state into the trust read (needs a TOML parser to solve a problem the profile creates); a separate batch-only profile (`kk apply` would still discard interactive choices); always passing every flag (kk’s defaults would override `config.toml` and a model saved by `/model`). [Design record](https://github.com/serpro69/agentstakk/blob/master/docs/feat/done/codex-launch-overrides/design.md)

## Consequences

Model switches and hook approvals made in a `kk codex` session are saved to `config.toml` and survive `kk apply`. On the maintainer’s installation, `kk codex exec` and `kk status --live` passed after a `/model` switch and a hook approval, the batch run used the saved model, and a guard handler disabled in `/hooks` still blocked the launch. [Verification record](https://github.com/serpro69/agentstakk/blob/master/docs/feat/done/codex-launch-overrides/verification/README.md)

**Latency.** Every launch without a named profile starts one extra `app-server` session, measured at 0.15–0.30 seconds, with a 5-second limit. A batch launch starts two: the lookup must finish before the final flags exist.

**Dependency on `config/read`.** kk needs the method at every launch and every `kk apply`. If Codex removes or renames it, installs and upgrades stop in `codex_profile.validate_files` with “kk checks setting names through Codex config/read, which failed”, and the previous release stays active. Launches print “could not read Codex configuration origins” and pass no kk values (`codex_launch.session_flags`). Warning and skipping the name check instead was considered and declined on 2026-11-25: a Codex that cannot answer gets none of kk’s values at launch anyway, and a skip would also cover a transient failure and let a misnamed key through. A skip limited to a missing method is not available, because Codex answers an unknown method with a generic `-32600`. Should the skip become necessary, the `except` around `codex_app.layers` in `validate_files` would print a warning and report nothing missing, `test_apply_needs_codex_to_answer_config_read` would expect a successful apply, and the provider page would drop the requirement. That only unblocks installation. Restoring kk’s values needs a replacement for the origin lookup.

**Vendor drift.** The apply-time check catches renamed settings. Other changes in how `config/read` reports origins would show up as wrong yielding, not as an error. The `--no-daemon` rule depends on a list of Codex 0.172 subcommands in the launcher. A subcommand added later is taken for a prompt and gets the flag until the list is updated.

**Shared background server.** Sessions with kk’s flags run in their own server. `kk apply` needs a Codex that knows `--no-daemon`.

**Managed configuration.** A value pinned by a system managed layer wins over kk’s flag. A pinned default yields. A pinned explicit value is passed without effect, and kk does not report it.

**Resumed sessions.** The lookup uses the starting directory. If a resumed session belongs to another repository, kk’s defaults and explicit values can shadow that repository’s values for the session. Dropping all kk flags for resumed sessions was the alternative. The same applies to the first session in a repository the user trusts inside `kk codex`: Codex reads the repository’s configuration only after trust, which comes after the lookup.

**Argument visibility.** Settings that lived in a 0600 file are now process arguments, which other local users can often read. `codex.settings` rejects `mcp_servers`, `model_providers`, `shell_environment_policy` and `otel`, whose exporters take headers such as API keys; the remaining preference values are documented as visible.

**Upgrade and rollback.** Choices Codex saved in the old profile are dropped once, with a notice. An existing `codex.settings` with an aliased key, a credential table or a dotted top-level key stops the upgrade until it is corrected. A relative path in `codex.settings` now resolves from the launch directory instead of `$CODEX_HOME`. Rollback to v0.26.x republishes that release’s profile from its own snapshot, and its launcher uses it. That release’s `kk apply` rejects a later `codex.defaults` key as unknown.

Batch launches lose `-p kk`, which is now refused like any other named profile. [Codex provider page](../providers/codex.md#launch-settings)
