# Design: Permission Guard Rework

> Status: draft
> Created: 2026-10-20
> Implementation plan: [./implementation.md](./implementation.md)
> Tasks: [./tasks.md](./tasks.md)
> Related: [ADR 0005](../../../adr/0005-codex-hook-enforcement-gap.md) (Codex hook enforcement gap), ADR 0012 (to be written by this feature; 0010 and 0011 are already allocated)
> Reviewed: 2026-10-25, two `/kk:review-design` passes merged and re-verified; all findings applied to this revision (see the git history for the per-finding mapping)

## 1. Problem

How might we let every claude-toolbox consumer inherit a small, certain
secrets-and-destruction guard across Claude Code and Codex, without blocking
the reads an agent needs to debug, and without letting a cloned repo weaken it?

The current guard is two overlapping layers created at the project's inception:
a `permissions.deny` list in `.claude/settings.json` and a substring-matching
PreToolUse hook (`klaude-plugin/scripts/validate-bash.sh`, mirrored in
`.codex/scripts/pretooluse-bash.sh`). Three defects were established during the
brainstorm that preceded this design:

1. **Deny rules can only ratchet tighter downstream.** The settings merge in
   `.claude/toolbox/scripts/template-sync.sh` (`smart_merge`, around line 1453)
   is add-only for arrays: downstream keeps every entry and gains new upstream
   entries, but nothing ever removes one. Commit `e0036b2` (2026-09-25, "Allow
   claude/codex to access .log file and node_modules") removed `Read(*.log)`
   upstream; every consumer synced before that date still
   denies logs today. Any design that keeps policy in a synced, union-merged
   array inherits this.
2. **The Bash hook matches substrings, not meaning.** It greps the raw command
   text for `.env`, `.git/`, `build/` and similar. It denies a `find` whose
   exclusion pattern mentions `.git/`, a `cat .env.example`, a path like
   `cmd/build/main.go`, and a commit message that names `dist/`. It has no
   read/write distinction and no path resolution. It also exits 0 on every
   internal failure, so a missing `jq` disables it silently.
3. **One mechanism carries three unrelated intents.** Secrets (`.env`,
   `service-account-key.json`, Terraform state) are a security concern. Noise
   (`build/`, `dist/`, `__pycache__/`, `*.lock*`, `.idea/`) is a context-window
   concern that the harness now handles natively (Read truncation, Bash output
   persistence) and that capy routes where installed. Project data (`*.csv`,
   `data/`, `./examples`) is repo-specific and nobody remembers why it was
   added.

A fourth observation reframes the hook's job: a settings rule such as
`Read(./**/.env)` governs the Read, Edit and Write tools only. `cat .env` in
Bash walks past it. The hook is therefore the **shell channel of the same
secrets policy**, not a second policy, and the two layers drifted because
nothing tied their lists together.

## 2. Goals and success criteria

Goals:

- Keep secrets out of the transcript on every tool channel.
- Deny data-losing commands in every permission mode.
- Stop denying the reads an agent needs to debug.
- Let a project tighten the guard and a machine owner loosen it, never the
  other way round.
- Make the Claude settings baseline, the hook and the Codex rules impossible
  to drift apart.

Success is measured by the test suite (see §13):

- A fixture corpus of real commands and paths passes 100%, including the known
  false positives as must-allow and the shell-evasion forms (`/bin/rm`,
  `sh -c 'rm ...'`, `xargs rm`) as must-deny.
- File-tool evaluation (Read, Grep, Glob, Edit, Write) p95 under 30 ms and
  full Bash evaluation p95 under 50 ms on the corpus, measured locally. CI
  prints the numbers and does not gate on them (shared runners make timing
  gates flaky).
- One template sync removes every stale deny entry from a downstream
  `settings.json` and reports what it removed.

## 3. Who this is for

Developers who trust themselves: the toolbox author and colleagues running
agents in their own repositories. The guard catches agent accidents and
prompt-injection outcomes, not the human. Loosening is a normal, documented
path, not a locked-down managed-settings scenario.

## 4. Constraints

1. The settings layer speaks Claude Code permission globs only (gitignore
   syntax with `//`, `~/`, `./` anchors). Nothing a hook returns can loosen a
   settings deny: the harness evaluates deny rules regardless of hook output.
2. Template sync copies `.claude/` and `.codex/` from the upstream repo root.
   Downstream stays master for everything except `permissions.deny`. Sync
   never deletes downstream files.
3. `klaude-plugin/` is self-contained and must work for plugin-only installs
   with no template, so the baseline ships inside the plugin. No ADR
   references inside plugin files.
4. Runtime: bash, `jq`, `python3` standard library only (the plugin already
   requires python3 through `scripts/cpr.py`). Python floor 3.8, because macOS
   Command Line Tools ship 3.8/3.9-era interpreters. Claude Code 2.1.295 or
   later for `onFailure: "block"`.
5. Codex hooks intercept Bash, `apply_patch` and MCP calls only; `read_file`
   stays advisory (ADR 0005). Capy's own hook entries and the per-event
   step-aside detection in `pretooluse-bash.sh` are preserved.
6. Off limits: `run_plugin_migration`'s `dirs_to_remove`, `docs/feat/done/**`,
   eval fixtures, and Claude Code's matching semantics (replicated, never
   altered).

## 5. Architecture

One declaration, rendered into three enforcement layers and the documentation.

```
klaude-plugin/scripts/guard/guard-rules.json   (single source of truth, shipped in the plugin)
        │
        ├─ generate-guard ──► .claude/settings.json  permissions.deny  (Claude baseline: Read/Edit/Write, best-effort Grep/Glob)
        ├─ generate-guard ──► .codex/rules/default.rules               (Codex prefix_rule forbids, unconditional literals only)
        ├─ generate-guard ──► .codex/scripts/guard/{guard.sh,guard.py,guard-rules.json}  (byte-identical engine copy)
        ├─ generate-guard ──► docs/user-guide/configuration.md         (rules table between markers)
        │
        └─ runtime ────────► klaude-plugin/scripts/guard/guard.sh ──► guard.py   (Claude hook, all channels)
                             .codex/scripts/guard/guard.sh ──► guard.py          (Codex hook via thin adapters)
```

**Layer 1, Claude settings baseline.** The template's `.claude/settings.json`
carries `permissions.deny` as a generated projection of the secrets globs in
`Read(...)` form. The harness applies `Read` deny rules to Read, Edit, Write
and best-effort to Grep and Glob. This layer is the fallback when hooks are
off and what the `/permissions` UI shows. Template sync replaces the array
instead of merging it (§10).

