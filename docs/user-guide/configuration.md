# Configuration

The machine installation supplies a Claude launch layer and Codex launch settings. Repositories can keep their own settings, instructions and project guard policy.

## How Configuration Works

Edit `${XDG_CONFIG_HOME:-$HOME/.config}/kk/config.json` for personal toolbox preferences. All keys are optional. Merge the keys you need into an existing file.

```json
{
  "launchNotice": false,
  "claude": {
    "defaults": {"skills": false},
    "optIn": {"webSearch": true},
    "settings": {"effortLevel": "medium"}
  },
  "codex": {
    "defaults": {"tui": false},
    "settings": {"model_reasoning_effort": "high"}
  }
}
```

**Claude.** Each `kk claude` launch builds a settings layer. The default effort is `high`. Baseline preferences yield to explicit user, project and local values, including individual environment variables. The baseline leaves model selection to Claude or the adopter. You can supply `claude.settings` and a `claude.settingsFile` path (relative to the override file or absolute). The file takes precedence over `claude.settings` for scalar preferences. A caller’s own `--settings` is composed too. The launcher appends the generated native secret denies to the final layer. Inspect it with `kk claude --print-layer`.

| Claude permission or preference | Machine default |
| --- | --- |
| `Skill(kk:*)` | Standing authorization for model-initiated calls to every matching skill, **including skills added by future releases**. Set `claude.defaults.skills` to `false` to review skill use individually. |
| Read access to the active release | Lets skills and reviewers read their bundled criteria. Set `claude.defaults.readRelease` to `false` to opt out. PAL needs a separate grant for its temporary review files. |
| `Bash(mkdir:*)` and `WebSearch` | Opt in separately with `claude.optIn.mkdir` and `claude.optIn.webSearch`. The legacy grants for `cat`, `grep`, `ls` and `sort` are dropped. |
| Statusline and instructions | The launcher supplies the statusline in trusted interactive wrapped sessions with hooks enabled. Set `claude.defaults.statusLine` to `false` to opt out. The plugin supplies behavioral instructions at session start and supports `claude.instructions`. |

