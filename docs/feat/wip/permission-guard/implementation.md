# Implementation Plan: Permission Guard Rework

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)
> Created: 2026-10-20

This plan is written for an experienced bash and Python developer with no
context on this repository. Every step names how to know it worked.

## Repository orientation

- `klaude-plugin/` is the canonical plugin; it ships standalone through the
  Claude Code marketplace. Hook registration lives in
  `klaude-plugin/hooks/hooks.json`; hook scripts in `klaude-plugin/scripts/`.
  The existing `set-plugin-root.sh` plus `cpr.py` pair is the precedent for a
  bash entry point delegating to Python.
- `.claude/` and `.codex/` are the template trees that `template-sync.sh`
  (under `.claude/toolbox/scripts/`) delivers to downstream repositories.
- `test/` holds bash suites built on `test/helpers.sh` (`log_test`,
  `assert_equals`, `assert_json_valid`, `assert_json_field`,
  `create_temp_dir`, `print_summary`). `test/test-cpr.sh` shows how a suite
  drives a Python script with env-var overrides. Run everything with
  `for t in test/test-*.sh; do $t; done`.
- Generators follow `make generate-kodex`: a make target regenerates output,
  CI checks `git diff --exit-code`.
- Plugin files must not reference ADRs or `docs/` paths; state rules in full
  inside the plugin file.
- Python floor is 3.8: no `match` statements, no `X | Y` type unions at
  runtime, no `str.removeprefix`.

## Task 1: Declaration, glob matcher and file-tool secrets check

**Goal.** The engine denies a Read, Edit, Write, NotebookEdit, Grep or Glob
call whose path matches a baseline secrets glob, and allows everything else.

**Files.**
- `klaude-plugin/scripts/guard/guard-rules.json` (new)
- `klaude-plugin/scripts/guard/guard.py` (new)
- `test/guard/test_guard.py` (new)
- `test/fixtures/guard/corpus.jsonl` (new)
- `test/fixtures/guard/glob-cases.json` (new)

**Steps.**

1. Write `guard-rules.json` with `version: 1` and the full baseline from
   design §6 (secrets, destructive, tmp_roots, selfmod). Destructive rules
   are data only in this task; the engine ignores them until Task 4.
   → verify: `jq . guard-rules.json` succeeds; every `secrets` entry starts
   with `./**/`, `~/` or `//`.
2. In `guard.py`, structure the module as pure functions plus a thin `main`
   so tests import it in-process (the safe-claude-code `test_guard.py`
   pattern: load via `importlib`, call `check_*` functions, assert a raised
   `Denied` exception or a return). Sections: payload parsing, declaration
   loading with version check, glob translation, path resolution, file-tool
   dispatch, decision emitter.
3. Implement `glob_to_regex(pattern, anchor_cwd, home)` per design §7.4.
   Return a compiled regex that matches absolute paths. Write
   `glob-cases.json` from the docs' examples: `./**/.env` matches
   `<cwd>/a/b/.env` and not `<parent>/.env`; `~/.ssh/**` matches
   `<home>/.ssh/id_rsa`; `//etc/**` matches `/etc/passwd`; `*` does not cross
   `/`; a bare `.env` matches at any depth under cwd.
   → verify: `python3 -I test/guard/test_guard.py` runs the glob table green.
4. Implement `resolve(path, cwd)`: expand `~`, join relative paths onto
   `cwd`, `os.path.realpath`. Return both the normalised requested path and
   the resolved path.
5. Implement `check_file_tool(tool_name, tool_input, cwd, policy)`: pick
   `file_path`, `notebook_path` or `path`; deny if either requested or
   resolved path matches any secrets glob. Grep and Glob with no `path` are
   allowed.
6. Implement the emitter: build the reason string in the `kk guard:
   <category> — <what>. Way through: <remedy>` format (design §7.5), print
   JSON to stdout, the same text to stderr, exit 2. Allowed calls print
   nothing and exit 0.
7. Implement `main`: read stdin, parse JSON (invalid JSON denies with the
   `failure` remedy), dispatch file tools, ignore Bash for now (allow).