**Layer 2, plugin hook.** Registered in `klaude-plugin/hooks/hooks.json` with
matcher
`Bash|Read|Edit|Write|NotebookEdit|Grep|Glob|mcp__capy__capy_execute|mcp__capy__capy_execute_file|mcp__capy__capy_batch_execute`,
`onFailure: "block"` and a 15-second timeout. A bash wrapper handles
fail-closed semantics; a Python engine does the matching (§7). The engine
reads the same declaration at runtime. Every matched tool reaches the engine;
there is no early exit for read tools (§7.1 explains why). The capy MCP
execution tools are matched because in a capy-enabled session they, not Bash,
are the ordinary execution channel for tests and builds; a `cat .env`
submitted to `capy_execute` is the same leak as one submitted to Bash.

**Layer 3, Codex.** The template syncs a byte-identical copy of the engine into
`.codex/scripts/guard/`. The existing PreToolUse Bash hook delegates to it, a
new `Edit|Write` matcher covers `apply_patch`, a new MCP matcher covers the
capy execution tools, and `.codex/rules/default.rules` becomes a generated
projection of the few destructive literals that are safe to forbid
unconditionally (§9, §11).

Freshness is enforced like `make generate-kodex`: a make target regenerates
every projection and CI fails on any diff.

A correction to the brainstorm wording: the single source of truth is the
plugin-shipped declaration. The project config (§8) extends it; it does not
replace it. Plugin-only installs therefore receive the full baseline.

## 6. The declaration

`klaude-plugin/scripts/guard/guard-rules.json` has five top-level keys.

### 6.1 `version`

Integer, currently `1`. The engine refuses to run against an unknown version
and fails closed, so a schema change can never silently match nothing.

### 6.2 `secrets`

A flat list of Claude Code permission globs. A lint test restricts every entry
to one of three unambiguous shapes, because the docs define bare patterns
inconsistently (prose says gitignore any-depth, a table example says
cwd-anchored) and never define a trailing `/`:

- `./**/<name-or-glob>` for project-relative files at any depth
- `~/<dir>/**` or `~/<file>` for home-relative paths
- `//<abs>/**` for absolute paths

Baseline (accepted in Step 4, Section 2):

| Scope | Globs | Rationale |
|---|---|---|
| Project | `./**/.env`, `./**/.env.local`, `./**/.env.*.local` | dotenv convention: these are the git-ignored files; `.env.example` and committed `.env.production` stay readable |
| Project | `./**/service-account*.json` | GCP service-account keys |
| Project | `./**/*.tfstate`, `./**/*.tfstate.backup`, `./**/.terraform/**` | Terraform state carries provider secrets |
| Project | `./**/*.pem`, `./**/id_rsa`, `./**/id_ed25519`, `./**/id_ecdsa` | private keys checked into or generated inside a repo; exact key names so `id_rsa.pub` stays readable |
| Home | `~/.ssh/**`, `~/.aws/**`, `~/.gnupg/**`, `~/.kube/**`, `~/.config/gcloud/**` | credential directories |
| Home | `~/.netrc`, `~/.pypirc`, `~/.docker/config.json`, `~/.claude/.credentials.json` | credential files |

Dropped from the current list and why: `.ansible/` is a cache directory and
vault files have no reliable name; a project that needs it adds it.

Accepted false positive: `*.pem` also matches public certificate bundles
(`ca.pem`, test fixtures). Private keys in `.pem` files are common enough that
the glob stays; the corpus pins a `cert.pem` read as a known deny so the
trade-off is visible, and a project that keeps public certs can ask the user
for a redacted copy as the deny message says.

### 6.3 `destructive`

A map of category name to a list of rules. Each rule uses a small matcher
vocabulary the engine implements:

| Field | Meaning |
|---|---|
| `program` | basename of the program in command position, after wrapper skipping (`env`, `nohup`, `timeout`, `nice`, `sudo` as a wrapper is itself denied) |
| `subcommand` | optional; a string or an ordered list of strings that must equal the leading non-option arguments in order (`"clean"`, `["stash", "drop"]`, `["volume", "rm"]`); program-level global options (`git -C dir`, `git -c k=v`, `docker --context x`) are skipped first |
| `flags_any` | optional; list of regexes, at least one must match an argument |
| `flags_all` | optional; list of regexes, every one must match some argument (`--delete` and `--force`) |
| `flags_none` | optional; list of regexes, none may match any argument (`restore` is destructive only *without* `--staged`/`-S`) |
| `exempt` | optional; a named exemption the engine knows, currently `targets_under_tmp` |
| `reason` | short text used in the deny message |
| `codex` | optional; a list of records `{ "pattern": [tokens], "match": [...], "not_match": [...] }`, one `prefix_rule` each; a token is a string or a list of literal alternatives (`["git", "push", ["--force", "-f"]]`). Present only on rules whose literal prefix is unconditional, see below |

Regexes in the three `flags_*` fields are matched against each argument
token after quote stripping; a short flag inside a cluster (`-rfD`) is
matched by writing the regex for the cluster (`^-[a-zA-Z]*D[a-zA-Z]*$`), and
the lint test requires every `-X` rule to ship the cluster form.

Baseline categories and rules (accepted in Step 4, Section 2):

- `filesystem`: `rm` (exempt `targets_under_tmp`); `shred`; `find` with
  `flags_any` `-delete`; `rsync` with `flags_any` `--delete*`
- `git`: `clean`; `reset` with `flags_any` `--hard`; `checkout` with
  `flags_any` `--` or `.`; `restore` with `flags_none` `--staged`, `-S`;
  `branch` with `flags_any` `-D` (cluster form) **or** `flags_all` `--delete`,
  `--force` (two rules); `push` with `flags_any` `--force`, `-f`,
  `--force-with-lease`, `--delete`; `["stash", "drop"]`; `["stash", "clear"]`
- `infra`: `terraform destroy`; `kubectl delete`; `helm uninstall`;
  `helm delete`; `docker rm`; `docker rmi`; `["system", "prune"]` under
  `docker`; `["volume", "rm"]` and `["volume", "prune"]` under `docker`
- `privilege`: `sudo`; `su`; `doas`

Every predicate the baseline needs (`flags_any`, `flags_all`, `flags_none`,
ordered `subcommand`) is in the vocabulary above; the lint test fails if a
rule uses a field the engine does not implement, and Task 1 writes the full
declaration before the matcher exists so the schema is frozen against real
entries, not invented during Task 4.

**Codex records.** Only `rm`, `shred`, `sudo`, `su` and `doas` carry `codex`
records. Two verified facts (codex-cli 0.164.0, 2026-10-25) force this:

