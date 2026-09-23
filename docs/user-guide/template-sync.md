# Template Sync

Repos created from this template can pull configuration updates via the **Template Sync** workflow.

## Prerequisites

- `.github/template-state.json` must exist (created automatically for new repos, or [manually for older ones](../getting-started/adopting.md))
- Allow actions to create pull-requests: repo **Settings** → **Actions**

## Using Template Sync

=== "GitHub Actions (creates a PR)"

    1. Go to **Actions** → **Template Sync** → **Run workflow**
    2. Choose a version: `latest` (default), `master`, or a specific tag (e.g., `v1.2.3`)
    3. Optionally enable **dry_run** to preview changes without creating a PR
    4. Review and merge the created PR

=== "Claude Code"

    ```
    /kk:template:sync
    /kk:template:sync --version v1.2.3
    /kk:template:sync --dry-run
    ```

=== "Local script"

    ```bash
    .claude/toolbox/scripts/template-sync.sh --local
    .claude/toolbox/scripts/template-sync.sh --local --version v1.2.3
    .claude/toolbox/scripts/template-sync.sh --local --dry-run  # preview only
    ```

    Requires `jq`, `git`, `curl`, and `yq` ([mikefarah/yq](https://github.com/mikefarah/yq)). Review changes with `git diff` before committing.

## Troubleshooting

### Sync stalls at "Fetching templates"

The script suppresses Git progress, so a slow or stalled transfer can leave this
message on screen without further output. It does not, by itself, establish
whether GitHub, your network, or your Git client is responsible.

If you already have a complete local checkout of `claude-toolbox`, you can use
it as the source and bypass the GitHub Git download. The checkout must contain
the desired commit and its file contents; a partial clone with missing objects
may still need network access. Obtain or update the checkout first if needed.

Set an **absolute path** to that checkout and pin its local `master` commit:

```bash
TOOLBOX_SOURCE="/absolute/path/to/claude-toolbox"
TOOLBOX_VERSION=$(git -C "$TOOLBOX_SOURCE" rev-parse --verify 'refs/heads/master^{commit}')
```

From the **downstream project's root**, preview the sync:

```bash
GIT_CONFIG_COUNT=1 \
GIT_CONFIG_KEY_0="url.file://${TOOLBOX_SOURCE}.insteadOf" \
GIT_CONFIG_VALUE_0=https://github.com/serpro69/claude-toolbox.git \
.claude/toolbox/scripts/template-sync.sh --local \
  --version "$TOOLBOX_VERSION" --dry-run
```

Review the preview, then repeat the same command without `--dry-run` to apply.
Review the resulting `git diff` before committing.

The environment variables supply one temporary Git setting: replace the
upstream HTTPS URL with the local `file://` URL. The setting is inherited by
the script's Git subprocesses, including after a script handoff, and does not
change your global Git configuration. See [Git's configuration documentation][git-config].

- **The source is local.** This does not refresh it from GitHub. `master` means
  the local source's branch, and uncommitted source edits are not included.
- **`--local` applies to the destination.** It applies changes to the current
  project; the Git URL rewrite is what selects the local source.
- **Reuse it across projects.** Update the source once and use the same pinned
  `TOOLBOX_VERSION` from each downstream project's root. No separate upstream
  Git download is needed for each project.
- **Match your upstream.** The example assumes `upstream_repo` in
  `.github/template-state.json` is `serpro69/claude-toolbox`. For a fork, change
  `GIT_CONFIG_VALUE_0` to its HTTPS Git URL and use a checkout of that repository.

If your environment already supplies `GIT_CONFIG_COUNT` entries, append the
rewrite at the next index and increase the count instead of replacing them.
The rewrite affects Git operations only, not other network requests.

#### Optional time limit

For a bounded preview, insert `timeout --kill-after=5 45` immediately before
`.claude/toolbox/scripts/template-sync.sh` in the preview command above.
[GNU `timeout`][gnu-timeout] sends `TERM` after 45 seconds, then `KILL` five
seconds later if the command remains running. The limit covers the entire run,
including any handoff, so adjust it for your project.

This requires GNU Coreutils; on macOS the command may be named `gtimeout`.
Omit the timeout prefix if neither command is installed.

**A timeout does not roll back applied changes.** If you also use it for an
apply run and it expires, inspect `git diff` for partial updates before retrying.

[git-config]: https://git-scm.com/docs/git-config
[gnu-timeout]: https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html

## What Gets Synced

**Updated:** `.claude/` (settings, CLAUDE.extra.md, statusline scripts), `.codex/` (config.toml, hooks, rules, scripts, agents), and the sync infrastructure itself (see [Syncing Workflow Files](#syncing-workflow-files) for permission requirements). Skills, commands, and hooks are managed by the plugin system — not template sync.

**Preserved:** Project-specific values (name, language, prompts), `settings.local.json`, gitignored files.

### settings.json merge behavior

The sync uses smart-merge semantics — your downstream `settings.json` is "master" and upstream fills gaps:

- **New keys** from upstream are added (e.g., new deny patterns, new env vars)
- **Existing values** are never overwritten (your customizations are preserved)
- **Arrays** are concatenated with deduplication (e.g., new upstream deny rules are appended)
- **Manifest variables** (`CC_MODEL`, `CC_EFFORT_LEVEL`, etc.) still override after the merge — these are your explicit choices

## Sync Exclusions

If you've removed template files you don't need, prevent sync from re-adding them.

Edit `.github/template-state.json` and add a `sync_exclusions` array:

```diff
{
  "schema_version": "1",
  "upstream_repo": "serpro69/claude-toolbox",
  "template_version": "v0.2.0",
  "synced_at": "2025-01-27T10:00:00Z",
+ "sync_exclusions": [
+   ".claude/CLAUDE.extra.md",
+   ".claude/settings.json"
+ ],
  "variables": { "..." : "..." }
}
```

**Pattern syntax:**

- Patterns use glob syntax where `*` matches any characters including directory separators
- Patterns are matched against project-relative paths (e.g., `.claude/settings.json`)
- Common patterns: `.claude/CLAUDE.extra.md` (single file), `.codex/*` (entire directory)

**Behavior:**

- Excluded files are NOT added if they exist upstream but not locally
- Excluded files are NOT updated if they exist in both places
- Excluded files are NOT flagged as deleted if they exist locally but not upstream
- Excluded files appear as "Excluded" in the sync report for transparency

## Self-Updating Sync Script

The sync script is itself a synced file. When the target version ships a different `template-sync.sh`, the running script hands the whole run over to that copy before touching anything: it stages the upstream script in a temp location and re-executes it with the same arguments. The version that matches the templates therefore drives the entire sync — including migrations that only the newer script knows about — in one invocation, and `--dry-run` previews reflect exactly what will be applied.

This applies to local runs (`--local`), to the CI workflow's staging run, and to the `--apply` step that turns staged changes into a PR.

Set `TEMPLATE_SYNC_NO_HANDOFF=1` to disable the handoff and run the locally installed script as-is (useful while developing the script itself).

!!! note "One-time transition for existing consumers"
    Scripts installed before this behavior existed cannot hand off. The first sync that crosses over to a handoff-capable version still behaves the old way: the report and apply complete, but bash may print a spurious `syntax error near unexpected token` right at the end because the script overwrote itself mid-run, and migrations introduced by the new version land on the next run. Simply run the sync once more. Every sync after that is single-pass.

## Syncing Workflow Files

Template sync updates its own workflow (`.github/workflows/template-sync.yml`) alongside everything else — the sync script is part of the `.claude/` directory and is synced as part of that tree. However, GitHub does not allow the default `GITHUB_TOKEN` to push changes to workflow files — the push is rejected with a `workflows` permission error ([details](https://github.com/peter-evans/create-pull-request/issues/3558)).

These updates are sometimes required for sync to work correctly (e.g., when the sync logic itself changes between versions), so skipping them indefinitely is not recommended.

### Option A: Update manually before running sync

Update the sync files locally, commit, push, then run the workflow:

```bash
VERSION="v0.12.0"  # use the version you want to sync to
curl -fsSL "https://raw.githubusercontent.com/serpro69/claude-toolbox/${VERSION}/.github/workflows/template-sync.yml" \
  -o .github/workflows/template-sync.yml
```

Or use `/kk:template:sync` in Claude Code — it syncs everything including the workflow files.

### Option B: Set up a GitHub App for automatic sync

A GitHub App token has the `workflows` permission that `GITHUB_TOKEN` lacks. Once configured, the sync workflow handles everything automatically — no manual steps needed.

1. **Create a GitHub App** ([guide](https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#authenticating-with-github-app-generated-tokens)) with these repository permissions:
    - **Contents:** Read & Write
    - **Pull requests:** Read & Write
    - **Workflows:** Read & Write

2. **Install the app** on the repository (or repositories) where you run template sync.

3. **Generate a private key** for the app (Settings → Private keys → Generate).

4. **Configure your repository:**
    - Add a **repository variable** named `CLAUDE_TOOLBOX_APP_ID` with the app's numeric ID
    - Add a **repository secret** named `CLAUDE_TOOLBOX_APP_KEY` with the app's private key (PEM contents)

    Go to repo **Settings** → **Secrets and variables** → **Actions** to add both.

The workflow detects these credentials automatically and uses them for both pushing the branch and creating the PR.

## Migrating from Task Master

Task Master MCP was removed in favor of native markdown-based task tracking integrated into the `/kk:design` and `/kk:implement` skills.

The easiest way to migrate is to run the migration command in Claude Code:

```
/kk:migrate-from-taskmaster:migrate
```

It will port pending tasks, clean up TM files, update configs, and walk you through each step with confirmation prompts.

??? note "Manual migration steps"

    If you prefer to migrate manually, follow these steps after syncing:

    1. **Port any pending tasks** to the new format: create `docs/feat/wip/[feature]/tasks.md` files following the example task file in the plugin. Completed tasks don't need porting.

    2. **Remove Task Master files and config:**

        ```bash
        rm -rf .taskmaster
        rm -rf .claude/commands/tm
        rm -f .claude/TM_COMMANDS_GUIDE.md
        rm -f .claude/agents/task-orchestrator.md
        rm -f .claude/agents/task-executor.md
        rm -f .claude/agents/task-checker.md
        ```

    3. **Remove Task Master from `~/.claude.json`:** delete the `task-master-ai` entry from your `mcpServers` config.

    4. **Remove TM variables from `.github/template-state.json`:** delete `TM_CUSTOM_SYSTEM_PROMPT`, `TM_APPEND_SYSTEM_PROMPT`, and `TM_PERMISSION_MODE` from the `variables` object.

    5. **Remove TM references from `CLAUDE.md`:** delete the "Task Master Integration" and "Task Master AI Instructions" sections (including the `@./.taskmaster/CLAUDE.md` import).

    6. **Update the template-sync workflow** ([why?](https://github.com/serpro69/claude-toolbox/issues/17)): the old workflow contains taskmaster-specific sync logic that will break future syncs. Run `/kk:template:sync` or manually replace both files:

        ```bash
        VERSION="v0.3.0"  # or use latest tag
        curl -fsSL "https://raw.githubusercontent.com/serpro69/claude-toolbox/${VERSION}/.github/workflows/template-sync.yml" \
          -o .github/workflows/template-sync.yml
        curl -fsSL "https://raw.githubusercontent.com/serpro69/claude-toolbox/${VERSION}/.claude/toolbox/scripts/template-sync.sh" \
          -o .claude/toolbox/scripts/template-sync.sh
        chmod +x .claude/toolbox/scripts/template-sync.sh
        ```

    Task tracking now lives in simple markdown files (`docs/feat/wip/[feature]/tasks.md`) created by the `/kk:design` skill and consumed by `/kk:implement`. No external MCP server required.

## Upgrading to the Plugin System (v0.5.0+)

Skills and commands have moved from the template to the **kk** plugin:

- Skills remain unprefixed: `/design` (annotated with `(kk)` in the menu)
- Commands are now namespaced: `/project:chain-of-verification` → `/kk:chain-of-verification:default`
- The template-sync workflow handles migration automatically on next sync
- After merging the sync PR, run `/plugin install kk@claude-toolbox`
