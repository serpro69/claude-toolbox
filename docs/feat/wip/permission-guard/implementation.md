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
   design §6 (secrets, destructive, tmp_roots, selfmod). Write every
   destructive rule in full now, using only the fields of design §6.3
   (`program`, string-or-list `subcommand`, `flags_any`, `flags_all`,
   `flags_none`, `exempt`, `reason`, optional `codex` records with
   per-record `pattern`/`match`/`not_match`). The schema is frozen against
   these real entries; Task 4 implements the matcher against them and may not
   add fields. The engine ignores destructive rules until Task 4.
   → verify: `jq . guard-rules.json` succeeds; every `secrets` entry starts
   with `./**/`, `~/` or `//`; `git restore` uses `flags_none`, `git branch
   --delete --force` uses `flags_all`, `stash drop` uses a list
   `subcommand`; `codex` records exist only on `rm`, `shred`, `sudo`, `su`,
   `doas`.
2. In `guard.py`, structure the module as pure functions plus a thin `main`
   so tests import it in-process (the safe-claude-code `test_guard.py`
   pattern: load via `importlib`, call `check_*` functions, assert a raised
   `Denied` exception or a return). Sections: payload parsing, declaration
   loading with version check, glob translation, path resolution, file-tool
   dispatch, decision emitter. Payload parsing yields a `Context` with two
   distinct fields: `project_root` (`KK_GUARD_PROJECT_ROOT`, else
   `CLAUDE_PROJECT_DIR`, else payload `cwd`) and `exec_dir` (payload `cwd`).
   Nothing downstream may use one where the other is meant.
3. Implement `glob_to_regex(pattern, project_root, home)` per design §7.4.
   Return a compiled regex that matches absolute paths. Write
   `glob-cases.json` from the docs' examples: `./**/.env` matches
   `<root>/a/b/.env` and not `<parent>/.env`; `~/.ssh/**` matches
   `<home>/.ssh/id_rsa`; `//etc/**` matches `/etc/passwd`; `*` does not cross
   `/`; a bare `.env` matches at any depth under the root.
   → verify: `python3 -I test/guard/test_guard.py` runs the glob table green.
4. Implement `resolve(path, exec_dir)`: expand `~`, join relative paths onto
   `exec_dir`, `os.path.realpath`. Return both the normalised requested path
   and the resolved path.
5. Implement `check_file_tool(tool_name, tool_input, ctx, policy)`: pick
   `file_path`, `notebook_path` or `path`; resolve against `ctx.exec_dir`;
   deny if either requested or resolved path matches any secrets glob
   anchored at `ctx.project_root`. Grep and Glob with no `path` are allowed.
6. Implement the emitter: build the reason string in the `kk guard:
   <category> — <what>. Way through: <remedy>` format (design §7.5), print
   JSON to stdout, the same text to stderr, exit 2. Allowed calls print
   nothing and exit 0.
7. Implement `main`: read stdin, parse JSON (invalid JSON denies with the
   `failure` remedy), dispatch file tools, ignore Bash for now (allow).
8. Define the corpus row schema (design §13): `tool_name`, `tool_input`,
   optional `cwd`, `project_root`, `project_config`, `user_config` (fixture
   paths relative to the corpus file, applied through the `KK_GUARD_*`
   overrides for that row), optional `pending_task`, `expect` (`allow` or
   `deny`), `category`, `note`. The replay runner points both config
   overrides at nonexistent files for rows that omit them. Add corpus cases
   for file tools: Read `/repo/.env` deny; Read
   `/repo/.env.example` allow; Edit `~/.claude/settings.json` allow in this
   task (selfmod arrives in Task 3) — mark with a `pending_task: 3` field the
   runner skips; Grep with `path: ~/.aws` deny; Read of a symlink under `/tmp`
   that resolves to `~/.ssh/id_rsa` deny; Read of `/repo/build/out.txt`
   allow; Read `/repo/app.log` allow; Read `/repo/certs/cert.pem` deny
   (accepted false positive, noted in the row); Read `/repo/.ssh/id_rsa.pub`
   allow; Read `../.env` with `cwd: /repo/sub` deny and Read `../README.md`
   with the same `cwd` allow (root anchoring); Read `/repo/.env` with the
   `KK_GUARD_PROJECT_CONFIG` and `KK_GUARD_USER_CONFIG` overrides pointing at
   nonexistent files deny (the plugin-only case: no config, baseline still
   applies).
   → verify: corpus replay in `test_guard.py` passes for all cases without
   `pending_task`.