1. Codex applies the most restrictive matching rule across every rules file,
   so a `forbidden` rule synced into a repository outranks an `allow` the
   machine owner writes in `~/.codex/rules/`. A generated forbid for
   `kubectl delete` would make the user-level loosening of §8.2 dead on Codex
   for exactly the ops repositories that motivated it. The five literals above
   are the ones no user config is expected to loosen, and `rm` is already
   forbidden by today's hand-written file, so nothing regresses.
2. Codex rejects a rules file at load when a `match` example does not match
   the rule it is attached to, so examples live on each record and
   alternatives are expressed as union tokens, never as two records sharing
   one example list.

Everything else in `git` and `infra` is hook-only on Codex and therefore
loosenable there like on Claude Code; §11 records the resulting asymmetry.

Deliberately absent: `git rebase` and `git commit --amend`. Both are
reflog-recoverable, Claude Code's own system prompt already forbids them
without an explicit request, and under flat deny the user could never ask the
agent to perform either.

### 6.4 `tmp_roots`

`/tmp`, `/private/tmp`, `/var/folders`, `/private/var/folders`, and the
literal `$TMPDIR`, which the engine resolves from its own environment at
runtime and `realpath`s.

### 6.5 `selfmod`

Write-protected paths, checked on every channel: `.claude/settings.json`,
`.claude/settings.local.json`, `.claude/kk-guard.json`,
`~/.claude/settings.json`, `~/.claude/settings.local.json`,
`~/.claude/kk-guard.json`, `.codex/hooks.json`, `.codex/rules/**`,
`.codex/scripts/**`, `~/.claude/plugins/**`. The last entry protects the
installed engine from the agent it guards.

## 7. Runtime engine

Files: `klaude-plugin/scripts/guard/guard.sh` (wrapper),
`klaude-plugin/scripts/guard/guard.py` (engine), the declaration.

### 7.1 Wrapper

- Reads the payload from stdin once, preserving trailing newlines.
- Extracts `tool_name` with bash parameter expansion; no fork before the
  interpreter starts. A tool name outside the matcher set exits 0 (defensive;
  the matcher should never deliver one).
- **No read skip path.** Every matched tool, including `Read`, `Grep` and
  `Glob`, reaches the engine. An earlier draft exited early for those three
  when no guard config file existed, reasoning that the settings baseline
  already covers reads. That is false for plugin-only installs: a plugin
  cannot ship `permissions`, and the plugin-only guide lists permission
  baselines as not included, so the skip would have removed the only
  secrets layer on `Read` precisely where the hook is the only layer. The
  file-tool path is a JSON parse plus a handful of regex matches; §13 budgets
  it.
- **Interpreter selection:** absolute candidates first (`/usr/bin/python3`,
  `/opt/homebrew/bin/python3`, `/usr/local/bin/python3`), then `python3` on
  `PATH` as a last resort for pyenv and uv users. Overridable for tests via
  `KK_GUARD_INTERPRETERS`. This departs from safe-claude-code, which never
  consults `PATH`; the audience here is developers and `-I` already prevents
  site-packages injection.
- Runs `python3 -I guard.py` with the payload on stdin.
- **Fail closed:** a missing or non-working interpreter, an engine crash, an
  exit code other than 0 or 2, or malformed engine output all produce a
  stderr reason, a JSON deny on stdout, and exit 2. On Codex this is the only
  fail-closed mechanism (§11), and exit 2 with empty stderr is treated as a
  failure that lets the call through, so every exit-2 path writes stderr
  first.

### 7.2 Engine pipeline

1. Parse the payload: `tool_name`, `tool_input`, `cwd`, `permission_mode`
   (used only in messages). Establish two directories that are never
   interchanged:
   - the **project root**: `KK_GUARD_PROJECT_ROOT` when an adapter set it
     (Codex, §11), else `CLAUDE_PROJECT_DIR`, else the payload `cwd`. It
     anchors every project-relative glob (§7.4) and locates the project
     config (§8.1);
   - the **execution directory**: the payload `cwd` (or the tool input's own
     `cwd` for the capy execution tools). Relative arguments resolve against
     it.
   Claude Code persists the shell working directory across Bash calls, so the
   payload `cwd` is routinely a subdirectory of the root; anchoring globs to
   it would let `cat ../.env` from `/repo/sub` slip past `./**/.env`.
2. Load the declaration; check `version`.
3. Load and merge project and user configs (§8).
4. Dispatch by tool:
   - **Read, Grep, Glob:** candidate path is `file_path` (Read) or `path`
     (Grep, Glob search root). Expand `~`, resolve relative to `cwd`, then
     `realpath`. Check both the requested and the resolved path against the
     effective secrets globs; a match on either denies. This mirrors the
     documented behaviour of deny rules, which "apply when either the
     requested path or the file it resolves to matches".
   - **Edit, Write, NotebookEdit:** same secrets check (`file_path` or
     `notebook_path`), plus the self-modification check.
   - **apply_patch (Codex):** parse `*** Add File:`, `*** Update File:`,
     `*** Delete File:` and `*** Move to:` header lines from the raw patch in
     `tool_input.command`; resolve each against `cwd`; apply secrets and
     self-modification checks; treat `Delete File` as `filesystem`-destructive
     (Claude Code's edit tools cannot delete, so parity says deny).
   - **Bash:** see 7.3.
   - **capy execution tools:** `capy_batch_execute` runs each
     `commands[].command` through the Bash analysis of 7.3. `capy_execute`
     with `language` `shell` runs `code` through the same analysis; any other
     language runs `code` through the inline-interpreter write scan (7.3 step
     6) and the path-like secrets scan. `capy_execute_file` checks `path` as a
     Read and `code` as above. The tool input's `cwd`, when present, is the
     execution directory for that call; the project root is unchanged.
5. Emit a decision (7.5).

### 7.3 Bash analysis

The order matters: executable text is extracted from the **original**
command before any lossy view is built. safe-claude-code does the same
(`substitution_bodies` and `strip_quotes` run on the raw command; `defang`
feeds only the prose-level pattern checks), and an earlier draft of this
section inverted that and would have turned `sh -c 'rm -rf x'` into
`sh -c Q` before recursion could see it.

1. **Structural extraction on the original text.** A quote-aware scan finds
   the bodies of `$(...)`, backticks, `<(...)`, `>(...)`, and the quoted
   argument of `sh -c`, `bash -c` (and other shells), plus the program run by
   `xargs`, `env`, `sudo`, `timeout N`, `nohup`. Each body is analysed
   recursively as a command in its own right, with its original characters,
   so `sh -c 'rm -rf x'` and `echo "$(rm x)"` are both seen.
2. **Heredocs.** A heredoc with a quoted delimiter (`<<'EOF'`) is literal:
   its body is dropped when the consumer is a data sink (`cat`, `tee`,
   `printf`, a redirect to a file). A heredoc with an unquoted delimiter is
   expandable: the shell evaluates `$(...)` and backticks inside it before the
   sink ever sees the text, so those substitutions are extracted by step 1
   first and only then is the body dropped. Bodies fed to a shell or an
   interpreter are kept whole. This removes commit-message prose, which
   Claude Code passes through `git commit -m "$(cat <<'EOF' ... EOF)"`.
3. **Segmentation.** Split on the separators Claude Code itself recognises:
   `&&`, `||`, `;`, `|`, `|&`, `&`, newline.
4. **Two views per segment.** The *prose view* is the segment after
   safe-claude-code's `defang` (multi-word quoted strings become a
   placeholder; single quoted words and glued quotes such as `'rm'` and `r'm'`
   stay tokens); it is used for program, subcommand and flag matching only.
   The *operand view* keeps every argument with its quotes stripped and its
   characters intact; path and write-target extraction use it, so
   `cat "/repo with spaces/.env"` still yields the secret path.
