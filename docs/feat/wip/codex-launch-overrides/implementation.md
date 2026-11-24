# Implementation: Codex launch overrides

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)

The machine CLI is Python 3.8-compatible standard-library code under `kk/lib/`. Tests are `unittest` modules under `test/kk/`, driven by `bash test/test-kk.sh`. They run the real `kk` dispatcher against a temporary `KK_HOME`, `CODEX_HOME` and `XDG_CONFIG_HOME` (`InstallFixture` in `test/kk/test_install.py`). Codex is replaced by the executable test double `test/kk/codex`, which answers by argument shape: `app-server` speaks JSON-RPC on stdin/stdout, and unknown commands echo their arguments as a JSON array so tests can assert the exact `argv` kk launched. Fixture files inside the fake `CODEX_HOME` (`fixture-reviewed`, `disabled-<n>`, `fixture-no-method`) steer its answers. `test_installed_codex_loads_profile_and_independent_forbids` is the only test that drives a real Codex CLI, and it is skipped when none is on `PATH`.

Code paths to know before starting:

- `kk/lib/codex_profile.py` — `codex_settings` (override validation), `compose` (baseline + overrides → currently TOML bytes), `validate_files` (scratch-home load check), `prepare`/`publish` (owned file plan and journaled publication, including obsolete-path removal), `toml_value`, `report_drift`.
- `kk/lib/codex_launch.py` — `launch_options` (argument scan: workspace, explicit profile, batch, caller configuration flags), `import_argument` (approved `AGENTS.md` imports → `-c developer_instructions=…`), `launch_checked` (gates, batch trust check, final `argv`).
- `kk/lib/codex_trust.py` — `hooks` (one `app-server` session, `hooks/list`), `check` (guard handler verdict), `machine` (status/apply view).
- `kk/lib/claude_launch.py:139-162` — `baseline_layer`, the Claude precedent for per-key yielding, the effort special case and `claude.defaults`.
- `kk/lib/live.py` — scratch-session live check used by `kk status --live` and `kk migrate`.

## App-server client and config/read

Create `kk/lib/codex_app.py` with one function that starts `codex [flags] app-server` with `CODEX_HOME` and `cwd`, performs `initialize` + `initialized`, sends an ordered list of `(method, params)` requests, and returns their results. Move the body of `codex_trust.hooks` into it unchanged in behavior: kill timer (parameter; callers pass 10 s for trust and 5 s for the interactive lookup), stderr discarded, process killed and reaped in `finally`, `ValueError` for vendor errors and for EOF/timeout, and a distinct exception for `-32601` on any method (today `NoTrustMethod` is raised only for `hooks/list`; keep that name importable from `codex_trust` or alias it so `check` and its tests keep working).

`codex_trust.hooks` becomes a thin caller that validates the `hooks/list` row shape as today.

Add an origin lookup that sends `config/read` with `{"cwd": str(directory), "includeLayers": false}` and returns `result["origins"]` and `result["config"]`. `origins` maps a dotted canonical leaf path (array elements indexed, e.g. `tui.status_line.0`) to `{"name": {"type": …}, "version": …}`; `config` is the effective configuration, where unset tables may be `null`.

Extend `test/kk/codex` `app_server()`:

- Parse its own configuration flags **in order** into one session dictionary, accepting every spelling `launch_options` accepts (`-c x`, `-cx`, `--config x`, `--config=x`): a dotted `-c a.b=v` sets that leaf; an inline-table `-c a={…}` replaces everything under `a`; `--enable x`/`--disable x` set `features.x`. Parse inline tables with a small helper limited to the shapes kk emits (strings, integers, booleans, arrays, nested inline tables, quoted keys). Do not rely on `tomllib`: the fake runs under the system `python3`, and `test/test-kk.sh` supports older interpreters through `KK_TEST_PYTHON`.
- Derive `features.hooks` from that dictionary instead of the current `"features.hooks=false" in args` substring test, so tests detect flag-order mistakes.
- Answer `config/read` like Codex 0.172: origins from an optional `fixture-origins.json` (canonical path → type) merged with `sessionFlags` for every non-empty leaf in the session dictionary, arrays indexed per element and no origin for empty arrays or tables; `config` built from the same layers plus an optional `fixture-config.json`. An optional `fixture-aliases.json` (input path → canonical path) renames session leaves before reporting, so kk's alias handling can be tested without real Codex. A `fixture-no-config-read` file makes it return `-32601`.

→ verify: tests drive the helper against the fake for `hooks/list`, `config/read` and both error shapes; a fake run with `-c features.hooks=false -c 'features={x=true}'` reports hooks present and the reverse order reports none; existing `codex_trust` tests stay green.