9. Guard against Python-version drift: run the tests once under the oldest
   interpreter available locally and note the version in the test header.
   → verify: no syntax errors under that interpreter.

## Task 2: Fail-closed wrapper and hook registration

**Goal.** The hook is wired for all channels (file tools, Bash and the capy
execution tools) through a wrapper that always runs the engine and fails
closed on every error path.

**Files.**
- `klaude-plugin/scripts/guard/guard.sh` (new)
- `klaude-plugin/hooks/hooks.json`
- `klaude-plugin/scripts/validate-bash.sh` (delete)
- `test/test-hooks.sh` (rewrite Sections 1–3; keep Section 4 capy test)
- `test/test-plugin-structure.sh` (Section 5 assertions)

**Steps.**

1. Write `guard.sh` modelled on safe-claude-code's `guard.sh`: read stdin
   once with the trailing-`x` trick; do not parse the payload (no read skip
   path and no tool-name gate: design §7.1; dispatch and the unknown-tool
   allow live in the engine); interpreter list from `KK_GUARD_INTERPRETERS`
   or the default absolute list plus `PATH` fallback; run
   `python3 -I guard.py` with the payload on stdin; any outcome other than
   exit 0 or 2 → `fail_closed` which writes stderr, prints a JSON deny, exits
   2.
   → verify: `printf '{"tool_name":"Read","tool_input":{"file_path":"/x"}}' | bash guard.sh; echo $?` prints 0 with no output; the same payload with `file_path` `.env` and `cwd` set exits 2 with no config files present.
2. Update `hooks.json`: matcher
   `Bash|Read|Edit|Write|NotebookEdit|Grep|Glob|mcp__.+__capy_(execute|execute_file|batch_execute)`
   (regex; the server segment is open so a differently named capy server
   still matches), command `${CLAUDE_PLUGIN_ROOT}/scripts/guard/guard.sh`,
   `"timeout": 15`, `"onFailure": "block"`. Keep the SessionStart entry
   untouched. Until Task 13 lands, the engine allows the capy tools (unknown
   dispatch → allow), so wiring the matcher early is safe.
   → verify: `jq . hooks.json` succeeds; structure test still finds
   `CLAUDE_PLUGIN_ROOT`.
3. Delete `validate-bash.sh`. Update `test-plugin-structure.sh` Section 5 to
   assert `guard.sh` exists and is executable, `guard.py` exists,
   `guard-rules.json` is valid JSON, and `hooks.json` contains `onFailure`.
   → verify: `bash test/test-plugin-structure.sh` green.
4. Rewrite `test-hooks.sh`: allow cases (exit 0, empty stdout) for `ls /tmp`,
   `cat app.log`, `cat node_modules/foo`, `cat build/out.txt`; deny cases
   (exit 2, valid JSON, `permissionDecision` deny, non-empty stderr) for
   `cat .env` and a Read of `.env` (the Read case runs with both config
   overrides pointing at nonexistent files, proving the plugin-only path
   denies); fail-closed cases: `KK_GUARD_INTERPRETERS=/nonexistent` → exit 2
   with stderr mentioning the interpreter; `KK_GUARD_RULES=/dev/null` → exit
   2; a payload that is not JSON → exit 2.
   Note that the Bash deny cases in this task pass only after Task 3; mark
   them with a comment and a skip until then, or land Task 3 before enabling.
   → verify: `bash test/test-hooks.sh` green for the enabled cases.