5. **Per segment:** skip leading assignments and wrappers (with their
   option-arguments), resolve the program basename, then:
   - match destructive rules by `program`, ordered `subcommand`, `flags_any`,
     `flags_all`, `flags_none`;
   - if a rule names `targets_under_tmp`, resolve every non-option operand
     (`~` expansion, execution-directory-relative, `realpath`) and allow only
     if all resolve under a `tmp_roots` entry; an operand containing `$`, a
     glob, or that cannot be resolved denies. **Directory tracking:** a
     preceding `cd` segment whose single argument is a literal absolute path
     updates the execution directory for the rest of the command; any other
     `cd`, `pushd`, `popd`, or a wrapper that changes directory (`env -C`,
     `env --chdir`, `make -C` as a wrapper) marks it uncertain, after which
     relative operands deny and only absolute operands under a `tmp_roots`
     entry are exempt. Without this, `cd /work/project && rm -rf ./work` with
     a payload `cwd` under `/tmp` would resolve `./work` under `/tmp` and be
     exempted while deleting project files;
   - collect path-like operands (contain `/`, start with `~` or `.`, or name
     an existing file) and check each against the secrets globs, raw and
     resolved;
   - collect **mutation operands** per command and check them against the
     self-modification set and the secrets globs: `>`, `>>`, `tee`, `sed -i`,
     `dd of=` write their target; `cp` and `install` write their last operand;
     `mv` mutates **every** operand, source and destination, because moving
     `.codex/hooks.json` to `/tmp` removes it just as surely as deleting it;
     `ln` writes the link name and, with `-f`, replaces the target. A
     mutation operand matches a self-modification entry when it is equal to
     it, beneath it, or an **ancestor** of it (`mv .codex /tmp/` carries
     `.codex/hooks.json` along).
6. **Inline interpreter code** (`python -c`, `node -e`, stdin scripts, and
   non-shell `capy_execute` code): the text is additionally scanned for a
   write call (`open(..., 'w'|'a'|'x')`, `writeFile*`, `Path(...).write_*`,
   `shutil.copy*`, `shutil.move`, `os.rename`, `os.remove`, `fs.rename*`,
   `fs.rm*`) whose argument names a protected file. Documented ceiling: a
   path assembled by concatenation is not detected.

Known false-positive class that remains: a heredoc line fed to a shell that
begins with a destructive program name. Accepted; the corpus pins the common
commit-message case as must-allow.

### 7.4 Glob matcher

Translates a permission glob to a regular expression:

- Anchor by prefix: `//` absolute; `~/` home-expanded; `./` or bare relative to
  the **project root** on every channel (§7.2 step 1), never to the payload
  `cwd`. The path being tested is the operand resolved against the execution
  directory, so a subdirectory shell reading `../.env` is tested as
  `<root>/.env` against `<root>/**/.env` and denied.
- `**/` becomes an optional run of directories; `/**` becomes "and anything
  beneath"; `*` matches within a single segment; `?` matches one character.
- A bare filename with no `/` matches its basename at any depth under the
  anchor (documented gitignore semantics: `Read(.env)` equals
  `Read(**/.env)`).
- Single-segment directory patterns in deny position match at any depth,
  matching the documented deny/ask behaviour.

A fixture table built from the docs' own examples pins these semantics.
Negation (`!pattern`) is out of scope for version 1; the baseline is shaped
not to need it.

### 7.5 Decision emitter

One function produces every deny:

- stdout: `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"<reason>"}}`
- stderr: the same reason text
- exit code 2

Both channels are used because Claude Code documents the JSON deny as
blocking in every permission mode including `bypassPermissions` and
`dontAsk` (hooks-guide, "Hooks and permission modes"), while exit 2 is
documented to route the same way as deny and is what Codex honours together
with stderr. Hook output is always valid JSON, since under `onFailure:
"block"` malformed output itself becomes a block.

The reason format is `kk guard: <category> — <what matched>. Way through:
<remedy>`:

| Category | Remedy text |
|---|---|
| secrets | "this path is a secret file; ask the user for the value you need, or for a redacted copy" |
| destructive | "run it yourself by typing `! <command>` in the prompt; or disable the `<category>` category for this project in `~/.claude/kk-guard.json`" |
| selfmod | "guard and settings files are protected from agent edits; the user edits them directly" |
| failure | "the guard could not run (<cause>); nothing was executed; fix the guard or run the command yourself" |

Allowed calls produce no stdout and exit 0. The hook never emits
`permissionDecision: "allow"`: deny rules are evaluated regardless of hook
output, so an allow buys nothing and could only mislead.

When a config file is invalid (§8), an allowed call prints
`{"systemMessage": "<file>: <problem>"}` as the only key of the stdout object
(no empty `hookSpecificOutput`, whose schema expects `hookEventName`) and
exits 0.

## 8. Configuration layering

### 8.1 Project config, tighten only

`.claude/kk-guard.json`, committed with the repository. Listed in
`BUILTIN_EXCLUSIONS` in `template-sync.sh` and stripped from staging, so sync
neither overwrites it nor reports it as deleted.

Keys: `version`; `secrets` (globs to add, same shape lint); `destructive`
(map of category to rules to add; existing or new category names); `selfmod`
(paths to add). There are no removal keys. Unknown keys are reported and
ignored.