## Baseline names

In `kk/baseline/codex.json`, rename `agents.max_threads` → `agents.max_concurrent_threads_per_session` and `tui.whimsy` → `tui.effects.starfield` (a nested table). Both are the names Codex 0.172 reports and accepts. The only other references are `test/kk/test_codex.py:41` and `:305` (`codex.settings` examples using `agents.max_threads`); switch them to the canonical name so they keep testing what they tested.

## Launch flag composition

**Sequencing.** The profile keeps being published (and batch launches keep comparing it) until the batch and apply tasks land. So in the interactive-launch task, add a launch-inputs function next to `compose` that shares its validation; `compose` keeps rendering TOML until the apply task deletes the rendering and the two converge. The end state is described below.

`codex_profile.compose(release, config)` returns launch inputs instead of TOML:

- **baseline leaves** — `(path_tuple, value)` pairs flattened from `baseline["profile"]`, excluding any top-level key switched off in `config["defaults"]`;
- **explicit leaves** — the selected `baseline["optIn"]` values plus `config["settings"]` flattened to `(path_tuple, value)`;
- **instructions** — the composed text, as today;
- **native** — the `nativeForbids` switch, as today.

Keep path components as tuples end to end; join with `.` only to compare against origin keys. A table key such as `docs.internal` stays one component and is rendered as one quoted key by `toml_value`.

Keep every existing validation in `compose`: `switches` for `optIn`, the hook/plugin enablement and `developer_instructions` rejections in `settings`. Add `mcp_servers`, `model_providers` and `shell_environment_policy` to the rejected `settings` keys with the existing "configure … in native Codex configuration" wording. `codex_settings` adds `"defaults"` to its accepted keys; validate `defaults` with `claude_launch.switches` against the baseline profile's top-level keys.

Add a function (in `codex_launch`) that, given the inputs, the caller's arguments and the lookup result (or `None` when the lookup failed), returns kk's `-c` arguments:

1. If the lookup result is `None`: return no baseline and no explicit leaves (approved imports are handled in step 5).
2. A leaf is **set** when some origin key equals its dotted path or starts with that path plus `.`, with an origin type other than `packagedDefaults`; or when the effective `config` holds an empty array or empty table at its path (Codex reports no origin for empty values).
3. Baseline leaf: drop if switched off, set, or shadowed by an explicit leaf at the same path. Model group (`model`, `model_reasoning_effort`, `model_context_window`, `model_auto_compact_token_limit`): drop all four baseline values when `model` is set, supplied as an explicit `codex.settings` leaf, or switched off in `codex.defaults`, or when the caller's arguments contain `-m`/`--model` (any spelling `launch_options` recognizes) or `--oss`.
4. Explicit leaf: drop only when it is set with origin type `project`. Drop the three approval/sandbox opt-in leaves when the caller's arguments contain `-s`/`--sandbox`, `-a`/`--ask-for-approval`, `--approve-for-me` or `--dangerously-bypass-approvals-and-sandbox`.
5. `developer_instructions`: an explicit leaf from the `codex-instructions.md` sidecar, unless imports were approved, in which case the import argument replaces it unconditionally (also when origins is `None`).
6. Group surviving leaves by top-level component and emit exactly one `-c` per group: `key=<toml_value>` for a scalar, `key=<inline table>` for a table built from all surviving leaves under it (baseline and explicit together). Never emit a dotted path.

Extend `launch_options` to return, in addition to its current values: the lookup directory (`-C` target or `Path.cwd()`, also for dynamic workspaces), the presence of the model, sandbox/approval, `--ignore-user-config` and `--trust` flags, and the caller's configuration flags in their original order (today's `trust_flags`).

`import_argument` currently returns `["-c", "developer_instructions=…"]` only when imports apply. Make it report whether imports replace the instructions so step 5 can apply, keeping its consent, size-limit and diagnostics behavior unchanged.

Read values from `record["releases"][active]["codex_snapshot"]["settings"]` and the active release payload, never from the live override file.

## Interactive launch

In `launch_checked`, for the non-batch path with no explicit profile:

- Replace the `kk.config.toml` presence check with: the selected `codex_profile.codex_home()` equals `snapshot["directory"]` (refuse with the same message and activation hint the batch path uses), and `$KK_HOME/codex-instructions.md` exists (refuse: run `kk apply`).
- Run the origin lookup with the caller's configuration flags and the lookup directory.
- On lookup failure print one stderr line, for example: `kk: could not read Codex configuration origins (<reason>); launching without kk defaults, opt-ins and instructions so repository settings keep precedence`, and compose with origins `None`.
- Build `argv` as `["codex", *kk_flags, *args]` with no `--profile`.