5. Add the file-tool latency check: time 100 Read payloads through `guard.sh`
   with `date +%s%N`, compute p95, always print it; assert under 60 ms (twice
   the 30 ms budget) only when `CI` is unset, so shared runners never fail
   on timing.
   → verify: the printed p95 on your machine; record it in the test comment.

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
   newline. **Order of operations is the contract (design §7.3):** a
   `extract_bodies(original_text)` pass runs first and returns the raw
   `$(...)`/backtick/`<(...)`/`>(...)` bodies and the quoted argument of
   `sh -c`/`bash -c` (quote-aware, like `substitution_bodies` in the source);
   each body is analysed recursively with its original characters. `defang`
   is applied afterwards, per segment, to produce the prose view used only
   for program/subcommand/flag matching. A separate operand view
   (quote-stripped tokens, characters intact) feeds every path and
   write-target check.
   → verify: unit tests: `sh -c 'rm -rf x'` yields a body `rm -rf x`;
   `echo "$(rm x)"` yields `rm x`; `cat "/repo with spaces/.env"` yields the
   operand `/repo with spaces/.env`; `git commit -m "clean up"` prose view is
   `git commit -m Q`.
2. Implement heredoc handling (design §7.3 step 1, which runs *before*
   `extract_bodies`): detect `<<[-]WORD` and whether `WORD` is quoted; find
   the terminator line; record the span. `extract_bodies` masks
   quoted-delimiter bodies so a literal `$(...)` inside them is never
   extracted, and scans unquoted-delimiter bodies normally. After
   extraction, drop a body whose consumer program is `cat`, `tee`, `printf`
   or a plain redirect; keep the body (analysed as a script) when the
   consumer is a shell or interpreter; keep it when the consumer is
   anything else (the documented false-positive class).
   → verify: unit test with Claude Code's commit-message form
   (`git commit -m "$(cat <<'EOF' ... EOF)"`) allowed even when a body line
   starts with `rm -rf` or contains the literal text `$(rm -rf x)`;
   `cat <<EOF\n$(rm -rf x)\nEOF` denied after Task 4;
   `bash <<'EOF'\nrm -rf x\nEOF` denied after Task 4;
   `./scripts/import.sh <<'EOF'\nrm -rf x\nEOF` denied after Task 4 with the
   row's note naming it the unknown-consumer false positive.
3. Implement path-like operand extraction per segment on the operand view:
   tokens containing `/`, starting with `~` or `.`, or naming an existing
   file relative to `ctx.exec_dir`. Resolve each against `ctx.exec_dir` and
   check raw and resolved against secrets globs anchored at
   `ctx.project_root`.
   → verify: corpus `cat .env` deny; `cat ./.env` deny; `cat /repo/.env`
   deny; `cat "/repo with spaces/.env"` deny; `cat ../.env` with `cwd:
   /repo/sub` deny and `cat ../README.md` with the same `cwd` allow;
   `cat .env.example` allow; `echo "see .env.example"` allow; `find .
   -not -path './.git/*'` allow.
