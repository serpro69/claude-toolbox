# Design: Codex launch overrides

> Issue: [#206](https://github.com/serpro69/agentstakk/issues/206) — choices made inside `kk codex` sessions drift the managed profile and break batch launches
> Status: design approved, 2026-11-24
> Evidence: Codex CLI 0.172.0, Linux

## Problem

`kk codex` launches `codex --profile kk`, which layers the kk-owned file `$CODEX_HOME/kk.config.toml`. Codex treats the selected profile as the place to save interactive choices: `/model` rewrites `model` and `model_reasoning_effort` there, and hook approvals add `[hooks.state]` tables. Batch launches (`exec`, `review`, the `kk migrate` live check, `kk status --live`) refuse unless that file matches the generated profile byte for byte, apart from the tip-counter table. A routine `/model` switch therefore breaks every later batch launch, and the failure surfaces days later in another repository. `kk apply` "fixes" it by discarding the choices.

The byte comparison is load-bearing today. The live trust read (`codex_trust.hooks`) starts `codex app-server` without the profile, so it sees plain-account hook state, while the batch run that follows loads the profile. The comparison is the only guarantee that the profile cannot change hook enablement or trust between the check and the run. Simply tolerating `[hooks.state]` would let a profile-held `enabled = false` for a guard handler pass the check.

The root cause is ownership: kk treats a file that Codex writes to as kk-owned and immutable.

**How might we** let people change models and approve hooks normally inside `kk codex`, while batch launches keep verifying the guard that will actually run, without kk owning a file Codex writes?

## Who and success

Anyone running `kk codex`: interactively (model switches, repository hook approvals) and in batch (`kk codex exec`/`review`, the `kk migrate` live check, `kk status --live`). The maintainer hit the failure twice.

Success:

1. After any interactive `kk codex` session, including `/model` and hook approvals, the next `kk codex exec "echo ok"` and the `kk migrate` live check pass without `kk apply`.
2. A guard handler that is disabled or untrusted for the run's workspace still blocks a batch launch, including when the user's own `-c` flags cause it.
3. A `model` set in `$CODEX_HOME/config.toml` or a trusted repository's `.codex/config.toml` is the one the session uses.
4. kk no longer writes `kk.config.toml`.

## Constraints and size

- kk supports Python 3.8: there is no standard TOML parser.
- kk writes nothing into repositories ([ADR 0014](../../../adr/0014-machine-level-delivery.md)).
- Offline rollback to an older release keeps working.
- Size and lifetime: one machine-wide launcher path that every `kk codex` launch crosses, recurring indefinitely. The change is confined to `kk/lib/codex_profile.py`, `codex_launch.py`, `codex_trust.py`, `live.py`, one new helper module, the fake Codex test double, `test/kk/` tests and the Codex user docs.

## Vendor evidence (Codex 0.172.0, scratch `CODEX_HOME`)

| Probe | Result |
| --- | --- |
| `codex --profile kk app-server` | Refused: `--profile only applies to runtime commands`; `app-server` is not one |
| `-c 'hooks.state={"<key>"={trusted_hash=…, enabled=false}}'` on `app-server` | `hooks/list` reports `enabled=false`, `trustStatus=trusted` |
| `-c 'hooks.state."<key with dots>".trusted_hash=…'` | Silently ignored: Codex splits dotted paths even inside quotes |
| `-c features.hooks=false` | All hooks disappear from `hooks/list` |
| Inline-table `-c` vs `config.toml` `hooks.state` | Merges field by field; unrelated entries untouched |
| `-c model=…` vs trusted project `.codex/config.toml` `model` | `-c` wins (origin `sessionFlags`) |
| `config/read` with `cwd` | Returns effective `config` and per-key `origins` (`user`, `project`, `sessionFlags`, …); unset keys have no origin |

Earlier evidence (machine-level-delivery design): the profile ranks above `config.toml` and below trusted project config; `-c developer_instructions=…` reaches the model as a developer message.

## Design

### 1. Launch flags instead of a profile

`kk codex` runs plain `codex` with `-c` flags built from three sources. Values come from the active release's saved snapshot (`codex_snapshot.settings`), not the live override file, so "edit `config.json`, then `kk apply`" keeps its meaning and `report_drift` still warns about unapplied edits.

| Class | Keys | Passed unless |
| --- | --- | --- |
| Baseline defaults | Leaves of the baseline `profile` in `kk/baseline/codex.json`: `model`, `model_reasoning_effort`, `model_context_window`, `model_auto_compact_token_limit`, `project_doc_max_bytes`, `agents.*`, `tui.*` | switched off in `codex.defaults`, or `config/read` reports any origin other than `packagedDefaults` |
| Explicit values | `developer_instructions` (the `codex-instructions.md` sidecar), the `codex.optIn` approval and sandbox values, `codex.settings` leaves | `config/read` reports a `project` origin |
| Approved imports | `developer_instructions` combined with imported files | never (unchanged behavior) |

Explicit values reproduce the profile's old precedence slot: they beat `config.toml` and yield to a trusted repository. This keeps the documented promises that existing project sandbox and approval settings win after migration and that a trusted repository's own `developer_instructions` win on ordinary launches. Baseline defaults also yield to `config.toml`, so a model chosen there (or saved there by Codex) is used.

`codex.defaults` mirrors `claude.defaults`: an object of booleans keyed by the baseline's top-level preference names; `false` switches that default off. `codex.settings` keeps its rejections (hook and plugin enablement, `developer_instructions`).

Encoding: a scalar is `-c key=value`; a table becomes one inline table per top-level key (`-c tui={…}`), which Codex merges field by field. Dotted paths are never emitted, because keys containing dots are ignored. Values render through the existing `toml_value`.

An explicit `--profile <name>` remains a pass-through with no kk flags and no imports. `--profile kk` loses its special meaning.

If `config/read` fails (timeout, vendor error, missing method), an interactive launch passes the explicit values, skips the baseline defaults and prints one line saying so. A batch launch refuses.

### 2. `app-server` client and origin lookup

The `initialize` / `initialized` / request plumbing in `codex_trust.hooks` moves to a small shared helper that runs a list of requests in one `app-server` session and returns their results, preserving today's error handling (including `-32601` for a missing method). `hooks/list` and `config/read` both use it.

The origin lookup sends `config/read` with `cwd` set to the launch directory (`-C` target or current directory). Its `app-server` process receives only the user's own `-c`/`--enable`/`--disable` flags, so a user `-c model=…` appears as `sessionFlags` and beats kk's default. Origins are keyed by dotted leaf path. The interactive lookup has a 5-second kill timer; the batch trust read keeps 10 seconds.

Sessions without a fixed workspace (`resume`, `fork`, `--remote`, `--worktree`) still run the lookup from the current directory. If the resumed session belongs to another repository, that repository's project values can be shadowed by kk's explicit values for the session. Imports are already skipped in this case; the trade-off is accepted rather than dropping all kk flags for resumed sessions.

### 3. Batch verification

`launch_checked` keeps the activation, fixed-workspace, `CODEX_HOME` and guard-receipt gates. It refuses any explicit `--profile`. It drops the `kk.config.toml` file checks, `compose` and `matches_profile`. It computes the launch flags (section 1), refusing if `config/read` fails, then calls `codex_trust.check` with the user's flags **plus kk's final flags**. The trust read and the `exec` that follows therefore share `CODEX_HOME`, working directory and `-c` set, which replaces the byte comparison as the guarantee that nothing changes hook state between check and run.

This is two `app-server` sessions per batch launch: the origin lookup must finish before the final flags exist, and Codex cannot change its layers mid-session. The second start adds about 0.2–0.4 seconds to a path that then starts a model session.

`TIP_TABLE`, `TIP_COUNTER` and `matches_profile` are deleted. `codex_trust.machine` (`kk status`, `kk apply`) and `migrate.verify_workspace` keep reading plain-account trust: they answer "is the guard reviewed?", while only the batch launcher answers "will the guard run for this launch?".

### 4. Apply, upgrade and rollback

`compose` returns launch inputs (baseline defaults after `codex.defaults`, explicit values, instruction text, the `nativeForbids` switch) instead of TOML bytes. `codex_settings` accepts the new `defaults` key. `prepare` stops publishing `kk.config.toml`; it still publishes `agents/kk-*.toml` and the opt-in `rules/kk.rules`. `validate_files` runs `codex <all candidate -c flags> debug prompt-input` in its existing scratch home, so a value Codex rejects still stops publication before any owned file changes.

On upgrade from a release that owned the profile, the existing obsolete-path logic unlinks `kk.config.toml` and removes it from `installed_paths`. `publish` then prints once: the managed profile was removed; model or hook-trust choices saved there no longer apply; set them in plain `codex` or `config.toml`. kk copies nothing out of the file, because `config.toml` is not kk's to write.

Rollback to v0.26.x republishes that release's profile from its own snapshot, and its launcher uses it. A `codex.defaults` key added afterwards makes the older release's `kk apply` reject `config.json` with its unknown-key error; this is documented, not handled.

The `codex-instructions.md` sidecar, the snapshot shape and `report_drift` are unchanged. The interactive "managed profile is missing" check becomes a check for the sidecar.

### 5. Output fixes

`live.run` strips a leading `kk: ` from the vendor stderr line it reuses as an exception message (fixing `kk: kk: …`), and returns `ok (guard denied the canary read)` instead of the bare guard reason, which read like an error. Attribution still requires the reason pattern to match.

## Assumptions

1. A key absent from `config/read` origins, or with origin `packagedDefaults`, is unset; every other origin type (`user`, `project`, `sessionFlags`, `system`, `mdm`, `enterpriseManaged`, legacy managed types) means kk yields.
2. `config/read` origins are keyed per leaf path, so `agents.max_threads` and `tui.status_line` resolve individually (observed only for `projects.<path>.trust_level`).
3. `-c developer_instructions=…` without a profile reaches the model as a developer message (observed earlier only with `--profile kk`).
4. An `app-server` session given kk's final flags and the run's working directory reports the same guard hook state that the following `exec` applies.
5. `config/read` costs about 0.2–0.4 seconds per interactive launch, like `hooks/list` (0.16–0.44 seconds measured).
6. Without a profile, `/model` and hook approvals either persist to `config.toml` or last only for the session. Either is acceptable; the design records which.

## Not Doing

- **Repository-scoped kk config** — repositories already override through their own Codex config, which the origin check reads.
- **Carrying choices from an existing `kk.config.toml` into `config.toml`** — kk never writes the adopter's Codex config; a one-time notice replaces it.
- **A TOML parser or a higher Python minimum** — unnecessary once kk owns no TOML file.
- **A diff in the profile-mismatch error** — the comparison is removed.
- **Keeping `--profile kk` working** — an explicit profile becomes a plain pass-through.

## Rejected Alternatives

- **Tolerate model keys and `[hooks.state]` in the byte comparison** — unsafe: the trust read does not load the profile, so a profile-held disabled guard handler would pass; line matching also breaks on reformatting.
- **Keep the profile, parse it and replay its `hooks.state` into the trust read** — works, but needs a TOML parser on Python 3.8 and a merge step in `kk apply`, to fix a problem the profile itself creates.
- **Separate kk-only batch profile** — fixes batch launches but `kk apply` still discards interactive choices, and kk owns two profile files.
- **Always pass `-c` unless opted out** — simpler, but kk defaults would beat `config.toml` and repository config until switched off globally, and `/model` saved to `config.toml` would be overridden on the next launch.
- **Force `developer_instructions` and approval/sandbox opt-ins over repository config** — changes the documented migration promise and lets kk's instructions replace a repository's own.