8. Add corpus cases for file tools: Read `/repo/.env` deny; Read
   `/repo/.env.example` allow; Edit `~/.claude/settings.json` allow in this
   task (selfmod arrives in Task 3) — mark with a `pending_task: 3` field the
   runner skips; Grep with `path: ~/.aws` deny; Read of a symlink under `/tmp`
   that resolves to `~/.ssh/id_rsa` deny; Read of `/repo/build/out.txt`
   allow; Read `/repo/app.log` allow.
   → verify: corpus replay in `test_guard.py` passes for all cases without
   `pending_task`.
9. Guard against Python-version drift: run the tests once under the oldest
   interpreter available locally and note the version in the test header.
   → verify: no syntax errors under that interpreter.

## Task 2: Fail-closed wrapper and hook registration

**Goal.** The hook is wired for all channels through a wrapper that is
sub-millisecond on the skip path and fails closed everywhere else.

**Files.**
- `klaude-plugin/scripts/guard/guard.sh` (new)
- `klaude-plugin/hooks/hooks.json`
- `klaude-plugin/scripts/validate-bash.sh` (delete)
- `test/test-hooks.sh` (rewrite Sections 1–3; keep Section 4 capy test)
- `test/test-plugin-structure.sh` (Section 5 assertions)

**Steps.**

1. Write `guard.sh` modelled on safe-claude-code's `guard.sh`: read stdin
   once with the trailing-`x` trick; extract `tool_name` with parameter
   expansion on the raw JSON (`${payload#*\"tool_name\"}` style, tolerant of
   whitespace); skip path for Read, Grep, Glob when
   `${CLAUDE_PROJECT_DIR:-$PWD}/.claude/kk-guard.json` and
   `${HOME}/.claude/kk-guard.json` are both absent (honour
   `KK_GUARD_PROJECT_CONFIG`/`KK_GUARD_USER_CONFIG` overrides); interpreter
   list from `KK_GUARD_INTERPRETERS` or the default absolute list plus `PATH`
   fallback; run `python3 -I guard.py`; any outcome other than exit 0 or 2
   → `fail_closed` which writes stderr, prints a JSON deny, exits 2.
   → verify: `printf '{"tool_name":"Read","tool_input":{"file_path":"/x"}}' | bash guard.sh; echo $?` prints 0 with no output when no configs exist.
2. Update `hooks.json`: matcher `Bash|Read|Edit|Write|NotebookEdit|Grep|Glob`,
   command `${CLAUDE_PLUGIN_ROOT}/scripts/guard/guard.sh`, `"timeout": 15`,
   `"onFailure": "block"`. Keep the SessionStart entry untouched.
   → verify: `jq . hooks.json` succeeds; structure test still finds
   `CLAUDE_PLUGIN_ROOT`.
3. Delete `validate-bash.sh`. Update `test-plugin-structure.sh` Section 5 to
   assert `guard.sh` exists and is executable, `guard.py` exists,
   `guard-rules.json` is valid JSON, and `hooks.json` contains `onFailure`.
   → verify: `bash test/test-plugin-structure.sh` green.
4. Rewrite `test-hooks.sh`: allow cases (exit 0, empty stdout) for `ls /tmp`,
   `cat app.log`, `cat node_modules/foo`, `cat build/out.txt`; deny cases
   (exit 2, valid JSON, `permissionDecision` deny, non-empty stderr) for
   `cat .env` and a Read of `.env`; fail-closed cases: `KK_GUARD_INTERPRETERS=/nonexistent` → exit 2 with stderr mentioning the interpreter;
   `KK_GUARD_RULES=/dev/null` → exit 2; a payload that is not JSON → exit 2.
   Note that the Bash deny cases in this task pass only after Task 3; mark
   them with a comment and a skip until then, or land Task 3 before enabling.
   → verify: `bash test/test-hooks.sh` green for the enabled cases.
5. Add the skip-path latency check: time 100 Read payloads through `guard.sh`
   with `date +%s%N`; assert total under 200 ms (twice the 100 ms budget).
   → verify: the printed total on your machine; record it in the test
   comment.