4. Implement mutation-operand extraction (design §7.3 step 5): `>`/`>>`
   targets (ignoring `2>`, `&>` to `/dev/null`), `tee` operands, `sed -i`
   file operands, `dd of=`, the last operand of `cp`/`install`, **every**
   operand of `mv`, the link name of `ln` (and its target with `-f`). Check
   against the selfmod set with equal/descendant/**ancestor** matching and
   against the secrets globs. Writing a secrets file is denied too, matching
   Claude Code where a Read deny blocks Edit and Write.
   → verify: corpus `echo x > .claude/settings.json` deny;
   `tee .claude/kk-guard.json` deny; `sed -i 's/a/b/' ~/.claude/kk-guard.json`
   deny; `mv .codex/hooks.json /tmp/saved.json` deny; `mv .codex /tmp/`
   deny; `mv src/a.go src/b.go` allow; `cat .claude/settings.json` allow
   (read, not write); `echo x 2>/dev/null` allow.
5. Implement inline-interpreter write detection: when a segment runs an
   interpreter with `-c`/`-e` or a stdin script, scan the code text for the
   write-call patterns in design §7.3 step 6 whose argument text contains a
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
- `klaude-plugin/scripts/guard/guard-rules.json` (not touched: the Task 1
  declaration is the fixture. If the matcher cannot express a rule written
  there, that is a design gap; stop, amend design §6.3 and the declaration
  together, and record why)
- `test/guard/test_guard.py`
- `test/fixtures/guard/corpus.jsonl`

**Steps.**

1. Implement the rule matcher on the prose view: for each segment, after
   wrapper skipping, compare the program basename to `program`; skip
   program-level global options (`git -C dir`, `git -c k=v`, `--git-dir`,
   `docker --context x`, as in safe-claude-code's `GIT` prefix); if
   `subcommand` is set, the leading non-option arguments must equal it in
   order (string or list); `flags_any`: at least one argument matches one
   regex; `flags_all`: every regex matches some argument; `flags_none`: no
   regex matches any argument. The declaration from Task 1 is the fixture;
   no new fields.
   → verify: unit tests: `git restore f` deny, `git restore --staged f`
   allow, `git restore -S f` allow; `git branch -D x` deny, `git branch -rfD
   x` deny (cluster), `git branch --delete --force x` deny, `git branch
   --delete x` allow, `git branch -d x` allow; `git stash drop` deny, `git
   stash list` allow; `docker volume rm v` deny, `docker volume ls` allow.
2. Wire recursion: the bodies returned by Task 3's `extract_bodies` (from
   the original text) and the programs run by `xargs`, `env`, `sudo` (sudo
   itself denies first), `timeout N`, `nohup` are each analysed as commands.
   → verify: corpus `/bin/rm -rf build` deny; `sh -c 'rm -rf x'` deny;
   `xargs rm` deny; `env rm x` deny; `timeout 5 rm x` deny;
   `echo "$(rm x)"` deny.
3. Implement `targets_under_tmp` with directory tracking: walk the segments
   in order keeping an `exec_dir` that starts at `ctx.exec_dir`; a `cd`
   segment with exactly one literal absolute-path argument updates it; any
   other `cd`, `pushd`, `popd`, or an `env -C`/`env --chdir` wrapper on the
   segment sets it to *uncertain*. For the `rm` segment, resolve every
   non-option operand against `exec_dir` (with `$TMPDIR` read from the
   engine's environment and `realpath`ed); allow only if all resolve under a
   `tmp_roots` entry; when `exec_dir` is uncertain only absolute operands can
   qualify and any relative operand denies; any operand containing `$`, `*`,
   `?` or `[` denies; `rm -rf /tmp/../home` resolves out of `/tmp` and
   denies.
   → verify: corpus `rm -rf /tmp/kk-test` allow; `rm /tmp/a /tmp/b` allow;
   `cd /tmp/kk-test && rm -rf ./x` allow; `cd /work/project && rm -rf ./work`
   with `cwd: /tmp/guard-probe` deny; `env -C /work/project rm -rf ./work`
   with the same `cwd` deny; `cd "$D" && rm -rf /tmp/x` allow (absolute
   survives uncertainty); `rm -rf "$T"` deny; `rm -rf /tmp/*` deny;
   `rm -rf /tmp/../etc` deny; `rm -rf ~` deny; `rm -rf /` deny; `rm -rf .`
   with `cwd` at the project root deny.
4. Add the remaining corpus rows for every rule in `git`, `infra`,
   `privilege` plus the must-allow neighbours: `git branch -d x`,
   `git rebase main`, `git commit --amend`, `git restore --staged f`,
   `git push origin main`, `git stash list`, `kubectl get pods`,
   `terraform plan`, `helm list`, `docker ps`. The equivalent-spelling rows
   added during Task 1 (`git push -d`/`:ref`/`+ref`, `git branch -df`,
   `git restore -SW`, `rsync --del`, `docker container rm`, `docker image
   rm`, `terraform apply -destroy`, each with a benign neighbour) already
   exist with `pending_task: 4`; remove `4` from `PENDING_TASKS` in
   `test_guard.py` to enable them.
   → verify: full corpus replay green.
5. Confirm the deny reason names the category and the rule's `reason`, and
   the destructive remedy names the category and the user config path.
   → verify: unit test on the emitted string.

## Task 5: Configuration layering

**Goal.** A project file tightens, a user file loosens, invalid files are
reported without weakening anything.

**Files.**
- `klaude-plugin/scripts/guard/guard.py`
- `klaude-plugin/scripts/guard/guard.sh` (confirm the `KK_GUARD_*` env
  overrides pass through to the engine)
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
   `KK_GUARD_USER_CONFIG` or `~/.claude/kk-guard.json`; select the `*` entry
   and the single longest key that is a path prefix of the `realpath`ed
   `ctx.project_root`; the effective entry is their union (lists
   concatenated, `disable_selfmod` true if either is). `allow_patterns` are
   tested per simple command: each segment and each recursively extracted
   body, after wrapper skipping, in the prose view; a match exempts that one
   simple command from destructive rules only.
   → verify: fixture disabling `infra` for `/work/ops` allows
   `kubectl delete pod x` with project root `/work/ops/cluster-a` and still
   denies it with root `/work/app`; with `*` disabling `privilege` and
   `/work/ops` disabling `infra`, root `/work/ops/x` has both disabled
   (union) and a `/work` entry disabling `git` contributes nothing;
   `allow_patterns: ["^git clean -n"]` allows `git clean -nd`, still denies
   `git clean -fd`, and denies `git clean -nd; rm -rf ./work` (the `rm`
   segment is not exempt); `allow_patterns` never allows `cat .env` or a
   write to `.claude/settings.json`; `disable_selfmod: true` allows an Edit
   of `.claude/settings.json`.
3. Emit `systemMessage` on allowed calls when a config was invalid: stdout is
   exactly `{"systemMessage": "<file>: <problem>"}` with no
   `hookSpecificOutput` key, exit 0.
   → verify: stdout is valid JSON, has only that key, and `test-hooks.sh`
   asserts the field.
4. Add wrapper tests: with `KK_GUARD_PROJECT_CONFIG` pointing at a fixture
   that adds a secrets glob, a Read of a file matching the extra glob is
   denied through `guard.sh`, and the same Read is allowed when the override
   points at a nonexistent file.
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
   one `prefix_rule(...)` per `codex` record, using that record's `pattern`
   (a token that is a list renders as a Starlark list, e.g. `["git", "push",
   ["--force", "-f"]]`), its own `match`/`not_match`, and the rule's
   `reason`; (c) `cp` the three engine files to `.codex/scripts/guard/`; (d)
   replace the block between the `GUARD-RULES` markers in `configuration.md`
   with a table of secrets globs, a table of destructive categories and
   rules with a column saying whether each is also a Codex forbid, and the
   one-line `disable_selfmod` example.
   → verify: run twice; the second run produces no diff (`git diff --stat`
   empty).
2. Confirm the `codex` records written in Task 1 render to valid Starlark:
   records exist only on `rm`, `shred`, `sudo`, `su`, `doas` (design §6.3
   says why: a repository `forbidden` outranks user rules on Codex, so every
   loosenable rule stays hook-only there). Each record's `match` examples
   must match its own `pattern` and `not_match` must not; Codex rejects the
   file at load otherwise, so two records may never share one example list.
   → verify: if the `codex` CLI is installed,
   `codex execpolicy check --pretty --rules .codex/rules/default.rules -- rm -rf x`
   reports forbidden, `-- ls -la` reports no match, and the file parses;
   record the CLI version in the test. Otherwise skip and note it.
3. Add `generate-guard` to the Makefile and to `generate-all`; add the
   freshness step to CI next to the generate-kodex one:
   `make generate-guard && git diff --exit-code .claude/settings.json .codex/rules .codex/scripts/guard docs/user-guide/configuration.md`.
   → verify: CI job definition parses; local `make generate-guard` succeeds.
4. Structure-test assertions: every secrets glob matches
   `^(\./\*\*/|~/|//)`; every destructive rule uses only the §6.3 field set
   (`jq` key check); `codex` records appear only on the five permitted rules;
   regenerate into a temp copy and diff against the tree; `cmp` each
   `.codex/scripts/guard/*` with its plugin source; `default.rules` starts
   with the generated header; `hooks.json` matcher names the three capy
   tools.
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

