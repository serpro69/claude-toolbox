# Design: Codex launch overrides

> Issue: [#206](https://github.com/serpro69/agentstakk/issues/206) — choices made inside `kk codex` sessions drift the managed profile and break batch launches
> Status: design approved, 2026-11-24; revised after two design reviews and a consistency pass with further probes, 2026-11-24; empty-value rule limited to arrays after the Task 1 probes, 2026-11-25; a failed apply-time `config/read` stops `kk apply` (maintainer decision after the Task 4 review), 2026-11-25; session launches with kk flags pass `--no-daemon`, and the apply-time name check accepts a name reported by any layer (maintainer decisions during the Task 6 verification), 2026-11-26; the resumed-session trade-off names kk's defaults as well as its explicit values (maintainer decision after the Task 7 review), 2026-11-26; `otel` joins the rejected credential tables, and the first-session and relative-path consequences are documented (maintainer decisions after the final review), 2026-11-26; `--yolo`, the plain-name rule and the Assumption 3 outcome recorded after the spec review, 2026-11-26
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
3. A `model` set in `$CODEX_HOME/config.toml`, a trusted repository's `.codex/config.toml` or the command line is the one the session uses, without kk's context-window, compaction or effort defaults sized for kk's own model. (A model the adopter puts in `codex.settings` is an explicit kk choice and beats `config.toml`, as the profile did.)
4. kk no longer writes `kk.config.toml`.

## Constraints and size

- kk supports Python 3.8: there is no standard TOML parser.
- kk writes nothing into repositories ([ADR 0014](../../../adr/0014-machine-level-delivery.md)).
- Offline rollback to an older release keeps working.
- Process arguments are readable by other local users on common Linux setups (`/proc/<pid>/cmdline` without `hidepid`), unlike the 0600 profile file.
- Size and lifetime: one machine-wide launcher path that every `kk codex` launch crosses, recurring indefinitely. The change is confined to `kk/lib/codex_profile.py`, `codex_launch.py`, `codex_trust.py`, `live.py`, the `kk codex` help text in `cli.py`, one new helper module, `kk/baseline/codex.json`, the fake Codex test double, `test/kk/` tests and the Codex user docs.

## Vendor evidence (Codex 0.172.0, scratch `CODEX_HOME`)

| Probe | Result |
| --- | --- |
| `codex --profile kk app-server` | Refused: `--profile only applies to runtime commands`; `app-server` is not one |
| `-c 'hooks.state={"<key>"={trusted_hash=…, enabled=false}}'` on `app-server` | `hooks/list` reports `enabled=false`, `trustStatus=trusted` |
| `-c 'hooks.state."<key with dots>".trusted_hash=…'` | Silently ignored: Codex splits dotted paths even inside quotes |
| `-c features.hooks=false` | All hooks disappear from `hooks/list` |
| Inline-table `-c` vs `config.toml` `hooks.state` | Merges field by field **across layers**; unrelated entries untouched |
| `-c features.hooks=false -c 'features={shell_snapshot=true}'` | The later inline table replaces the earlier flag: hooks stay enabled. In the reverse order hooks are off. Within the `-c` layer, order matters |
| `-c model=…` vs trusted project `.codex/config.toml` `model` | `-c` wins (origin `sessionFlags`) |
| `config/read` with `cwd` | Returns effective `config` and per-leaf `origins` (`user`, `project`, `sessionFlags`, …); unset keys have no origin |
| `config/read` origin key names | Canonical, not as written: `agents.max_threads` → `agents.max_concurrent_threads_per_session`, `tui.whimsy` → `tui.effects.starfield`; arrays per element (`tui.status_line.0`, `.1`, …) |
| Canonical names as `-c` input | Accepted and reported under the same names |
| Keys Codex does not know (`my_new_preference`, `tui.made_up`) | Reported under the raw name with origin `sessionFlags` |
| Empty array or table (`tui.status_line = []`), from `-c` or `config.toml` | **No origin reported**; the effective `config` shows the empty value. With nothing set, Codex's own value for kk's array leaves is absent (`config.tui` is `null`); once another `tui` value is set they stay `null`, while `tui.default_hosts`, `tui.presets` and `tui.model_availability_nux` default to `{}` |
| Origin types with nothing configured | Only `user` (for `projects.*`); `packagedDefaults` was not observed |
| `codex -c developer_instructions=… debug prompt-input`, no profile | The value arrives as a `developer` message |
| `exec`-only flags | `--ignore-user-config` omits `config.toml` from the run; `--trust` writes project trust during the run. `app-server` accepts neither |

Earlier evidence (machine-level-delivery design): the profile ranks above `config.toml` and below trusted project config.

## Design

### 1. Launch flags instead of a profile

`kk codex` runs plain `codex` with `-c` flags built from three sources. Values come from the active release's saved snapshot (`codex_snapshot.settings`), not the live override file, so "edit `config.json`, then `kk apply`" keeps its meaning and `report_drift` still warns about unapplied edits.

| Class | Keys | Passed unless |
| --- | --- | --- |
| Baseline defaults | Leaves of the baseline `profile` in `kk/baseline/codex.json`: `model`, `model_reasoning_effort`, `model_context_window`, `model_auto_compact_token_limit`, `project_doc_max_bytes`, `agents.*`, `tui.*` | switched off in `codex.defaults`; or set elsewhere (see origin matching); or, for the model group, the model is not kk's baseline model |
| Explicit values | `developer_instructions` (the `codex-instructions.md` sidecar), the `codex.optIn` approval and sandbox values, `codex.settings` leaves | `config/read` reports a `project` origin; or, for approval and sandbox values, a dedicated command-line flag sets them |
| Approved imports | `developer_instructions` combined with imported files | never (unchanged behavior) |

Explicit values reproduce the profile's old precedence slot: they beat `config.toml` and yield to a trusted repository. This keeps the documented promises that existing project sandbox and approval settings win after migration and that a trusted repository's own `developer_instructions` win on ordinary launches. Baseline defaults also yield to `config.toml`, so a model chosen there (or saved there by Codex) is used. A `codex.settings` leaf at the same path as a baseline leaf replaces the baseline leaf, as `overlay` does today.

**Origin matching.** The baseline uses Codex's canonical key names (`agents.max_concurrent_threads_per_session`, `tui.effects.starfield`), which Codex accepts as input. A kk leaf counts as set when an origin key equals its dotted path or starts with that path plus `.` (array elements), with an origin type other than `packagedDefaults` (never observed, but defined by the protocol as Codex's own default). Because Codex reports no origin for an empty array, a leaf also counts as set when the effective `config` holds an empty array at its path; Codex's own value for kk's array leaves is absent, so an empty array can only come from a configuration layer. An empty table does not count, because Codex fills some tables (`tui.presets`, for example) with `{}` by default. `kk apply` checks the mapping (section 4), so a future vendor rename or an aliased `codex.settings` key fails loudly instead of silently never yielding.