## Task 3: Bash channel tokenizer, path extraction, secrets and self-modification

**Goal.** `cat .env`, `/bin/cat ./.env`, `sh -c 'cat .env'`, redirects into
settings files and inline interpreter writes to protected files are denied;
the false-positive corpus is allowed.

**Files.**
- `klaude-plugin/scripts/guard/guard.py`
- `test/guard/test_guard.py`
- `test/fixtures/guard/corpus.jsonl`

**Steps.**

1. Port the tokenizer pieces from safe-claude-code's `guard.py` with
   attribution in a module docstring (no ADR references): `defang`,
   `strip_quotes`, `basename`, `command_position_tokens`, wrapper tables
   (`WRAPPERS`, `WRAPPER_OPTIONS_WITH_ARG`, `WRAPPER_POSITIONAL`), the
   segment and chain splitters, and `substitution_bodies`. Extend the segment
   separators to the exact Claude Code set: `&&`, `||`, `;`, `|`, `|&`, `&`,
   newline.
2. Implement heredoc stripping (design §7.3 step 1): detect `<<[-]'?WORD'?`,
   find the terminator line, and drop the body only when the heredoc's
   consumer program is `cat`, `tee`, `printf` or a plain redirect. Keep the
   body when the consumer is a shell or interpreter.
   → verify: unit test with Claude Code's commit-message form
   (`git commit -m "$(cat <<'EOF' ... EOF)"`) allowed even when a body line
   starts with `rm -rf`; `bash <<'EOF'\nrm -rf x\nEOF` denied after Task 4.
3. Implement path-like argument extraction per segment: tokens containing
   `/`, starting with `~` or `.`, or naming an existing file relative to
   `cwd`. Resolve each and check raw and resolved against secrets globs.
   → verify: corpus `cat .env` deny; `cat ./.env` deny; `cat /repo/.env`
   deny; `cat .env.example` allow; `echo "see .env.example"` allow; `find .
   -not -path './.git/*'` allow.
4. Implement write-target extraction: `>`/`>>` targets (ignoring `2>`,
   `&>` to `/dev/null`), `tee` operands, `sed -i` file operands, the last
   operand of `mv`/`cp`/`ln`/`install`, `dd of=`. Check against the selfmod
   set and the secrets globs. Writing a secrets file is denied too, matching
   Claude Code where a Read deny blocks Edit and Write.
   → verify: corpus `echo x > .claude/settings.json` deny;
   `tee .claude/kk-guard.json` deny; `sed -i 's/a/b/' ~/.claude/kk-guard.json`
   deny; `cat .claude/settings.json` allow (read, not write);
   `echo x 2>/dev/null` allow.
5. Implement inline-interpreter write detection: when a segment runs an
   interpreter with `-c`/`-e` or a stdin script, scan the code text for the
   write-call patterns in design §7.3 step 5 whose argument text contains a
   protected path.
   → verify: corpus `python3 -c "open('.claude/settings.json','w')"` deny;
   `python3 -c "open('.claude/settings.json').read()"` allow.
6. Enable the self-modification check on Edit, Write and NotebookEdit in the
   file-tool path (the `pending_task: 3` cases from Task 1).
   → verify: full corpus replay green for all cases without `pending_task`.
7. Enable the Bash deny cases in `test-hooks.sh`.
   → verify: `bash test/test-hooks.sh` green.

## Task 4: Destructive tier with the temp exemption and wrapper recursion

**Goal.** Every destructive rule in the declaration denies in all its
evasion forms; `rm` under a temp root is allowed; git and infra read-only
commands are allowed.

**Files.**
- `klaude-plugin/scripts/guard/guard.py`
- `klaude-plugin/scripts/guard/guard-rules.json` (only if a rule needs a
  field the engine cannot express; prefer not to touch)
- `test/guard/test_guard.py`
- `test/fixtures/guard/corpus.jsonl`

**Steps.**