**Goal.** Codex Bash, `apply_patch` and capy MCP execution calls are guarded
by the shared engine; failures block; the session advisory lists the current
secrets.

**Files.**
- `.codex/scripts/pretooluse-bash.sh`
- `.codex/scripts/pretooluse-patch.sh` (new)
- `.codex/scripts/pretooluse-mcp.sh` (new)
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
   `export KK_GUARD_PROJECT_ROOT="$REPO_ROOT"` followed by
   `printf '%s' "$INPUT" | bash "$REPO_ROOT/.codex/scripts/guard/guard.sh"`
   (the variable must reach the right-hand side of the pipe, so export it
   rather than prefixing `printf`; Codex sets no `CLAUDE_PROJECT_DIR` and the
   engine must not anchor globs to the payload `cwd`); propagate exit 2 and
   stderr; wrap the whole script so any unexpected failure writes stderr and
   exits 2.
   → verify: `test-codex-hooks.sh` Section 3/4 denylist cases now assert
   exit 2, JSON deny and a reason containing `kk guard`; a `cat ../.env`
   payload with `cwd` at a subdirectory of the test repo denies; capy
   handoff cases unchanged and green.
3. Add `pretooluse-patch.sh` (same delegation and root export, no HTTP
   section) and the `hooks.json` entry with matcher `Edit|Write` running it.
   → verify: new tests feed an `apply_patch` payload updating `.env` and one
   updating `src/a.py`; first denies, second allows; `test-codex-structure.sh`
   asserts the entry exists.