Invalid JSON or schema failure: the engine enforces the baseline, skips the
project additions, and returns a `systemMessage` naming the file and the
error. A committed typo therefore weakens nothing and is never silent. This
follows supercharger's isolated-custom-patterns rule: user-supplied rules are
evaluated separately so a bad one cannot disable the built-ins.

### 8.2 User config, loosen only

`~/.claude/kk-guard.json`, outside every repository. Keys: `version`;
`projects`, a map whose keys are `*` or an absolute path.

Resolution: the engine `realpath`s the project root (§7.2 step 1) and
selects two entries: `*`, and the single entry whose key is the longest path
prefix of the root. The effective entry is their **union**:
`disable_categories` and `allow_patterns` concatenated, `disable_selfmod`
true if either sets it. Shorter matching prefixes contribute nothing (`/work`
is ignored when `/work/ops` also matches). One entry for a parent directory
therefore covers nested checkouts and git worktrees.

Per-entry keys:

- `disable_categories`: list of destructive category names to switch off.
- `allow_patterns`: regexes tested against each normalised **simple command**
  on its own: every segment of §7.3 step 3 and every recursively extracted
  body of step 1, after wrapper skipping, with the prose view's quoting. A
  match exempts that one simple command from destructive rules only. With
  `^git clean -n`, the command `git clean -nd; rm -rf ./work` keeps the dry
  run and still denies the `rm`; a user does not have to anticipate shell
  composition in the regex.
- `disable_selfmod`: boolean. Needed wherever the agent is expected to edit
  settings or guard files: this repository, and any repository where asking
  the agent to add a `permissions.allow` entry to `.claude/settings.json` is
  routine (the `update-config` and `fewer-permission-prompts` skills do
  exactly that). The selfmod deny message names this key and file so the way
  through is one line, not a search.

Nothing in the user config touches secrets. An invalid user config is reported
through `systemMessage` and applies no loosening.

### 8.3 Effective policy

- Secrets: baseline ∪ project.
- Destructive: (baseline ∪ project) − disabled categories, with
  `allow_patterns` exempting individual commands.
- Self-modification: baseline ∪ project, switched off only by
  `disable_selfmod`. `allow_patterns` never exempt it.

### 8.4 Test overrides

`KK_GUARD_RULES`, `KK_GUARD_PROJECT_CONFIG`, `KK_GUARD_USER_CONFIG` and
`KK_GUARD_INTERPRETERS` redirect the respective inputs, following the
`CPR_PLUGINS_FILE` precedent in `cpr.py`. The hook process inherits the
harness environment, not the agent's shell environment, so the agent cannot
set them from a Bash call.

## 9. Generators and parity

`scripts/generate-guard.sh` (bash and `jq`), run by `make generate-guard`,
included in `make generate-all`. CI runs it and fails on
`git diff --exit-code` over every generated path. `jq` rather than a Go
generator because it preserves object key order and the repo already drives
every settings mutation through `jq`; Go's JSON encoder would reorder the
hand-authored keys of `settings.json`.

Projections:

1. **Settings baseline.** Replace `.permissions.deny` in the template
   `.claude/settings.json` with one `Read(<glob>)` per secrets glob, sorted.
   Nothing else lives in that array; `Bash(rm:*)` leaves settings because the
   hook owns destructive commands.
2. **Codex rules.** `.codex/rules/default.rules` becomes generated, with a
   do-not-edit header naming the source file. Each `codex` record on a rule
   renders one `prefix_rule(pattern = [...], decision = "forbidden",
   justification = "<reason>", match = [...], not_match = [...])` with that
   record's own examples; union tokens render as Starlark lists inside
   `pattern`. Only the five rules listed in §6.3 carry records, and the lint
   test fails if any other rule gains one, because a repository `forbidden`
   outranks every user-level rule on Codex and would silently disable §8.2
   loosening there. Codex validates each rule's `match`/`not_match` at load,
   so the examples live in the declaration next to the pattern they prove.
3. **Codex engine copy.** `guard.sh`, `guard.py` and `guard-rules.json`
   copied byte-for-byte to `.codex/scripts/guard/`. The generated Codex
   plugin ships no scripts, so the template is the only delivery path.
4. **Docs table.** A generated block in `docs/user-guide/configuration.md`
   between `<!-- BEGIN GUARD-RULES -->` and `<!-- END GUARD-RULES -->`,
   listing secrets globs, destructive categories and where each is extended
   or loosened. Same marker pattern as the vendored profile indexes.

Structure-test assertions: secrets globs pass the shape lint; destructive
rules use only the fields of §6.3 and `codex` records appear only on the
five permitted rules; regenerating into a temporary directory produces no
diff; the Codex copies compare identical to the plugin files; `hooks.json`
carries the all-channel matcher (including the three capy execution tools)
and `onFailure: "block"`.

`AGENTS.md` moves `.codex/rules/default.rules` from the hand-authored list to
the generated list and documents `make generate-guard`.

## 10. Template sync changes

In `template-sync.sh`:

- The settings merge keeps smart-merge semantics for every key except
  `permissions.deny`, which is set to the upstream array after the merge.
- Before replacing, compute downstream-only deny entries into a new tracking
  array. The terminal diff report and the PR markdown summary gain a section
  "Permission deny entries removed" listing them with guidance: secrets globs
  belong in `.claude/kk-guard.json` under `secrets`, destructive rules under
  `destructive`, and a repository that wants full control of settings adds
  `.claude/settings.json` to `sync_exclusions` (already documented). CI mode
  emits `dropped_deny_count`.
- `permissions.allow` stays union-merged: it is project convenience, not
  policy.
- `.claude/kk-guard.json` joins `BUILTIN_EXCLUSIONS` and is stripped from
  staging in `fetch_upstream_templates`.
- The `.codex/` tree syncs as today. The existing `hooks.json` ownership rule
  (toolbox owns entries whose command runs a script under `.codex/scripts/`)
  already covers the new patch hook.

Sync never deletes downstream files; this remains true.

## 11. Codex adapter and parity gaps

Verified facts about Codex that shape this section: hooks are enabled by
default; a PreToolUse matcher may use `Edit` or `Write` as aliases for
`apply_patch`; the payload carries `cwd`, `permission_mode` and
`tool_input.command` (the raw patch text for `apply_patch`); a block is a
JSON deny with a non-empty reason, or exit 2 with non-empty stderr; any other
non-zero exit, or exit 2 with empty stderr, fails the hook run and lets the
call proceed; hook `ask` is unsupported; Starlark rules offer only literal
`prefix_rule` tokens (plus `host_executable` and `network_rule`, neither
argument-aware), with `forbidden` > `prompt` > `allow`; and commands
containing wildcards, `$VAR`, redirection or substitution are not tokenised
but evaluated as a single `bash -lc` script.