An explicit `--profile`/`-p` keeps today's pass-through: no kk flags, no imports, no lookup.

→ verify: tests assert the echoed `argv` for (a) no origins → every baseline and explicit key present, no `--profile`, one `-c` per top-level key; (b) `user` origin for `model` → none of the four model-group flags, other defaults present; (c) `-m x` → no model-group flags; (d) `project` origin for `approval_policy` with the opt-in on → flag absent, `user` origin → present; (e) `-s read-only` → no opt-in approval/sandbox flags; (f) `codex.defaults.tui=false` → no `tui` flag; (g) lookup failure → no kk flags except approved imports, one warning line; (h) a `tui.status_line.0` origin suppresses the `status_line` leaf while other `tui` leaves stay in one inline table; (i) a `codex.settings` table key containing a dot renders as one quoted key; (j) a launch under a different `CODEX_HOME` refuses (rework `test_unowned_profile_in_another_codex_home`); (k) an empty `tui.status_line` in the fake's effective config suppresses kk's `status_line`; (l) `codex.settings.model` or `codex.defaults.model=false` → none of the four baseline model-group flags.

## Batch verification

In `launch_checked` for batch launches:

- Refuse any explicit profile (`explicit is not None`) with the existing "cannot verify" wording minus its "with the kk profile" advice, and refuse `--ignore-user-config` and `--trust` with a message saying the guard cannot be verified for that configuration. Both refusals happen before any `app-server` or model process starts.
- Delete the `kk.config.toml` regular-file check, the `compose(...)[0]` comparison and the drift error. Reword the different-`CODEX_HOME` refusal so it speaks of kk's Codex settings rather than the managed profile, and share it with the interactive path.
- Compute kk's flags exactly as the interactive path does, including the same lookup-failure behavior.
- Call `codex_trust.check(release, codex_home, directory, kk_flags + caller_config_flags, …)`, where `caller_config_flags` are the caller's `-c`/`--enable`/`--disable` flags in their original order. Launch `["codex", *kk_flags, *args]`. The two sequences put every configuration flag in the same relative order by construction.

Keep the activation, fixed-workspace, `CODEX_HOME`-match and guard-receipt gates and the `unverified` behavior unchanged.