4. Add `pretooluse-mcp.sh` (same delegation and root export) and the
   `hooks.json` PreToolUse entry with matcher
   `^mcp__[^[:space:]]+__capy_(execute|execute_file|batch_execute)$` running
   it. Capy's own entry for these tools stays untouched; the new entry is
   toolbox-owned under the existing ownership rule because its command runs
   a script under `.codex/scripts/`. Requires Task 13's engine dispatch.
   → verify: a `capy_execute` payload with `language: shell` and `code: cat
   .env` denies; `language: shell`, `code: go test ./...` allows;
   `test-codex-structure.sh` asserts the entry exists and that capy's entry
   is still present.
5. Fail-open mitigation test: point `KK_GUARD_INTERPRETERS` at a nonexistent
   path and confirm all three adapter scripts exit 2 with non-empty stderr.
   → verify: assertions green.
6. `session-start.sh`: render a "Protected files" paragraph from
   `.codex/scripts/guard/guard-rules.json` with `jq` (fall back to a static
   sentence if the file is missing) stating that reading these paths is
   prohibited by policy.
   → verify: `test-codex-hooks.sh` Section 1/2 assert the paragraph lists
   `.env` in both legacy and capy modes.
7. Update `docs/providers/codex.md`: hook descriptions (three adapters), the
   parity-gap table from design §11 including the "not loosenable on Codex"
   row.
   → verify: read-through.

## Task 9: Assumption closure for latency, bypass mode and Codex cwd

**Goal.** The three unverified runtime assumptions are measured or observed
and recorded.

**Files.**
- `test/test-hooks.sh` (Bash-path latency)
- `docs/feat/wip/permission-guard/design.md` §16 (record results)

**Steps.**