Changes:

- **Bash hook.** `.codex/scripts/pretooluse-bash.sh` keeps capy step-aside
  detection and the legacy HTTP routing, but its substring denylist is
  replaced by a call to `.codex/scripts/guard/guard.sh` with the buffered
  payload on stdin, placed before the HTTP section so a deny wins. Every
  adapter exports `KK_GUARD_PROJECT_ROOT="$REPO_ROOT"` before delegating,
  because Codex sets no `CLAUDE_PROJECT_DIR` and the engine must not fall
  back to the payload `cwd` for glob anchoring (§7.2 step 1).
- **Patch hook.** New PreToolUse entry in `.codex/hooks.json` with matcher
  `Edit|Write` running `.codex/scripts/pretooluse-patch.sh`, which delegates
  to the wrapper. The engine handles `tool_name: apply_patch` as in 7.2.
- **MCP execution hook.** New PreToolUse entry with matcher
  `^mcp__[^[:space:]]+__capy_(execute|execute_file|batch_execute)$` running
  `.codex/scripts/pretooluse-mcp.sh`, which delegates to the wrapper. Capy's
  own entry for the same tools stays; hooks are additive and a deny from
  either blocks. This entry is toolbox-owned under the existing `hooks.json`
  ownership rule (its command runs a script under `.codex/scripts/`).
- **Fail-open mitigation.** All three adapter scripts trap unexpected
  failures into a stderr message and exit 2. The wrapper writes stderr on
  every exit-2 path.
- **Advisory for `read_file`.** `session-start.sh` renders the secrets globs
  from `.codex/scripts/guard/guard-rules.json` into its injected context at
  runtime, so the uninterceptable read path carries the current list without
  a further generated artifact.
- **Rules.** Generated as in §9 for `rm`, `shred`, `sudo`, `su`, `doas`
  only. Because the rules layer forbids literal `rm`, there is effectively no
  temp exemption on Codex, and because a repository `forbidden` outranks
  user-level rules, `filesystem` (its `rm`/`shred` part) and `privilege`
  cannot be loosened on Codex through §8.2. `git` and `infra` are hook-only
  there and loosen exactly as on Claude Code.

Parity gaps, documented in `docs/providers/codex.md`:

| Gap | Reason | Mitigation |
|---|---|---|
| `read_file` of secrets not enforced | Codex hooks cannot intercept it (ADR 0005) | advisory list in session context; optional sandbox permission profile (stretch task) |
| `rm` has no temp exemption; `rm`, `shred`, `sudo`, `su`, `doas` cannot be loosened by user config | Starlark is literal-only and most-restrictive-wins across files (verified codex-cli 0.164.0) | documented; user runs scratch cleanup; a repository that must loosen these adds `.codex/rules/default.rules` to `sync_exclusions` and edits it |
| function-style `apply_patch` may bypass hooks | Codex docs: "treat tool hooks as a useful guardrail, not a complete enforcement boundary" | documented |

Optional stretch (separate task, droppable): a Codex sandbox permission
profile with `[permissions.<name>.filesystem]` denies for the secrets globs,
generated into `config.toml`. The feature is marked Beta and the sync's TOML
merge must preserve the table; verify before relying on it.

## 12. Security considerations

What the guard protects against: an agent deleting or rewriting work by
accident; an agent reading credentials into the transcript; a prompt
injection steering the agent toward either; an agent editing the guard's own
configuration to escape it.

What it does not protect against: a human who approves or runs the command
themselves (by design); a repository that installs a mod which approves
denied calls (the docs note this is possible without managed settings or a
Team login); content-level leakage through Grep or Glob results (only the
search root is checked); interpreter code that assembles a protected path by
concatenation; function-style `apply_patch` on Codex; execution tools other
than Bash, `apply_patch` and the three capy execution tools (a third-party
MCP shell server is not inspected; adding one means adding its matcher and a
payload mapping in §7.2).

The self-modification rule has a deliberate cost: it blocks the ordinary
request to add a `permissions.allow` entry to `.claude/settings.json`,
because the deny baseline and the hook registration live in that file and a
rule that protects them cannot tell the two edits apart. The deny message
hands the user the one-line `disable_selfmod` entry (§8.2); the
configuration guide documents it next to the rules table.

Threat ordering follows the data: deny decisions are reachable in every
permission mode; configuration can only tighten inside a repository; the
loosening file lives outside any clone and is itself write-protected.

## 13. Testing strategy

**Corpus.** `test/fixtures/guard/corpus.jsonl`, one case per line: tool
name, input, optional `cwd`, expected `allow` or `deny`, expected category,
note. Must-allow: a `find` excluding `.git/`; `cat .env.example`; a heredoc
commit message naming `build/` and `dist/`; reading logs, `node_modules`,
lockfiles, build output; `rm -rf /tmp/kk-test`; `git branch -d`;
`git rebase`; `git commit --amend`; `kubectl get`; `terraform plan`.
Must-deny: `cat .env`; `/bin/rm`; `sh -c 'rm -rf x'`; `xargs rm`; `rm -rf ~`;
`rm -rf .` from the project root; `rm "$T"`; `sudo`; every git rule;
`find -delete`; `rsync --delete`; the infra rules; `cat ~/.ssh/id_rsa`;
redirects, `tee` and `sed -i` into settings and guard files; inline Python
`open(..., 'w')` on settings; a Read of `.env`; an Edit of the user settings;
a Grep rooted at `~/.aws`; an `apply_patch` updating `.env`.

Cases added by the 2026-10-25 reviews, each paired with its benign
neighbour: `cat ../.env` with payload `cwd` at `<root>/sub` (deny) and
`cat ../README.md` (allow); `cd /work/project && rm -rf ./work` with payload
`cwd` under `/tmp` (deny), `env -C /work/project rm -rf ./work` (deny),
`cd /tmp/kk-test && rm -rf ./x` (allow, literal absolute `cd`); `sh -c 'rm
-rf x'` and `echo "$(rm x)"` (deny, quoted bodies survive extraction);
`cat "/repo with spaces/.env"` (deny); `cat <<EOF` whose body contains
`$(rm -rf x)` (deny) beside the quoted-delimiter commit message (allow);
`mv .codex/hooks.json /tmp/saved.json` (deny), `mv .codex /tmp/` (deny),
`mv src/a.go src/b.go` (allow); with user `allow_patterns: ["^git clean -n"]`,
`git clean -nd; rm -rf ./work` (deny) and `git clean -nd` (allow);
`capy_execute` shell `cat .env` (deny), python `open('.env').read()` (deny),
`capy_batch_execute` with `go test ./...` (allow), `capy_execute_file` on
`.env` (deny); `cert.pem` Read (deny, the accepted false positive); a Read of
`.env` with no project or user config present (deny: the plugin-only case).