1. Implement the rule matcher: for each segment, after wrapper skipping,
   compare the program basename to `program`; if `subcommand` is set, the
   first non-option argument must equal it; if `flags_any` is set, at least
   one argument must match one regex. Git global options (`-C dir`, `-c k=v`,
   `--git-dir`) are skipped before the subcommand, as in safe-claude-code's
   `GIT` prefix.
2. Implement recursion into `sh -c`/`bash -c` bodies, `xargs <prog>`,
   `env <prog>`, `sudo <prog>` (sudo itself denies first), `timeout N <prog>`,
   `nohup <prog>`, `$(...)`, backticks, `<(...)`.
   → verify: corpus `/bin/rm -rf build` deny; `sh -c 'rm -rf x'` deny;
   `xargs rm` deny; `env rm x` deny; `timeout 5 rm x` deny;
   `echo $(rm x)` deny.
3. Implement `targets_under_tmp`: resolve every non-option argument of the
   segment; allow only if all resolve under a `tmp_roots` entry (with
   `$TMPDIR` read from the engine's environment and `realpath`ed); any
   argument containing `$`, `*`, `?` or `[` denies; `rm -rf /tmp/../home`
   resolves out of `/tmp` and denies.
   → verify: corpus `rm -rf /tmp/kk-test` allow; `rm /tmp/a /tmp/b` allow;
   `rm -rf "$T"` deny; `rm -rf /tmp/*` deny; `rm -rf /tmp/../etc` deny;
   `rm -rf ~` deny; `rm -rf /` deny; `rm -rf .` with `cwd` at the project
   root deny.
4. Add the remaining corpus rows for every rule in `git`, `infra`,
   `privilege` plus the must-allow neighbours: `git branch -d x`,
   `git rebase main`, `git commit --amend`, `git restore --staged f`,
   `git push origin main`, `git stash list`, `kubectl get pods`,
   `terraform plan`, `helm list`, `docker ps`.
   → verify: full corpus replay green.
5. Confirm the deny reason names the category and the rule's `reason`, and
   the destructive remedy names the category and the user config path.
   → verify: unit test on the emitted string.

## Task 5: Configuration layering

**Goal.** A project file tightens, a user file loosens, invalid files are
reported without weakening anything.

**Files.**
- `klaude-plugin/scripts/guard/guard.py`
- `klaude-plugin/scripts/guard/guard.sh` (skip-path config detection already
  present; confirm env overrides)
- `test/guard/test_guard.py`
- `test/fixtures/guard/project-config/*.json`, `test/fixtures/guard/user-config/*.json` (new)
- `test/test-hooks.sh`

**Steps.**

1. Implement project-config loading per design §8.1: path from
   `KK_GUARD_PROJECT_CONFIG` or `<project root>/.claude/kk-guard.json`;
   schema check (`version`, optional `secrets`, `destructive`, `selfmod`;
   nothing else); shape lint on added secrets; merge as unions. On any error:
   keep baseline, record a `systemMessage`.
   → verify: fixture with an extra secrets glob denies a Read of that file;
   fixture with a `disable_categories` key is ignored with a `systemMessage`
   naming the unknown key; fixture with invalid JSON leaves `cat .env` denied
   and returns a `systemMessage`.
2. Implement user-config loading per design §8.2: path from
   `KK_GUARD_USER_CONFIG` or `~/.claude/kk-guard.json`; apply `*` then the
   longest key that is a path prefix of the `realpath`ed project root;
   `disable_categories`, `allow_patterns`, `disable_selfmod`.
   → verify: fixture disabling `infra` for `/work/ops` allows
   `kubectl delete pod x` with `cwd=/work/ops/cluster-a` and still denies it
   with `cwd=/work/app`; `allow_patterns: ["^git clean -n"]` allows the
   dry-run and still denies `git clean -fd`; `allow_patterns` never allows
   `cat .env` or a write to `.claude/settings.json`; `disable_selfmod: true`
   allows an Edit of `.claude/settings.json`.
3. Emit `systemMessage` on allowed calls when a config was invalid: top-level
   key in the stdout JSON alongside an otherwise empty `hookSpecificOutput`.
   → verify: stdout is valid JSON and `test-hooks.sh` asserts the field.
4. Add wrapper tests: with `KK_GUARD_PROJECT_CONFIG` pointing at a fixture,
   a Read payload reaches the engine (no skip) and a Read of the extra glob
   is denied.
   → verify: `bash test/test-hooks.sh` green.

## Task 6: Generators, parity and freshness

**Goal.** Settings deny, Codex rules, the Codex engine copy and the docs
table render from the declaration, and CI refuses drift.

**Files.**
- `scripts/generate-guard.sh` (new)
- `Makefile` (`generate-guard` target; add to `generate-all`)
- `.github/workflows/*.yml` (the job that runs `make generate-kodex` freshness; add the guard check beside it)
- `.claude/settings.json` (generated `permissions.deny`)
- `.codex/rules/default.rules` (generated)
- `.codex/scripts/guard/` (generated copies)
- `docs/user-guide/configuration.md` (marker block)
- `test/test-plugin-structure.sh`, `test/test-codex-structure.sh`
- `AGENTS.md` (generated-files list, make target)

**Steps.**

1. Write `generate-guard.sh`: read the declaration with `jq`; (a) set
   `.permissions.deny` in `.claude/settings.json` to the sorted
   `Read(<glob>)` list using `jq` in place so key order is preserved and
   2-space indentation matches; (b) render `default.rules` with a header
   comment "GENERATED by scripts/generate-guard.sh from
   klaude-plugin/scripts/guard/guard-rules.json — do not edit" followed by
   one `prefix_rule(...)` per entry in each rule's `codex.prefix`, using the
   rule's `codex.match`/`codex.not_match` and `reason`; (c) `cp` the three
   engine files to `.codex/scripts/guard/`; (d) replace the block between
   the `GUARD-RULES` markers in `configuration.md` with a table of secrets
   globs and a table of destructive categories and rules.
   → verify: run twice; the second run produces no diff (`git diff --stat`
   empty).
2. Populate `codex.prefix`/`match`/`not_match` for every destructive rule in
   the declaration so the Starlark output is valid. For `rm` the prefix is
   `["rm"]`; for `git push --force` include both `["git","push","--force"]`
   and `["git","push","-f"]`, and so on. `match` examples must match the
   prefix; `not_match` examples must not.
   → verify: if the `codex` CLI is installed,
   `codex execpolicy check --pretty --rules .codex/rules/default.rules -- rm -rf x`
   reports forbidden; otherwise skip and note it.
3. Add `generate-guard` to the Makefile and to `generate-all`; add the
   freshness step to CI next to the generate-kodex one:
   `make generate-guard && git diff --exit-code .claude/settings.json .codex/rules .codex/scripts/guard docs/user-guide/configuration.md`.
   → verify: CI job definition parses; local `make generate-guard` succeeds.
4. Structure-test assertions: every secrets glob matches
   `^(\./\*\*/|~/|//)`; regenerate into a temp copy and diff against the
   tree; `cmp` each `.codex/scripts/guard/*` with its plugin source;
   `default.rules` starts with the generated header.
   → verify: `bash test/test-plugin-structure.sh` and
   `bash test/test-codex-structure.sh` green.
5. Update `AGENTS.md`: move `.codex/rules/default.rules` to the generated
   list, add `.codex/scripts/guard/` as generated, document
   `make generate-guard` next to `make generate-kodex`.
   → verify: read-through; no stale "hand-authored" claim remains.

## Task 7: Template sync deny replacement and dropped-entry report

**Goal.** A downstream sync replaces `permissions.deny`, reports what it
dropped, and never touches `.claude/kk-guard.json`.

**Files.**
- `.claude/toolbox/scripts/template-sync.sh`
- `test/test-template-sync.sh`
- `docs/user-guide/template-sync.md`

**Steps.**

1. In the settings smart-merge block (around line 1453), after
   `smart_merge`, compute `DROPPED_DENY_ENTRIES` as downstream deny minus
   upstream deny, then set `.permissions.deny = $upstream[0].permissions.deny`.
   Keep `allow` union-merged.
   → verify: new test "deny replaced, allow unioned": downstream has
   `Read(*.log)` and `Bash(go test *)` in deny/allow; after
   `apply_substitutions` the output deny equals upstream's and allow contains
   both entries.
2. Report: add a "Permission deny entries removed" section to
   `generate_diff_report` and `generate_markdown_summary` listing the
   dropped entries with the guidance text from design §10; add
   `dropped_deny_count` to the CI outputs.
   → verify: new test asserts the markdown summary contains the entry name
   and the guidance line when entries were dropped, and omits the section
   when none were.
3. Add `.claude/kk-guard.json` to `BUILTIN_EXCLUSIONS` and strip it in
   `fetch_upstream_templates`.
   → verify: new test: a project with `.claude/kk-guard.json` and no such
   file upstream reports zero deleted files.
4. Update `template-sync.md` §"settings.json merge behavior": `deny` is
   replaced; dropped entries appear in the PR summary; `sync_exclusions` is
   the opt-out.
   → verify: read-through.

## Task 8: Codex adapter

**Goal.** Codex Bash and `apply_patch` calls are guarded by the shared
engine; failures block; the session advisory lists the current secrets.

**Files.**
- `.codex/scripts/pretooluse-bash.sh`
- `.codex/scripts/pretooluse-patch.sh` (new)
- `.codex/hooks.json`
- `.codex/scripts/session-start.sh`
- `klaude-plugin/scripts/guard/guard.py` (apply_patch parsing; regenerate the copy)
- `test/test-codex-hooks.sh`, `test/test-codex-structure.sh`

**Steps.**

1. Implement `apply_patch` handling in the engine per design §7.2: parse the
   four header kinds, resolve against `cwd`, run secrets and selfmod checks,
   treat `Delete File` as `filesystem`-destructive with the temp exemption.
   Regenerate the Codex copy.
   → verify: corpus `apply_patch` cases: Update `.env` deny; Update
   `src/main.go` allow; Delete `/tmp/x` allow; Delete `src/old.go` deny;
   Update `.codex/hooks.json` deny.
2. Rewrite `pretooluse-bash.sh`: keep `capy_hook_registered` and the HTTP
   section; replace the `FORBIDDEN_PATTERNS` loop with
   `printf '%s' "$INPUT" | bash "$REPO_ROOT/.codex/scripts/guard/guard.sh"`;
   propagate exit 2 and stderr; wrap the whole script so any unexpected
   failure writes stderr and exits 2.
   → verify: `test-codex-hooks.sh` Section 3/4 denylist cases now assert
   exit 2, JSON deny and a reason containing `kk guard`; capy handoff cases
   unchanged and green.
3. Add `pretooluse-patch.sh` (same delegation, no HTTP section) and the
   `hooks.json` entry with matcher `Edit|Write` running it.
   → verify: new tests feed an `apply_patch` payload updating `.env` and one
   updating `src/a.py`; first denies, second allows; `test-codex-structure.sh`
   asserts the entry exists.
4. Fail-open mitigation test: point `KK_GUARD_INTERPRETERS` at a nonexistent
   path and confirm both adapter scripts exit 2 with non-empty stderr.
   → verify: assertions green.
5. `session-start.sh`: render a "Protected files" paragraph from
   `.codex/scripts/guard/guard-rules.json` with `jq` (fall back to a static
   sentence if the file is missing) stating that reading these paths is
   prohibited by policy.
   → verify: `test-codex-hooks.sh` Section 1/2 assert the paragraph lists
   `.env` in both legacy and capy modes.
6. Update `docs/providers/codex.md`: hook descriptions, the parity-gap table
   from design §11.
   → verify: read-through.

## Task 9: Assumption closure for latency, bypass mode and Codex cwd

**Goal.** The three unverified runtime assumptions are measured or observed
and recorded.

**Files.**
- `test/test-hooks.sh` (Bash-path latency)
- `docs/feat/wip/permission-guard/design.md` §16 (record results)

**Steps.**

1. Add the Bash-path latency test: run the corpus's Bash cases through
   `guard.sh`, compute p95, assert under 100 ms (twice the 50 ms budget),
   print the measured value.
   → verify: printed p95 on Linux; if a macOS machine is available, record
   that too.
2. Throwaway bypass check: in a scratch directory with the plugin installed,
   start Claude Code with the bypass flag and ask it to run `rm -rf ./scratch`
   and `cat .env`; confirm both are denied and the reason text appears.
   → verify: record date, Claude Code version and outcome in design §16.
3. Codex `cwd` check: in a Codex session on a scratch repo, trigger an
   `apply_patch` to a relative path and confirm the hook resolves it against
   `cwd` (deny on `.env`, allow on `src/a.py`).
   → verify: record date, Codex version and outcome in design §16.

## Task 10: Documentation, ADR and version bump

**Goal.** Every page that describes the old guard describes the new one;
the decisions are recorded as an ADR.

**Files.**
- `docs/adr/0010-permission-guard-single-declaration.md` (new)
- `docs/adr/0005-codex-hook-enforcement-gap.md` (dated update)
- `docs/contributing/adrs.md`
- `docs/user-guide/configuration.md` (prose around the generated block; hooks table; new config subsection)
- `docs/providers/claude-code.md`
- `docs/getting-started/plugin-only.md`
- `docs/contributing/plugin-development.md`, `docs/contributing/testing.md`, `docs/contributing/architecture.md`
- `klaude-plugin/README.md`
- `klaude-plugin/.claude-plugin/plugin.json` (minor version bump)

**Steps.**

1. Write ADR 0010 with Nygard's sections. Context: the add-only merge
   (commit `3b08e134`), substring false positives, three intents. Decision:
   one declaration rendered to three channels; tighten-only project config,
   loosen-only user config; flat deny for destructive commands in every
   mode. Consequences: rejected alternatives (design §18), Codex gaps (design
   §11), revisit conditions (flat deny too restrictive → mode-aware ask using
   `permission_mode`). Cite operative files by path.
   → verify: `plugin-graph validate` still passes (no plugin file links to
   the ADR).
2. Add the dated update to ADR 0005. Add the 0010 row to `adrs.md`. The
   index lacks 0008 and 0009 rows; ask the user before adding them.
3. Update the user guide, provider pages, plugin-only page, contributing
   pages, plugin README per design §15. In `plugin-development.md`, replace
   the "Always exit 0" PreToolUse paragraph with the fail-closed contract and
   add the toolbox-repo `disable_selfmod` note.
   → verify: `grep -rn "validate-bash" docs/ klaude-plugin/ AGENTS.md` returns
   only historical references under `docs/feat/done/`.
4. Bump `plugin.json` to the next minor version.
   → verify: `bash test/test-plugin-structure.sh` green.

## Task 11 (optional): Codex sandbox permission profile

**Goal.** Close the `read_file` gap natively where the Codex version supports
filesystem permission profiles.

**Files.**
- `scripts/generate-guard.sh`
- `.codex/config.toml`
- `.claude/toolbox/scripts/template-sync.sh` (TOML merge must preserve the table)
- `test/test-codex-structure.sh`, `test/test-template-sync.sh`

**Steps.**

1. Confirm the installed Codex version documents
   `[permissions.<name>.filesystem]` with glob keys and `"deny"` values, and
   that the profile can be selected by default. If not, stop and leave this
   task pending with the version checked.
2. Render a `[permissions.kk-guard.filesystem]` table from the project-scope
   secrets globs (home-scope globs expand differently; include only if the
   docs show `~` support).
   → verify: `codex` loads the config without error; a `read_file` of `.env`
   is denied in a scratch session.
3. Ensure the TOML merge in sync preserves the generated table and the
   freshness check covers it.
   → verify: sync test with a downstream `config.toml` containing a capy
   table keeps both tables.

## Task 12: Final verification

Run `/kk:test`, `/kk:document`, `/kk:review-code` (bash and Python), and
`/kk:review-spec` against this feature directory.