1. Add the Bash-path latency test: run the corpus's Bash cases through
   `guard.sh`, compute p95, always print it, assert under 100 ms (twice the
   50 ms budget) only when `CI` is unset.
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
- `docs/adr/0012-permission-guard-single-declaration.md` (new; 0010 and 0011 exist, re-check the next free number before creating)
- `docs/adr/0005-codex-hook-enforcement-gap.md` (dated update)
- `docs/contributing/adrs.md`
- `docs/user-guide/configuration.md` (prose around the generated block; hooks table; new config subsection)
- `docs/providers/claude-code.md`
- `docs/getting-started/plugin-only.md`
- `docs/contributing/plugin-development.md`, `docs/contributing/testing.md`, `docs/contributing/architecture.md`
- `klaude-plugin/README.md`
- `klaude-plugin/.claude-plugin/plugin.json` (minor version bump)

**Steps.**

1. Write ADR 0012 with Nygard's sections. Context: the add-only merge
   (commit `e0036b2`), substring false positives, three intents. Decision:
   one declaration rendered to three channels; tighten-only project config,
   loosen-only user config; flat deny for destructive commands in every
   mode; Codex forbids limited to unconditional literals. Consequences:
   rejected alternatives (design §18), Codex gaps (design §11), the
   hooks-off `rm` regression (design §14), revisit conditions (flat deny too
   restrictive → mode-aware ask using `permission_mode`). Cite operative
   files by path.
   → verify: `plugin-graph validate` still passes (no plugin file links to
   the ADR).
2. Add the dated update to ADR 0005. Add the 0012 row to `adrs.md`. The
   index lacks 0008, 0009 and 0011 rows; ask the user before adding them.
3. Update the user guide, provider pages, plugin-only page, contributing
   pages, plugin README per design §15. In `plugin-development.md`, replace
   the "Always exit 0" PreToolUse paragraph with the fail-closed contract and
   add the toolbox-repo `disable_selfmod` note. In `configuration.md`, state
   next to the rules table that selfmod blocks agent edits of
   `.claude/settings.json` (including adding allow entries) and show the
   `disable_selfmod` entry that lifts it.
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

## Task 13: capy MCP execution channel

**Goal.** A shell program or script submitted to `capy_execute`,
`capy_execute_file` or `capy_batch_execute` is held to the same policy as a
Bash call, on both Claude Code (hook matcher from Task 2) and Codex (adapter
from Task 8 step 4). Numbered after Task 12 because it was added by the
2026-10-25 reviews; it is not last in execution order (see tasks.md).

**Files.**
- `klaude-plugin/scripts/guard/guard.py` (dispatch for the three tools)
- `test/guard/test_guard.py`
- `test/fixtures/guard/corpus.jsonl`
- `test/test-hooks.sh`

**Steps.**

1. Implement dispatch per design §7.2: `capy_batch_execute` → run each
   `tool_input.commands[].command` through the Bash analysis; `capy_execute`
   → `language` `shell` runs `code` through the Bash analysis, any other
   language runs `code` through the inline-interpreter write scan (§7.3 step
   6) and the path-like secrets scan; `capy_execute_file` → check `path` as a
   Read, then `code` as above. `tool_input.cwd`, when present, is the
   execution directory for the call: absolute as given, relative resolved
   against the project root (capy documents relative `cwd` as
   project-relative); the project root itself is unchanged. The tool name
   arrives with the server prefix (`mcp__capy__capy_execute`); match on the
   suffix after the last `__`.
   → verify: corpus: `capy_execute` shell `cat .env` deny; shell
   `go test ./...` allow; python `open('.env').read()` deny; python
   `print(1)` allow; javascript `fs.writeFileSync('.claude/settings.json',
   x)` deny; `capy_batch_execute` with `[{command: "ls"}, {command: "rm -rf
   ."}]` deny; `capy_execute_file` with `path: .env` deny, `path:
   README.md` allow.
2. Add `test-hooks.sh` cases: a `capy_execute` payload through `guard.sh`
   denies with the secrets reason; a benign one exits 0 with empty stdout.
   → verify: `bash test/test-hooks.sh` green.
3. Document the channel in `docs/user-guide/configuration.md` (hooks table)
   and `docs/providers/codex.md` (adapter list).
   → verify: read-through.