**Python in-process tests.** `test/guard/test_guard.py` imports the engine
and replays the corpus; unit tests for the glob matcher (fixture table from
the docs' examples), tokenizer (structural extraction before defanging,
wrapper skipping, segmentation, directory tracking), symlink resolution (a
`/tmp` link to home), config merge (removal keys ignored, invalid config
behaviour, `*` plus longest-prefix union, per-simple-command allow
patterns), rule predicates (`flags_all`, `flags_none`, ordered
`subcommand`), emitter output.

**Bash contract tests.** `test/test-hooks.sh` rewritten for the wrapper:
exit 0 and empty stdout on allow; exit 2, valid JSON and non-empty stderr on
deny; a Read of `.env` denied with no configs present; fail-closed with an
empty interpreter list and with a corrupted rules file; latency: 100 Read
payloads with p95 under 30 ms and Bash-path p95 under 50 ms, always printed,
asserted only when `CI` is unset and then only beyond twice the budget.

**Codex and sync tests.** `test/test-codex-hooks.sh` swaps denylist assertions
for guard delegation, adds patch-hook and MCP-hook cases, the fail-open
mitigation, and one check that each adapter exports `KK_GUARD_PROJECT_ROOT`
(a `cat ../.env` payload with `cwd` at a subdirectory is denied). Where the
`codex` CLI is installed, `codex execpolicy check` runs against the generated
rules file for `rm -rf x` (forbidden) and `ls` (no match) and the suite
records the CLI version.
`test/test-template-sync.sh` adds deny replacement, dropped-entries report,
allow still unioned, the new exclusion. `test/test-plugin-structure.sh` gains
shape lint, freshness and copy-identity checks. `test/test-codex-structure.sh`
checks the generated-file header and the patch hook entry.

## 14. Migration and rollout

Two independent channels deliver the change: hook logic via plugin update,
settings replacement and Codex files via template sync. Both intermediate
states are safe. Plugin first: the new hook runs beside the old noise denies
until sync removes them (over-restricted, never under-protected). Sync first:
trimmed settings run beside the old substring hook until the plugin updates
(`cat .env` still denied on Bash). Neither order weakens secrets protection.

The plugin version bumps a minor. `validate-bash.sh` is deleted; the structure
test that asserts its existence is updated to assert the `guard/` files
instead.

One regression is accepted and stated here so the ADR can carry it: a
consumer who runs with hooks disabled (`disableAllHooks`) keeps the secrets
baseline through Layer 1 but loses the `rm` guard, because `Bash(rm:*)`
leaves `permissions.deny` (§9). It has to leave: a settings deny cannot be
loosened by the hook, so keeping it would make the temp exemption and the
`filesystem` category toggle impossible. Layer 1 is the hooks-off fallback
for secrets only.

Developing this repository with an agent requires a user-level entry for the
toolbox path with `disable_selfmod: true`. Documented in
`docs/contributing/plugin-development.md`.

## 15. Documentation and ADR changes

- `docs/user-guide/configuration.md`: generated rules table replaces the
  permission-baselines prose; hooks table describes the guard; new subsection
  on project and user config files.
- `docs/user-guide/template-sync.md`: merge section records that
  `permissions.deny` is replaced and dropped entries appear in the summary.
- `docs/providers/claude-code.md`, `docs/providers/codex.md`: hook
  description, parity gaps.
- `docs/getting-started/plugin-only.md`: hook covers all channels.
- `docs/contributing/plugin-development.md`: fail-closed hook contract
  replaces "always exit 0"; toolbox-repo `disable_selfmod` note.
- `docs/contributing/testing.md`, `docs/contributing/architecture.md`,
  `klaude-plugin/README.md`, `AGENTS.md`: file lists, suites, make target.
- `docs/adr/0012-permission-guard-single-declaration.md`: Context (add-only
  merge, substring false positives, three intents), Decision (one declaration
  rendered to three channels; tighten-only project config, loosen-only user
  config; flat deny for destructive commands in every mode; Codex forbids
  limited to unconditional literals), Consequences (rejected alternatives,
  Codex gaps, the hooks-off `rm` regression, revisit conditions). Cites
  operative plugin files; plugin files do not cite it back. 0010 and 0011 are
  taken (`0010-proportionate-verification.md`,
  `0011-isolated-review-external-backend.md`); the implementer re-checks the
  next free number at the time of writing.
- `docs/adr/0005-codex-hook-enforcement-gap.md`: dated update noting the
  `apply_patch` hook exists and the advisory list is rendered from the
  declaration.
- `docs/contributing/adrs.md`: add the 0012 row. The index currently lacks
  rows for 0008, 0009 and 0011; adding them is adjacent cleanup, flagged for
  the implementer to confirm with the user rather than done silently.

## 16. Assumptions

Each is a testable bet the design depends on:

1. Wrapper plus engine evaluate a file-tool payload (Read, Grep, Glob, Edit,
   Write) in under 30 ms p95: interpreter start dominates, the work is a JSON
   parse and a handful of regex matches. Test: 100 Read payloads, p95
   printed, asserted locally.
2. Full Bash evaluation under `python3 -I` stays under 50 ms p95 on the
   corpus. Linux interpreter start measured at 10 ms; macOS unmeasured.
3. The glob matcher reproduces Claude Code deny semantics for the three
   explicit shapes. Test: fixture table from the docs' examples.
4. Exit 2 blocks under `bypassPermissions` in Claude Code. The JSON deny is
   documented to; exit 2 is inferred. Test: one throwaway hook run under the
   bypass flag, recorded in this document.
5. Codex `apply_patch` header paths are relative to the payload `cwd`. Test:
   one real Codex session.
6. Downstream repositories carry no deny entries upstream never shipped, so
   replace semantics lose nothing. Sync reports dropped entries regardless.
7. `python3` at 3.8 or newer exists on every consumer machine, as `cpr.py`
   already assumes. The engine avoids syntax newer than 3.8.
8. The heredoc-stripping heuristic (data-sink consumers only) removes
   commit-message prose without hiding shell bodies. Test: corpus cases for
   both.

## 17. Not Doing

- Context-protection rules in any layer. Read truncation, Bash output
  persistence and capy own that.
- Project-data rules (`*.csv`, `data/`, `./examples`). Obsolete; a project
  adds its own.
