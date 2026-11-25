# Tasks: Codex launch overrides

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-11-24
> Not Doing: repository-scoped kk config, carrying choices from the old profile into config.toml, TOML parser or higher Python minimum, diff in the profile-mismatch error, keeping `--profile kk` working, hiding `codex.settings` values from process listings

## Task 1: App-server client with config/read
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Slicing:** Contract-First — the request helper is the boundary both launch paths, the trust read and the apply-time check share
- **Can run in parallel with:** Task 5
- **Docs:** [implementation.md#app-server-client-and-configread](./implementation.md#app-server-client-and-configread)

### Subtasks
- [ ] 1.1 Create `kk/lib/codex_app.py`: one `app-server` session running an ordered request list, with a caller-supplied kill timeout, today's error mapping and a distinct exception for `-32601`
- [ ] 1.2 Rewrite `codex_trust.hooks` as a caller of the helper, keeping `NoTrustMethod` behavior for `check` → verify: existing `test_codex_activation.py` trust tests pass unchanged
- [ ] 1.3 Add the origin lookup (`config/read` with `cwd`, `includeLayers: false`) returning `origins` and the effective `config`
- [ ] 1.4 Teach `test/kk/codex` to apply its configuration flags in order in every accepted spelling, derive `features.hooks` from the result, and answer `config/read` like Codex 0.172 (canonical and array-indexed origins, no origin for empty values, effective `config`) with the `fixture-origins.json`, `fixture-config.json`, `fixture-aliases.json` and `fixture-no-config-read` controls
- [ ] 1.5 Tests for the lookup (user/project/sessionFlags origins, empty values, missing method, timeout) and for the fake's flag order → verify: `bash test/test-kk.sh` passes

## Task 2: Interactive launch with origin-checked flags
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [design.md#1-launch-flags-instead-of-a-profile](./design.md#1-launch-flags-instead-of-a-profile), [implementation.md#baseline-names](./implementation.md#baseline-names), [implementation.md#launch-flag-composition](./implementation.md#launch-flag-composition), [implementation.md#interactive-launch](./implementation.md#interactive-launch)

### Subtasks
- [ ] 2.1 Rename the baseline's `agents.max_threads` and `tui.whimsy` to their canonical names in `kk/baseline/codex.json` and in the two `test_codex.py` settings examples; in `codex_profile.py`, accept and validate `codex.defaults`, reject `mcp_servers`, `model_providers` and `shell_environment_policy` in `codex.settings`, and add a launch-inputs function sharing `compose`'s validation that returns baseline and explicit leaves as path tuples, instructions and the native switch
- [ ] 2.2 Extend `launch_options` to return the lookup directory (also for dynamic workspaces), the caller's configuration flags in order, and the presence of model, sandbox/approval, `--ignore-user-config` and `--trust` flags
- [ ] 2.3 In `codex_launch.py`, add flag building per implementation.md steps 1–6: set-detection by exact or prefix origin key and by empty effective values, model group, dedicated-flag handling, explicit-over-baseline at the same path, no kk values when the lookup failed, one `-c` per top-level key with inline tables and quoted keys
- [ ] 2.4 Make the sidecar instructions an explicit leaf and let approved imports replace them unconditionally, keeping `import_argument`'s consent and size behavior
- [ ] 2.5 Switch the interactive path in `launch_checked`: shared different-`CODEX_HOME` refusal, sidecar presence check, origin lookup with the caller's flags and lookup directory, one warning line and no kk values on lookup failure, `argv` = kk flags then caller arguments without `--profile`; explicit `--profile` stays a pass-through
- [ ] 2.6 Update tests that assert the interactive `argv` or the old interactive profile check, and add tests for the cases (a)–(l) in implementation.md §Interactive launch → verify: `bash test/test-kk.sh` passes

## Task 3: Batch launch verifies the final flags
- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [design.md#3-batch-verification](./design.md#3-batch-verification), [implementation.md#batch-verification](./implementation.md#batch-verification)

### Subtasks
- [ ] 3.1 In `launch_checked`, refuse explicit profiles, `--ignore-user-config` and `--trust` for batch launches before any process starts; remove the `kk.config.toml` file check, the profile comparison and its error; reword the remaining refusals so none mentions the managed profile
- [ ] 3.2 Compute kk's flags for batch launches with the interactive rules (including the lookup-failure behavior); pass kk's flags followed by the caller's configuration flags in order to `codex_trust.check`, and launch kk's flags followed by the caller's arguments
- [ ] 3.3 Delete `matches_profile`; keep `TIP_TABLE` and `TIP_COUNTER` for the renderer until Task 4
- [ ] 3.4 Update the ready-state `argv` expectation and the `matches_profile` part of `test_toml_round_trip`; replace `test_batch_profile_drift_explains_how_to_preserve_preferences` and `test_vendor_model_tip_update_preserves_batch_checks` with tests (1)–(5) in implementation.md §Batch verification → verify: `bash test/test-kk.sh` passes

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
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4
- **Docs:** [design.md#5-output-fixes](./design.md#5-output-fixes), [implementation.md#live-check-output](./implementation.md#live-check-output)

### Subtasks
- [ ] 5.1 In `live.run`, strip a leading `kk: ` from the reused vendor stderr line and return `ok (guard denied the canary read)` after the reason pattern matches
- [ ] 5.2 Update `test_status.py` expectations and assert a failure message has no duplicated prefix → verify: `bash test/test-kk.sh` passes

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

## Dependency Graph

```
Task 1 ─→ Task 2 ─→ Task 3 ─→ Task 4 ─→ Task 6 ─→ Task 7 ─→ Task 8
Task 5 ─────────────────────────────→ Task 6
```
