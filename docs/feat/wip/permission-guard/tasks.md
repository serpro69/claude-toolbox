# Tasks: Permission Guard Rework

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: in-progress
> Created: 2026-10-20
> Not Doing: context-protection rules, project-data rules, ask/mode-aware destructive decisions, project-level loosening, Grep/Glob content filtering, negation patterns, Codex read_file enforcement (optional stretch only), pre-edit backups, curl-pipe-sh rules, Windows wrapper support, deny ledger, execution channels beyond Bash/apply_patch/capy MCP tools, non-literal `cd` tracking

## Task 1: Declaration, glob matcher and file-tool secrets check
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2, Task 7
- **Slicing:** Risk-First (the glob matcher's parity with Claude Code is the most uncertain piece)
- **Docs:** [implementation.md#task-1](./implementation.md#task-1-declaration-glob-matcher-and-file-tool-secrets-check)

### Subtasks
- [x] 1.1 Create `klaude-plugin/scripts/guard/guard-rules.json` with `version: 1` and the full baseline from design §6 (secrets, destructive, tmp_roots, selfmod); every destructive rule written in full with the frozen §6.3 vocabulary (`flags_all`/`flags_none`/ordered `subcommand` where needed); `codex` records only on `rm`, `shred`, `sudo`, `su`, `doas`, each with its own `pattern`/`match`/`not_match`
- [x] 1.2 Create `klaude-plugin/scripts/guard/guard.py` as importable pure functions plus `main`: payload parsing into a `Context` with distinct `project_root` (`KK_GUARD_PROJECT_ROOT` → `CLAUDE_PROJECT_DIR` → payload `cwd`) and `exec_dir` (payload `cwd`), declaration loading with version check, `glob_to_regex` anchored at the project root, `resolve` against the execution directory, `check_file_tool`, decision emitter (stdout JSON + stderr + exit 2)
- [x] 1.3 Create `test/fixtures/guard/glob-cases.json` from the docs' examples and `test/guard/test_guard.py` that loads the engine in-process and runs the glob table
- [x] 1.4 Create `test/fixtures/guard/corpus.jsonl` with the file-tool cases (Read `.env` deny, `.env.example` allow, Grep `~/.aws` deny, symlink-to-`~/.ssh` deny, logs and build output allow, `cert.pem` deny as the accepted false positive, `id_rsa.pub` allow, `../.env` from a subdirectory `cwd` deny, Read `.env` with no config files deny) and the corpus replay in `test_guard.py`
- [x] 1.5 Run the tests under the oldest local interpreter; note the version in the test header (floor 3.8)

### Execution context
- 2026-10-25 (observed): baseline `de00583`, clean tree. Intent and authority: design §6 (declaration), §7.2 step 1 (two directories), §7.4 (glob matcher), §7.5 (emitter), §13 (corpus schema); implementation.md Task 1 steps 1–9. All new files; no existing file is modified by this task. Hook wiring (Task 2), Bash analysis and selfmod (Task 3), destructive matching (Task 4) and config loading (Task 5) stay pending: the engine allows Bash and ignores `destructive`/`selfmod` entries for now.
- 2026-10-25 (observed): local interpreters are 3.10.12 (`/usr/bin/python3`, oldest), 3.11.13, 3.12.11; no 3.8/3.9 available, so the floor is checked by `ast.parse(..., feature_version=(3, 8))` in the test plus a run under 3.10.
- 2026-10-25 (decision within requirements): `codex` records carry `match`/`not_match` as command strings, the form the existing `.codex/rules/default.rules` already uses, so Task 6 renders them without a format change.
- 2026-10-25 (decision within requirements): corpus rows use `{root}`, `{home}`, `{tmp}` placeholders that the replay runner substitutes into a per-run sandbox (project dir, fake `HOME` with `.ssh/id_rsa`, and a `{tmp}/kk-secret-link` symlink to it). The row schema stays as design §13 defines it; the sandbox is the runner's fixture, not a row field.
- 2026-10-25 (decision within requirements): `test/test-guard.sh` wraps the Python suite the way `test/test-review-instructions.sh` wraps `review_instructions_test.py`, so `for t in test/test-*.sh` runs it. Not listed in the task's file list; added for suite discoverability.
- 2026-10-25 (verified): `python3 -I test/guard/test_guard.py` under `/usr/bin/python3` 3.10.12 → `Ran 25 tests … OK`; `KK_GUARD_TEST_PYTHON=python3.12 bash test/test-guard.sh` → exit 0. Corpus: 31 rows, 29 replayed, 2 skipped as `pending_task: 3` (Edit of user settings → selfmod; Bash cat of the dotenv file → secrets). `bash test/test-plugin-structure.sh` → 238 assertions passed, 0 failed; `plugin-graph validate` → no broken edges or orphans. Evidence limit: no 3.8/3.9 interpreter was run; the 3.8 floor rests on the `ast.parse(feature_version=(3, 8))` drift guard and manual avoidance of post-3.8 APIs.
- 2026-10-25 (review, isolated `/kk:review-code`): internal code-reviewer → COMMENT (1 P2, 4 P3); external `codex` clink (OpenAI, provider assumed from PAL's shipped manifest; read trace stripped so receipt unverified) → REQUEST_CHANGES (2 P1, 1 P2); external `agy` failed (headless mode auto-denied its file reads; not retried). Findings fixed in the same session, each with a regression test: (a) `resolve` ran `realpath` after `normpath`, so `<symlink-to-~/.ssh>/../.netrc` collapsed lexically to a path outside home and was allowed (codex P1); (b) secrets globs were anchored only at the logical `HOME`/project root, so a physical-path Read under a symlinked root (macOS `/tmp`, `/var/folders`) was allowed (codex P1, code-reviewer P2); (c) `**` regexes stopped at newlines and `$` ignored a trailing newline (codex P2, code-reviewer P3) → `re.DOTALL` + `\Z`; (d) `version: true`/`1.0` passed the `in (1,)` check (code-reviewer P3) → integer type required; (e) a relative payload `cwd` or project root produced an anchor no absolute path could match (code-reviewer P2 second trigger) → fails closed; (f) single-`/` anchors and `[`/`]`/`!` globs compiled with semantics that may differ from Claude Code's (code-reviewer P3) → `validate_glob` rejects them so a bad glob fails closed rather than silently diverging from the settings projection; (g) `TODO(Task N)` comments in the plugin file (code-reviewer prerequisite) → reworded to describe the missing capability without repository task numbers.
- 2026-10-25 (verified after fixes): `python3 -I test/guard/test_guard.py` → `Ran 30 tests … OK` under 3.10.12 and 3.12.11. Corpus: 33 rows, 31 replayed, 2 pending (Task 3).
- 2026-10-25 (review round 2): code-reviewer → APPROVE (Task 1 code; the spelling proposal stays with the user); `codex` → all three original findings resolved, one new P2: `validate_glob` rejected a literal `!` anywhere, while design §7.4 excludes only leading `!pattern` negation. Fixed: only a leading `!` is rejected; a literal `!` inside a name matches (fixture added). Also applied from round 2: `.`/`..`/empty glob segments are rejected because a normalised path can never match them (code-reviewer, otherwise a Task 5 project glob would silently match nothing); `home_dir` requires an absolute `HOME` and falls back to the password database (code-reviewer: an empty `HOME` made `expanduser` return `/`); the two remaining `Task N` comment leftovers in `guard.py` removed. Re-verified: `Ran 31 tests … OK` under 3.10.12 and 3.12.11; `grep -n 'Task [0-9]'` and `grep -nE 'adr|docs/'` over the plugin files return nothing. Not applied (no evidence any harness does it): checking a whitespace-stripped copy of `file_path` as an extra candidate.
- 2026-10-25 (review round 3, confirmation): code-reviewer → APPROVE stands for the Task 1 code; optional hardening applied: `home_dir` fails closed when even the password-database fallback is not absolute, and `test_home_must_be_absolute` accepts either an absolute home or that failure (the earlier `!= "/"` assertion was host-fragile). `codex` → its round-2 P2 resolved; one new narrow P2: `validate_glob` stripped `~` from every tilde-prefixed pattern while the matcher treats only `~`/`~/` as the home anchor, so a bare `~.` filename glob was rejected. Fixed by using the matcher's anchor predicate; fixtures `~.` and `~backup/.env` pin it. Decision: no fourth review round for this one-line predicate alignment pinned by fixture (proportionate verification; further checks unlikely to change the decision). Final: `Ran 31 tests … OK` under 3.10.12 and 3.12.11.
- 2026-10-25 (accepted by the user in the implementing session, "Accept all six"; applied): the proposal below is now in `guard-rules.json` and design §6.3. `rsync` uses `^--del(ete.*)?$`; a second `git restore` rule with `flags_any` `--worktree`/`-W`; the `git branch` `flags_all` rule accepts `-d`/`-f` cluster forms; `git push` `flags_any` adds `-d` (cluster), `^\+` and `^:`; `terraform apply` with `flags_any` `^--?destroy(=.*)?$` (`-destroy=false` also denies, accepted as harmless); `docker` `["container", "rm"]` and `["image", "rm"]`. No `codex` records. `test_equivalent_destructive_spellings_are_declared` pins the regexes now; 17 corpus rows (deny plus benign neighbours) carry `pending_task: 4` and become live when Task 4 removes `4` from `PENDING_TASKS`.
- 2026-10-25 (proposal, superseded by the accepted entry above; owner: user → Task 4): code-reviewer P3 lists data-losing spellings the accepted §6.3 baseline does not cover and the frozen vocabulary can express: `git push -d` / refspec `+ref` and `:ref`; `git branch -d -f` / `-df`; `git restore --staged --worktree` / `-SW` (currently exempted by `flags_none`); `rsync --del` (use `^--del(ete.*)?$` to avoid `--delay-updates`); `docker container rm` / `docker image rm`; `terraform apply -destroy`. The baseline was accepted in design Step 4, so this is not applied; decide before Task 4 writes its corpus rows. Verification condition: corpus rows for each added spelling plus its benign neighbour.
- 2026-10-25 (deferred, owner: Task 2): engine exceptions outside `main`'s `try` (stdin unreadable, `BrokenPipeError` while emitting) exit 1 with a traceback; the wrapper must turn every non-0/2 outcome into a deny and `test-hooks.sh` should cover both. (owner: Task 5): project-config `secrets` must go through `validate_glob` before compile so an out-of-shape glob yields `systemMessage`, not an engine failure. (owner: Task 9): the code-reviewer recalls Claude Code may ignore stdout JSON on exit 2; if so the bypass-mode guarantee rests on exit 2 alone (design Assumption 4); confirm against the current hooks reference. (observation, no owner): macOS case-insensitive filesystems (`.ENV` opens `.env` but matches no glob) and Grep content leakage via the `glob` parameter are documented design limits (§12, §17), not Task 1 defects.

## Task 2: Fail-closed wrapper and hook registration
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 1, Task 7
- **Slicing:** Contract-First (wrapper and engine agree on the exit-code and stdin contract before either is finished)
- **Docs:** [implementation.md#task-2](./implementation.md#task-2-fail-closed-wrapper-and-hook-registration)

### Subtasks
- [x] 2.1 Create `klaude-plugin/scripts/guard/guard.sh`: single stdin read, no payload parsing (no skip path, no tool-name gate; dispatch is the engine's), interpreter list with `KK_GUARD_INTERPRETERS` override, `python3 -I guard.py`, `fail_closed` on every non-0/2 outcome
- [x] 2.2 Update `klaude-plugin/hooks/hooks.json`: matcher `Bash|Read|Edit|Write|NotebookEdit|Grep|Glob|mcp__.+__capy_(execute|execute_file|batch_execute)`, command `${CLAUDE_PLUGIN_ROOT}/scripts/guard/guard.sh`, `timeout: 15`, `onFailure: "block"`
- [x] 2.3 Delete `klaude-plugin/scripts/validate-bash.sh`; update `test/test-plugin-structure.sh` Section 5 to assert the `guard/` files and the `onFailure` key
- [x] 2.4 Rewrite `test/test-hooks.sh` Sections 1–3: allow cases, deny cases (exit 2, JSON, stderr) including a Read of `.env` with no config files present (plugin-only), fail-closed cases (bad interpreter list, empty rules file, non-JSON payload); keep Section 4
- [x] 2.5 Add the file-tool latency measurement (100 Read payloads, p95 always printed, asserted under 60 ms only when `CI` is unset) and record the measured value

### Execution context
- 2026-10-25 (observed): clean baseline `774f553227bfc01d61c8332cece9b2e43d22914f`; Task 1 is done. Authority: design §7.1/§7.5 and implementation Task 2. Scope: wrapper, plugin hook registration, retired substring hook, hook/structure tests, and this task log. Preserve SessionStart and the capy degradation test; do not change the engine's policy.
- 2026-10-25 (decision within requirements): validate captured engine output before forwarding it, including the future exit-0 `systemMessage` shape. Wrapper failure messages use controlled text so JSON denial does not itself require a working Python or jq. Exercise the Task 1 deferred stdin/emitter exceptions through isolated engine fixtures.
- 2026-10-25 (delivery limit): this is an intermediate feature task, not a releasable plugin. The plan explicitly permits the replacement hook to allow Bash until Task 3; destructive checks (Task 4), capy dispatch (Task 13), configuration (Task 5), Codex delivery (Tasks 6/8), and runtime acceptance (Task 9) remain pending with those task owners. Release only after the required feature tasks and Task 12 verification complete. Existing installed/deployed plugin revisions were not inspected.
- 2026-10-25 (verified): `bash test/test-hooks.sh` → 32 cases, 151 assertions passed, 1 planned Task 3 skip; Read p95 25.04 ms across 100 complete wrapper calls on Linux with system Python 3.10.12, below both the 30 ms target and 60 ms local gate (Capy run `f81ed8bf-3613-483a-a6a2-94378f733715`). `bash test/test-guard.sh` → 32 tests OK; `bash test/test-plugin-structure.sh` → exit 0 (batch `22bbaed3-a4c8-42c1-999a-c7bc39eb6a86`). `make plugin-graph` → tests pass and no broken edges/orphans; existing cycle warning remains. No macOS runtime or installed harness invocation was tested.
- 2026-10-25 (fixed during verification): first hook run exposed Bash's signal diagnostic outside engine capture; group redirection now captures it. Second run hung on closed stdin because command substitution reused fd 0 for its own pipe; cancelled run `39ac9116-3591-4f00-92b9-768155b93847`, then saved stdin before any substitution. Both cases pass in the final run. Timing uses one Python `perf_counter` driver instead of GNU-only `date +%s%N` so the test also runs with BSD date; it still measures every complete wrapper invocation and applies the specified CI gate.
- 2026-10-25 (review fix): independent code-reviewer identified one P2 hard-contract violation: Bash variable buffering drops raw NUL bytes, turning malformed JSON into an allowed payload. Probe `0cfd2975-bbe3-40c8-bea1-dce89c6a47ff` confirmed wrapper exit 0 versus engine exit 2. Replaced the plan's suggested trailing-`x` buffering with a private temporary payload file: read original stdin once, preserve all bytes, redirect the file into each candidate interpreter, clean up on exit. The wrapper still performs no payload parsing. Added a raw-NUL regression; reviewer inspected the correction and found no remaining actionable issues.
- 2026-10-25 (final verification, supersedes earlier counts/timing): `bash test/test-hooks.sh` → 33 cases, 157 assertions passed, 1 planned Task 3 skip; Read p95 **25.72 ms** over 100 calls. The same captured command then passed `shellcheck -e SC1091` and `bash -n` for wrapper, hook tests and interpreter fixture (run `e460de66-80af-4936-b84e-4a2a158bb39a`, exit 0). Engine tests remain 32 OK and structure tests 243 assertions passed; the payload-buffer correction changes neither engine nor structure. Git whitespace checks pass using the repository's existing space indentation (the host's global `indent-with-non-tab` setting flags existing JSON/Python style).
- 2026-10-25 (external review coverage): `/kk:review-code` selected the clink backend once (no API providers). Authoring provider OpenAI; eligible roster `agy`/Google and `claude`/Anthropic, both provider mappings assumed from PAL's shipped manifest (operator declarations override them); `codex` absent and same authoring provider, `gemini` absent/retired. Automatic approval review initially rejected sending the bundle; the user explicitly approved it in this session before dispatch. `agy` failed because its native headless permissions denied `read_file`; `claude` failed with a tool timeout after 300 seconds. Neither returned findings, model identity, or evidence of source receipt; no external corroboration claimed, no failed client retried or permissions changed. Supplemental external review remains unavailable; operator-owned follow-up, if desired, is to enable scoped CLI read permissions/resolve the timeout and request a fresh review. The isolated workflow permits completion with the independent local review.
- 2026-10-25 (completed): independent `code-reviewer` (gpt-6.1-sol, OpenAI) → **APPROVE** for Task 2 after inspecting the final canonical wrapper and NUL regression. All seven changed files reviewed against baseline `774f553227bfc01d61c8332cece9b2e43d22914f`; no remaining actionable findings or evidence requests. No systemic P0/P1 findings to index, and no new project conventions beyond this documented contract. Task 2 is done; feature release remains blocked by the explicitly pending tasks above. Task 3 is next.
- 2026-10-25 (cleanup limit): temporary review evidence remains at `/tmp/kk-permission-review.pjgCjysK`; the repository's `Bash(rm:*)` deny blocked cleanup before execution. No workaround attempted. Optional cleanup owner: user; remove that exact temporary directory when no longer needed. No repository artifact depends on it.

## Task 3: Bash channel tokenizer, path extraction, secrets and self-modification
- **Status:** done
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 2, Task 7
- **Docs:** [implementation.md#task-3](./implementation.md#task-3-bash-channel-tokenizer-path-extraction-secrets-and-self-modification)

### Subtasks
- [x] 3.1 Port `defang`, `strip_quotes`, `basename`, `command_position_tokens`, wrapper tables, segment/chain splitters and `substitution_bodies` into `guard.py` with attribution; use Claude Code's exact separator set; enforce the order of design §7.3: `extract_bodies` on the original text first, `defang` only for the per-segment prose view, a quote-stripped operand view for all path checks; unit-test `sh -c 'rm -rf x'`, `echo "$(rm x)"` and `cat "/repo with spaces/.env"` survive extraction
- [x] 3.2 Implement heredoc handling before body extraction: quoted-delimiter bodies are masked from `extract_bodies` and dropped for data-sink consumers; unquoted-delimiter bodies are scanned for substitutions, then dropped for data sinks; shell/interpreter and unknown consumers keep the body; unit-test the commit-message form (including a literal `$(rm -rf x)` line) as allow, `cat <<EOF` with `$(rm -rf x)` as deny (after Task 4), a `bash <<EOF` body as kept, and the unknown-consumer case as the documented deny
- [x] 3.3 Implement path-like operand extraction resolved against the execution directory and matched against secrets globs anchored at the project root, raw and resolved; corpus: `cat .env` deny, `cat ../.env` from `cwd: /repo/sub` deny, `cat ../README.md` from the same `cwd` allow, `cat .env.example` allow, `find . -not -path './.git/*'` allow
- [x] 3.4 Implement mutation-operand extraction (`>`, `>>`, `tee`, `sed -i`, `dd of=`, last operand of `cp`/`install`, every operand of `mv`, `ln` link name) against selfmod (equal, descendant and ancestor matching) and secrets; corpus: redirect into `.claude/settings.json` deny, `mv .codex/hooks.json /tmp/x` deny, `mv .codex /tmp/` deny, `mv src/a.go src/b.go` allow, `cat .claude/settings.json` allow
- [x] 3.5 Implement inline-interpreter write detection; corpus: `python3 -c "open('.claude/settings.json','w')"` deny, read form allow
- [x] 3.6 Enable selfmod on Edit/Write/NotebookEdit and the pending corpus cases; enable the Bash deny cases in `test-hooks.sh`

### Execution context
- 2026-10-25 (observed): clean baseline `608077c749a0290fc3884e5776b88d0e08d0856a`. Authority: design §7.2–7.5 and implementation Task 3. Scope: the canonical engine, Python tests/corpus, hook tests and this task log. Preserve file-tool secrets, project-root versus execution-directory anchoring, wrapper failure semantics and benign command/prose cases. Destructive matching/temp-directory tracking (Task 4), configuration (Task 5), generated projections/adapters (Tasks 6/8), runtime acceptance (Task 9) and capy dispatch (Task 13) remain pending; this intermediate feature state is not releasable.
- 2026-10-25 (implementation approach): extract executable bodies before constructing prose views, retain quoted path operands, classify heredocs before recursion, and check mutation targets against protected paths including ancestors. Reuse the existing standard-library-only Python 3.8 contract and unittest/corpus runners. Verification will cover the engine and complete hook boundary under available Python versions, then independent isolated review. No deployed plugin revision is claimed as verified.
- 2026-10-25 (verified initial candidate): captured run `73c4d2d9-2a12-4142-8423-99f510e50d19` passed 43 engine tests under Python 3.10.12 and 3.12.11, the hook suite (35 cases, 169 assertions, no failures), ShellCheck for the changed hook tests, and plugin structure checks. Read-wrapper p95 was 30.71 ms over 100 calls: above the 30 ms target, below the 60 ms local gate. No Python 3.8/3.9 interpreter or macOS/harness runtime was exercised; the existing 3.8 syntax drift check runs in the suite.
- 2026-10-25 (isolated review, repairs underway): independent `code-reviewer` requested changes for ANSI-C quoted paths, clustered `sed -Ei`, attached `cp -tDIR`, attached interpreter code and here-string scripts, Python keyword argument order, BSD `sed -i ''` false blocks, and a lexer progress bug on non-shell whitespace. Author probe `5baa865d-1733-47d5-9548-5a906079ae7f` confirmed the first five command-form bypasses without executing the commands. Added decoding/option binding/stdin handling and regression/control cases. Repair run `96725523-e1fa-430e-bbfe-aeedeafbdee4` exposed a flawed benign fixture: `/tmp` is an ancestor of the sandbox's protected paths and must deny under the agreed ancestor rule. Changed that control to the sandbox's sibling scratch directory; the ancestor-deny requirement is unchanged.
- 2026-10-25 (delivery follow-up, owner: Task 6): tokenizer helpers/tables are adapted from safe-claude-code at `126fe5b94ab2716af389660d9cb4bbba6ed142b0`; attribution and a byte-identical copy of its ELv2 license now ship beside the canonical engine. The generator is intentionally pending. Include `guard/LICENSE.md` alongside the three engine files in the Codex copy and freshness checks; verify the license remains byte-identical. No new third-party runtime dependency was introduced.
- 2026-10-25 (verified repairs): final engine run `b44f81fe-5d20-4a42-812b-c687f8f927ae` passed **46 tests** on both Python 3.10.12 and 3.12.11, including the review's follow-up cases for clustered `python3 -Ic`/`-Bc` and here strings piped through `cat` into a shell/interpreter. Corpus: 76 rows, 56 active and 20 explicitly pending Task 4. Run `ed7111f2-3a89-4bab-94f2-94ad26eb38b4` passed the complete hook suite (35 cases, 169 assertions, zero failures), Read p95 **29.07 ms**; its graph step found the new license orphan. Added a plugin README attribution/link; `make plugin-graph` then passed with no broken edges/orphans in run `bfe89639-c645-4c9d-83be-8bd1d34dab48` (existing cycle warning unchanged). The earlier plugin structure and ShellCheck results remain applicable; no skill/generator source changed. Git whitespace and upstream license comparison pass.
- 2026-10-25 (external review coverage): one-time PAL discovery selected clink, with no API providers. Authoring provider OpenAI; `agy`/Google and `claude`/Anthropic were eligible, both provider mappings assumed from PAL's shipped manifest (operator declarations override them). `codex` was absent and also excluded as the authoring provider; `gemini` was absent/retired. Automatic approval review rejected export initially; the user approved clink, then explicitly approved Claude after its destination-specific rejection. Actual `agy` invocation failed because the executable was missing despite the startup observation. Actual Claude invocation timed out after 300 seconds. Neither returned findings, model identity or observable source receipt; no external corroboration is claimed, and neither failed client was retried after invocation. Optional operator-owned follow-up: restore the CLI executable / resolve the timeout, then request a fresh external review. The isolated workflow allows the independent local review to stand without external corroboration.
- 2026-10-25 (completed): independent `code-reviewer` (gpt-6.1-sol, OpenAI) reviewed the seven changed files and four unchanged contracts, then **APPROVED** the final snapshot (`bc5e992a25b5f4125b220f1cc5d783e7830ad67513f1bfe6fe0d36c8c9fc5ce1` diff SHA256). All seven original findings and both continuation cases were resolved, with no remaining findings/evidence requests. Source-only reviewer; executed checks are author-attributed above. The systemic literal-spelling lesson is indexed as `kk:review-findings:permission-guard-literal-spellings`; no additional project conventions were established. Task 3 is done; Task 4 is next. Full-feature release remains blocked by the explicitly pending tasks.
- 2026-10-25 (cleanup limit, owner: user): repository `Bash(rm:*)` policy in `.claude/settings.json` denied deletion before execution, so this session's review snapshots remain at `/tmp/kk-permission-task3-review.tz3J0I11`, `/tmp/kk-permission-task3-fixed.Y79b3qNH`, and `/tmp/kk-permission-task3-final.8mAl99CS`. No workaround attempted. Optional next action: remove those exact directories when no longer wanted; verify only those snapshots were removed. No repository artifact depends on them.

## Task 4: Destructive tier with the temp exemption and wrapper recursion
- **Status:** done
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 7
- **Docs:** [implementation.md#task-4](./implementation.md#task-4-destructive-tier-with-the-temp-exemption-and-wrapper-recursion)

### Subtasks
- [x] 4.1 Implement the rule matcher (`program`, ordered `subcommand`, `flags_any`, `flags_all`, `flags_none`) with program-level global-option skipping, against the Task 1 declaration with no new fields; unit-test `git restore f` deny vs `--staged` allow, `git branch -D`/`-rfD`/`--delete --force` deny vs `--delete`/`-d` allow, `git stash drop` deny vs `git stash list` allow, `docker volume rm` deny vs `docker volume ls` allow
- [x] 4.2 Wire recursion over the bodies extracted in 3.1 (`sh -c`, `bash -c`, `$(...)`, backticks, `<(...)`) and the wrapped programs of `xargs`, `env`, `sudo`, `timeout`, `nohup`; corpus: `/bin/rm`, `sh -c 'rm -rf x'`, `xargs rm`, `env rm x`, `echo "$(rm x)"` all deny
- [x] 4.3 Implement `targets_under_tmp` with `$TMPDIR` resolution and directory tracking (literal absolute `cd` updates the execution directory; any other `cd`/`pushd`/`popd`/`env -C` marks it uncertain so only absolute operands qualify); corpus: `rm -rf /tmp/kk-test` allow, `cd /tmp/kk-test && rm -rf ./x` allow, `cd /work/project && rm -rf ./work` with `cwd` under `/tmp` deny, `env -C /work/project rm -rf ./work` deny, `rm -rf "$T"` deny, `rm -rf /tmp/*` deny, `rm -rf /tmp/../etc` deny, `rm -rf ~` deny, `rm -rf .` at project root deny
- [x] 4.4 Add corpus rows for every `git`, `infra` and `privilege` rule plus the must-allow neighbours (`git branch -d`, `git rebase`, `git commit --amend`, `git restore --staged`, `kubectl get`, `terraform plan`, `docker ps`); enable the equivalent-spelling rows already in the corpus with `pending_task: 4` (added in Task 1)
- [x] 4.5 Unit-test the destructive deny reason: names the category, the rule reason, the `!` remedy and the user config path

### Execution context
- 2026-10-25 (observed): clean baseline `9caaaf52e0a42ebaeaa1dc88846ec6c73ff354e7`. Authority: design §6.3–6.4, §7.3 and implementation Task 4. Scope: canonical engine, Python tests/corpus, hook transport checks and this log. Preserve secrets/selfmod checks, quoted prose, interpreter isolation and the Python 3.8 floor. Configuration, generated delivery, adapters and runtime acceptance remain with their pending tasks; this increment is not a feature release.
- 2026-10-25 (implementation approach): match the existing declaration without schema changes, retain wrapper identities for privilege checks, associate recursive bodies with their segment's directory, and grant temporary cleanup only for literal resolved targets. Directory uncertainty must not grant relative cleanup. Destructive fixtures using relative paths require an explicit non-temporary cwd because the corpus sandbox itself lives under `/tmp`; assertions remain deny.
- 2026-10-25 (verification correction): first run `0b98310b-1693-4d25-9c27-df8498516dd7` failed the old Task 3 expectation that `sudo sh -c 'cat .env'` reports secrets. Task 4 explicitly requires sudo itself to deny first, so the test now expects the destructive privilege reason; other wrapper secret expectations remain unchanged. Initial corrected run `e5c1ab46-29c6-402a-8edc-1b0c8fe9a7e8` passed 54 tests on Python 3.10.12/3.12.11, the hook suite and plugin structure. ShellCheck and Bash syntax passed in run `1e17ac6e-a7c1-4122-a278-6920565f2d04`.
- 2026-10-25 (isolated review corrections): independent `code-reviewer` requested changes for five P1 issues: skipped/pipelined `cd` incorrectly granted an exemption; uncertain cwd lost protected-path locations; substitution output became a literal `cd` target; `env -S` dropped trailing operands; clustered `env -iC` hid the program. Engine-only probes `79665d97-5ed4-42d2-a96b-a365d9f31570` and `38472ee8-b8aa-41af-9cbd-3714fea23557` confirmed the original bypasses without executing shell fixtures. Corrected by retaining known possible directories for deny checks, requiring raw literal same-shell directory transitions for exemption, binding clustered wrapper options, and preserving the full raw argument tail during split-string recursion. Follow-up probes `d62e80c1-1fb6-43e6-8fc4-cd16425200a2` and `6db6f4d4-687f-4f8f-abea-23bb150c3ff8` confirmed two residuals, now covered and fixed: xargs's unknown appended arguments survive env recursion; relative env chdir values contribute protected-path candidates. The context-preservation lesson is indexed as `kk:review-findings:permission-guard-exemption-context`.
- 2026-10-25 (verified final code): run `ea1e682c-baa4-4d14-acf8-ec330b007a52` passed **57 tests** under both Python 3.10.12 and 3.12.11, including **127 active corpus rows**, then the complete hook suite (**37 cases / 178 assertions / zero failures**). Read wrapper p95 **31.96 ms**: above the 30 ms target, below the 60 ms local gate; full runtime acceptance remains Task 9. Intermediate repair runs `a25e1e11-1017-4197-86c2-d12528ba1b9a`, `506eb4c9-7339-42a1-a388-751ef8207085` and `76ac90ed-ff6d-4a33-be4e-de7713c8f8a7` also passed their then-current cases. No Python 3.8/3.9, macOS or installed harness execution claimed; the existing 3.8 syntax drift check passes. Declaration unchanged; no skill or generated output changed. Git whitespace checks pass using repository indentation conventions.
- 2026-10-25 (external review coverage): one-time PAL discovery selected clink with no API providers. Eligible `claude` maps to Anthropic by the shipped-manifest assumption (operator declarations override it); authoring provider is OpenAI. `agy` and `codex` executables were missing; `codex` also shares the authoring provider; `gemini` is retired/missing. Automatic approval review initially rejected exporting the snapshot; the user explicitly selected "Approve external Claude review" in this session. The authorized invocation timed out after 300 seconds and returned no findings, observed model or source receipt. No retry, provider substitution or external corroboration. Optional operator-owned follow-up: diagnose the Claude CLI timeout and request a fresh review if desired; the isolated workflow permits scoped completion from the independent local review.
- 2026-10-25 (completed): independent `code-reviewer` (gpt-6.1-sol, OpenAI) **APPROVED** the final Task 4 snapshot, diff SHA256 `123fc038cb5c10bf04f72b244a5fe38f86c772c06d303d719cc63a54829027fa`, after inspecting all five changed files, five affected contracts and the exact historical engine. All five original findings and both residuals are resolved; no remaining findings or evidence requests. Source-only reviewer; execution results are author-attributed above. Final engine/test hashes match the reviewed snapshot. Task 4 is done; Task 5 is next. Full-feature release remains pending the separate delivery and acceptance tasks. No new project conventions beyond the documented contract.
- 2026-10-25 (retained review evidence): snapshots `/tmp/kk-permission-task4-review-20261025` and `/tmp/kk-permission-task4-fixed-20261025` retain the failed external request's inputs, reviewed corrections and historical provenance. Optional cleanup owner: user; remove these two exact directories when the review/timeout record is no longer needed. No repository runtime depends on them.

## Task 5: Configuration layering
- **Status:** done
- **Depends on:** Task 4
- **Size:** M
- **Can run in parallel with:** Task 7
- **Docs:** [implementation.md#task-5](./implementation.md#task-5-configuration-layering)

### Subtasks
- [x] 5.1 Implement project-config loading (`KK_GUARD_PROJECT_CONFIG` or `<root>/.claude/kk-guard.json`): schema check, shape lint, union merge, invalid → baseline kept plus `systemMessage`
- [x] 5.2 Implement user-config loading (`KK_GUARD_USER_CONFIG` or `~/.claude/kk-guard.json`): union of the `*` entry and the single longest path-prefix entry for the `realpath`ed project root (shorter prefixes ignored); `disable_categories`; `allow_patterns` tested per simple command (each segment and extracted body) and exempting only that command from destructive rules; `disable_selfmod`
- [x] 5.3 Create fixtures under `test/fixtures/guard/project-config/` and `test/fixtures/guard/user-config/`; unit tests for tighten-only enforcement, unknown-key reporting, invalid JSON, category disable scoped by path, `*` plus prefix union with an ignored intermediate prefix, `git clean -nd; rm -rf ./work` denied under `^git clean -n`, allow pattern not touching secrets or selfmod, `disable_selfmod`
- [x] 5.4 Emit `{"systemMessage": ...}` as the only stdout key on allowed calls when a config was invalid; assert the field and the absence of `hookSpecificOutput` in `test-hooks.sh`
- [x] 5.5 Wrapper test: with `KK_GUARD_PROJECT_CONFIG` pointing at a fixture that adds a secrets glob, a matching Read is denied through `guard.sh`; with the override pointing at a nonexistent file, the same Read is allowed

### Execution context
- 2026-10-25 (observed): clean baseline `52abf1d5dc71bd2ca72a4f12e0b05fad93d69274`. Authority: design §8 and §7.5, implementation Task 5. Scope: canonical engine, config fixtures, Python/corpus tests, hook transport tests and this log. Preserve baseline policy, command recursion, directory tracking and Python 3.8 compatibility. No dependency changes; delivery/generators, adapters, capy dispatch and runtime acceptance remain with their existing pending tasks.
- 2026-10-25 (implementation approach): validate each config independently before applying it; invalid project additions or user loosening leave the other valid layer intact. Unknown top-level keys are reported and ignored. Select user entries by path-component prefix of the real project root; apply exceptions separately to each destructive command check, retaining secrets/selfmod checks and recursive-body inspection. Return config diagnostics on allowed and denied calls. Verification compares this task against the baseline above with the existing engine/corpus and wrapper suites; no installed/deployed harness result is claimed.
- 2026-10-25 (verified): captured run `7754e6e6-ad0b-437f-8b50-eb7da5e0f920` passed `python3 -I test/guard/test_guard.py` under Python 3.10.12 and `KK_GUARD_TEST_PYTHON=python3.12 bash test/test-guard.sh` under 3.12.11: **71 tests each, 139 active corpus rows**. `bash test/test-hooks.sh` passed **42 cases / 202 assertions**; `shellcheck -e SC1091 test/test-hooks.sh` passed; `bash test/test-plugin-structure.sh` passed **47 cases / 243 assertions**. Read wrapper p95 **32.87 ms**, below the 60 ms local gate and above the 30 ms target; runtime acceptance remains Task 9. Existing Python 3.8 syntax drift check passes, but no 3.8/3.9 interpreter, macOS or installed-harness run is claimed. Wrapper source required no changes: its existing environment forwarding and warning/deny schema already satisfy the contract. Git whitespace checks pass with repository indentation conventions; no skill or generated output changed.
- 2026-10-25 (isolated internal review): independent `code-reviewer` (gpt-6.1-sol, OpenAI) **APPROVED** Task 5 with no P0–P3 findings or evidence requests after inspecting all 11 changed/new files, seven unchanged contracts and the historical engine at the baseline above. Snapshot diff SHA256 `0295513a57a0b970d51e1e14d5b5fc5f3d0d33d16bc7c46aa8c88bd55991a2b3`; engine/test/corpus hashes match the reviewed snapshot. Review was source-only; execution results above are author-attributed. No findings or new project conventions to index. Full-feature release remains pending Tasks 6, 8–10, 12 and 13; Task 11 is optional.
- 2026-10-25 (external review coverage): one-time PAL discovery selected clink, with no API providers. Eligible `claude` maps to Anthropic by the shipped-manifest assumption (operator declarations override it); authoring provider OpenAI. `agy` and `codex` executables were missing; `codex` also shares the authoring provider; `gemini` is retired/missing. Automatic approval review initially rejected exporting the snapshot; the user explicitly selected "Approve external Claude review" in this session. The authorized invocation timed out after 300 seconds (`timed out awaiting tools/call after 300s`), returning no findings, observed model or source receipt. Configured model unknown; no external corroboration, failed-client retry or provider substitution. Optional operator-owned follow-up: diagnose the Claude CLI timeout and request a fresh review if desired; the isolated workflow permits completion from the independent local approval.
- 2026-10-25 (completed): all five subtasks, verification and scoped review are complete. Task 5 is done; Task 6 is next. This closes the user's one-task request, not the full feature. Review inputs and historical provenance remain at `/tmp/kk-permission-task5-review-20261025` for the failed external-request record; optional cleanup owner: user, remove that exact directory once the record is no longer needed. No runtime depends on it.

## Task 6: Generators, parity and freshness
- **Status:** pending
- **Depends on:** Task 1, Task 4
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7
- **Docs:** [implementation.md#task-6](./implementation.md#task-6-generators-parity-and-freshness)

### Subtasks
- [ ] 6.1 Create `scripts/generate-guard.sh`: settings `permissions.deny` projection via `jq` in place, `default.rules` rendering with generated header (one `prefix_rule` per `codex` record, union tokens as Starlark lists, per-record examples), engine copy to `.codex/scripts/guard/`, docs table between `GUARD-RULES` markers in `docs/user-guide/configuration.md` with a "Codex forbid" column and the `disable_selfmod` example
- [ ] 6.2 Confirm the Task 1 `codex` records (only `rm`, `shred`, `sudo`, `su`, `doas`) render to a file Codex loads; validate with `codex execpolicy check` for `rm -rf x` (forbidden) and `ls -la` (no match) when the CLI is available and record its version
- [ ] 6.3 Add `generate-guard` to the Makefile and `generate-all`; add the freshness `git diff --exit-code` step to CI beside generate-kodex
- [ ] 6.4 Structure-test assertions: secrets shape lint, destructive field-set lint, `codex` records restricted to the five permitted rules, regenerate-and-diff, `cmp` of Codex copies, generated header in `default.rules`, capy tools present in the `hooks.json` matcher
- [ ] 6.5 Update `AGENTS.md`: `default.rules` and `.codex/scripts/guard/` are generated; document `make generate-guard`

## Task 7: Template sync deny replacement and dropped-entry report
- **Status:** done
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6
- **Docs:** [implementation.md#task-7](./implementation.md#task-7-template-sync-deny-replacement-and-dropped-entry-report)

### Subtasks
- [x] 7.1 In `template-sync.sh` settings merge: compute `DROPPED_DENY_ENTRIES`, then set `.permissions.deny` to upstream's array; keep `allow` unioned; test "deny replaced, allow unioned"
- [x] 7.2 Add the "Permission deny entries removed" section to the diff report and markdown summary with the guidance text; add `dropped_deny_count` CI output; tests for present and absent cases
- [x] 7.3 Add `.claude/kk-guard.json` to `BUILTIN_EXCLUSIONS` and strip it in `fetch_upstream_templates`; test zero deleted files when only downstream has it
- [x] 7.4 Update `docs/user-guide/template-sync.md` merge-behavior section

### Execution context
- 2026-10-25 (observed): task scoped to design §10 and implementation Task 7. Independent worktree `/tmp/claude-toolbox-permission-guard-task7`, branch `feat/permission-guard-task7`, based on `master` at `de00583`. Existing guard work on `feat/permission_guard` is outside this diff. Preserve downstream scalars, allow-list union, manifest overrides, sync exclusions and the existing no-file-deletion contract.
- 2026-10-25 (implementation decision within requirements): report downstream-only deny entries only when settings are eligible for sync; reset tracking on each substitution pass. Treat an absent upstream deny list as empty. `.claude/kk-guard.json` is excluded on both fetch and comparison paths. Runtime loading of that config remains Task 5; this task does not claim the full guard is ready for release.
- 2026-10-25 (observed and corrected): `apply_changes` used recursive `cp` without consulting exclusions, so the documented settings opt-out only affected the report. Apply now checks the same exclusion predicate per staged entry; regression coverage checks excluded settings and guard config, an ordinary update, empty directories and symlinks. This adjacent correction is necessary for Task 7's opt-out contract.
- 2026-10-25 (verified): `bash test/test-template-sync.sh` passes 155 cases / 316 assertions (Capy run `c52f15c8-4463-4866-a1ff-4e5e564210e9`); cleanup and manifest suites and Bash syntax checks passed in batch `178f7c76-0cba-4b51-be05-3dd657e28ec6`. The first sync-suite attempt failed a new test that captured stdout warnings from stderr; corrected the capture, with the warning assertion retained. Git's global `indent-with-non-tab` setting conflicts with this script's existing space indentation; `git -c core.whitespace=space-before-tab,trailing-space diff --check` passes without changing repository or user configuration.
- 2026-10-25 (verified, broader checks): all 13 `test/test-*.sh` suites passed across the focused and broader runs. Broader run `d48a85ea-28b5-448f-bf5b-a6eddcb7f3fd` exposed environment failures in Codex TOML validation (no parser under default Python 3.10) and functional-review tools (require Python 3.11+). Both passed unchanged using the installed Python 3.11.13 in batch `5b354ff0-3714-4ff4-8b41-b6dec45175cd`; no test assertions were relaxed.
- 2026-10-25 (isolated internal review): `code-reviewer` (OpenAI GPT-6.1) approved Task 7 with no P0–P3 findings and no evidence requests. Source review covered all four changed files plus unchanged workflow/helpers and task contracts; test execution remained author-attributed. Full guard release readiness and downstream deployment are outside this task. No findings to index.
- 2026-10-25 (inherited limitation, deferred, owner unassigned): legacy `run_plugin_migration` edits hooks/marketplace registration despite settings copy exclusions; it preserves `permissions.deny`. Kept outside Task 7 because changing legacy migration semantics is separate from deny replacement and staged-file copying. The guide now states this limit. Follow-up: decide whether migration must honor settings exclusions, then add a pre-plugin-upgrade fixture checking excluded settings and required plugin registration together.
- 2026-10-25 (external review coverage): PAL discovery selected clink (no API models). Eligible clients were `agy` → Google and `claude` → Anthropic, both provider mappings assumed from PAL's shipped manifest; operator declarations override those defaults. Configured/observed external models are unknown. `codex` was unavailable and excluded as the authoring provider (OpenAI); `gemini` was unavailable/retired. Initial egress approval rejections were resolved by the user's explicit external-review approvals, including Claude specifically. Actual `agy` invocation failed when native headless permissions denied `read_file`; actual `claude` invocation timed out at 300 seconds. Neither produced findings or verified source receipt; no external approval or corroboration is claimed. No failed client was retried after execution. Both received the same 14-path manifest (four common criteria, diff, four changed sources, workflow/helpers, design/implementation and factual context); snapshots are retained at `/tmp/permission-guard-task7-review.An5uxY` for the failed-attempt record.
- 2026-10-25 (completion): isolated internal approval stands after review of the documentation clarification; all four subtasks and verification are complete. External failures are disclosed under `/kk:review-code`'s degraded-review path. No new conventions need indexing. Only Task 7 is done; full guard release readiness remains with the pending feature tasks.

## Task 8: Codex adapter
- **Status:** pending
- **Depends on:** Task 2, Task 4, Task 6, Task 13
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [implementation.md#task-8](./implementation.md#task-8-codex-adapter)

### Subtasks
- [ ] 8.1 Implement `apply_patch` handling in `guard.py` (header parsing, `cwd` resolution, secrets and selfmod, `Delete File` as filesystem-destructive); regenerate the Codex copy; corpus cases
- [ ] 8.2 Rewrite `.codex/scripts/pretooluse-bash.sh`: keep capy detection and HTTP section, replace the denylist loop with delegation to `guard.sh` with `KK_GUARD_PROJECT_ROOT="$REPO_ROOT"` exported, trap failures to stderr + exit 2; update `test-codex-hooks.sh` denylist assertions and add a subdirectory-`cwd` `cat ../.env` deny
- [ ] 8.3 Create `.codex/scripts/pretooluse-patch.sh` (same delegation and root export) and the `Edit|Write` PreToolUse entry in `.codex/hooks.json`; tests in `test-codex-hooks.sh` and `test-codex-structure.sh`
- [ ] 8.4 Create `.codex/scripts/pretooluse-mcp.sh` and the PreToolUse entry with matcher `^mcp__[^[:space:]]+__capy_(execute|execute_file|batch_execute)$`, leaving capy's own entry in place; tests: shell `cat .env` via `capy_execute` denies, `go test ./...` allows, structure test asserts both entries
- [ ] 8.5 Fail-open mitigation test: bad interpreter list → all three adapters exit 2 with stderr
- [ ] 8.6 `session-start.sh`: render the protected-files paragraph from the synced declaration with `jq`; assert in both legacy and capy modes
- [ ] 8.7 Update `docs/providers/codex.md` with the three adapters and the parity-gap table including the "not loosenable on Codex" row

## Task 9: Assumption closure for latency, bypass mode and Codex cwd
- **Status:** pending
- **Depends on:** Task 2, Task 4, Task 5, Task 8
- **Size:** S
- **Can run in parallel with:** Task 10
- **Docs:** [implementation.md#task-9](./implementation.md#task-9-assumption-closure-for-latency-bypass-mode-and-codex-cwd)

### Subtasks
- [ ] 9.1 Add the Bash-path p95 latency measurement (always printed; fail beyond 100 ms only when `CI` is unset); record the measured value
- [ ] 9.2 Run the throwaway bypass-mode check in a scratch project; record date, version and outcome in design §16
- [ ] 9.3 Run the Codex `apply_patch` relative-path check; record date, version and outcome in design §16

## Task 10: Documentation, ADR and version bump
- **Status:** pending
- **Depends on:** Task 6, Task 7, Task 8
- **Size:** M
- **Can run in parallel with:** Task 9
- **Docs:** [implementation.md#task-10](./implementation.md#task-10-documentation-adr-and-version-bump)

### Subtasks
- [ ] 10.1 Write `docs/adr/0012-permission-guard-single-declaration.md` (0010 and 0011 are taken; re-check the next free number) with Context (commit `e0036b2`), Decision, Consequences including rejected alternatives, Codex gaps, the hooks-off `rm` regression and revisit conditions
- [ ] 10.2 Add the dated update to ADR 0005; add the 0012 row to `docs/contributing/adrs.md`; ask the user before adding the missing 0008/0009/0011 rows
- [ ] 10.3 Update `docs/user-guide/configuration.md` prose and hooks table (including the capy MCP channel) plus the new config subsection with the selfmod-blocks-settings-edits note and `disable_selfmod` example; `docs/providers/claude-code.md`; `docs/getting-started/plugin-only.md`
- [ ] 10.4 Update `docs/contributing/plugin-development.md` (fail-closed contract, toolbox `disable_selfmod` note), `testing.md`, `architecture.md`, `klaude-plugin/README.md`
- [ ] 10.5 Bump `klaude-plugin/.claude-plugin/plugin.json` minor version; confirm no live reference to `validate-bash` remains outside `docs/feat/done/`

## Task 11: Codex sandbox permission profile (optional)
- **Status:** pending
- **Depends on:** Task 6
- **Size:** S
- **Can run in parallel with:** Task 9, Task 10
- **Docs:** [implementation.md#task-11](./implementation.md#task-11-optional-codex-sandbox-permission-profile)

### Subtasks
- [ ] 11.1 Confirm the installed Codex version documents `[permissions.<name>.filesystem]` glob denies; stop here if not, recording the version
- [ ] 11.2 Render the `[permissions.kk-guard.filesystem]` table from project-scope secrets globs in `generate-guard.sh`; verify a scratch `read_file` of `.env` is denied
- [ ] 11.3 Ensure the sync TOML merge preserves the table and the freshness check covers it

## Task 12: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 13
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 12.1 Run `/kk:test` to verify all tasks: full bash suites, Python tests, corpus, latency
- [ ] 12.2 Run `/kk:document` to update any relevant docs
- [ ] 12.3 Run `/kk:review-code` with bash and Python as the project languages
- [ ] 12.4 Run `/kk:review-spec` to verify the implementation matches design.md and implementation.md

## Task 13: capy MCP execution channel
- **Status:** pending
- **Depends on:** Task 4
- **Size:** S
- **Can run in parallel with:** Task 5, Task 6, Task 7
- **Slicing:** added by the 2026-10-25 reviews (R7); numbered after Task 12 but executed before Task 8
- **Docs:** [implementation.md#task-13](./implementation.md#task-13-capy-mcp-execution-channel)

### Subtasks
- [ ] 13.1 Implement engine dispatch for `capy_execute` (shell → Bash analysis; other languages → inline-interpreter and secrets scans), `capy_execute_file` (`path` as a Read, then `code`), `capy_batch_execute` (each `commands[].command`); honour `tool_input.cwd` as the execution directory; match the tool name by its suffix after the server prefix
- [ ] 13.2 Corpus cases: shell `cat .env` deny, shell `go test ./...` allow, python `open('.env').read()` deny, python `print(1)` allow, javascript write to `.claude/settings.json` deny, batch containing `rm -rf .` deny, `capy_execute_file` on `.env` deny and on `README.md` allow
- [ ] 13.3 `test-hooks.sh`: a `capy_execute` payload through `guard.sh` denies with the secrets reason; a benign one exits 0 with empty stdout
- [ ] 13.4 Document the channel in `docs/user-guide/configuration.md` and `docs/providers/codex.md`

## Dependency Graph

```
Task 1 ──► Task 3 ──► Task 4 ──┬──► Task 5 ────────────┐
  │                     │      │                       ├──► Task 9 ──┐
  └──────► Task 6 ◄─────┘      └──► Task 13 ──┐        │             │
Task 2 ────────────────┬──────────────────────┴► Task 8 ┤             ├──► Task 12
                       │                        ▲      │             │
Task 6 ────────────────┴────────────────────────┘      ├──► Task 10 ─┘
Task 7 ────────────────────────────────────────────────┘ (Task 10 only)
Task 6 ──► Task 11 (optional) ───────────────────────────────────────► (not gating Task 12)
```

Task 9 depends on Tasks 2, 4, 5 and 8; Task 10 on Tasks 6, 7 and 8; Task 8
on Tasks 2, 4, 6 and 13. The `Depends on` lines above are authoritative where
the drawing is ambiguous.