- Ask or mode-aware decisions for destructive commands. Rejected for now;
  revisit if flat deny proves too restrictive.
- Project-level loosening. Clone safety.
- Content-level filtering of Grep and Glob results. Only the search root is
  checked.
- Negation patterns in guard config. The baseline is shaped not to need them.
- Codex `read_file` enforcement. ADR 0005 stands; the sandbox permission
  profile is an optional stretch task.
- Pre-edit backups. Claude Code checkpointing covers it.
- Download-pipeline and code-execution rules (`curl | sh`). Not data-losing;
  capy owns HTTP.
- Windows support for the wrapper. Documented as requiring Git Bash.
- A forensic deny ledger. The deny reason lands in the transcript.
- Execution channels beyond Bash, `apply_patch` and the three capy execution
  tools. A third-party MCP shell server needs its own matcher and payload
  mapping; none is in use here.
- Tracking non-literal directory changes in Bash. A `cd "$DIR"` or `cd ..`
  marks the execution directory uncertain and the temp exemption falls back
  to absolute paths; full shell emulation is out of scope.

## 18. Rejected alternatives

| Alternative | Why it lost |
|---|---|
| Sync retirement list (remove entries upstream once shipped) | hand-maintained list that only covers entries upstream remembers shipping |
| Leave sync alone, document hand-editing | the original complaint |
| Hook on Bash and edit tools only | downstream secrets rules would cover some channels and not others, which is worse than none |
| Context protection as hook `ask`, advisory context, or command rewrite | friction, duplication of capy's tip, or silent semantic change |
| Destructive commands as an `ask` tier | non-default permission modes are common; an ask is only worth something where a human is guaranteed to see it |
| Mode-aware: ask in supervised modes, deny otherwise | feasible (payload carries `permission_mode`), but the user chose the blunt guarantee for now |
| Project-level loosening behind self-modification denies | travels with the clone; the Bash channel of the protection is a regex arms race |
| Tighten-only everywhere, no loosening | ops repositories where `kubectl delete` is the daily job become unusable |
| Direction A: Python engine with test-enforced parity, no generator | three hand-edited lists that a test catches drifting after the fact |
| Direction B: pure bash engine | rebuilds the substring approach that produced today's false positives; symlink and glob machinery in bash 3.2 |
| Go generator | `encoding/json` reorders the hand-authored keys of `settings.json` |
| Read/Grep/Glob skip path when no guard config exists | plugin-only installs have no settings baseline, so the skip would have removed the only read-channel layer exactly there (review R1, 2026-10-25) |
| Codex `forbidden` rule for every destructive rule | a repository rule outranks user-level rules on Codex, which would make §8.2 loosening dead for ops repositories; forbids are kept only for literals nobody loosens (review R6) |
| Defang before structural extraction (the earlier §7.3 order) | turns `sh -c 'rm -rf x'` into `sh -c Q` before recursion sees it; safe-claude-code itself extracts bodies from the raw text (review R2) |

## 19. Borrowed from

- **safe-claude-code** (`~/Projects/personal/safe-claude-code/hooks/`): the
  fail-closed wrapper (`-I`, absolute interpreters, exit 2 on every failure
  path), the tokenizer (basename resolution, wrapper skipping, quote
  defanging, inline-interpreter and `sh -c` inspection), protected-path
  checks on edit tools, and the deny-message shape that hands the action to
  the human. Not taken: the blanket deny list, root-owned managed settings,
  pre-edit backups.
- **claude-supercharger** (`hooks/safety.sh`, `hooks/lib-deny.sh`,
  `hooks/cmd-normalize.sh`): categories with toggles and allow patterns
  (relocated to the user level), additive custom patterns evaluated in
  isolation, cross-channel self-modification protection that no config can
  exempt, the decision-emitter insight that only the reason string reaches
  the model, per-segment splitting, and the structural fast path. Not taken:
  the hook count, the state-directory sprawl, project-level loosening, bash
  as the engine.

## 20. Verified facts and sources

Facts established by isolated verification on 2026-10-20 (Chain-of-Verification,
six sub-agents) and by two docs-lookup agents earlier the same day:

- Claude Code hooks: payload carries `permission_mode` with values `default`,
  `plan`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`; PreToolUse
  `hookSpecificOutput` supports `additionalContext`; `onFailure: "block"`
  requires 2.1.295; a hook `permissionDecision: "deny"` blocks in every mode
  including bypass (hooks-guide); exit 2 routes the same way as deny; hook
  `ask` forces a prompt in auto mode. Sources: code.claude.com/docs/en/hooks,
  /hooks-guide, /permissions, /permission-modes.
- Claude Code permission rules: gitignore syntax; `*` within a segment, `**`
  across; `//`, `~/`, `/`, `./`/bare anchors; bare filenames match at any
  depth; deny rules match requested and resolved paths; `Read` deny also
  blocks Edit and Write and applies best-effort to Grep and Glob; `Write(...)`
  rules are never consulted; separators `&&`, `||`, `;`, `|`, `|&`, `&`,
  newline; deny > ask > allow across scopes. Source: /permissions.
- Codex rules and hooks: as summarised in §11. Sources:
  developers.openai.com/codex/rules, /hooks, /permissions; `openai/codex`
  `codex-rs/execpolicy` and `codex-rs/hooks` sources.
- CPython `-I` implies `-E`, `-P`, `-s`; macOS `/usr/bin/python3` is a
  Command Line Tools shim. Sources: docs.python.org/3/using/cmdline.html,
  `xcode-select(1)`.

Facts established during the 2026-10-25 design reviews, by running
`codex execpolicy check` (codex-cli 0.164.0) against throwaway rules files:

- A `prefix_rule` pattern token may be a list of literal alternatives
  (`["git", "push", ["--force", "-f"]]`); `git push -f origin main` matches
  it and `git push origin main` does not.
- A rules file fails to parse when a rule's `match` example does not match
  that rule's own pattern ("expected every example to match at least one
  rule"), even when another rule in the same file would match it.
- With a project rule `forbidden` and a user rule `allow` for the same
  prefix, the decision is `forbidden`.
- safe-claude-code's `check_command` runs `substitution_bodies` and
  `strip_quotes` on the raw command and applies `defang` only to the
  pattern-level checks (`hooks/guard.py`, `check_command` and
  `check_shell_text`).
- `.codex/hooks.json` already registers capy's own PreToolUse matcher for the
  capy MCP tools separately from the toolbox Bash matcher; capy's tools
  accept `language`, `code`, optional `cwd` (`capy_execute`), `path`
  (`capy_execute_file`) and `commands[].command` (`capy_batch_execute`).
