# Implementation: Codex launch overrides

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)

The machine CLI is Python 3.8-compatible standard-library code under `kk/lib/`. Tests are `unittest` modules under `test/kk/`, driven by `bash test/test-kk.sh`. They run the real `kk` dispatcher against a temporary `KK_HOME`, `CODEX_HOME` and `XDG_CONFIG_HOME` (`InstallFixture` in `test/kk/test_install.py`). Codex is replaced by the executable test double `test/kk/codex`, which logs nothing itself but answers by argument shape: `app-server` speaks JSON-RPC on stdin/stdout, and unknown commands echo their arguments as a JSON array so tests can assert the exact `argv` kk launched. Fixture files inside the fake `CODEX_HOME` (`fixture-reviewed`, `disabled-<n>`, `fixture-no-method`) steer its answers. `test_installed_codex_loads_profile_and_independent_forbids` is the only test that drives a real Codex CLI, and it is skipped when none is on `PATH`.

Code paths to know before starting:

- `kk/lib/codex_profile.py` — `codex_settings` (override validation), `compose` (baseline + overrides → currently TOML bytes), `validate_files` (scratch-home load check), `prepare`/`publish` (owned file plan and journaled publication, including obsolete-path removal), `toml_value`, `report_drift`.
- `kk/lib/codex_launch.py` — `launch_options` (argument scan: workspace, explicit profile, batch, user trust flags), `import_argument` (approved `AGENTS.md` imports → `-c developer_instructions=…`), `launch_checked` (gates, batch trust check, final `argv`).
- `kk/lib/codex_trust.py` — `hooks` (one `app-server` session, `hooks/list`), `check` (guard handler verdict), `machine` (status/apply view).
- `kk/lib/claude_launch.py:139-162` — `baseline_layer`, the Claude precedent for per-key yielding and `claude.defaults`.
- `kk/lib/live.py` — scratch-session live check used by `kk status --live` and `kk migrate`.

## App-server client and config/read

Create `kk/lib/codex_app.py` with one function that starts `codex [flags] app-server` with `CODEX_HOME` and `cwd`, performs `initialize` + `initialized`, sends an ordered list of `(method, params)` requests, and returns their results. Move the body of `codex_trust.hooks` into it unchanged in behavior: kill timer (parameter; callers pass 10 s for trust and 5 s for the interactive lookup), stderr discarded, process killed and reaped in `finally`, `ValueError` for vendor errors and for EOF/timeout, and a distinct exception for `-32601` on any method (today `NoTrustMethod` is raised only for `hooks/list`; keep that name importable from `codex_trust` or alias it so `check` and its tests keep working).

`codex_trust.hooks` becomes a thin caller that validates the `hooks/list` row shape as today.

Add an origin lookup (in `codex_launch` or `codex_app`, whichever keeps `codex_launch` readable) that sends `config/read` with `{"cwd": str(directory), "includeLayers": false}` and returns `result["origins"]`: a mapping from dotted leaf path to `{"name": {"type": …}, "version": …}`.

Extend `test/kk/codex` `app_server()` to answer `config/read`: origins come from an optional JSON fixture in `CODEX_HOME` (for example `fixture-origins.json`, mapping path → type), plus `sessionFlags` for every `-c key=…` in its own `args` (top-level key and, for inline tables, each `key.leaf`). A `fixture-no-config-read` file makes it return `-32601`.

→ verify: unit tests drive the helper against the fake for `hooks/list`, `config/read` and both error shapes; existing `codex_trust` tests stay green.

## Launch flag composition

**Sequencing.** The profile keeps being published (and batch launches keep comparing it) until the batch and apply tasks land. So in the interactive-launch task, add a launch-inputs function next to `compose` that shares its validation; `compose` keeps rendering TOML until the apply task deletes the rendering and the two converge. The end state is described below.

`codex_profile.compose(release, config)` returns launch inputs instead of TOML:

- **baseline defaults** — flattened leaves of `baseline["profile"]` (dotted path → value), excluding any top-level key switched off in `config["defaults"]`;
- **explicit values** — the selected `baseline["optIn"]` values plus flattened `config["settings"]` leaves;
- **instructions** — the composed text, as today;
- **native** — the `nativeForbids` switch, as today.

