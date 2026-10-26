# Configuration

claude-toolbox provides opinionated defaults for permissions, statusline, hooks, and project settings.

## How Configuration Works

!!! note
    Claude Code settings are split between two project-scoped files:

    - **`.claude/settings.json`** — upstream-managed defaults, synced from this template (permissions baseline, env vars, model, plugins, statusline)
    - **`.claude/settings.local.json`** — your per-repo overrides, never synced (hooks, MCP server enables, additional permissions, personal preferences)

    Use `settings.local.json` for personal settings. Template sync merges most settings, but replaces `permissions.deny` with the upstream secrets baseline and reports removed entries; `permissions.allow` remains union-merged. The guard protects both settings files from agent edits. A person can edit them directly, or enable the scoped `disable_selfmod` exception described below.

## Permission Baselines

The permission guard separates secrets, destructive operations and changes to its own configuration. Its baseline allows ordinary logs, dependencies, build output and `.env.example`; projects can add their own restrictions. A settings allow entry cannot override a secrets deny.

The tables below are generated from `klaude-plugin/scripts/guard/guard-rules.json` with `make generate-guard`. Template sync replaces `permissions.deny` with the secrets projection; project additions belong in `.claude/kk-guard.json`. See [template sync](template-sync.md) for dropped-entry reports and the `sync_exclusions` opt-out. Per-repo MCP tool permissions go in `settings.local.json`.

Self-modification protection also blocks an agent from adding an allow entry to `.claude/settings.json` or `.claude/settings.local.json`. The `disable_selfmod` example below lets the user authorize those edits for a chosen project; it does not loosen secrets.

<!-- BEGIN GUARD-RULES -->
### Secrets

These globs generate the Claude settings deny list and apply in the guard. Add project globs in `.claude/kk-guard.json` under `secrets`; user exceptions never loosen secrets.

| Scope | Glob |
|-------|------|
| Project | `./**/*.pem` |
| Project | `./**/*.tfstate` |
| Project | `./**/*.tfstate.backup` |
| Project | `./**/.env` |
| Project | `./**/.env.*.local` |
| Project | `./**/.env.local` |
| Project | `./**/.terraform/**` |
| Project | `./**/id_ecdsa` |
| Project | `./**/id_ed25519` |
| Project | `./**/id_rsa` |
| Project | `./**/service-account*.json` |
| Home | `~/.aws/**` |
| Home | `~/.claude/.credentials.json` |
| Home | `~/.config/gcloud/**` |
| Home | `~/.docker/config.json` |
| Home | `~/.gnupg/**` |
| Home | `~/.kube/**` |
| Home | `~/.netrc` |
| Home | `~/.pypirc` |
| Home | `~/.ssh/**` |

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

Project config may add paths under `selfmod`. To let an agent edit settings or guard files for one checkout, the user can add this entry to `~/.claude/kk-guard.json` (substitute the absolute project path):

```json
{"version":1,"projects":{"/absolute/path/to/repo":{"disable_selfmod":true}}}
```

This exception does not allow reading or writing secrets.
<!-- END GUARD-RULES -->

## Guard Configuration

The baseline ships inside the Claude plugin and runs even when neither configuration file exists. The Codex template carries the same engine and declaration. These files are independent of provider permission settings:

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
    "/absolute/path/to/claude-toolbox": {"disable_selfmod": true}
  }
}
```

Use physical absolute project paths (`pwd -P`). The engine combines `*` with the single longest matching directory prefix; shorter matching prefixes contribute nothing. Lists are combined, and `disable_selfmod` is enabled if either selected entry enables it. A parent path covers nested repositories and worktrees.

`allow_patterns` applies separately to each normalized simple command, including extracted shell bodies. Thus `^git clean -n` can exempt `git clean -nd`, but not the `rm` in `git clean -nd; rm -rf ./work`. These patterns never exempt secrets or protected configuration. `disable_selfmod` permits settings/guard edits only; it also leaves secrets protected. On Codex, native forbids for `rm`, `shred`, `sudo`, `su` and `doas` still win over guard exceptions.

Missing config files leave the baseline active. Invalid JSON or invalid supported values produce a visible `systemMessage` and skip that file's changes; the other valid layer still applies. Unknown keys are reported and ignored. Secrets are never loosened by user configuration.

## Hooks

The Claude plugin ships two hooks. It needs Bash, `jq`, Python 3.8+ and Claude Code 2.1.295+ for the declared [`onFailure: "block"` behavior](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails).

| Hook | Trigger | Description |
|------|---------|-------------|
| Plugin root export | `SessionStart` | Exports `TOOLBOX_PLUGIN_ROOT` into the session environment so every Bash call has a reliable path to the plugin installation directory |
| Permission guard | `PreToolUse` on `Bash`, `Read`, `Grep`, `Glob`, `Edit`, `Write`, `NotebookEdit`, and capy execution tools | Enforces secrets, destructive-command rules, and protected configuration paths; denies on guard failures |

Ordinary allowed calls produce no output and exit 0; invalid-config warnings may emit `systemMessage`. Denials emit JSON, a reason on stderr, and exit 2. Missing/broken interpreters, a corrupt declaration, crashes and malformed engine output deny the call. Claude also blocks hook failures/timeouts through `onFailure: "block"`. A machine without a working Python interpreter blocks every matched tool, including reads, until repaired.

The wrapper runs the standard-library-only engine with `-I -S`, isolating Python environment/user-site settings and skipping unused site startup. On macOS it prefers Python at the standard Homebrew locations, then system Python; elsewhere it checks system Python first. PATH lookup remains the final fallback. Homebrew is not required.

Destructive operations are denied in every permission mode, including bypass mode. The reason names the matched category and the way through: the user runs the operation directly or configures an applicable exception. Disabling Claude hooks removes destructive and self-modification protection. Template users retain the native secrets settings baseline; plugin-only users have no such fallback.

The guard checks `capy_execute`, `capy_execute_file`, and `capy_batch_execute` even when capy is registered under a different MCP server name. Shell code uses the same checks as Bash; other languages use the existing literal-path and write-call scans. Every batch command is checked independently, and one denied command blocks the entire batch before execution.

For capy code, omitted `cwd` means the project root. Relative cwd overrides resolve from that root; absolute overrides select that directory. Each batch command starts in the selected directory. The `capy_execute_file.path` input stays project-root-relative regardless of where its processing code runs. These path parameters are literal paths, without shell-variable or tilde expansion.

Inspection is static: the guard does not execute submitted code or read the contents of an execute-file input. Paths assembled dynamically are outside its detection coverage, and non-shell mutation checks cover recognized literal write-call forms. Grep/Glob checks cover the search root, not every result's contents. Other execution tools need their own payload mapping. The Codex template supplies Bash, patch and capy adapters; see [Codex limitations](../providers/codex.md#known-limitations).

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

- `CLAUDE.md` — project-specific instructions for Claude Code (checked into the repo)
- `.claude/CLAUDE.extra.md` — behavioral instructions (independent thinking, fail-loud, assumptions)
- `AGENTS.md` — equivalent instructions for Codex