**Model group.** `model`, `model_reasoning_effort`, `model_context_window` and `model_auto_compact_token_limit` are sized together for kk's default model. All four baseline values are dropped when the session's model will not be kk's baseline model: `model` is set elsewhere, supplied by `codex.settings`, switched off in `codex.defaults`, or the command line carries `-m`/`--model` or `--oss`. Otherwise each still yields individually. A `codex.settings` value for one of the other three is explicit and stays. This mirrors `kk claude`'s special-casing of effort.

**Dedicated flags.** `-s`/`--sandbox`, `-a`/`--ask-for-approval`, `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox` and its alias `--yolo` (accepted by Codex 0.172 though `--help` does not list it) express the caller's sandbox and approval choice for this launch; when any is present, kk passes none of its approval and sandbox opt-in values. Their precedence against `-c` is therefore never relied on.

`codex.defaults` mirrors `claude.defaults`: an object of booleans keyed by the baseline's top-level preference names; `false` switches that default off. It covers the case where an adopter wants Codex's own built-in value without pinning one in `config.toml`, and keeps the two launchers' override files symmetric; the adopter asked for opt-outs explicitly.

`codex.settings` keeps its rejections (hook and plugin enablement, `developer_instructions`) and additionally rejects the credential-bearing tables `mcp_servers`, `model_providers`, `shell_environment_policy` and `otel` (whose exporters take headers such as API keys, which Codex itself redacts in `config/read`) with the existing "configure … in native Codex configuration" message. Those belong in `config.toml`, where the MCP guide already puts them, not in process arguments. A top-level `codex.settings` key must also be a plain name (`[A-Za-z0-9_-]+`): as a launch flag Codex splits a key on every dot, so `"features.hooks"`, an inert quoted key in the profile, would switch hooks off past the enablement rejection (confirmed by the maintainer, 2026-11-26). Other `codex.settings` values become visible in the Codex command line, which the docs state.