Keep every existing validation in `compose`: `switches` for `optIn`, the hook/plugin enablement and `developer_instructions` rejections in `settings`. `codex_settings` adds `"defaults"` to its accepted keys; validate `defaults` with `claude_launch.switches` against the baseline profile's top-level keys. The TUI tip-table special-casing (`TIP_TABLE`, `TIP_COUNTER`, the `model_availability_nux` pop) and `matches_profile` are deleted. A `codex.settings.tui.model_availability_nux` value becomes an ordinary explicit leaf.

Add a function (in `codex_launch`) that, given the inputs and an origins mapping (or `None` when the lookup failed), returns the `-c` arguments:

1. Baseline leaf: keep when origins is not `None` and the leaf's origin is absent or `packagedDefaults`. When origins is `None`, drop every baseline leaf.
2. Explicit leaf: drop only when its origin type is `project`.
3. `developer_instructions`: treated as an explicit leaf unless imports were approved, in which case the import argument replaces it unconditionally (today's `import_argument` behavior).
4. Regroup surviving leaves by top-level key: a top-level scalar renders as `key=<toml_value>`; a table renders as `key=<inline table>` built from its surviving leaves. Never emit a dotted path (Codex ignores dotted keys containing dots). Use `toml_value` for all values.

`import_argument` currently returns `["-c", "developer_instructions=…"]` only when imports apply. Make the base instruction text from the `codex-instructions.md` sidecar an explicit leaf in the normal path, and let `import_argument` signal "imports replace instructions" so step 3 can apply. Keep its consent, size-limit and diagnostics behavior unchanged.

Read values from `record["releases"][active]["codex_snapshot"]["settings"]` and the active release payload, never from the live override file.

## Interactive launch

In `launch_checked`, for the non-batch path with no explicit profile:

- Replace the `kk.config.toml` presence check with a check that `$KK_HOME/codex-instructions.md` exists (message unchanged in spirit: run `kk apply`).
- Run the origin lookup with the user's own trust flags (`trust_flags` from `launch_options`) and `cwd` = the launch directory; use `Path.cwd()` (or the `-C` target) when `directory` is `None` for `resume`/`fork`/`--remote`/`--worktree`.
- On lookup failure print one stderr line (for example: `kk: could not read Codex configuration origins (<reason>); launching without kk's preference defaults`) and compose with origins `None`.
- Build `argv` as `["codex", *kk_flags, *args]` with no `--profile`.

An explicit `--profile`/`-p` keeps today's pass-through: no kk flags, no imports, no lookup.

→ verify: tests assert the echoed `argv` for (a) no origins → every baseline and explicit key present, no `--profile`; (b) `user` origin for `model` → no `model` flag, explicit values present; (c) `project` origin for `approval_policy` with the opt-in on → flag absent; `user` origin → flag present; (d) `codex.defaults.tui=false` → no `tui` flag; (e) lookup failure → explicit values only, one warning line; (f) a table default split across origins renders one inline table with only the surviving leaves.

## Batch verification

In `launch_checked` for batch launches:

- Refuse any explicit profile (`explicit is not None`) with the existing "cannot verify" wording.
- Delete the `kk.config.toml` regular-file check, the `compose(...)[0]` comparison and the drift error.
- Compute kk's flags exactly as the interactive path, but with the 10 s trust timeout budget available and **refuse** when the origin lookup fails (`ValueError` naming the vendor error).
- Call `codex_trust.check(release, codex_home, directory, trust_flags + kk_flags, …)` so `hooks/list` runs under the run's final layers. Pass the same `kk_flags` into `argv`.

Keep the activation, fixed-workspace, `CODEX_HOME`-match and guard-receipt gates and the `unverified` behavior unchanged.

→ verify: tests show (1) a `config.toml` containing a changed `model` and a `[hooks.state]` table does not block `exec`; (2) `-cfeatures.hooks=false` still blocks with "absent" (the fake already honours it); (3) the fake `app-server` receives kk's `-c` flags on the `hooks/list` session (assert via a fixture-driven difference, e.g. a fake rule that disables hooks when a given kk flag is present, or by having the fake record its args); (4) `-pkk exec` is refused; (5) `fixture-no-config-read` makes `exec` refuse.

## Apply, upgrade and the removed profile

`prepare`:

- Stop adding `directory / "kk.config.toml"` to `files`.
- `validate_files` no longer writes a scratch profile; it runs `[executable, *all_candidate_flags, "debug", "prompt-input"]` in the scratch home (all baseline and explicit leaves plus instructions, no origin filtering), keeping the `config.toml` symlink and the `kk.rules` checks.

`publish`:

- The existing obsolete loop already unlinks paths in `record["codex_paths"]` that are no longer in `files`. When the removed path's name is `kk.config.toml`, print the one-time notice from design §4 to stdout.

Fake Codex: replace the exact-match `["--profile", "kk", "debug", "prompt-input"]` branch with "any arguments ending in `debug prompt-input`", answering `[]`.

Update `test_codex.py`, `test_codex_activation.py` and `test_lifecycle.py`:

- Assertions on `self.profile` contents become assertions on launch `argv` or on the absence of `kk.config.toml`.
- `test_collision_stops_before_activation` no longer uses `kk.config.toml` as the colliding path; use an owned agent path (`agents/kk-code-reviewer.toml`) so the collision behavior stays covered.
- `test_batch_profile_drift_explains_how_to_preserve_preferences` and `test_vendor_model_tip_update_preserves_batch_checks` test removed behavior; replace them with the success-criterion tests above rather than deleting coverage silently.
- `test_toml_round_trip` keeps the `toml_value` round-trip (still used for `-c` values) and drops the profile and `matches_profile` parts.
- The real-Codex test switches from `--profile kk debug prompt-input` to invoking `debug prompt-input` with kk's composed flags, and asserts the developer message as before.
- Add an upgrade test: seed a record whose `codex_paths` and `installed_paths` contain `kk.config.toml` with arbitrary drifted contents, run `kk apply`, assert the file is gone, the path is dropped from both lists, and the notice is printed once.

`test/guard/test_guard.py` uses `kk.config.toml` only as sample `installed_paths` data for self-modification protection; leave it.

## Live-check output

In `live.run`:

- When the vendor exits non-zero, strip a leading `kk: ` from the selected stderr line before raising.
- On success return `ok (guard denied the canary read)` after the reason pattern matches.

Update `test/kk/test_status.py` assertions that expect the reason text (`assertIn("kk guard: secrets", cli.live.run(...))`) to expect the new summary, and add an assertion that a failing launch's message does not start with `kk: `.

## Documentation and ADR

- `docs/providers/codex.md`: remove `kk.config.toml` from the files table; rewrite "Where Codex saves trust decisions" (trust is saved where plain Codex keeps it; state what the real-Codex verification observed for `/model`); delete "Recover a changed managed profile"; describe the launch flags, the two precedence classes, `codex.defaults`, the `config/read` latency and failure behavior, and the one-time removal notice; update "Project instruction budget" wording ("the managed profile sets" → "kk passes").
- `docs/user-guide/configuration.md`: rewrite the Codex paragraph and opening sentence; add `codex.defaults` to the example and prose; update the `installed_paths` list (no Codex profile).
- `docs/getting-started/overview.md:51`: replace "selects the managed profile".
- `docs/adr/0015-codex-launch-overrides.md` (Nygard template): context (#206, the ownership conflict, the probe table), decision (per-launch `-c`, two classes via `config/read`, batch trust read with final flags), consequences (latency, resumed-session trade-off, rollback asymmetry, choices in the old profile dropped once). In `docs/adr/0014-machine-level-delivery.md`, amend the Status line to note that ADR 0015 supersedes its Codex profile sentence.
- Do not edit `docs/feat/done/**`.

## Real-Codex verification

Probe in a scratch `CODEX_HOME` with Codex 0.172 (or the installed version, recorded), writing results to `docs/feat/wip/codex-launch-overrides/verification/README.md`:

- Assumption 2: set `agents.max_threads` in `config.toml` and `tui.whimsy` in a trusted project; `config/read` origins report each leaf separately.
- Assumption 3: `codex -c developer_instructions="MARKER" debug prompt-input` (no profile) shows `MARKER` in a developer message.
- Assumption 1: record the origin type reported for a key Codex supplies only from packaged defaults, if any.

After Tasks 2–5, against the maintainer's real `~/.codex`:

- Reproduce #206: interactive `kk codex`, switch `/model`, approve a repository hook, exit; then `kk codex exec "echo ok"` and `kk status --live` pass.
- Record where `/model` and the hook approval were saved (`config.toml` diff, or nowhere) — assumption 6 — and reflect it in `docs/providers/codex.md`.
- Assumption 4: with the guard trusted, toggle one guard handler off in plain `codex` `/hooks`; `kk codex exec` refuses; re-enable and it passes.
- Assumption 5: time the origin lookup call itself (not a whole `kk codex` launch) over a few runs and record the range.