→ verify: tests show (1) a `config.toml` containing a changed `model` and a `[hooks.state]` table does not block `exec`; (2) `-cfeatures.hooks=false` still blocks with "absent", including when `codex.settings` contains another `features` leaf (kk's inline `features` table precedes the caller flag in both sequences); (3) the configuration flags the fake `app-server` received equal those of the echoed `exec` argv, in order; (4) `-pkk exec`, `exec --ignore-user-config` and `exec --trust` refuse without starting a session; (5) with `fixture-no-config-read`, `exec` launches without kk flags and prints the omission line.

In the same task, update tests whose assertions depend on the batch argv or the removed comparison: the ready-state expectation `["--profile", "kk", "exec", "hello"]`, the `matches_profile` part of `test_toml_round_trip`, `test_batch_profile_drift_explains_how_to_preserve_preferences` and `test_vendor_model_tip_update_preserves_batch_checks` (replace the last two with the success-criterion tests above rather than deleting coverage silently). Delete `matches_profile`; keep `TIP_TABLE`/`TIP_COUNTER` until the apply task removes the renderer that still uses them.

## Apply, upgrade and the removed profile

`prepare`:

- Converge `compose` with the launch-inputs function, delete TOML profile rendering, `TIP_TABLE` and `TIP_COUNTER`, and stop adding `directory / "kk.config.toml"` to `files`.
- `validate_files` no longer writes a scratch profile. In the scratch home it (1) runs `[executable, *all_candidate_flags, "debug", "prompt-input"]` (every baseline and explicit leaf plus instructions, no origin filtering), and (2) runs the origin lookup with the same flags and the scratch directory as `cwd`, and requires every kk leaf to match a `sessionFlags` origin by the origin-key part of §Launch flag composition step 2, skipping leaves whose value is an empty array or table. Report a mismatch as the leaf's dotted path plus the unmatched `sessionFlags` keys Codex reported. Keep the `config.toml` symlink and the `kk.rules` checks.
- Error messages from `validate_files` name the operation (`debug prompt-input`, `config/read`, `execpolicy check`) and Codex's stderr, never the argument list.

`publish`:

- The existing obsolete loop already unlinks paths in `record["codex_paths"]` that are no longer in `files`. When the removed path's name is `kk.config.toml`, print the one-time notice from design §4 to stdout.

Fake Codex: replace the exact-match `["--profile", "kk", "debug", "prompt-input"]` branch with "any arguments ending in `debug prompt-input`", answering `[]`.

Update `test_codex.py`, `test_codex_activation.py` and `test_lifecycle.py`:

- Remaining assertions on `self.profile` contents become assertions on launch `argv` or on the absence of `kk.config.toml`.
- `test_collision_stops_before_activation` no longer uses `kk.config.toml` as the colliding path; use an owned agent path (`agents/kk-code-reviewer.toml`) so the collision behavior stays covered.
- `test_toml_round_trip` keeps the `toml_value` round-trip (still used for `-c` values).
- The real-Codex test switches from `--profile kk debug prompt-input` to `debug prompt-input` with kk's composed flags and asserts the developer message as before; it also asserts the apply-time mapping check passes for the shipped baseline.
- Add tests: an aliased `codex.settings` key fails `kk apply` with a message naming the canonical key (fake: `fixture-aliases.json` mapping `agents.max_threads` → `agents.max_concurrent_threads_per_session`); an empty-array `codex.settings` leaf passes the mapping check; `codex.settings.mcp_servers` is rejected; a rejected candidate's error output does not contain a synthetic marker value placed in `codex.settings`.
- Add an upgrade test: seed a record whose `codex_paths` and `installed_paths` contain `kk.config.toml` with arbitrary drifted contents, run `kk apply`, assert the file is gone, the path is dropped from both lists, and the notice is printed once.

`test/guard/test_guard.py` uses `kk.config.toml` only as sample `installed_paths` data for self-modification protection; leave it.

Update the `kk codex` help string (`kk/lib/cli.py`, `commands.add_parser("codex", …)`) and the `codex_launch` module docstring so neither mentions the managed profile.

## Live-check output

In `live.run`:

- When the vendor exits non-zero, strip a leading `kk: ` from the selected stderr line before raising.
- On success return `ok (guard denied the canary read)` after the reason pattern matches.

Update `test/kk/test_status.py` assertions that expect the reason text (`assertIn("kk guard: secrets", cli.live.run(...))`) to expect the new summary, and add an assertion that a failing launch's message does not start with `kk: `.

## Documentation and ADR

- `docs/providers/codex.md`: remove `kk.config.toml` from the files table; rewrite "Where Codex saves trust decisions" (trust is saved where plain Codex keeps it; state what the real-Codex verification observed for `/model`); delete "Recover a changed managed profile"; describe the launch flags, the two precedence classes, the model group, dedicated-flag handling, `codex.defaults`, the `config/read` latency and failure behavior, the batch refusals (`--ignore-user-config`, `--trust`, explicit profiles), the one-time removal notice, that `codex.settings` values appear in the Codex command line and credential tables belong in `config.toml`; update "Project instruction budget" wording ("the managed profile sets" → "kk passes").
- `docs/user-guide/configuration.md`: rewrite the Codex paragraph and opening sentence; add `codex.defaults` to the example and prose; update the `installed_paths` list (no Codex profile); note the canonical names for kk's agent and TUI defaults.
- `docs/getting-started/overview.md:51`: replace "selects the managed profile".
- `docs/adr/0015-codex-launch-overrides.md` (Nygard template): context (#206, the ownership conflict, the probe table), decision (per-launch `-c`, two classes via `config/read`, batch trust read with the final ordered flags), consequences (latency, resumed-session trade-off, rollback asymmetry, choices in the old profile dropped once, argument visibility). In `docs/adr/0014-machine-level-delivery.md`, amend the Status line to note that ADR 0015 supersedes its Codex profile sentence.
- Do not edit `docs/feat/done/**`.

## Real-Codex verification

The vendor behaviors the rules depend on were probed during design (design.md §Vendor evidence). After the code tasks, verify the end-to-end result against the maintainer's real `~/.codex` and record it, with the Codex version, in `docs/feat/wip/codex-launch-overrides/verification/README.md`:

- Reproduce #206: interactive `kk codex`, switch `/model`, approve a repository hook, exit; then `kk codex exec "echo ok"` and `kk status --live` pass.
- Assumption 3: record where `/model` and the hook approval were saved (`config.toml` diff, or nowhere) and reflect it in `docs/providers/codex.md`. If wrapped sessions now save hook trust to `config.toml`, the "review in plain codex (without --profile)" guidance (`codex_trust.REVIEW_UI` and the provider docs) no longer needs the qualifier; simplify it in the docs task.
- Assumption 1: with the guard trusted, toggle one guard handler off in plain `codex` `/hooks`; `kk codex exec` refuses; re-enable and it passes.
- Assumption 2: time the origin lookup call itself (not a whole `kk codex` launch) over a few runs and record the range.
