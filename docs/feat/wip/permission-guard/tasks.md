# Tasks: Permission Guard Rework

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-20
> Not Doing: context-protection rules, project-data rules, ask/mode-aware destructive decisions, project-level loosening, Grep/Glob content filtering, negation patterns, Codex read_file enforcement (optional stretch only), pre-edit backups, curl-pipe-sh rules, Windows wrapper support, deny ledger

## Task 1: Declaration, glob matcher and file-tool secrets check
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2, Task 7
- **Slicing:** Risk-First (the glob matcher's parity with Claude Code is the most uncertain piece)
- **Docs:** [implementation.md#task-1](./implementation.md#task-1-declaration-glob-matcher-and-file-tool-secrets-check)

### Subtasks
- [ ] 1.1 Create `klaude-plugin/scripts/guard/guard-rules.json` with `version: 1` and the full baseline from design §6 (secrets, destructive, tmp_roots, selfmod)
- [ ] 1.2 Create `klaude-plugin/scripts/guard/guard.py` as importable pure functions plus `main`: payload parsing, declaration loading with version check, `glob_to_regex`, `resolve`, `check_file_tool`, decision emitter (stdout JSON + stderr + exit 2)
- [ ] 1.3 Create `test/fixtures/guard/glob-cases.json` from the docs' examples and `test/guard/test_guard.py` that loads the engine in-process and runs the glob table
- [ ] 1.4 Create `test/fixtures/guard/corpus.jsonl` with the file-tool cases (Read `.env` deny, `.env.example` allow, Grep `~/.aws` deny, symlink-to-`~/.ssh` deny, logs and build output allow) and the corpus replay in `test_guard.py`
- [ ] 1.5 Run the tests under the oldest local interpreter; note the version in the test header (floor 3.8)

## Task 2: Fail-closed wrapper and hook registration
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 1, Task 7
- **Slicing:** Contract-First (wrapper and engine agree on the exit-code and stdin contract before either is finished)
- **Docs:** [implementation.md#task-2](./implementation.md#task-2-fail-closed-wrapper-and-hook-registration)

### Subtasks
- [ ] 2.1 Create `klaude-plugin/scripts/guard/guard.sh`: single stdin read, `tool_name` via parameter expansion, Read/Grep/Glob skip path when no project or user config exists, interpreter list with `KK_GUARD_INTERPRETERS` override, `python3 -I guard.py`, `fail_closed` on every non-0/2 outcome
- [ ] 2.2 Update `klaude-plugin/hooks/hooks.json`: matcher `Bash|Read|Edit|Write|NotebookEdit|Grep|Glob`, command `${CLAUDE_PLUGIN_ROOT}/scripts/guard/guard.sh`, `timeout: 15`, `onFailure: "block"`
- [ ] 2.3 Delete `klaude-plugin/scripts/validate-bash.sh`; update `test/test-plugin-structure.sh` Section 5 to assert the `guard/` files and the `onFailure` key
- [ ] 2.4 Rewrite `test/test-hooks.sh` Sections 1–3: allow cases, deny cases (exit 2, JSON, stderr), fail-closed cases (bad interpreter list, empty rules file, non-JSON payload); keep Section 4
- [ ] 2.5 Add the skip-path latency assertion (100 Read payloads under 200 ms) and record the measured total

## Task 3: Bash channel tokenizer, path extraction, secrets and self-modification
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 2, Task 7
- **Docs:** [implementation.md#task-3](./implementation.md#task-3-bash-channel-tokenizer-path-extraction-secrets-and-self-modification)

### Subtasks
- [ ] 3.1 Port `defang`, `strip_quotes`, `basename`, `command_position_tokens`, wrapper tables, segment/chain splitters and `substitution_bodies` into `guard.py` with attribution; use Claude Code's exact separator set
- [ ] 3.2 Implement heredoc stripping for data-sink consumers only; unit-test the commit-message form as allow and a `bash <<EOF` body as kept
- [ ] 3.3 Implement path-like argument extraction and secrets matching on raw and resolved paths; corpus: `cat .env` deny, `cat .env.example` allow, `find . -not -path './.git/*'` allow
- [ ] 3.4 Implement write-target extraction (`>`, `>>`, `tee`, `sed -i`, `mv`/`cp`/`ln`/`install`, `dd of=`) against selfmod and secrets; corpus: redirect into `.claude/settings.json` deny, `cat .claude/settings.json` allow
- [ ] 3.5 Implement inline-interpreter write detection; corpus: `python3 -c "open('.claude/settings.json','w')"` deny, read form allow
- [ ] 3.6 Enable selfmod on Edit/Write/NotebookEdit and the pending corpus cases; enable the Bash deny cases in `test-hooks.sh`

## Task 4: Destructive tier with the temp exemption and wrapper recursion
- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 7
- **Docs:** [implementation.md#task-4](./implementation.md#task-4-destructive-tier-with-the-temp-exemption-and-wrapper-recursion)

### Subtasks
- [ ] 4.1 Implement the rule matcher (`program`, `subcommand`, `flags_any`) with git global-option skipping
- [ ] 4.2 Implement recursion into `sh -c`, `bash -c`, `xargs`, `env`, `sudo`, `timeout`, `nohup`, `$(...)`, backticks, `<(...)`; corpus: `/bin/rm`, `sh -c 'rm -rf x'`, `xargs rm`, `env rm x`, `echo $(rm x)` all deny
- [ ] 4.3 Implement `targets_under_tmp` with `$TMPDIR` resolution; corpus: `rm -rf /tmp/kk-test` allow, `rm -rf "$T"` deny, `rm -rf /tmp/*` deny, `rm -rf /tmp/../etc` deny, `rm -rf ~` deny, `rm -rf .` at project root deny
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
- [ ] 5.2 Implement user-config loading (`KK_GUARD_USER_CONFIG` or `~/.claude/kk-guard.json`): `*` entry plus longest path-prefix match on the `realpath`ed project root; `disable_categories`, `allow_patterns` (destructive only), `disable_selfmod`
- [ ] 5.3 Create fixtures under `test/fixtures/guard/project-config/` and `test/fixtures/guard/user-config/`; unit tests for tighten-only enforcement, unknown-key reporting, invalid JSON, category disable scoped by path, allow pattern not touching secrets or selfmod, `disable_selfmod`
- [ ] 5.4 Emit `systemMessage` on allowed calls when a config was invalid; assert the field in `test-hooks.sh`
- [ ] 5.5 Wrapper test: with a project config present, a Read payload reaches the engine and an added glob is denied

## Task 6: Generators, parity and freshness
- **Status:** pending
- **Depends on:** Task 1, Task 4
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7
- **Docs:** [implementation.md#task-6](./implementation.md#task-6-generators-parity-and-freshness)

### Subtasks
- [ ] 6.1 Create `scripts/generate-guard.sh`: settings `permissions.deny` projection via `jq` in place, `default.rules` rendering with generated header, engine copy to `.codex/scripts/guard/`, docs table between `GUARD-RULES` markers in `docs/user-guide/configuration.md`
- [ ] 6.2 Fill `codex.prefix`/`match`/`not_match` for every destructive rule in `guard-rules.json`; validate with `codex execpolicy check` when the CLI is available
- [ ] 6.3 Add `generate-guard` to the Makefile and `generate-all`; add the freshness `git diff --exit-code` step to CI beside generate-kodex
- [ ] 6.4 Structure-test assertions: secrets shape lint, regenerate-and-diff, `cmp` of Codex copies, generated header in `default.rules`
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
- **Depends on:** Task 2, Task 4, Task 6
- **Size:** M
- **Can run in parallel with:** Task 5
- **Docs:** [implementation.md#task-8](./implementation.md#task-8-codex-adapter)

### Subtasks
- [ ] 8.1 Implement `apply_patch` handling in `guard.py` (header parsing, `cwd` resolution, secrets and selfmod, `Delete File` as filesystem-destructive); regenerate the Codex copy; corpus cases
- [ ] 8.2 Rewrite `.codex/scripts/pretooluse-bash.sh`: keep capy detection and HTTP section, replace the denylist loop with delegation to `guard.sh`, trap failures to stderr + exit 2; update `test-codex-hooks.sh` denylist assertions
- [ ] 8.3 Create `.codex/scripts/pretooluse-patch.sh` and the `Edit|Write` PreToolUse entry in `.codex/hooks.json`; tests in `test-codex-hooks.sh` and `test-codex-structure.sh`
- [ ] 8.4 Fail-open mitigation test: bad interpreter list → both adapters exit 2 with stderr
- [ ] 8.5 `session-start.sh`: render the protected-files paragraph from the synced declaration with `jq`; assert in both legacy and capy modes
- [ ] 8.6 Update `docs/providers/codex.md` with hook descriptions and the parity-gap table

## Task 9: Assumption closure for latency, bypass mode and Codex cwd
- **Status:** pending
- **Depends on:** Task 2, Task 4, Task 5, Task 8
- **Size:** S
- **Can run in parallel with:** Task 10
- **Docs:** [implementation.md#task-9](./implementation.md#task-9-assumption-closure-for-latency-bypass-mode-and-codex-cwd)

### Subtasks
- [ ] 9.1 Add the Bash-path p95 latency test (fail beyond 100 ms); record the measured value
- [ ] 9.2 Run the throwaway bypass-mode check in a scratch project; record date, version and outcome in design §16
- [ ] 9.3 Run the Codex `apply_patch` relative-path check; record date, version and outcome in design §16

## Task 10: Documentation, ADR and version bump
- **Status:** pending
- **Depends on:** Task 6, Task 7, Task 8
- **Size:** M
- **Can run in parallel with:** Task 9
- **Docs:** [implementation.md#task-10](./implementation.md#task-10-documentation-adr-and-version-bump)

### Subtasks
- [ ] 10.1 Write `docs/adr/0010-permission-guard-single-declaration.md` (Context, Decision, Consequences with rejected alternatives, Codex gaps, revisit conditions)
- [ ] 10.2 Add the dated update to ADR 0005; add the 0010 row to `docs/contributing/adrs.md`; ask the user before adding the missing 0008/0009 rows
- [ ] 10.3 Update `docs/user-guide/configuration.md` prose and hooks table plus the new config subsection; `docs/providers/claude-code.md`; `docs/getting-started/plugin-only.md`
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
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 12.1 Run `/kk:test` to verify all tasks: full bash suites, Python tests, corpus, latency
- [ ] 12.2 Run `/kk:document` to update any relevant docs
- [ ] 12.3 Run `/kk:review-code` with bash and Python as the project languages
- [ ] 12.4 Run `/kk:review-spec` to verify the implementation matches design.md and implementation.md

## Dependency Graph

```
Task 1 ──► Task 3 ──► Task 4 ──► Task 5 ──┐
  │                     │                 ├──► Task 9 ──┐
  └──────► Task 6 ◄─────┘                 │             │
Task 2 ────────────────┬──────► Task 8 ───┤             ├──► Task 12
                       │          ▲        │             │
Task 6 ────────────────┴──────────┘        ├──► Task 10 ─┘
Task 7 ────────────────────────────────────┘
Task 6 ──► Task 11 (optional) ─────────────────────────► (not gating Task 12)
```
