# Tasks: Codex launch overrides

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-11-24
> Not Doing: repository-scoped kk config, carrying choices from the old profile into config.toml, TOML parser or higher Python minimum, diff in the profile-mismatch error, keeping `--profile kk` working, hiding `codex.settings` values from process listings

## Task 1: App-server client with config/read
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Slicing:** Contract-First — the request helper is the boundary both launch paths, the trust read and the apply-time check share
- **Can run in parallel with:** Task 5
- **Docs:** [implementation.md#app-server-client-and-configread](./implementation.md#app-server-client-and-configread)

### Subtasks
- [x] 1.1 Create `kk/lib/codex_app.py`: one `app-server` session running an ordered request list, with a caller-supplied kill timeout, today's error mapping and a distinct exception for `-32601`
- [x] 1.2 Rewrite `codex_trust.hooks` as a caller of the helper, keeping `NoTrustMethod` behavior for `check` → verify: existing `test_codex_activation.py` trust tests pass unchanged
- [x] 1.3 Add the origin lookup (`config/read` with `cwd`, `includeLayers: false`) returning `origins` and the effective `config`
- [x] 1.4 Teach `test/kk/codex` to apply its configuration flags in order in every accepted spelling, derive `features.hooks` from the result, and answer `config/read` like Codex 0.172 (canonical and array-indexed origins, no origin for empty values, effective `config`) with the `fixture-origins.json`, `fixture-config.json`, `fixture-aliases.json` and `fixture-no-config-read` controls
- [x] 1.5 Tests for the lookup (user/project/sessionFlags origins, empty values, missing method, timeout) and for the fake's flag order → verify: `bash test/test-kk.sh` passes

### Execution context
- 2026-11-25, observed (branch `feat/codex_overrides` at 450c0afe, clean tree): `codex_trust.hooks` is the only `app-server` client; its callers are `codex_trust.check` (used by `codex_launch.launch_checked`, `cli.py`, `migrate.verify_workspace`). `test_codex_activation.py` patches `trust.hooks` and raises `trust.NoTrustMethod`, so both names must stay on `codex_trust`.
- 2026-11-25, observed: today `-32601` raises `NoTrustMethod` only for `hooks/list`; on `initialize` it is a `ValueError`, which `check` reports as "awaiting review" with no acknowledgement path.
- 2026-11-25, inferred (implementation.md §App-server client says "a distinct exception for `-32601` on any method" and "unchanged in behavior"): the distinct exception covers every method in the caller's request list; the `initialize` handshake keeps its `ValueError`. Otherwise a vendor that rejects the handshake could reach `check`'s "unverified" acknowledgement, which it cannot today.
- 2026-11-25, observed: kk passes configuration flags to `app-server` only in the separated form (`launch_options` normalizes to `[key, value]`). The fake still accepts the attached spellings, as subtask 1.4 requires.
- 2026-11-25, observed (Codex CLI 0.172.0, scratch `CODEX_HOME` under `~/.cache`, driven through `codex_app.origins`/`session`; no credentials):
  - `config/read` answered in about 0.4 s. An origin is `{"name": {"type": …}, "version": "sha256:…"}`; `user` adds `file` and `profile`, `project` adds `dotCodexFolder`. A trusted repository's `.codex/config.toml` reports type `project`.
  - The effective `config` lists every known key, with `null` for unset scalars and tables (`model`, `agents`, `tui`). Once any `tui` value is set the table is populated with Codex's defaults: `status_line` and `terminal_title` stay `null`, but `default_hosts`, `presets` and `model_availability_nux` are `{}` **without any layer setting them**. `project_doc_max_bytes` is `32768` with no origin. Keys Codex does not know get an origin but are absent from `config`.
  - **`--enable`/`--disable` apply after every `-c`, wherever they appear**: `--disable hooks -c 'features={shell_snapshot=true}'` leaves `features.hooks=false`, and `--enable hooks -c features.hooks=false` leaves it `true`. implementation.md §App-server client implies argument order for the toggles. The fake follows the vendor: `-c` in order, then toggles. The Task 3 guarantee is unaffected, because the trust read and `exec` receive the same sequence.
  - **An unknown method returns `-32600`** (`Invalid request: unknown variant`), not `-32601`. No vendor evidence for `-32601` exists in the repository; `fixture-no-method` and `fixture-no-config-read` model it as specified. For the origin lookup both are a lookup failure, so nothing changes. For the trust read it means a Codex without `hooks/list` would be reported as "could not verify" rather than reach the acknowledgement path.
- 2026-11-25, accepted (maintainer, in the Task 1 session, after seeing the toggle-order observation above): implementation.md §App-server client now states that the fake applies `-c` flags in order and feature toggles after them. Rationale: the document described argument order for toggles, which Codex 0.172 does not follow.
- 2026-11-25, accepted (maintainer, in the Task 1 session): the empty-value part of set-detection applies to **arrays only**. Source: the `tui` observation above; design.md §1 said an empty array or table "can only come from a configuration layer", which is false for `tui.presets`, `tui.default_hosts` and `tui.model_availability_nux` (`{}` by default once `tui` is populated). Rationale: the only baseline leaves that can be empty-valued are the arrays `tui.status_line` and `tui.terminal_title`, and both stay `null` unless a layer sets them. design.md §1 and its evidence table, implementation.md §Launch flag composition step 2 and subtask 2.3 are updated. Known limit, unchanged by this decision: an empty array has no origin, so the rule protects baseline defaults only; an explicit `codex.settings` array still overrides a repository that sets the same key to `[]`.
- 2026-11-25, accepted (maintainer, in the Task 1 session): the trust read keeps treating only `-32601` on `hooks/list` as "method unavailable"; `-32600 … unknown variant` stays a "could not verify" refusal. Rationale: widening it would loosen a guard check on the strength of an error message. Follow-up at subtask 8.5 (see Task 8's Execution context).
- 2026-11-25, accepted within the task's scope: `codex_app.origins` raises `ValueError` when `origins` or `config` is not an object, so a changed vendor answer is a lookup failure instead of an attribute error at launch.
- 2026-11-25, verification (author-run, Python 3.10.12, fake Codex; real Codex 0.172.0 on `PATH` for the two real-CLI tests): `bash test/test-kk.sh` ran 109 tests, OK, 2 skipped for existing environment reasons (`tomllib unavailable`, `full retirement tag unavailable`); this is the rerun after the review corrections. The 10 new tests are in `test/kk/test_codex_app.py`; `test_codex_activation.py` is unchanged. Limits: Python 3.8 was checked for grammar only (`ast.parse(feature_version=(3, 8))`); no 3.8 interpreter is installed here, so the CI matrix is the runtime check.
- 2026-11-25, review (`/kk:review-code` isolated; base 450c0afe, candidate the uncommitted tree): the independent `code-reviewer` and an external Codex CLI reviewer (PAL clink, provider assumed OpenAI) both returned APPROVE for the Task 1 code with no P0–P2 findings. The `code-reviewer` raised two P3 items, both corrected and re-reviewed as resolved: `codex_app.session` now turns a reply without `result`, a non-object `error` and non-object lines into `ValueError` or skips them, so its documented exceptions (`NoMethod`, `ValueError`, `OSError`) are complete; the fake's TOML reader accepts decimal and exponent numbers, which `toml_value` can emit. The external reviewer saw the candidate before these corrections and did not read the selected patch in full (it read the candidate files directly).
- 2026-11-25, deferred, owner: unassigned (inherited, not introduced here; act only if Task 6 timing or a real failure shows it): the kill timer ends only the direct `app-server` child, so a descendant holding stdout could outlive the timeout; and `text=True` decodes with the locale, so non-UTF-8 locales turn unusual `config/read` text into a lookup failure. Next action: pin `encoding="utf-8"` and start the child in its own process group if Task 6 observes either. Verification: the Task 6 lookup timing runs.
- 2026-11-25, deferred, owner: whoever writes the Task 2–4 tests: the fake keeps stale indexed origins from `fixture-origins.json` when a flag sets a shorter array at the same path, and it places keys Codex does not know in the effective `config` (Codex omits them). Neither affects a Task 1 test. Next action: give such tests consistent `fixture-origins.json` and `fixture-config.json`, or extend the fake when a test needs the vendor behavior.
- 2026-11-25, prerequisite outside this task: the CI matrix (Python 3.8 and 3.x) has to run `bash test/test-kk.sh`; `kk/lib/codex_app.py` and `test/kk/test_codex_app.py` are new files and must be committed with the task.
- Preserved: `check`, `machine`, `report` and every existing fixture control (`fixture-reviewed`, `disabled-<n>`, `fixture-no-method`, `fixture-guard-off`). No launch behavior changes in this task; `launch_checked` is untouched until Task 2.

## Task 2: Interactive launch with origin-checked flags
- **Status:** done
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [design.md#1-launch-flags-instead-of-a-profile](./design.md#1-launch-flags-instead-of-a-profile), [implementation.md#baseline-names](./implementation.md#baseline-names), [implementation.md#launch-flag-composition](./implementation.md#launch-flag-composition), [implementation.md#interactive-launch](./implementation.md#interactive-launch)

### Subtasks
- [x] 2.1 Rename the baseline's `agents.max_threads` and `tui.whimsy` to their canonical names in `kk/baseline/codex.json` and in the two `test_codex.py` settings examples; in `codex_profile.py`, accept and validate `codex.defaults`, reject `mcp_servers`, `model_providers` and `shell_environment_policy` in `codex.settings`, and add a launch-inputs function sharing `compose`'s validation that returns baseline and explicit leaves as path tuples, instructions and the native switch
- [x] 2.2 Extend `launch_options` to return the lookup directory (also for dynamic workspaces), the caller's configuration flags in order, and the presence of model, sandbox/approval, `--ignore-user-config` and `--trust` flags
- [x] 2.3 In `codex_launch.py`, add flag building per implementation.md steps 1–6: set-detection by exact or prefix origin key and by empty effective arrays, model group, dedicated-flag handling, explicit-over-baseline at the same path, no kk values when the lookup failed, one `-c` per top-level key with inline tables and quoted keys
- [x] 2.4 Make the sidecar instructions an explicit leaf and let approved imports replace them unconditionally, keeping `import_argument`'s consent and size behavior
- [x] 2.5 Switch the interactive path in `launch_checked`: shared different-`CODEX_HOME` refusal, sidecar presence check, origin lookup with the caller's flags and lookup directory, one warning line and no kk values on lookup failure, `argv` = kk flags then caller arguments without `--profile`; explicit `--profile` stays a pass-through
- [x] 2.6 Update tests that assert the interactive `argv` or the old interactive profile check, and add tests for the cases (a)–(l) in implementation.md §Interactive launch → verify: `bash test/test-kk.sh` passes

### Execution context
- 2026-11-25, carried from Task 1 (details and evidence in its Execution context):
  - The lookup-failure handler should catch `codex_app.NoMethod`, `ValueError` and `OSError`; that is everything `codex_app.origins` raises.
  - Set-detection by an empty effective value applies to arrays only (accepted 2026-11-25): Codex 0.172 reports `{}` for `tui.presets`, `tui.default_hosts` and `tui.model_availability_nux` whenever `tui` is populated. Unset tables and scalars are `null`, not absent.
  - Codex applies `--enable`/`--disable` after every `-c`, wherever they appear; the fake does the same.
- 2026-11-25, observed (branch `feat/codex_overrides` at d5b81034, clean tree): `launch_checked` has one `explicit is None` block serving batch and interactive launches; `launch_options` and `launch_checked` have no callers outside `codex_launch.launch` (one test reads `launch_options(...)[0]`). `test_lifecycle.py` patches the literal `profile = baseline["profile"]` in `codex_profile.py`, so that line must survive until Task 4 rewrites the test. `test_status.py` asserts an interactive `kk codex` writes nothing to the terminal, so a successful lookup must stay silent.
- 2026-11-25, inferred (design.md §1 "explicit values … the `codex-instructions.md` sidecar", implementation.md step 5): the `developer_instructions` leaf is read from `$KK_HOME/codex-instructions.md`, the same text `import_argument` extends, not from the instructions `launch_inputs` returns. That is why the interactive gate requires the sidecar.
- 2026-11-25, inferred (design.md §1 "Their precedence against `-c` is therefore never relied on"): a dedicated sandbox or approval flag drops kk's `approval_policy`, `approvals_reviewer` and `sandbox_mode` leaves by path, so a `codex.settings` value for one of them is dropped too.
- 2026-11-25, **proposed and implemented, not yet confirmed by the maintainer**: `kk apply` rejects a top-level `codex.settings` key that is not a plain name (`[A-Za-z0-9_-]+`), for example `"features.hooks"`. Source: implementation.md step 6 "Never emit a dotted path"; design.md §Vendor evidence row 3 (Codex splits a `-c` key on dots even inside quotes). Reason: in the profile such a key was an inert quoted key; as a launch flag it would become `features.hooks=false` and switch hooks off for interactive sessions, bypassing the existing enablement rejection. The design covers dotted keys only inside tables. Consequence: an adopter whose `config.json` has such a key is stopped at `kk apply` or upgrade with `codex.settings key "…" is not a plain name; write a nested table as a JSON object`. To undo: remove the `PLAIN_KEY` loop in `codex_profile.validated` and its assertion in `test_reserved_enablement_settings`; the key is then emitted as a dotted `-c` path.
- 2026-11-25, accepted within the task's scope:
  - `launch_options` returns a named tuple (`workspace`, `profile`, `batch`, `config_flags`, `directory`, `model`, `permissions`, `ignore_user_config`, `trust`); `launch_checked(home, args, options, lock)` takes it. Task 3 reads `ignore_user_config` and `trust`; nothing reads them yet.
  - The different-`CODEX_HOME` refusal is `require_applied_home`, shared by both paths and already reworded ("kk's Codex settings were applied to a different CODEX_HOME"). This is the part of subtask 3.1 that concerns that message.
  - `interactive_flags` holds the interactive rules (gates, imports, lookup, warning line). Task 3 can call it for batch launches; it currently passes `sys.stdin.isatty()` as the import prompt switch, which batch must not.
  - `compose` honors `codex.defaults` in the TOML profile too, so batch and interactive launches agree until Task 3. `validated` is the shared validation; `launch_inputs` and `compose` both call it.
  - `read_origins` (in `codex_launch`) reduces each origin to its layer type and raises `ValueError` for an entry without a string `name.type`, so a changed vendor answer is a failed lookup.
  - The lookup-failure line says "without kk defaults and opt-ins" when approved imports still carry the instructions, and "without kk defaults, opt-ins and instructions" otherwise.
  - The `mcp_servers`, `model_providers` and `shell_environment_policy` rejections are asserted in `test_reserved_enablement_settings` already; subtask 4.6's `mcp_servers` item only needs checking, not a new test.
  - The fake merges an optional `fixture-origins.json` from the directory named in the `config/read` request over the one in `CODEX_HOME`, so a test can give one repository its own `project` origins.
- 2026-11-25, observed (Codex CLI 0.172.0, scratch `CODEX_HOME` under `~/.cache`, no credentials, driven through `launch_flags`/`read_origins`):
  - With every opt-in and a `docs = {"docs.internal" = {depth = 2}}` setting, each kk leaf came back with a `sessionFlags` origin under the same name (`agents.max_concurrent_threads_per_session`, `tui.effects.starfield`, `tui.status_line.0`…). `codex <flags> debug prompt-input` exited 0 with the instructions as a developer message.
  - A `config.toml` with `model` and `[tui] status_line = []` gave origins `{"model": "user"}` and an effective `tui.status_line == []`; the flags then omitted the four model-group keys and `status_line`.
  - `-c 'tui={ "model_availability_nux" = { "gpt.5" = 1 } }'` gave an effective `{"gpt.5": 1}`: a quoted dotted key inside an inline table stays one key.
  - `-c` flags before `--version`, `resume --help` and `login status` were accepted.
  - **`--yolo` is accepted although `--help` does not list it**; `--full-auto` is rejected. kk treats `--yolo` like `--dangerously-bypass-approvals-and-sandbox` (inferred from the vendor's naming; only its acceptance was observed). design.md §1 "Dedicated flags" lists four names without it.
- 2026-11-25, verification (author-run, Python 3.10.12, fake Codex, real Codex 0.172.0 on `PATH`): `bash test/test-kk.sh` on the candidate after the review corrections ran 117 tests, OK, 2 skipped for existing environment reasons (`tomllib unavailable`, `full retirement tag unavailable`). Earlier runs are kept for the record: the first run had 1 error in `test_both_launchers_return_while_update_fetch_is_blocked`, a test defect (it read the terminal once and the echoed kk flags, about 5.5 KB, no longer fit one read); the test now drains the terminal and kills a stalled launcher. Cases (a)–(i), (k), (l) are in the new `test/kk/test_codex_launch.py` (8 tests), case (j) in `test_codex.py`. The one-line `--yolo` addition came after the full run and was checked with `test_codex_launch.py` only (8 tests OK on 3.10.12 and 3.12.11). On Python 3.12.11 `test_toml_round_trip` also passed. Limits: Python 3.8 was checked for grammar only; no real interactive session was started through `kk codex` (Task 6).
- 2026-11-25, review (`/kk:review-code` isolated; base d5b81034, candidate the uncommitted tree): the independent `code-reviewer` and an external Codex CLI reviewer (PAL clink, provider assumed OpenAI) both returned APPROVE with no P0–P2 findings. The `code-reviewer` raised three P3 items, all corrected and re-reviewed as resolved by both reviewers: `compose` removed `tui.model_availability_nux` from the saved settings when `codex.defaults.tui` was off (now copies the table; a test fails without the copy); no launcher-level test showed the lookup uses the `-C` directory (the fake fixture above and a `-C repository resume` case); the rewritten terminal test could hang on a stalled launcher. Limits: the external reviewer's first read of the patch was truncated and it did not read `claude_launch.py`, `cli.py`, `codex_plugins.py`, the fake or two test files; neither reviewer saw the `--yolo` line, which was added after the re-review.
- 2026-11-25, deferred, owner: whoever takes Task 7: the user docs must state that `codex.settings` top-level keys must be plain names (if the proposal above is confirmed), and list `--yolo` with the dedicated flags. Verification: `docs/providers/codex.md` and `docs/user-guide/configuration.md` mention both.
- 2026-11-25, deferred, owner: unassigned (interim state between this task and Task 4): interactive sessions no longer load `kk.config.toml`, so a model or hook approval Codex saved there no longer applies to them, and the removal notice arrives only in Task 4. Next action: none unless the tasks are released separately; Tasks 3 and 4 close it.
- 2026-11-25, prerequisite outside this task: `test/kk/test_codex_launch.py` is a new file and must be committed with the task; the CI matrix (Python 3.8 and 3.x) has to run `bash test/test-kk.sh`.
- Preserved: explicit `--profile` pass-through, `import_argument`, every batch gate and the batch `argv` (`--profile kk`), the published profile's contents apart from the two canonical key names.

## Task 3: Batch launch verifies the final flags
- **Status:** done
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [design.md#3-batch-verification](./design.md#3-batch-verification), [implementation.md#batch-verification](./implementation.md#batch-verification)

### Subtasks
- [x] 3.1 In `launch_checked`, refuse explicit profiles, `--ignore-user-config` and `--trust` for batch launches before any process starts; remove the `kk.config.toml` file check, the profile comparison and its error; reword the remaining refusals so none mentions the managed profile
- [x] 3.2 Compute kk's flags for batch launches with the interactive rules (including the lookup-failure behavior); pass kk's flags followed by the caller's configuration flags in order to `codex_trust.check`, and launch kk's flags followed by the caller's arguments
- [x] 3.3 Delete `matches_profile`; keep `TIP_TABLE` and `TIP_COUNTER` for the renderer until Task 4
- [x] 3.4 Update the ready-state `argv` expectation and the `matches_profile` part of `test_toml_round_trip`; replace `test_batch_profile_drift_explains_how_to_preserve_preferences` and `test_vendor_model_tip_update_preserves_batch_checks` with tests (1)–(5) in implementation.md §Batch verification → verify: `bash test/test-kk.sh` passes

### Execution context
- 2026-11-25, carried from Task 2 (details in its Execution context): the different-`CODEX_HOME` refusal is already shared and reworded (`require_applied_home`); `interactive_flags` computes kk's flags and needs a way to turn the import prompt off for batch launches; `Options.ignore_user_config` and `Options.trust` exist and are unread; `launch_checked` still has a batch-only block that checks the profile path and passes `--profile kk`.
- 2026-11-25, observed (branch `feat/codex_overrides` at fab6653e, clean tree apart from this file): `matches_profile` has one caller (`launch_checked`) and one test use (`test_toml_round_trip`), and it is the only user of `TIP_COUNTER`; `compose` uses `TIP_TABLE` only. `live.run` and `kk migrate` reach batch launches through `kk codex exec` as a subprocess, so they need no change. `live.run` passes `--sandbox read-only`, which drops kk's approval and sandbox opt-ins for that run.
- 2026-11-25, **deviation from subtask 3.3's wording, not yet confirmed by the maintainer**: `TIP_COUNTER` is deleted together with `matches_profile`; `TIP_TABLE` stays. Source: design.md §3 ("deleted once nothing references them"); the subtask keeps both "for the renderer", but the renderer never used `TIP_COUNTER`, and its comment described the removed byte comparison. No behavior depends on it. To undo: restore the constant in `codex_profile.py`; subtask 4.1 then deletes it as written.
- 2026-11-25, accepted within the task's scope:
  - `interactive_flags` is now `session_flags(home, release, saved, codex_home, options, executable, prompt)`. Both paths call it; batch passes `prompt=False`, so imports apply only with a stored approval, as before. The caller supplies `codex_home` from `require_applied_home`, which batch needs earlier for the guard-receipt gate.
  - Batch order: workspace/profile refusal, `--ignore-user-config`/`--trust` refusal, `CODEX_HOME` match, guard receipt, flags (sidecar check, imports, origin lookup with the 5-second timer), trust read with `kk flags + caller configuration flags`, then the run. A missing `codex-instructions.md` now refuses a batch launch with "run kk apply", like an interactive one.
  - `-pkk exec` is refused like any other named profile. The refusal reads "cannot verify the Codex guard for this session's workspace or named profile; use an interactive session, or select a local directory and no profile". The flag refusal names the flags given: "cannot verify the Codex guard with --trust: the guard check cannot reproduce such a configuration or trust change; launch without --trust".
  - The trust read receives the caller's flags as separated pairs (`-cx=1` becomes `-c x=1`), while the run receives them as typed. Order and values are the same; only the spelling differs.
  - The fake appends one line per `app-server` request (method and arguments, including `initialize`) to `fixture-requests` in `CODEX_HOME` when a test has created that file. Tests (3) and (4) use it to compare the trust read's flags with the run's and to show that a refused launch starts no session.
  - Tests (1)–(5) are in `test/kk/test_codex_launch.py` (`CodexLaunchFlags`, the five tests after `review_guard`). Test (1) also appends the saved choices to the still-published `kk.config.toml`, which is the #206 reproduction until Task 4 stops publishing the file; Task 4 can drop those two lines. Tests (1) and (5) also show that a disabled guard handler still blocks.
- 2026-11-25, verification (author-run, Python 3.10.12, fake Codex, real Codex on `PATH` for the two real-CLI tests): `bash test/test-kk.sh` ran 120 tests, OK, 2 skipped for existing environment reasons (`tomllib unavailable`, `full retirement tag unavailable`). The count is Task 2's 117, minus the two replaced tests, plus five. On Python 3.12.11, `test_toml_round_trip` and `test_refusals_and_ready_states` passed. Two deliberate defects were applied and reverted to check the new tests: passing the caller's flags before kk's to the trust read failed tests (2) and (3); removing the profile and flag refusals failed test (4). An earlier focused run had one failure in test (3), a test defect: the fake's log includes `initialize` lines, which the test now filters out. Limits: Python 3.8 was checked for grammar only; no batch session was run against a real Codex (Task 6), so "root-level `-c` flags before `exec` reach the run" rests on the Task 2 probes and the previous `--profile kk exec` form.
- 2026-11-25, observed (Codex CLI 0.172.0, scratch `CODEX_HOME` under `~/.cache`, no credentials; run after the review to answer its open points):
  - `codex -c model=rootmodel exec -c model=execmodel …` printed `model: execmodel` in the run header, so a `-c` after `exec` is applied after one before it. This supports the trust read's single sequence (caller flags in argument order, after kk's) for a scalar. An inline table at one position against a dotted flag at the other was not probed; the suggested Task 6 probe is `codex -c features.hooks=false exec -c 'features={x=true}'` compared with `app-server` given both flags.
  - `exec --trust=true` and `exec --ignore-user-config=true` exit 2 with "unexpected value", and the abbreviation `--ignore-user-conf` is rejected as an unknown argument. `launch_options` recognizes only the bare flags, so these spellings are not refused by kk, but Codex rejects them before any session, so they cannot bypass the refusal. No code was added for them.
- 2026-11-25, review (`/kk:review-code` isolated; base fab6653e, candidate the uncommitted tree): the independent `code-reviewer` and an external Codex CLI reviewer (PAL clink, provider assumed OpenAI, model not reported) both returned APPROVE for the Task 3 code with no P0–P2 findings. The `code-reviewer` raised one P3, deferred below. Limits: neither reviewer ran tests; the external reviewer's read commands were returned truncated, so its reading of all eight criteria files is only partly visible, and it read unchanged files in sections. Both reviewers saw the tree before the probe notes above were added to this file; no code changed after the review.
- 2026-11-25, deferred (review P3), owner: whoever integrates Task 5, which has uncommitted edits to the same statement in the `task5` worktree: `live.run` reports the **first** stderr line starting with `kk: ` as the failure reason (`kk/lib/live.py`, the `if result.returncode:` block). Batch launches now print the origin-lookup omission line before the trust read, so when the lookup fails and the launch is then refused or the vendor session fails, `kk status --live` and `kk migrate` name the omitted defaults instead of the real cause. The guard still blocks; only the message is wrong. The same already applied to the older warning lines (`unverified`, imports, override drift) when the vendor session failed. Next action: in `live.run`, take the last `kk: ` line (the dispatcher prints its fatal message last) and fall back to the "vendor session exited" text when the only `kk: ` lines are warnings. Verification: a `test_status.py` case with `fixture-no-config-read` and an unreviewed guard, asserting the reported reason is the guard refusal.
- 2026-11-25, deferred, owner: whoever takes Task 4: if the `TIP_COUNTER` deviation above is confirmed, subtask 4.1 has only `TIP_TABLE` left to delete; and test (1) in `test_codex_launch.py` appends to `kk.config.toml`, which Task 4 stops publishing (drop those two lines). Verification: `rg TIP_ kk/lib` finds nothing after Task 4.
- 2026-11-25, deferred, owner: whoever takes Task 7: the user docs must say that batch launches refuse every named profile, including the formerly accepted `-p kk`, and refuse `--ignore-user-config` and `--trust`. Verification: `docs/providers/codex.md` lists the three refusals (already in subtask 7.1's scope).
- 2026-11-25, prerequisite outside this task: the CI matrix (Python 3.8 and 3.x) has to run `bash test/test-kk.sh` on the committed task; Task 6 runs the first real-Codex batch session through the new path.
- Preserved: activation, fixed-workspace, `CODEX_HOME` and guard-receipt gates, the `unverified` behavior, the interactive path, explicit `--profile` pass-through for interactive launches, `import_argument`, `codex_trust.machine`, `migrate.verify_workspace`, and the published profile's contents.

## Task 4: Stop publishing the managed profile
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [design.md#4-interactive-gates-apply-upgrade-and-rollback](./design.md#4-interactive-gates-apply-upgrade-and-rollback), [implementation.md#apply-upgrade-and-the-removed-profile](./implementation.md#apply-upgrade-and-the-removed-profile)

### Subtasks
- [ ] 4.1 Converge `compose` with the launch-inputs function; delete TOML profile rendering, `TIP_TABLE` and `TIP_COUNTER`; drop `kk.config.toml` from `prepare`'s files
- [ ] 4.2 Make `validate_files` run `debug prompt-input` with all candidate flags and the apply-time `config/read` mapping check (skipping empty values) in the scratch home, keep the `kk.rules` checks, and report failures by operation and Codex stderr without the argument list; update the fake Codex's `debug prompt-input` branch to accept any flags
- [ ] 4.3 In `publish`, print the one-time removal notice when the obsolete path removed is `kk.config.toml`
- [ ] 4.4 Update the `kk codex` help text in `cli.py` and the `codex_launch` module docstring
- [ ] 4.5 Rewrite remaining profile-content assertions in `test_codex.py`, `test_codex_activation.py` and `test_lifecycle.py`; move the collision test to an owned agent path; switch the real-Codex test to `debug prompt-input` with kk's flags plus the mapping check
- [ ] 4.6 Add tests: aliased `codex.settings` key fails `kk apply` naming the canonical key; an empty-array leaf passes the mapping check; `mcp_servers` rejected; a synthetic marker value never appears in a validation error; upgrade removes an owned, drifted `kk.config.toml` with record cleanup and a single notice → verify: `bash test/test-kk.sh` passes

## Task 5: Live-check output fixes
- **Status:** done
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4
- **Docs:** [design.md#5-output-fixes](./design.md#5-output-fixes), [implementation.md#live-check-output](./implementation.md#live-check-output)

### Subtasks
- [x] 5.1 In `live.run`, strip a leading `kk: ` from the reused vendor stderr line and return `ok (guard denied the canary read)` after the reason pattern matches
- [x] 5.2 Update `test_status.py` expectations and assert a failure message has no duplicated prefix → verify: `bash test/test-kk.sh` passes

### Execution context
- 2026-11-25, observed (worktree branch `task5` at fab6653e, Tasks 1–2 committed, clean tree): `live.run` has three callers, all printing its return value as `<tool> live: <value>`: `cli.py` (`kk status --live`, which prints an exception as `<tool> live: failed: <message>`) and two sites in `migrate.py` (an exception there reaches the dispatcher's own `kk: ` prefix). `test_migrate.py` replaces `live.run` with a stub, so only `test_status.py` asserts its real return value. No file under `docs/` outside `docs/feat/` quotes the live-check output.
- 2026-11-25, observed (base fab6653e, fake Codex, temporary probe in `test_live_command_tries_both_tools_and_fails_on_missing_evidence`, not kept): with the guard unreviewed, `kk status --live` printed `codex live: failed: kk: Codex guard awaiting review for "/tmp/kk-live-…": …`. That is the duplicated prefix at the dispatcher level. With the guard reviewed, both tools fail with "did not report the installed guard denying the canary read", which carries no prefix, so that test cannot detect the duplication as written.
- 2026-11-25, accepted within the task's scope:
  - The 500-character cap applies after the prefix is removed. A stderr line that is exactly `kk: ` falls back to the "vendor session exited" message, as an absent line does.
  - The success path no longer returns the matched reason text; no caller used it other than to print it.
  - The duplicated-prefix assertion is a new test on `live.run` (`test_live_failure_reuses_the_launcher_message_without_its_prefix`) with a failing launcher for both tools and one unrelated stderr line before the `kk: ` line. The dispatcher-level reproduction above was not added as a test: it would add a second full `status --live` run (about 2 s) to assert the same string through an unchanged `print`.
- 2026-11-25, verification (author-run, Python 3.10.12, fake Codex; real Codex on `PATH`): before the `live.py` change, the updated `test_live_requires_tool_evidence_from_each_scratch_workspace` and the new test both failed (`'kk guard: secrets — …' != 'ok (guard denied the canary read)'`, `'kk: the guard is awaiting review' != 'the guard is awaiting review'`). After it, `bash test/test-kk.sh` ran 118 tests, OK, 2 skipped for existing environment reasons (`tomllib unavailable`, `full retirement tag unavailable`). Limits: Python 3.8 was checked for grammar only (`ast.parse(feature_version=(3, 8))`); no real vendor session was run through `kk status --live` (Task 6.2).
- 2026-11-25, review (`/kk:review-code` isolated; base fab6653e, candidate the uncommitted tree): the independent `code-reviewer` returned APPROVE for the Task 5 code with no P0–P2 findings and one inherited P3, deferred below. It ran no tests. The external review did not happen: the one eligible client (Codex CLI through PAL clink, provider assumed OpenAI) read nothing, because capy's Codex `PreToolUse` hook blocked every command with "overlapping Codex installations share owner ID" for the worktree and the main checkout that contains it (`.claude/worktrees/task5`). The client was not retried. So this task has one independent review, not two.
- 2026-11-25, deferred, owner: unassigned (inherited from the base, raised by the `code-reviewer` as P3, outside design.md §5): `live.run` reuses the **first** stderr line starting with `kk: `, and the Codex launcher prints warnings with that prefix before it can fail (`codex_launch.py`: "Codex guard is unverified for this run", the skipped-import lines, the origin-lookup line; `codex_profile.report_drift`: "Codex overrides changed"). The dispatcher prints the real error last (`cli.py`, `print("kk:", exc)`), so a failed live check can show a warning as its cause, for example `codex live: failed: Codex overrides changed. Run kk apply to apply them.` Read from source, not reproduced. Next action: reuse the last stderr line when it starts with `kk: `, otherwise the "vendor session exited" message; test with a warning before the fatal line and with vendor output after a warning. Verification: those two tests, or a Task 6.2 failure that shows the wrong line.
- 2026-11-25, noted by the `code-reviewer`, not acted on: no test feeds `live.run` a denial whose reason fails the pattern (another glob or rule) and expects "did not report"; the base had the same gap and the pattern is unchanged. The success line no longer shows which rule denied the read.
- Preserved: the reason pattern and its attribution requirement, the "did not report" and "vendor session exited" messages, the scratch-workspace setup, and every caller's output format.

## Task 6: Real-Codex end-to-end verification
- **Status:** pending
- **Depends on:** Task 4, Task 5
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#real-codex-verification](./implementation.md#real-codex-verification)

### Subtasks
- [ ] 6.1 From the reviewed checkout, run `kk upgrade --local .` and confirm `~/.codex/kk.config.toml` is removed with the notice
- [ ] 6.2 Reproduce #206: interactive `kk codex`, switch `/model`, approve a repository hook, exit → verify: `kk codex exec "echo ok"` and `kk status --live` pass without `kk apply`
- [ ] 6.3 Record where `/model` and the hook approval were saved (`config.toml` diff or session-only) (assumption 3)
- [ ] 6.4 Disable one guard handler in plain `codex` `/hooks` → verify: `kk codex exec` refuses; re-enable → it passes (assumption 1)
- [ ] 6.5 Time the origin lookup over a few runs (assumption 2); write all results with the Codex version to `verification/README.md`

## Task 7: Docs and ADR
- **Status:** pending
- **Depends on:** Task 6
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#documentation-and-adr](./implementation.md#documentation-and-adr)

### Subtasks
- [ ] 7.1 Update `docs/providers/codex.md` per implementation.md §Documentation and ADR, including the Task 6 `/model` and hook-trust observation, batch refusals and argument visibility; simplify the plain-codex review guidance and `codex_trust.REVIEW_UI` if Task 6 showed wrapped sessions save trust to `config.toml`
- [ ] 7.2 Update `docs/user-guide/configuration.md` (Codex paragraph, `codex.defaults`, canonical default names, `installed_paths` list) and `docs/getting-started/overview.md:51`; in `docs/user-guide/mcp-servers.md` §Codex client, replace the managed-profile drift reason for not wrapping PAL’s `codex exec` with the remaining batch gates (guard trust read, refused flags)
- [ ] 7.3 Write `docs/adr/0015-codex-launch-overrides.md` and amend ADR 0014's Status line → verify: `make docs-build` passes

## Task 8: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 8.1 Run `/kk:test` for the four success criteria and the launch-flag cases, plus `bash test/test-kk.sh` and the full `test/test-*.sh` suite; broaden only if shared launcher or state code changed beyond the planned modules
- [ ] 8.2 Run `/kk:document` to check the docs changed in Task 7 against the shipped behavior
- [ ] 8.3 Run `/kk:review-code` with the Python input to review the implementation
- [ ] 8.4 Run `/kk:review-spec` to verify the implementation matches design.md and implementation.md
- [ ] 8.5 Ask the user how to follow up on any outstanding non-blocking items (for example, GitHub issues)
- [ ] 8.6 Move the feature docs from `docs/feat/wip/` to `docs/feat/done/`, updating markdown references

Sufficient evidence: green `test/test-kk.sh` with the success-criterion tests, plus the Task 6 real-Codex reproduction. Broaden verification if Task 6 contradicts an assumption, or if the trust session and `exec` disagree on guard state.

### Execution context
- 2026-11-25, carried from Task 1 for subtask 8.5, owner: maintainer: Codex 0.172 answers an unknown `app-server` method with `-32600`, so the trust read's `-32601` acknowledgement path and the "unverified" state may be unreachable with a real Codex. Decide whether to remove them (this touches `kk status`, `kk apply` and `kk migrate`), for example through a GitHub issue. Evidence so far is one probe with an invented method name; what a Codex without `hooks/list` returns has not been checked.

## Dependency Graph

```
Task 1 ─→ Task 2 ─→ Task 3 ─→ Task 4 ─→ Task 6 ─→ Task 7 ─→ Task 8
Task 5 ─────────────────────────────→ Task 6
```
