# Tasks: Codex launch overrides

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-11-24
> Not Doing: repository-scoped kk config, carrying choices from the old profile into config.toml, TOML parser or higher Python minimum, diff in the profile-mismatch error, keeping `--profile kk` working

## Task 1: Probe the unverified Codex behaviors
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Slicing:** Risk-First — assumptions 1–3 decide whether the origin rules and instruction delivery work as designed
- **Can run in parallel with:** Task 2, Task 6
- **Docs:** [implementation.md#real-codex-verification](./implementation.md#real-codex-verification), [design.md#assumptions](./design.md#assumptions)

### Subtasks
- [ ] 1.1 In a scratch `CODEX_HOME`, set `agents.max_threads` in `config.toml` and `tui.whimsy` in a trusted project's `.codex/config.toml`; send `config/read` with that `cwd` → verify: each leaf has its own origin entry with the expected type (assumption 2)
- [ ] 1.2 Run `codex -c developer_instructions="<marker>" debug prompt-input` without a profile → verify: the marker appears in a developer-role message (assumption 3)
- [ ] 1.3 Record which origin type, if any, `config/read` reports for keys supplied only by Codex itself (assumption 1)
- [ ] 1.4 Write results with the Codex version to `verification/README.md`; update design.md Assumptions and any section a result contradicts

## Task 2: App-server client with config/read
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Slicing:** Contract-First — the request helper is the boundary both launch paths and the trust read share
- **Can run in parallel with:** Task 1, Task 6
- **Docs:** [implementation.md#app-server-client-and-configread](./implementation.md#app-server-client-and-configread)

### Subtasks
- [ ] 2.1 Create `kk/lib/codex_app.py`: one `app-server` session running an ordered request list, with a caller-supplied kill timeout, today's error mapping and a distinct exception for `-32601`
- [ ] 2.2 Rewrite `codex_trust.hooks` as a caller of the helper, keeping `NoTrustMethod` behavior for `check` → verify: existing `test_codex_activation.py` trust tests pass unchanged
- [ ] 2.3 Add the origin lookup (`config/read` with `cwd`, `includeLayers: false`) returning the `origins` map
- [ ] 2.4 Teach `test/kk/codex` to answer `config/read` from a `fixture-origins.json` plus `sessionFlags` for its own `-c` arguments, and `-32601` when `fixture-no-config-read` exists
- [ ] 2.5 Tests for the lookup: user/project/sessionFlags origins, missing method, timeout → verify: `bash test/test-kk.sh` passes

## Task 3: Interactive launch with origin-checked flags
- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** Task 6
- **Docs:** [design.md#1-launch-flags-instead-of-a-profile](./design.md#1-launch-flags-instead-of-a-profile), [implementation.md#launch-flag-composition](./implementation.md#launch-flag-composition), [implementation.md#interactive-launch](./implementation.md#interactive-launch)

### Subtasks
- [ ] 3.1 In `codex_profile.py`, accept and validate `codex.defaults` in `codex_settings`; add a launch-inputs function sharing `compose`'s validation that returns baseline-default leaves, explicit leaves, instructions and the native switch
- [ ] 3.2 In `codex_launch.py`, add flag building: baseline leaves kept only when unset (absent or `packagedDefaults`), explicit leaves dropped only for `project`, regrouped into one `-c` per top-level key with inline tables and `toml_value`; no dotted paths
- [ ] 3.3 Make the sidecar instructions an explicit leaf and let approved imports replace them unconditionally, keeping `import_argument`'s consent and size behavior
- [ ] 3.4 Switch the interactive path in `launch_checked`: sidecar presence check instead of the profile check, origin lookup with the user's trust flags and the launch directory (current directory for resumed sessions), one warning line and explicit-only flags on lookup failure, `argv` without `--profile`; explicit `--profile` stays a pass-through
- [ ] 3.5 Tests asserting echoed `argv` for the six cases in implementation.md §Interactive launch → verify: `bash test/test-kk.sh` passes

## Task 4: Batch launch verifies the final flags
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 6
- **Docs:** [design.md#3-batch-verification](./design.md#3-batch-verification), [implementation.md#batch-verification](./implementation.md#batch-verification)

### Subtasks
- [ ] 4.1 In `launch_checked`, refuse any explicit profile for batch launches and remove the `kk.config.toml` file check, the profile comparison and its error
- [ ] 4.2 Compute kk's flags for batch launches, refusing when the origin lookup fails; pass the user's flags plus kk's flags to `codex_trust.check` and the same kk flags into `argv`
- [ ] 4.3 Delete `matches_profile`, `TIP_TABLE` and `TIP_COUNTER` from `codex_profile.py`
- [ ] 4.4 Replace `test_batch_profile_drift_explains_how_to_preserve_preferences` and `test_vendor_model_tip_update_preserves_batch_checks` with tests for: changed `model` and `[hooks.state]` in `config.toml` still launch; `-cfeatures.hooks=false` still blocks; the trust session receives kk's flags; `-pkk exec` is refused; a failed lookup refuses → verify: `bash test/test-kk.sh` passes

## Task 5: Stop publishing the managed profile
- **Status:** pending
- **Depends on:** Task 4
- **Size:** M
- **Can run in parallel with:** Task 6
- **Docs:** [design.md#4-apply-upgrade-and-rollback](./design.md#4-apply-upgrade-and-rollback), [implementation.md#apply-upgrade-and-the-removed-profile](./implementation.md#apply-upgrade-and-the-removed-profile)

### Subtasks
- [ ] 5.1 Converge `compose` with the launch-inputs function and delete TOML profile rendering; drop `kk.config.toml` from `prepare`'s files
- [ ] 5.2 Make `validate_files` run `debug prompt-input` with all candidate `-c` flags in the scratch home, keeping the `kk.rules` checks; update the fake Codex's `debug prompt-input` branch to accept any flags
- [ ] 5.3 In `publish`, print the one-time removal notice when the obsolete path removed is `kk.config.toml`
- [ ] 5.4 Rewrite profile-content assertions in `test_codex.py`, `test_codex_activation.py` and `test_lifecycle.py`; move the collision test to an owned agent path; keep the `toml_value` round-trip; switch the real-Codex test to `debug prompt-input` with kk's flags
- [ ] 5.5 Add an upgrade test that seeds an owned, drifted `kk.config.toml` and asserts removal, record cleanup and a single notice → verify: `bash test/test-kk.sh` passes

## Task 6: Live-check output fixes
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 5
- **Docs:** [design.md#5-output-fixes](./design.md#5-output-fixes), [implementation.md#live-check-output](./implementation.md#live-check-output)

### Subtasks
- [ ] 6.1 In `live.run`, strip a leading `kk: ` from the reused vendor stderr line and return `ok (guard denied the canary read)` after the reason pattern matches
- [ ] 6.2 Update `test_status.py` expectations and assert a failure message has no duplicated prefix → verify: `bash test/test-kk.sh` passes

## Task 7: Real-Codex end-to-end verification
- **Status:** pending
- **Depends on:** Task 5, Task 6
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#real-codex-verification](./implementation.md#real-codex-verification)

### Subtasks
- [ ] 7.1 Install the branch locally (`kk upgrade --local`) and confirm `~/.codex/kk.config.toml` is removed with the notice
- [ ] 7.2 Reproduce #206: interactive `kk codex`, switch `/model`, approve a repository hook, exit → verify: `kk codex exec "echo ok"` and `kk status --live` pass without `kk apply`
- [ ] 7.3 Record where `/model` and the hook approval were saved (`config.toml` diff or session-only) (assumption 6)
- [ ] 7.4 Disable one guard handler in plain `codex` `/hooks` → verify: `kk codex exec` refuses; re-enable → it passes (assumption 4)
- [ ] 7.5 Time the origin lookup over a few runs (assumption 5); append all results to `verification/README.md`

## Task 8: Docs and ADR
- **Status:** pending
- **Depends on:** Task 7
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#documentation-and-adr](./implementation.md#documentation-and-adr)

### Subtasks
- [ ] 8.1 Update `docs/providers/codex.md`: files table, trust-saving section with the Task 7 observation, removal of the profile-recovery section, launch flags, precedence classes, `codex.defaults`, lookup latency and failure behavior, removal notice, instruction-budget wording
- [ ] 8.2 Update `docs/user-guide/configuration.md` (Codex paragraph, `codex.defaults`, `installed_paths` list) and `docs/getting-started/overview.md:51`
- [ ] 8.3 Write `docs/adr/0015-codex-launch-overrides.md` and amend ADR 0014's Status line → verify: `make docs-build` passes

## Task 9: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 9.1 Run `/kk:test` for the four success criteria and the launch-flag cases, plus `bash test/test-kk.sh` and the full `test/test-*.sh` suite; broaden only if shared launcher or state code changed beyond the planned modules
- [ ] 9.2 Run `/kk:document` to check the docs changed in Task 8 against the shipped behavior
- [ ] 9.3 Run `/kk:review-code` with the Python input to review the implementation
- [ ] 9.4 Run `/kk:review-spec` to verify the implementation matches design.md and implementation.md
- [ ] 9.5 Ask the user how to follow up on any outstanding non-blocking items (for example, GitHub issues)
- [ ] 9.6 Move the feature docs from `docs/feat/wip/` to `docs/feat/done/`, updating markdown references

Sufficient evidence: green `test/test-kk.sh` with the success-criterion tests, plus the Task 7 real-Codex reproduction. Broaden verification if Task 1 or Task 7 contradicts an assumption, or if the trust session and `exec` disagree on guard state.

## Dependency Graph

```
Task 1 ─┐
Task 2 ─┴→ Task 3 ─→ Task 4 ─→ Task 5 ─→ Task 7 ─→ Task 8 ─→ Task 9
Task 6 ─────────────────────────────────→ Task 7
```
