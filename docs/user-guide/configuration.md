# Configuration

claude-toolbox provides opinionated defaults for permissions, statusline, hooks, and project settings.

## How Configuration Works

!!! note
    Claude Code settings are split between two project-scoped files:

    - **`.claude/settings.json`** — upstream-managed defaults, synced from this template (permissions baseline, env vars, model, plugins, statusline)
    - **`.claude/settings.local.json`** — your per-repo overrides, never synced (hooks, MCP server enables, additional permissions, personal preferences)

    You can edit `settings.json` directly — values will be intelligently merged with upstream settings. But the general advice is to place your customizations in `settings.local.json`. As an added bonus, "Don't ask again" grant prompts in Claude Code sessions land in local settings automatically (as of v2.1.92).

## Permission Baselines

The permission baseline below is generated from `klaude-plugin/scripts/guard/guard-rules.json` with `make generate-guard`. Template sync replaces `permissions.deny` with this baseline; project additions belong in `.claude/kk-guard.json`. Other settings, including `permissions.allow`, retain their normal merge behavior. Per-repo MCP tool permissions go in `settings.local.json`.

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

## Hooks

The plugin ships two hooks:

| Hook | Trigger | Description |
|------|---------|-------------|
| Plugin root export | `SessionStart` | Exports `TOOLBOX_PLUGIN_ROOT` into the session environment so every Bash call has a reliable path to the plugin installation directory |
| Bash validation | `PreToolUse` on `Bash` | Blocks commands touching `.env`, `.git/`, `node_modules`, `build/`, `dist/`, `venv/`, and other sensitive paths |

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