**Codex.** Each `kk codex` launch passes its settings to plain `codex` as `-c` flags. The release defaults yield to a value set anywhere else: `config.toml`, trusted project configuration or your command line. Your `codex.optIn` and `codex.settings` values take precedence over `config.toml` and yield to trusted project configuration and to your own CLI flags. [Launch settings](../providers/codex.md#launch-settings)

- `codex.defaults` switches a release default off, so that Codex uses its own value. Its keys are `model`, `model_reasoning_effort`, `model_context_window`, `model_auto_compact_token_limit`, `project_doc_max_bytes`, `agents` and `tui`; set one to `false`.
- `codex.settings` sets Codex values, including your own value for a release default. Use the names Codex reports. Two release defaults have aliases that stop `kk apply`: write `agents.max_concurrent_threads_per_session` and `tui.effects.starfield`, not `agents.max_threads` and `tui.whimsy`. Top-level keys are plain names, with nested tables written as JSON objects.
- These values appear in the Codex command line. Keep `mcp_servers`, `model_providers`, `shell_environment_policy` and `otel` in `config.toml`; kk rejects them here. Write path values as absolute paths: Codex resolves a relative path in a flag from the directory it starts in. Configure hook and plugin enablement in native Codex settings too.

After editing overrides, run `kk apply`. It checks the values with your Codex CLI and updates the active release’s owned files offline. `kk status` and `kk codex` report pending edits.

There are two independent opt-ins:

1. **Approval and sandbox defaults.** Enable the values you want under `codex.optIn`: `"approval_policy": true` supplies `on-request`, `"approvals_reviewer": true` supplies `user`, and `"sandbox_mode": true` supplies `read-only`. Otherwise the machine owner’s native settings govern. With a sandbox or approval flag on the command line (`-s`/`--sandbox`, `-a`/`--ask-for-approval`, `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox` or `--yolo`), kk passes none of these three values for that launch. Migrated repositories keep their existing three project values until someone removes them.
2. **Account-wide native forbids.** Set `"nativeForbids": true` under `codex.optIn` and run `kk apply` to install `$CODEX_HOME/rules/kk.rules`. Those rules apply to **bare Codex and unrelated repositories** using that Codex home. Project settings and guard exceptions cannot loosen a native forbid. Switch it off and run `kk apply` to remove the toolbox-owned file.

Machine updates replace the previous per-repository sync PRs. Review the chosen release before upgrading. A local user install covers sessions that load its plugin. Hosts without it, including fresh CI runners and cloud sessions, need separate provisioning if migration removes committed plugin enablement. See the [migration guide](template-sync.md) for team-wide effects.

## Permission Baselines

The permission guard separates secrets, destructive operations and changes to its own configuration. Its baseline allows ordinary logs, dependencies, build output and `.env.example`; projects can add their own restrictions. A settings allow entry cannot override a secrets deny.

The tables below are generated from `klaude-plugin/scripts/guard/guard-rules.json` with `make generate-guard`. The hook enforces the shared declaration. Wrapped Claude sessions also receive the native deny list. Project additions belong in `.claude/kk-guard.json`. Keep per-repository MCP tool permissions in `.claude/settings.local.json`.

Self-modification protection also blocks an agent from adding an allow entry to `.claude/settings.json` or `.claude/settings.local.json`. The `disable_selfmod` example below lets the user authorize those edits for a chosen project; it does not loosen secrets.

<!-- BEGIN GUARD-RULES -->
### Secrets

These globs generate the Claude settings deny list and apply in the guard. Add project globs in `.claude/kk-guard.json` under `secrets`; user exceptions never loosen secrets.

| Scope | Glob |
|-------|------|
| Project | `./**/*.kubeconfig` |
| Project | `./**/*.pem` |
| Project | `./**/*.tfstate` |
| Project | `./**/*.tfstate.backup` |
| Project | `./**/.env` |
| Project | `./**/.env.*.local` |
| Project | `./**/.env.local` |
| Project | `./**/.kube/**` |
| Project | `./**/.terraform/**` |
| Project | `./**/id_ecdsa` |
| Project | `./**/id_ed25519` |
| Project | `./**/id_rsa` |
| Project | `./**/kubeconfig` |
| Project | `./**/kubeconfig.yaml` |
| Project | `./**/kubeconfig.yml` |
| Project | `./**/service-account*.json` |
| Home | `~/.aws/**` |
| Home | `~/.claude/.credentials.json` |
| Home | `~/.config/gcloud/**` |
| Home | `~/.config/sops/age/**` |
| Home | `~/.docker/config.json` |
| Home | `~/.gnupg/**` |
| Home | `~/.kube/**` |
| Home | `~/.netrc` |
| Home | `~/.pypirc` |
| Home | `~/.ssh/**` |
| Home | `~/Library/Application Support/sops/age/**` |

### Destructive commands

Add rules in project config under `destructive`. User config at `~/.claude/kk-guard.json` can disable categories or exempt individual commands with `allow_patterns`. Native Codex forbids take precedence over those exceptions.

| Category | Command | Denied operation | Codex forbid |
|----------|---------|------------------|--------------|
| filesystem | `rm` | rm deletes files and directories with no undo | Yes |
| filesystem | `shred` | shred overwrites file contents before deleting them | Yes |
| filesystem | `find` | find -delete removes every file the search matches | No |
| filesystem | `rsync` | rsync --delete (and its --del alias) removes destination files missing from the source | No |
| git | `git clean` | git clean deletes untracked files, which are not recoverable from git | No |
| git | `git reset` | git reset --hard discards every uncommitted change | No |
| git | `git checkout` | git checkout -- &lt;path&gt; and git checkout . discard uncommitted edits | No |
| git | `git restore` | git restore without --staged discards uncommitted edits in the working tree | No |
| git | `git restore` | git restore --worktree discards uncommitted edits in the working tree even alongside --staged | No |
| git | `git branch` | git branch -D deletes a branch even when it is not merged | No |
| git | `git branch` | git branch --delete --force (also -d -f and -df) deletes a branch even when it is not merged | No |
| git | `git push` | force pushes and remote deletes rewrite or remove history that may exist only on the remote | No |
| git | `git stash drop` | git stash drop discards stashed work that git cannot recover | No |
| git | `git stash clear` | git stash clear discards every stash entry | No |
| infra | `terraform destroy` | terraform destroy tears down live infrastructure | No |
| infra | `terraform apply` | terraform apply -destroy tears down live infrastructure | No |
| infra | `kubectl delete` | kubectl delete removes live cluster resources | No |
| infra | `helm uninstall` | helm uninstall removes a live release and its resources | No |
| infra | `helm delete` | helm delete removes a live release and its resources | No |
| infra | `docker rm` | docker rm removes containers and their writable layers | No |
| infra | `docker rmi` | docker rmi removes images | No |
| infra | `docker container rm` | docker container rm removes containers and their writable layers | No |
| infra | `docker image rm` | docker image rm removes images | No |
| infra | `docker system prune` | docker system prune removes every unused container, network and image | No |
| infra | `docker volume rm` | docker volume rm deletes persistent data volumes | No |
| infra | `docker volume prune` | docker volume prune deletes every unused data volume | No |
| decryption | `sops` | sops -d (--decrypt) outputs the plaintext of an encrypted secrets file | No |
| decryption | `sops decrypt` | sops decrypt outputs the plaintext of an encrypted secrets file | No |
| decryption | `sops exec-env` | sops exec-env hands decrypted secrets to a command through its environment | No |
| decryption | `sops exec-file` | sops exec-file hands decrypted secrets to a command through a temporary file | No |
| decryption | `sops edit` | sops edit opens the plaintext of an encrypted secrets file in $EDITOR | No |
| privilege | `sudo` | sudo runs a command as the administrator | Yes |
| privilege | `su` | su switches to another user account | Yes |
| privilege | `doas` | doas runs a command as another user | Yes |

The hook exempts literal `rm` targets strictly beneath its temporary roots: `/tmp`, `/private/tmp`, `/var/folders`, `/private/var/folders`, `$TMPDIR`. Secrets and protected configuration still apply. Codex native rules forbid `rm` even for temporary targets.

### Protected configuration

The guard blocks mutations of these paths, including moving their parent directories:

- `.claude/settings.json`
- `.claude/settings.local.json`
- `.claude/kk-guard.json`
- `~/.claude/settings.json`
- `~/.claude/settings.local.json`
- `~/.claude/kk-guard.json`
- `.codex/hooks.json`
- `.codex/rules/**`
- `.codex/scripts/**`
- `~/.claude/plugins/**`
- `$KK_HOME/**`
- `$XDG_CONFIG_HOME/kk/config.json`
- Each path recorded in `$KK_HOME/state.json` under `installed_paths`, including the `~/.local/bin/kk` launcher, the opt-in Codex rules file and toolbox sub-agents.
- `$CODEX_HOME/plugins/cache/**`

The toolbox home defaults to `${XDG_DATA_HOME:-~/.local/share}/kk`. The configuration and Codex homes default to `~/.config` and `~/.codex`. A file in a shared directory becomes protected when the installer records its exact path. Reads still follow the secrets policy.

When copying an unrelated executable into `~/.local/bin/`, name its destination file explicitly. A directory-only destination is checked as a parent of the protected `kk` launcher.

Project config may add paths under `selfmod`. To let an agent edit settings or guard files for one checkout, the user can add this entry to `~/.claude/kk-guard.json` (substitute the absolute project path):

```json
{"version":1,"projects":{"/absolute/path/to/repo":{"disable_selfmod":true}}}
```

This exception does not allow reading or writing secrets.
<!-- END GUARD-RULES -->

## Guard Configuration

The baseline ships inside the Claude plugin and runs even when neither configuration file exists. The standalone Codex guard plugin carries the same engine and declaration. These files are independent of provider permission settings:

| File | Owner and purpose |
|------|-------------------|
| `<project>/.claude/kk-guard.json` | Committed project restrictions; adds secrets globs, destructive rules or protected paths |
| `~/.claude/kk-guard.json` | Machine owner's exceptions; loosens destructive categories or self-modification protection for selected projects |

### Project restrictions

Project configuration only adds protection. For example:

```json
{
  "version": 1,
  "secrets": ["./**/local-secrets.json"],
  "selfmod": [".project-policy.json"],
  "destructive": {
    "deployment": [
      {"program": "deploy", "subcommand": "prod", "reason": "deploy prod changes production"}
    ]
  }
}
```

Secrets globs use `./**/` for project paths, `~/` for home paths, or `//` for absolute paths. They match requested and resolved paths. Project-relative policy stays anchored to the project root even when a shell runs in a subdirectory. Destructive rules use `program`, optional ordered `subcommand`, argument regex lists `flags_any`/`flags_all`/`flags_none`, and a `reason`; use the shipped declaration as the complete rule reference. The only supported named exemption is `targets_under_tmp`. Project config cannot disable categories or remove baseline rules. Template sync leaves this project-owned file alone.

### User exceptions

The user edits this file directly; the guard protects it from agent writes. Merge entries into an existing `projects` object rather than replacing other project entries. For example:

```json
{
  "version": 1,
  "projects": {
    "*": {"allow_patterns": ["^git clean -n"]},
    "/absolute/path/to/ops": {"disable_categories": ["infra"]},
    "/absolute/path/to/agentstakk": {"disable_selfmod": true}
  }
}
```

Use physical absolute project paths (`pwd -P`). The engine combines `*` with the single longest matching directory prefix; shorter matching prefixes contribute nothing. Lists are combined, and `disable_selfmod` is enabled if either selected entry enables it. A parent path covers nested repositories and worktrees.

`allow_patterns` applies separately to each normalized simple command, including extracted shell bodies. Thus `^git clean -n` can exempt `git clean -nd`, but not the `rm` in `git clean -nd; rm -rf ./work`. These patterns never exempt secrets or protected configuration. For sessions in the selected project, `disable_selfmod` permits edits to every path listed under **Protected configuration**, including the machine installation and plugin cache. The secrets policy still applies. On Codex, installed native forbids for `rm`, `shred`, `sudo`, `su` and `doas` still win over guard exceptions.

Missing config files leave the baseline active. Invalid JSON or invalid supported values produce a visible `systemMessage` and skip that file's changes; the other valid layer still applies. Unknown keys are reported and ignored. Secrets are never loosened by user configuration.

## Hooks

The Claude plugin ships three hook handlers. It needs Bash, `jq`, Python 3.9+ and Claude Code 2.1.295+ for the declared [`onFailure: "block"` behavior](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails).

| Hook | Trigger | Description |
|------|---------|-------------|
| Plugin root export | `SessionStart` | Exports `TOOLBOX_PLUGIN_ROOT` into the session environment so every Bash call has a reliable path to the plugin installation directory |
| Session instructions | `SessionStart` on startup, resume, clear and compaction | Supplies the plugin’s behavioral instructions. Git-marketplace installs also supply plugin-root guidance. Each legacy project instruction file takes precedence over the corresponding hook text. |
| Permission guard | `PreToolUse` on `Bash`, `Read`, `Grep`, `Glob`, `Edit`, `Write`, `NotebookEdit`, and capy execution tools | Enforces secrets, destructive-command rules, and protected configuration paths; denies on guard failures |

Ordinary allowed calls produce no output and exit 0; invalid-config warnings may emit `systemMessage`. Denials emit JSON, a reason on stderr, and exit 2. Missing/broken interpreters, a corrupt declaration, crashes and malformed engine output deny the call. Claude also blocks hook failures/timeouts through `onFailure: "block"`. A machine without a working Python interpreter blocks every matched tool, including reads, until repaired.

Codex adapters preserve the guard's denial reason and exit status. A normal policy denial does not mean the hook needs repair; the separate "adapter could not run" diagnostic indicates an adapter failure, such as a missing guard wrapper or unreadable hook input.

The wrapper runs the standard-library-only engine with `-I -S`, isolating Python environment/user-site settings and skipping unused site startup. On macOS it prefers Python at the standard Homebrew locations, then system Python; elsewhere it checks system Python first. PATH lookup remains the final fallback. Homebrew is not required.

Destructive operations are denied in every permission mode, including bypass mode. The reason names the matched category and the way through: the user runs the operation directly or configures an applicable exception. Disabling Claude hooks removes destructive and self-modification protection. Wrapped Claude sessions also carry the native secret denies. Bare Claude, the IDE extension and desktop sessions rely on the loaded plugin hook for the toolbox guard after migration.

The guard checks `capy_execute`, `capy_execute_file`, and `capy_batch_execute` even when capy is registered under a different MCP server name. Shell code uses the same checks as Bash; other languages use the literal-path, write-call and spawned-command scans described below. Every batch command is checked independently, and one denied command blocks the entire batch before execution.

For capy code, omitted `cwd` means the project root. Relative cwd overrides resolve from that root; absolute overrides select that directory. Each batch command starts in the selected directory. The `capy_execute_file.path` input stays project-root-relative regardless of where its processing code runs. These path parameters are literal paths, without shell-variable or tilde expansion.

Code in other languages, whether sent to capy or passed inline to an interpreter in Bash (`python3 -c`, `node -e`, a heredoc), is also checked for the commands it starts. The check is lexical. It runs when the code, with its line comments removed, names a process-starting call (`subprocess`, `os.system`, `child_process`, `exec(`, `spawn`, `popen`, `exec.Command` and similar) or contains a backtick string. Only the code counts here: a call that is merely named inside a string or a comment does not, except that a string which is exactly a spawn module's name (`"child_process"`, `"subprocess"`, `"os/exec"`) is taken for an import. Every string literal is then read as a possible command and the destructive rules apply: a command string such as `os.system("git reset --hard")`, or adjacent literals forming an argument list such as `["kubectl", "-n", ns, "delete", "pod", name]`. Category exceptions and `allow_patterns` apply as in Bash, where an exception matches a whole command: one that the code is still building, such as `"rm -rf build " + extra`, is matched with its unknown operand, as `rm -rf build $extra` would be. This is stricter than Bash in one respect: while a command is still being built, no exception applies to anything in it, including a complete command chained before the continuation or nested in a shell body, and a string passed through `.split()` counts as still being built. Code that names no such call keeps its literals as data. A literal that merely looks like a destructive command, in code that does name one, is denied.

The temporary-cleanup exemption is narrower here than in Bash. It applies only when the whole command is handed directly to a recognised spawn call, as a closed literal list or a single string, and every target is an absolute path under a temporary root: `subprocess.run(["rm", "-rf", "/tmp/build"])`. A command that is kept in a variable, concatenated, formatted or given a relative target does not earn it, because the guard cannot see what finally runs. Nor does one whose call takes further operands, as in `exec.Command("rm", "-rf", "/tmp/build", extra)`. One known gap remains: a Node shell line followed by a variable argument list, `spawnSync("rm -rf /tmp/build", args, {shell: true})`, is treated as whole although Node appends `args`.

Deleting through a library call is treated as `rm`, whether or not the code starts a process. The recognised calls are Python's `shutil.rmtree` (also as `rmtree` imported by name), `os.remove` and `os.unlink`; Node's `fs.rm`, `fs.rmdir` and `fs.unlink` with their `Sync` forms, also when `rmSync`, `rmdirSync` or `unlinkSync` is imported by name; an `unlink(...)` function, whose target counts as unknown when it is given several; and an `.unlink()` method called without a positional argument, as on a `pathlib` path. A bare `rm(...)` or `rmdir(...)` is not one of them, and a call named in a comment or a string is ignored. The `rm` rule decides the rest, so the `filesystem` category, its exceptions and the temporary-cleanup exemption apply: `shutil.rmtree("/tmp/build")` is allowed, while a relative target or one that is not a single literal is denied, as `rm "$dir"` is in Bash.

This scan is a floor for ordinary code, not containment. It does not see a script that is written to a file and then run, a command assembled at runtime or across separate calls (`cmd.append("delete")`, a builder chain), a destructive library call other than those deletions (an API client, `fs.promises`, a deletion call in another language), or a spawn mechanism outside the recognized set. Code inside a string is scanned only where it is plainly run: after `-c`, `-e` or `--eval` in an argument list whose program is a known interpreter, or directly after a variable program such as `sys.executable`, not as the argument of `exec(...)` or `eval(...)`. With a variable program, another option before the flag (`[sys.executable, "-u", "-c", code]`) hides the code, and the code is always read as interpreter code, so a shell body there (`[shell, "-c", "rm -rf build"]`) is not checked as a command. Inline code for `php -r`, `Rscript -e` and `deno eval` in Bash is not inspected at all.

Line comments are recognised without knowing the language: `#` or `//` at the start of a line or after whitespace begins one, and the rest of that line is not scanned for commands or deletion calls. Code that follows such a marker on the same line is therefore missed: after a Python floor division written `a // b`, after Lua's length operator in `n = #items`, or in a JavaScript private member declared at the start of a line. A marker attached to code, as in `$#array`, `this.#field` or `a//b`, is not a comment.

A command handed directly to a recognised spawn call as its first argument also gets the secrets and protected-configuration rules, as it would in Bash: `subprocess.run("cat .env", shell=True)` and `subprocess.run(["cp", "payload", ".claude/settings.json"])` are denied. Every other literal gets the destructive rules only, so prose that mentions a secret path is not mistaken for a read. A command string that reaches the call through a variable is therefore checked for destructive commands but not for the secret paths inside it; a secret path that is a literal of its own is always checked.

Inspection is static: the guard does not execute submitted code or read the contents of an execute-file input. Paths assembled dynamically are outside its detection coverage, and non-shell mutation checks cover recognized literal write-call forms. Grep/Glob checks cover the search root, not every result's contents. Other execution tools need their own payload mapping. The Codex guard plugin supplies Bash, patch and capy adapters; see [Codex limitations](../providers/codex.md#known-limitations).

For shell paths, the guard retains possible directories after literal relative changes and checks existing matches of unquoted filename wildcards. Quoted or escaped wildcard characters remain literal. Interpreter checks decode common character escapes in literal paths while preserving raw strings. These checks inspect filenames and submitted text, without executing code or reading matched file contents.

## Statusline

Rich statusline with model, context %, git branch, session duration, thinking mode, and rate limits.

**Themes:** Set `CLAUDE_STATUSLINE_THEME` to `darcula`, `nord`, or `catppuccin`, and `CLAUDE_STATUSLINE_MODE` to `dark` (default) or `light` to match your terminal background.

## Recommended Settings

!!! tip
    Configure via `claude /config`. The config file is usually at `~/.claude.json`.

**I can't recommend enough disabling auto-compact** — I've seen many a time claude starting to compact conversations in the middle of a task, which produces very poor results for the remaining work it does after compacting.

??? example "Full `/config` settings"

    ```
    > /config
    ────────────────────────────────────────────────────────────
     Configure Claude Code preferences

        Auto-compact                              false
        Show tips                                 true
        Reduce motion                             false
        Thinking mode                             true
        Prompt suggestions                        true
        Rewind code (checkpoints)                 true
        Verbose output                            false
        Terminal progress bar                     true
        Default permission mode                   Default
        Respect .gitignore in file picker         true
        Auto-update channel                       latest
        Theme                                     Dark mode
        Notifications                             Auto
        Output style                              default
        Language                                  Default (English)
        Editor mode                               vim
        Show code diff footer                     true
        Show PR status footer                     true
        Model                                     opus
        Auto-connect to IDE (external terminal)   false
        Claude in Chrome enabled by default       false
    ```

## Project Instructions

To turn off the Claude plugin’s instruction hook, set `claude.instructions` to `false` in `${XDG_CONFIG_HOME:-~/.config}/kk/config.json`.

```json
{"claude": {"instructions": false}}
```

The default is `true`. Plugin-only projects receive the toolbox’s behavioral guidance, including its task-tracking and commit-message conventions. The hook reads the switch at each matching session event. An invalid value fails the instruction hook with a diagnostic naming the configuration file. Claude still loads any instruction files that your project imports.

- `CLAUDE.md` — project-specific instructions for Claude Code (checked into the repo)
- `.claude/CLAUDE.extra.md` — legacy project instructions retained in some repositories. The machine plugin supplies behavioral instructions when the legacy file is absent.
- `AGENTS.md` — equivalent instructions for Codex
