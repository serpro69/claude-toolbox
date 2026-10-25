# Tasks: Permission Guard Rework

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-20
> Not Doing: context-protection rules, project-data rules, ask/mode-aware destructive decisions, project-level loosening, Grep/Glob content filtering, negation patterns, Codex read_file enforcement (optional stretch only), pre-edit backups, curl-pipe-sh rules, Windows wrapper support, deny ledger, execution channels beyond Bash/apply_patch/capy MCP tools, non-literal `cd` tracking

## Task 1: Declaration, glob matcher and file-tool secrets check
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2, Task 7
- **Slicing:** Risk-First (the glob matcher's parity with Claude Code is the most uncertain piece)
- **Docs:** [implementation.md#task-1](./implementation.md#task-1-declaration-glob-matcher-and-file-tool-secrets-check)

### Subtasks
- [ ] 1.1 Create `klaude-plugin/scripts/guard/guard-rules.json` with `version: 1` and the full baseline from design §6 (secrets, destructive, tmp_roots, selfmod); every destructive rule written in full with the frozen §6.3 vocabulary (`flags_all`/`flags_none`/ordered `subcommand` where needed); `codex` records only on `rm`, `shred`, `sudo`, `su`, `doas`, each with its own `pattern`/`match`/`not_match`
- [ ] 1.2 Create `klaude-plugin/scripts/guard/guard.py` as importable pure functions plus `main`: payload parsing into a `Context` with distinct `project_root` (`KK_GUARD_PROJECT_ROOT` → `CLAUDE_PROJECT_DIR` → payload `cwd`) and `exec_dir` (payload `cwd`), declaration loading with version check, `glob_to_regex` anchored at the project root, `resolve` against the execution directory, `check_file_tool`, decision emitter (stdout JSON + stderr + exit 2)
- [ ] 1.3 Create `test/fixtures/guard/glob-cases.json` from the docs' examples and `test/guard/test_guard.py` that loads the engine in-process and runs the glob table
- [ ] 1.4 Create `test/fixtures/guard/corpus.jsonl` with the file-tool cases (Read `.env` deny, `.env.example` allow, Grep `~/.aws` deny, symlink-to-`~/.ssh` deny, logs and build output allow, `cert.pem` deny as the accepted false positive, `id_rsa.pub` allow, `../.env` from a subdirectory `cwd` deny, Read `.env` with no config files deny) and the corpus replay in `test_guard.py`
- [ ] 1.5 Run the tests under the oldest local interpreter; note the version in the test header (floor 3.8)

## Task 2: Fail-closed wrapper and hook registration
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 1, Task 7
- **Slicing:** Contract-First (wrapper and engine agree on the exit-code and stdin contract before either is finished)
- **Docs:** [implementation.md#task-2](./implementation.md#task-2-fail-closed-wrapper-and-hook-registration)

### Subtasks
- [ ] 2.1 Create `klaude-plugin/scripts/guard/guard.sh`: single stdin read, no payload parsing (no skip path, no tool-name gate; dispatch is the engine's), interpreter list with `KK_GUARD_INTERPRETERS` override, `python3 -I guard.py`, `fail_closed` on every non-0/2 outcome
- [ ] 2.2 Update `klaude-plugin/hooks/hooks.json`: matcher `Bash|Read|Edit|Write|NotebookEdit|Grep|Glob|mcp__.+__capy_(execute|execute_file|batch_execute)`, command `${CLAUDE_PLUGIN_ROOT}/scripts/guard/guard.sh`, `timeout: 15`, `onFailure: "block"`
- [ ] 2.3 Delete `klaude-plugin/scripts/validate-bash.sh`; update `test/test-plugin-structure.sh` Section 5 to assert the `guard/` files and the `onFailure` key
- [ ] 2.4 Rewrite `test/test-hooks.sh` Sections 1–3: allow cases, deny cases (exit 2, JSON, stderr) including a Read of `.env` with no config files present (plugin-only), fail-closed cases (bad interpreter list, empty rules file, non-JSON payload); keep Section 4
- [ ] 2.5 Add the file-tool latency measurement (100 Read payloads, p95 always printed, asserted under 60 ms only when `CI` is unset) and record the measured value

## Task 3: Bash channel tokenizer, path extraction, secrets and self-modification
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 2, Task 7
- **Docs:** [implementation.md#task-3](./implementation.md#task-3-bash-channel-tokenizer-path-extraction-secrets-and-self-modification)

### Subtasks
- [ ] 3.1 Port `defang`, `strip_quotes`, `basename`, `command_position_tokens`, wrapper tables, segment/chain splitters and `substitution_bodies` into `guard.py` with attribution; use Claude Code's exact separator set; enforce the order of design §7.3: `extract_bodies` on the original text first, `defang` only for the per-segment prose view, a quote-stripped operand view for all path checks; unit-test `sh -c 'rm -rf x'`, `echo "$(rm x)"` and `cat "/repo with spaces/.env"` survive extraction
- [ ] 3.2 Implement heredoc handling before body extraction: quoted-delimiter bodies are masked from `extract_bodies` and dropped for data-sink consumers; unquoted-delimiter bodies are scanned for substitutions, then dropped for data sinks; shell/interpreter and unknown consumers keep the body; unit-test the commit-message form (including a literal `$(rm -rf x)` line) as allow, `cat <<EOF` with `$(rm -rf x)` as deny (after Task 4), a `bash <<EOF` body as kept, and the unknown-consumer case as the documented deny
- [ ] 3.3 Implement path-like operand extraction resolved against the execution directory and matched against secrets globs anchored at the project root, raw and resolved; corpus: `cat .env` deny, `cat ../.env` from `cwd: /repo/sub` deny, `cat ../README.md` from the same `cwd` allow, `cat .env.example` allow, `find . -not -path './.git/*'` allow
- [ ] 3.4 Implement mutation-operand extraction (`>`, `>>`, `tee`, `sed -i`, `dd of=`, last operand of `cp`/`install`, every operand of `mv`, `ln` link name) against selfmod (equal, descendant and ancestor matching) and secrets; corpus: redirect into `.claude/settings.json` deny, `mv .codex/hooks.json /tmp/x` deny, `mv .codex /tmp/` deny, `mv src/a.go src/b.go` allow, `cat .claude/settings.json` allow
- [ ] 3.5 Implement inline-interpreter write detection; corpus: `python3 -c "open('.claude/settings.json','w')"` deny, read form allow
- [ ] 3.6 Enable selfmod on Edit/Write/NotebookEdit and the pending corpus cases; enable the Bash deny cases in `test-hooks.sh`

## Task 4: Destructive tier with the temp exemption and wrapper recursion
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 7
- **Docs:** [implementation.md#task-4](./implementation.md#task-4-destructive-tier-with-the-temp-exemption-and-wrapper-recursion)

### Subtasks
- [ ] 4.1 Implement the rule matcher (`program`, ordered `subcommand`, `flags_any`, `flags_all`, `flags_none`) with program-level global-option skipping, against the Task 1 declaration with no new fields; unit-test `git restore f` deny vs `--staged` allow, `git branch -D`/`-rfD`/`--delete --force` deny vs `--delete`/`-d` allow, `git stash drop` deny vs `git stash list` allow, `docker volume rm` deny vs `docker volume ls` allow
- [ ] 4.2 Wire recursion over the bodies extracted in 3.1 (`sh -c`, `bash -c`, `$(...)`, backticks, `<(...)`) and the wrapped programs of `xargs`, `env`, `sudo`, `timeout`, `nohup`; corpus: `/bin/rm`, `sh -c 'rm -rf x'`, `xargs rm`, `env rm x`, `echo "$(rm x)"` all deny
- [ ] 4.3 Implement `targets_under_tmp` with `$TMPDIR` resolution and directory tracking (literal absolute `cd` updates the execution directory; any other `cd`/`pushd`/`popd`/`env -C` marks it uncertain so only absolute operands qualify); corpus: `rm -rf /tmp/kk-test` allow, `cd /tmp/kk-test && rm -rf ./x` allow, `cd /work/project && rm -rf ./work` with `cwd` under `/tmp` deny, `env -C /work/project rm -rf ./work` deny, `rm -rf "$T"` deny, `rm -rf /tmp/*` deny, `rm -rf /tmp/../etc` deny, `rm -rf ~` deny, `rm -rf .` at project root deny
- [ ] 4.4 Add corpus rows for every `git`, `infra` and `privilege` rule plus the must-allow neighbours (`git branch -d`, `git rebase`, `git commit --amend`, `git restore --staged`, `kubectl get`, `terraform plan`, `docker ps`)
- [ ] 4.5 Unit-test the destructive deny reason: names the category, the rule reason, the `!` remedy and the user config path

## Task 5: Configuration layering
- **Status:** pending
- **Depends on:** Task 4
- **Size:** M
- **Can run in parallel with:** Task 7
- **Docs:** [implementation.md#task-5](./implementation.md#task-5-configuration-layering)

### Subtasks
- [ ] 5.1 Implement project-config loading (`KK_GUARD_PROJECT_CONFIG` or `<root>/.claude/kk-guard.json`): schema check, shape lint, union merge, invalid → baseline kept plus `systemMessage`
- [ ] 5.2 Implement user-config loading (`KK_GUARD_USER_CONFIG` or `~/.claude/kk-guard.json`): union of the `*` entry and the single longest path-prefix entry for the `realpath`ed project root (shorter prefixes ignored); `disable_categories`; `allow_patterns` tested per simple command (each segment and extracted body) and exempting only that command from destructive rules; `disable_selfmod`
- [ ] 5.3 Create fixtures under `test/fixtures/guard/project-config/` and `test/fixtures/guard/user-config/`; unit tests for tighten-only enforcement, unknown-key reporting, invalid JSON, category disable scoped by path, `*` plus prefix union with an ignored intermediate prefix, `git clean -nd; rm -rf ./work` denied under `^git clean -n`, allow pattern not touching secrets or selfmod, `disable_selfmod`
- [ ] 5.4 Emit `{"systemMessage": ...}` as the only stdout key on allowed calls when a config was invalid; assert the field and the absence of `hookSpecificOutput` in `test-hooks.sh`
- [ ] 5.5 Wrapper test: with `KK_GUARD_PROJECT_CONFIG` pointing at a fixture that adds a secrets glob, a matching Read is denied through `guard.sh`; with the override pointing at a nonexistent file, the same Read is allowed

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
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6
- **Docs:** [implementation.md#task-7](./implementation.md#task-7-template-sync-deny-replacement-and-dropped-entry-report)

### Subtasks
- [ ] 7.1 In `template-sync.sh` settings merge: compute `DROPPED_DENY_ENTRIES`, then set `.permissions.deny` to upstream's array; keep `allow` unioned; test "deny replaced, allow unioned"
- [ ] 7.2 Add the "Permission deny entries removed" section to the diff report and markdown summary with the guidance text; add `dropped_deny_count` CI output; tests for present and absent cases
- [ ] 7.3 Add `.claude/kk-guard.json` to `BUILTIN_EXCLUSIONS` and strip it in `fetch_upstream_templates`; test zero deleted files when only downstream has it
- [ ] 7.4 Update `docs/user-guide/template-sync.md` merge-behavior section

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