**Encoding.** Leaves keep their key components through composition; dotted strings are used only to compare with `config/read` origins. kk emits **exactly one** `-c` per top-level key: a scalar is `key=value`; a table is one inline table built from every surviving baseline and explicit leaf under that key (`-c tui={…}`). A second inline table for the same key would replace the first. Dotted paths are never emitted, because keys containing dots are ignored. A key containing a dot (for example a table named `docs.internal`) stays one quoted inline-table key. Values render through the existing `toml_value`.

**Order.** The final command is `codex <kk flags> <caller arguments>`. Caller `-c` flags come after kk's, so a caller flag for the same leaf wins, and a caller inline table replaces kk's table for that key, as the caller asked.

**Shared background server.** Codex 0.172 attaches the session TUI to a shared background `app-server` and falls back to a server of its own when the launch carries configuration flags, with a startup warning (`Running without the shared background server: command-line configuration overrides … requires embedded mode`). The managed profile had the same effect ([#205](https://github.com/serpro69/agentstakk/issues/205)), so this is an existing limitation of `kk codex`, accepted and documented (decided 2026-11-26). To keep Codex from warning at every start, kk puts `--no-daemon` in front of its flags when it passes at least one and the launch opens the session TUI: no subcommand, a prompt, `resume` or `fork`. A first word that is not a Codex subcommand counts as a prompt. kk does not add the flag when the caller gave `--remote` or `--no-daemon` (Codex refuses both combinations), for other subcommands (`queue` and `remote-control` refuse it), or for batch launches, which show no such warning. The flag changes no behavior: the session runs in its own server either way.

An explicit `--profile <name>` remains a pass-through with no kk flags and no imports. `--profile kk` loses its special meaning.

**Lookup failure.** If `config/read` fails (timeout, vendor error, missing method), kk cannot tell which values a repository or the account already set. Interactive and batch launches then pass no origin-dependent kk values: no baseline defaults and no explicit values. Approved imports still apply, because the adopter consented to them replacing repository instructions. kk prints one line saying that kk's defaults, opt-ins and instructions were omitted and why. Batch launches proceed to the trust read with these reduced flags; the guard guarantee comes from that read, not from the origins.

### 2. `app-server` client and origin lookup

The `initialize` / `initialized` / request plumbing in `codex_trust.hooks` moves to a small shared helper that runs a list of requests in one `app-server` session and returns their results, preserving today's error handling (including `-32601` for a missing method). `hooks/list` and `config/read` both use it.

The origin lookup sends `config/read` with `cwd` set to the lookup directory and returns both `origins` and the effective `config` (needed for empty arrays). `launch_options` returns that directory separately from the verified workspace: the `-C` target or current directory, even for `resume`, `fork`, `--remote` and `--worktree`, where the verified workspace stays `None`. The lookup's `app-server` process receives only the caller's own `-c`/`--enable`/`--disable` flags in their original order, so a caller `-c model=…` appears as `sessionFlags` and beats kk's default. The interactive lookup has a 5-second kill timer; the batch trust read keeps 10 seconds.

For resumed sessions, if the session belongs to another repository, that repository's project values can be shadowed by kk's defaults and explicit values for the session: the lookup reads the starting directory, so a default that neither that directory nor the account sets is passed too. Imports are already skipped in this case; the trade-off is accepted rather than dropping all kk flags for resumed sessions.

The same holds for the first session in a repository the user trusts inside `kk codex`: Codex reports no `project` origin for an untrusted repository, so the lookup sees none, and when the user trusts the folder in that session Codex loads the repository's configuration below kk's flags. Later sessions are correct; trusting the folder in plain `codex` first avoids it. Accepted and documented (2026-11-26). Path values in `codex.settings` resolve from the launch directory as flags, not from `$CODEX_HOME` as in the profile; the docs ask for absolute paths.

### 3. Batch verification

`launch_checked` keeps the activation, fixed-workspace, `CODEX_HOME` and guard-receipt gates. It additionally refuses:

- any explicit `--profile`;
- `--ignore-user-config` and `--trust`, whose configuration and trust effects the `app-server` trust read cannot reproduce. The refusal happens before any model session starts. `--dangerously-bypass-hook-trust` is not refused: it can only make the run stricter than the read.

It drops the `kk.config.toml` file checks, `compose` and `matches_profile`. It computes the launch flags (section 1), then calls `codex_trust.check` with **the configuration flags of the final command in their final order**: kk's flags followed by the caller's `-c`/`--enable`/`--disable` flags, extracted from the caller's arguments in order. The trust read and the `exec` that follows therefore share `CODEX_HOME`, working directory and an identical ordered configuration-flag sequence, which replaces the byte comparison as the guarantee that nothing changes hook state between check and run.

This is two `app-server` sessions per batch launch: the origin lookup must finish before the final flags exist, and Codex cannot change its layers mid-session. The second start adds about 0.2–0.4 seconds to a path that then starts a model session.

`TIP_TABLE`, `TIP_COUNTER` and `matches_profile` are deleted once nothing references them. `codex_trust.machine` (`kk status`, `kk apply`) and `migrate.verify_workspace` keep reading plain-account trust: they answer "is the guard reviewed?", while only the batch launcher answers "will the guard run for this launch?".

### 4. Interactive gates, apply, upgrade and rollback

Interactive launches without an explicit profile keep a `CODEX_HOME` gate: the selected home must equal the snapshot's `directory`, as batch launches already require; otherwise the launch refuses with the existing activation hint. The `codex-instructions.md` sidecar must also exist. This replaces today's "profile path is recorded in `codex_paths`" check, which also failed in a home kk was never applied to.

`compose` returns launch inputs (baseline leaves after `codex.defaults`, explicit leaves, instruction text, the `nativeForbids` switch) instead of TOML bytes. `codex_settings` accepts the new `defaults` key. `prepare` stops publishing `kk.config.toml`; it still publishes `agents/kk-*.toml` and the opt-in `rules/kk.rules`. `validate_files`, in its existing scratch home:

1. runs `codex --no-daemon <all candidate -c flags> debug prompt-input`, so a value Codex rejects still stops publication before any owned file changes, and so does a Codex that does not know `--no-daemon`, which would otherwise refuse every session launch;
2. sends `config/read` with the same flags and requires every kk leaf to be reported under a matching key (section 1). The origin is `sessionFlags` unless a layer that outranks the flags sets the same key: a system `managed_config.toml` does (origin `legacyManagedConfigTomlFromFile`, observed in Task 6), and the name it is reported under is just as good evidence that kk's name is the one Codex uses (decided 2026-11-26; until then only `sessionFlags` counted, which stopped `kk apply` on a machine whose administrator pins a key kk passes). Leaves whose value is an empty array or table are skipped, because Codex reports no origin for them. A mismatch names the leaf and the keys Codex reported instead, for example an aliased `codex.settings` name. If `config/read` itself fails (missing method, vendor error, timeout), validation fails with a message naming `config/read` and nothing is published; the check is not skipped (see Not Doing).

Validation errors name the operation and the stderr of Codex, never the argument list, so `codex.settings` values are not copied into kk's output.

On upgrade from a release that owned the profile, the existing obsolete-path logic unlinks `kk.config.toml` and removes it from `installed_paths`. `publish` then prints once: the managed profile was removed; model or hook-trust choices saved there no longer apply; set them in plain `codex` or `config.toml`. kk copies nothing out of the file, because `config.toml` is not kk's to write. An existing `codex.settings` that uses an aliased key name, a newly rejected credential table or a top-level key that is not a plain name stops the upgrade with the validation message; the adopter renames the key, moves the table to `config.toml` or writes the dotted key as a nested object, and reruns the upgrade.

Rollback to v0.26.x republishes that release's profile from its own snapshot, and its launcher uses it. A `codex.defaults` key added afterwards makes the older release's `kk apply` reject `config.json` with its unknown-key error; this is documented, not handled.

The snapshot shape and `report_drift` are unchanged.

### 5. Output fixes

`live.run` strips a leading `kk: ` from the vendor stderr line it reuses as an exception message (fixing `kk: kk: …`), and returns `ok (guard denied the canary read)` instead of the bare guard reason, which read like an error. Attribution still requires the reason pattern to match. The `kk codex` help text, the `codex_launch` module docstring and the launcher's remaining messages (the batch "named profile … with the kk profile" refusal and the "different CODEX_HOME" refusal, now shared with interactive launches) stop mentioning the managed profile.

## Assumptions

1. An `app-server` session given the final ordered configuration flags and the run's working directory reports the same guard hook state that the following `exec` applies.
2. `config/read` costs about 0.2–0.4 seconds per interactive launch, like `hooks/list` (0.16–0.44 seconds measured).
3. Without a profile, `/model` and hook approvals either persist to `config.toml` or last only for the session. Either is acceptable; the design records which. Observed with Codex 0.172.0 (Task 6): `/model`, folder trust and hook approvals made in a `kk codex` session are all saved to `config.toml`.
4. The `config/read` behavior in the evidence table (canonical keys, indexed arrays, unreported empty values, raw unknown keys) holds for the Codex versions kk supports. The apply-time mapping check catches renames; other changes would surface as wrong yielding, not as an error.
5. Codex keeps the `config/read` method on `app-server`. kk depends on it at every launch and at every `kk apply`. What breaks if it goes away, and where, is recorded under Not Doing.

## Not Doing

- **Repository-scoped kk config** — repositories already override through their own Codex config, which the origin check reads.
- **Carrying choices from an existing `kk.config.toml` into `config.toml`** — kk never writes the adopter's Codex config; a one-time notice replaces it.
- **A TOML parser or a higher Python minimum** — unnecessary once kk owns no TOML file.
- **A diff in the profile-mismatch error** — the comparison is removed.
- **Keeping `--profile kk` working** — an explicit profile becomes a plain pass-through.
- **Hiding `codex.settings` values from process listings** — credential tables are rejected; remaining preference values are documented as visible.
- **Skipping the apply-time name check when `config/read` fails** (warn and keep `debug prompt-input` as the only gate) — decided 2026-11-25. `kk apply`, install and upgrade stop instead, and the previous release stays active. Reasons: every launch depends on the same request, so a Codex that cannot answer it gets none of kk's defaults, opt-ins or instructions anyway; and a skip would also cover a transient failure on a working Codex, letting a misnamed key through, which then overrides a repository's value at launch. A skip limited to "the method is missing" is not available without matching error text: Codex 0.172 answers an unknown method with a generic `-32600`. This is not about supporting older Codex versions. It is recorded so the dependency can be traced: **if Codex removes or renames `config/read`**, installs and upgrades stop in `codex_profile.validate_files` with "kk checks setting names through Codex config/read, which failed", and launches print "could not read Codex configuration origins" and pass no kk values (`codex_launch.session_flags`). Skipping the check would then only unblock installation; restoring kk's values needs a replacement for the origin lookup (`codex_app.origins`). To apply the skip: in `validate_files`, the `except` around `codex_app.layers` (inside `unreported`) prints one `kk:` warning that setting names were not checked and why, and reports nothing missing instead of raising, so `debug prompt-input` and the `kk.rules` checks still gate publication; `test_apply_needs_codex_to_answer_config_read` in `test/kk/test_codex.py` then expects a successful apply with that warning; and the Codex provider docs drop the `config/read` requirement. Accept with it that a misnamed `codex.settings` key is no longer caught whenever the lookup fails.

## Rejected Alternatives

- **Tolerate model keys and `[hooks.state]` in the byte comparison** — unsafe: the trust read does not load the profile, so a profile-held disabled guard handler would pass; line matching also breaks on reformatting.
- **Keep the profile, parse it and replay its `hooks.state` into the trust read** — works, but needs a TOML parser on Python 3.8 and a merge step in `kk apply`, to fix a problem the profile itself creates.
- **Separate kk-only batch profile** — fixes batch launches but `kk apply` still discards interactive choices, and kk owns two profile files.
- **Always pass `-c` unless opted out** — simpler, but kk defaults would beat `config.toml` and repository config until switched off globally, and `/model` saved to `config.toml` would be overridden on the next launch.
- **Force `developer_instructions` and approval/sandbox opt-ins over repository config** — changes the documented migration promise and lets kk's instructions replace a repository's own.
- **Refuse batch launches when `config/read` fails** — the guard guarantee comes from the trust read with the final flags, so refusing would only block Codex builds without the method; omitting origin-dependent values keeps precedence safe.
- **Drop `codex.defaults`** — no success criterion needs it, but the adopter asked for opt-outs, and it keeps parity with `claude.defaults`.
