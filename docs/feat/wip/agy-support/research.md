# Antigravity (`agy`) support — research and port map

> Issue: https://github.com/serpro69/claude-toolbox/issues/173
> Status: research (pre-design). Input for `/kk:design` → `docs/feat/wip/agy-support/design.md`.
> Date: 2026-10-17
> Sources: antigravity.google docs (every page serves markdown at `<url>.md`; index at
> `https://antigravity.google/llms.txt`), local `agy` 1.3.3 (`~/.local/bin/agy`, state under
> `~/.gemini/`), its builtin skills (`~/.gemini/antigravity-cli/builtin/skills/agy-customizations`),
> and the experiments in §7.

"agy" is **Google Antigravity**, a platform with four surfaces (App, CLI, IDE/extensions, Python
SDK). The CLI binary is `agy`. All surfaces share the workspace customization root (`.agents/`),
the global root (`~/.gemini/config/`), and the same skill/agent/rule/hook/MCP formats, so one port
serves all of them. The CLI additionally keeps settings, keybindings, statusline and logs under
`~/.gemini/antigravity-cli/`.

## 0. Handoff status and how to resume

- This file is the only artifact of the research session. It was written in the git worktree
  `/tmp/tmp.8Gn40NQGDT` on branch `feat/agy` and is **uncommitted**. Commit it (or copy it into the
  main checkout) before that worktree is discarded.
- No repo code was changed. Scratch experiment directories (`/tmp/agy-validate.*`, `/tmp/agy-ws.*`)
  may still exist and are disposable. The `kk` plugin that §7.4 installed into
  `~/.gemini/config/plugins/` was uninstalled; `agy plugin list` is empty.
- Next step: run `/kk:design` with this document as the idea input to produce `design.md`,
  `implementation.md` and `tasks.md` in this directory. Resolve the §5 questions first where
  possible; they need an interactive `agy` session with the user's credentials (headless runs reuse
  cached credentials, and read-only slash commands such as `/skills` make no model call).
- Harness notes for Claude Code sessions in this repo: `WebFetch` and `curl` are blocked by the capy
  routing hooks, so fetch Antigravity docs with `capy_execute` (JavaScript `fetch()` of
  `<page-url>.md`) or read the builtin skills under `~/.gemini/antigravity-cli/builtin/skills/`.
  The repo's own Bash guard rejects any command whose text contains `rm`, `.git/`, or the dotenv
  filename, so write files that mention those with the editor tools, not heredocs.
- §8 lists every doc page consulted, the Antigravity tool names, a worked hook example, and the
  exact repo touch points, so no session transcript is needed.

## 1. Antigravity's customization model (what we are mapping onto)

| Concept | Workspace location | Global location | Format |
|---|---|---|---|
| Skills | `.agents/skills/<name>/SKILL.md` | `~/.gemini/antigravity-cli/skills/` (CLI), `~/.gemini/config/skills/` (App/IDE) | `SKILL.md`; frontmatter `name` (optional), `description` (required). Every skill becomes a slash command `/<name>`; `disable-slash-command: true` hides it from the menu. |
| Custom agents | `.agents/agents/<name>.md` or `<name>/agent.md` | `~/.gemini/config/agents/` | Markdown + YAML frontmatter: `name`, `description`, `tools[]` (agy tool names), `model` (`inherit`, `flash`, `pro`), `subagent`, `mainAgent`, `commandExecutionPolicy`, `mcpServers`, `skills`, `rules`, `agents`, `excludeDefaultComponents`. |
| Rules | `AGENTS.md` / `GEMINI.md` in any dir; `.agents/rules/*.md` | `~/.gemini/AGENTS.md`, `~/.gemini/config/rules/*.md` | `AGENTS.md` has no frontmatter and is always on. `rules/*.md` MUST carry `trigger: always_on`, `model_decision`, `glob` or `manual`. 24 000-byte per-file cap, 20k-token aggregate budget. `@[label](path)` inlines another file (frontmatter stripped). |
| Hooks | `.agents/hooks.json` | `~/.gemini/config/hooks.json` (or inside CLI `settings.json`) | Named groups → events `SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`. JSON on stdin/stdout, camelCase. Hook cwd = directory containing `hooks.json`. |
| MCP | `.agents/mcp_config.json` | `~/.gemini/config/mcp_config.json` | `{"mcpServers": {name: {command,args,env,cwd}}}` for stdio; `serverUrl` + `headers` for remote. Stdio shape identical to Claude's `.mcp.json`. |
| Plugins | `.agents/plugins/<name>/` | `~/.gemini/config/plugins/<name>/` (observed install target), `~/.gemini/antigravity-cli/plugins/` (documented) | `plugin.json` at root or in `.antigravity-plugin/` / `.gemini-plugin/`; may bundle `skills/`, `agents/`, `rules/`, `hooks.json`, `mcp_config.json`, `bin/`, `sidecars/`. |
| Permissions | none in repo | `~/.gemini/antigravity-cli/settings.json` → `permissions.{allow,deny,ask}` | `action(target)` strings: `command(prefix)`, `command(regex:…)`, `read_file(path)`, `write_file(path)`, `read_url(domain)`, `execute_url(domain)`, `mcp(server/tool)`, `unsandboxed(prefix)`. Precedence Deny > Ask > Allow. `/permissions` has Project / Shared / Global scopes, all persisted under `~/.gemini`. |
| Settings | none in repo | `~/.gemini/antigravity-cli/settings.json` | `toolPermission`, `artifactReviewPolicy`, `enableTerminalSandbox`, `agentMode`, `model`, `statusLine`, `title`, `colorScheme`, … (`agy -p "/config"` lists all keys). |
| Status line / title | none in repo | `settings.json` → `statusLine: {type: command, command, padding, enabled, stack_with_default}`, `title: {…}` | Script receives a JSON payload on stdin (§7.6). |
| Marketplace | — | official `antigravity-plugins-official` only | Third-party install: `agy plugin install <github-url>` (subpaths + branch supported), `agy plugin install <local-path>`, or drop the directory into `.agents/plugins/`. |

Codex and Antigravity **share the `.agents/` namespace**: Codex reads `.agents/skills/` and
`.agents/plugins/marketplace.json`; Antigravity reads `.agents/{skills,agents,rules,hooks.json,
mcp_config.json,plugins/<dir>/}`. Verified: Antigravity still discovers everything with Codex's
`marketplace.json` file sitting in `.agents/plugins/` (§7.5).

## 2. Port map

Legend — **Direct**: copy with at most the existing generator transforms. **Transform**: mechanical
rewrite the generator can own. **Hand-author**: schema differs too much; write by hand like the
Codex equivalents. **None**: no Antigravity surface for it.

| Toolbox artifact | Antigravity target | Class | What changes / caveats |
|---|---|---|---|
| `klaude-plugin/skills/*/SKILL.md` + process files, evals, `shared-*.md` symlinks | plugin `skills/` | **Direct** | Frontmatter already matches (`name`, `description`). Symlinks must become real files (the kodex generator already resolves them; `agy plugin install` does too). Plugin skills are namespaced `kk:<name>` and listed that way by `/skills` (§7.3) → **keep `/kk:` references as-is**, no `skill_prefix_rewrite`. `kk:model` does not collide with the builtin `/model`. `${CLAUDE_PLUGIN_ROOT}` / `${TOOLBOX_PLUGIN_ROOT}` must be resolved (reuse `plugin_root_resolve` with `../..`) and/or the absolute root injected by a SessionStart hook (below). The `/kk:name:variant` command syntax has no meaning here. |
| `klaude-plugin/skills/_shared/` | plugin `skills/_shared/` | Direct | Same as kodex. |
| `klaude-plugin/profiles/` | plugin `profiles/` | Direct | Same as kodex: copy without `plugin_root_resolve`. |
| `klaude-plugin/commands/<name>/<variant>.md` | — | **None** | Antigravity has no custom slash commands besides skills; "workflows" are deprecated (stop working 2026-10-19). `agy plugin install` reports `commands: skipped (not found)` for the nested layout. No `$ARGUMENTS` substitution exists. Options: drop (Codex precedent) or convert the isolated variants into skills (e.g. `review-code-isolated`). |
| `klaude-plugin/agents/*.md` | plugin `agents/*.md` (also valid: `.agents/agents/`) | **Transform** (md → md) | Same file shape, but `model: claude-*` makes Antigravity **silently drop the agent**; only `inherit`, `flash`, `pro` load (§7.2). Map opus-class → `pro`, sonnet-class → `flash` (or `inherit`). Drop `effort` (accepted but meaningless; effort is session-wide via `/effort`). Map `tools` to agy names: `Read`→`view_file`, `Grep`→`grep_search`, `Glob`→`find_by_name` (+`list_dir`), `mcp__capy__capy_search`→ MCP tool name TBD (docs warn unmapped tool names can hang the subagent). Add `subagent: true`, `mainAgent: false`. Unlike Codex, agents ship **inside the plugin**, so template-sync delivery is unnecessary. Spawning prose (`Agent(subagent_type=…)`) maps to the `invoke_subagent` tool — cover via the SessionStart tool-name mapping, as for Codex. |
| `klaude-plugin/hooks/hooks.json` | plugin-root `hooks.json`; template `.agents/hooks.json` | **Hand-author** | Different schema: `{"<hook-name>": {"SessionStart": [{type,command}], "PreToolUse": [{"matcher": "run_command", "hooks": [...]}]}}`. Matcher is an agy tool-name regex (`run_command`, not `Bash`). `agy plugin install` copies the Claude file unconverted and it does nothing useful (§7.4). |
| `scripts/validate-bash.sh` | `.agents/scripts/pretooluse-run-command.sh` | Transform (small) | Read `.toolCall.args.CommandLine`; emit `{"decision":"deny","reason":"…"}`. PreToolUse can also match `view_file`, `read_url_content`, `search_web`, `write_to_file` and MCP tools → the file-path denylist becomes enforceable on **reads**, closing the gap Codex has (ADR 0005). `decision` also allows `allow`, `auto_approve`, `ask`, `force_ask`, `deny_unless_prior_grant`; `permissionOverrides` grants `command(…)`/`read_file(…)` dynamically; `overwrite` rewrites tool args. |
| `scripts/set-plugin-root.sh` + `cpr.py` | SessionStart hook emitting `{"injectSteps":[{"systemMessage":{"systemMessage":"Plugin root: <abs>"}}]}` | Transform (simplifies) | Hook cwd is the directory containing `hooks.json`, i.e. the plugin root, so `pwd` is the answer. There is no env-file mechanism (nothing like `CLAUDE_ENV_FILE`); inject the path as context instead. The `cpr.py` cascade is unnecessary. |
| `.codex/scripts/session-start.sh` analogue | `.agents/scripts/session-start.sh` | Hand-author | Same job as Codex: provider identity, tool-name mapping (Read→`view_file`, Edit→`replace_file_content`, Write→`write_to_file`, Bash→`run_command`, Grep→`grep_search`, Glob→`find_by_name`, WebFetch→`read_url_content`, WebSearch→`search_web`, Agent/Task→`invoke_subagent`, Skill→`/kk:<name>`), `.claude/CLAUDE.*.md` extras, capy guidance. Output shape is `injectSteps`, not `additionalContext`. |
| `.claude/settings.json` `permissions.deny` (`Bash(rm:*)`, dotenv/secret reads, …) | `permissions.deny` in global `settings.json` | **Transform, but not repo-shippable** | Rules translate (`Bash(rm:*)`→`command(rm)`; file reads→`read_file(<path-prefix>)`), but every scope lives under `~/.gemini`; there is no project settings file to sync. Ship the baseline as a repo hook (`.agents/hooks.json` PreToolUse → deny) and document recommended global rules. |
| `.claude/settings.json` model/effort/mode/statusline | global `settings.json` (`model`, `agentMode`, `toolPermission`, `statusLine`) or flags (`--model`, `--effort`, `--mode`, `--sandbox`) | **None per-repo** | Nothing for template-sync variables to substitute. Document recommended settings (as the Claude `/config` section does). |
| `.mcp.json` (capy) | `.agents/mcp_config.json` and plugin `mcp_config.json` | **Direct** | Same `mcpServers` stdio schema (§7.4 validated `mcpServers 1`). Remote servers use `serverUrl`, not `url`. capy v0.17.3 has no Antigravity platform (`capy setup --help`: claude-code, codex) → toolbox ships the wrapper (`.agents/scripts/capy.sh`) and routing hooks itself, with the same stateless hand-off check Codex uses once capy adds it. MCP tools default to **Ask**; an `mcp(capy/*)` allow rule or a hook `auto_approve` avoids prompts. |
| `AGENTS.md` (repo), `CLAUDE.md` | `AGENTS.md` / `GEMINI.md` read natively | Direct (shared with Codex) | **This repo's `AGENTS.md` is 28 058 bytes; Antigravity truncates rule files at 24 000** — split or include. `.claude/toolbox/CLAUDE.md` is Claude-specific; exclude. |
| `.claude/CLAUDE.extra.md`, `.capy/AGENTS.md` | `.agents/rules/<name>.md` with `trigger: always_on`, or `@[label](.claude/CLAUDE.extra.md)` include from `AGENTS.md`, or SessionStart injection, or plugin `rules/AGENTS.md` | Transform | Pick one; the include syntax keeps a single source and strips frontmatter. |
| `.claude/toolbox/scripts/statusline_enhanced.sh` | `statusLine.command` (global settings) | **Transform** | Payload is a superset of Claude's: `model.display_name`, `context_window.{context_window_size,current_usage.*}` identical; `cwd`; plus `vcs.{branch,dirty}` (drop the `git` shell-outs), `quota.<bucket>.{remaining_fraction,reset_time}` (replaces the OAuth usage API), `agent_state`, `product`, `terminal_width`, `execution_mode`, `cost`, `conversation_title`, `vim.mode`. Branch on `product == "antigravity"` or ship a sibling script. Themes via the same env vars. Global-only: user runs `/statusline <path>`; `stack_with_default: true` keeps the builtin line. Terminal title: `title.command`, same payload. |
| `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` | — | **None** | Only the official marketplace exists. Distribution: `agy plugin install https://github.com/serpro69/claude-toolbox/tree/<ref>/<plugin-dir>` (verify), local path, or template-synced `.agents/plugins/kk/` (heavy: full copy per repo — not recommended). |
| `klaude-plugin/.claude-plugin/plugin.json` | root `plugin.json` (or `.antigravity-plugin/plugin.json`) | Transform (generate) | Fields: `name`, `description`, optional `displayName`, `version`, `logo`, `suggestedPrompts`, `disabled`. Claude-style extras (`author` object, `homepage`, `repository`, `license`, `keywords`) pass `agy plugin validate --strict` (§7.4). Name regex `^[a-zA-Z0-9-_]+$`. |
| `kodex-plugin/` generation (`cmd/generate-kodex`) | new target (name TBD, e.g. `kagy-plugin/`) | Reuse | `plugin_root_resolve` (`../..`), `inject_header`, profiles copy and manifest generation reuse. **Do not** apply `skill_prefix_rewrite` or `read_only_tool_guidance` (Codex-specific). New: md-agent writer (frontmatter rewrite + tool map), agy keys in `manifest.extra_fields`, plugin-level `hooks.json`/`mcp_config.json` emission. |
| `template-sync.sh` | `.agents/` | Extend | Add `.agents` to the sparse checkout and both `dir_map`s, `chmod +x .agents/scripts/*.sh`, keep `.gitignore` `!.agents` (already present), make `template-cleanup.sh` preserve `.agents`. Syncing `.agents/` wholesale also carries Codex's `plugins/marketplace.json` (fine, it is template content). |
| Tests | `test/test-agy-structure.sh` | New | Mirror `test-codex-structure.sh`: JSON validity, hook stdin/stdout contracts (feed `{"toolCall":{"name":"run_command","args":{"CommandLine":"…"}}}` and assert `.decision == "deny"`), **agent `model` ∈ {inherit, flash, pro}**, no `claude-*` models, no `${CLAUDE_PLUGIN_ROOT}` literals, `agy plugin validate --json --strict` when `agy` is on PATH. Add to `make test-structure` and the CI freshness diff. |
| Docs | `docs/providers/antigravity.md`, providers index (3rd column), `mkdocs.yml` nav, READMEs, `mcp-servers.md` section | New | Install: `curl -fsSL https://antigravity.google/cli/install.sh \| bash`. |

## 3. Where Antigravity beats Codex

- **Hooks cover every tool**, including reads, URL fetches, web search and MCP calls, and can
  rewrite tool arguments (`overwrite`) or inject permission grants. The Codex enforcement gap does
  not exist.
- **Agents ship inside the plugin** (`agents/*.md`), in Markdown, with frontmatter close to Claude's.
- **Plugin-level `hooks.json` and `mcp_config.json`** mean a plugin-only install can carry capy
  wiring and the Bash guard, not just skills.
- **Skill namespacing** (`kk:<name>`) matches Claude's `/kk:` convention, so skill prose ports
  unchanged in that respect.
- **SessionStart hook cwd is the plugin root**, which removes the `TOOLBOX_PLUGIN_ROOT`/`cpr.py`
  machinery.
- `agy -p "/skills"`, `/hooks`, `/config`, `/permissions` answer headlessly without a model call, and
  `agy --agent <bogus> -p …` lists discovered agents — usable in a smoke test when credentials exist.

## 4. Where it is worse or missing

- No per-project settings or permissions file: model, effort, mode, statusline and allow/deny lists
  are user-global. Enforcement must come from repo hooks; preferences from docs.
- No marketplace for third parties; no `--sparse`; install is a GitHub URL (subpath) or local path.
- No custom slash commands beyond skills; `commands/` has no home.
- `agy plugin install` on a Claude plugin only *copies* agents and hooks (§7.4): agents stay broken
  (`model: claude-*`), hooks keep Claude's schema and `${CLAUDE_PLUGIN_ROOT}`. Converting
  `klaude-plugin/` at install time is therefore not an option; a generated plugin is required.
- Rule-file size cap (24 KB) bites this repo's `AGENTS.md`.
- The portable **Agent Plugins 1.0.0** spec (`https://agent-plugins.org`: root `plugin.json` with
  `$schema`, `skills/`, `mcp.json`, client extension directories) is supported by Codex and sits
  behind a flag in `agy` (`enable-agent-plugins-spec`; `agy plugin validate --json` reports
  `agentPluginsSpec`). It is the eventual convergence point for `kodex-plugin/` and the agy plugin,
  but not usable today.

## 5. Open questions to verify in an interactive `agy` session

1. Slash form of plugin skills: `/kk:design` (expected from the `/skills` naming) — confirm, and
   confirm text after the skill name reaches the model as arguments.
2. `invoke_subagent` with a generated agent (`model: pro`, mapped `tools`) actually runs; the name of
   capy's MCP tool inside `tools:` (or whether `mcpServers` on the agent is needed).
3. Plugin `hooks.json` relative `command` paths resolve against the plugin dir (docs say yes; the
   scratch run loaded them but did not execute them).
4. `agy plugin install https://github.com/serpro69/claude-toolbox/tree/<ref>/<agy-plugin-dir>`
   works with the generated plugin (subpath install is in the changelog).
5. Observed install path `~/.gemini/config/plugins/<name>` (shared with App/IDE) vs documented
   `~/.gemini/antigravity-cli/plugins/` — observed is the better one; confirm it is stable.
6. MCP permission UX: do plugin `mcp_config.json` servers need an `mcp(capy/*)` allow rule, or does a
   PreToolUse `auto_approve` hook suffice.

## 6. Proposed shape (for `/kk:design`)

1. **Generator**: make `cmd/generate-kodex` multi-target (or add a sibling command) driven by
   `scripts/agy-generate-manifest.yml`; emit `<agy-plugin>/` with `plugin.json`, `skills/`,
   `profiles/`, `agents/` (rewritten frontmatter), `hooks.json`, `mcp_config.json`, `scripts/`.
   Transforms: `plugin_root_resolve(../..)`, `inject_header`, new `agent_frontmatter_rewrite`
   (model map, tool map, drop `effort`, add `subagent`/`mainAgent`), new tool-name mapping header.
   No `skill_prefix_rewrite`.
2. **Template configs**: `.agents/hooks.json`, `.agents/mcp_config.json`, `.agents/rules/*.md`,
   `.agents/scripts/{session-start.sh,pretooluse-run-command.sh,pretooluse-read.sh,capy.sh,
   statusline.sh}`; extend template-sync/cleanup; keep Codex's `.agents/plugins/marketplace.json`.
3. **Docs + tests** as in §2.
4. **ADR**: `.agents/` as the shared Codex/Antigravity workspace root, and "hooks as the per-repo
   permission mechanism on Antigravity" (counterpart to ADR 0005).

## 7. Evidence

### 7.1 Environment
`agy --version` → `1.3.3`. Subcommands: `agent(s)`, `changelog`, `install`, `mcp {add,remove,list,
enable,disable}`, `models`, `plugin {list [--json],import [gemini|claude],install,uninstall,enable,
disable,validate [--json --strict],link}`, `remote-control`, `update`. Flags include `--agent`,
`--model`, `--effort low|…|max`, `--mode accept-edits|auto|plan`, `--sandbox`, `-p/--print`,
`--output-format text|json|stream-json`, `--dangerously-skip-permissions`.

### 7.2 Agent frontmatter bisect (`agy plugin validate --json`, one agent per plugin)

| Variant (code-reviewer body) | agents loaded |
|---|---|
| frontmatter as in `klaude-plugin/agents/code-reviewer.md` | 0 |
| `name` + single-line `description` | 1 |
| `name` + multi-line `description: \|` | 1 |
| + `model: claude-opus-5-5` | **0** |
| + `effort: xhigh` | 1 |
| + Claude `tools` (`Read`, `Grep`, `Glob`, `mcp__capy__capy_search`) | 1 |
| + agy `tools` (`view_file`, `grep_search`, `find_by_name`) | 1 |
| + `model: pro`, `subagent: true`, `mainAgent: false` | 1 |

`agy --agent does-not-exist -p "/skills"` in the scratch workspace listed
`probe-dir, probe-minimal, probe-stripped, ws-probe`; the `claude-opus-5-5` probe was the only one
missing, and the CLI log contained no warning about it.

### 7.3 `agy -p "/skills"` with `klaude-plugin` copied to `.agents/plugins/kk/` (+ root `plugin.json`)
Lists the two builtins plus `kk:brainstorm … kk:test` (all 15), each with the full Claude
`description`. `agy -p "/hooks"` listed the two agy-format hooks from the plugin's `hooks.json`
(`kk-bash-guard PreToolUse run_command`, `kk-session SessionStart`); the log reported
`loaded 2 named hooks from 1 hooks.json file(s)`.

### 7.4 `agy plugin install <copy of klaude-plugin>` (then uninstalled)
```
[ok] kk   skills: 15 processed · agents: 6 processed · commands: skipped (not found)
          mcpServers: skipped (not found) · hooks: 1 processed
```
Installed to `~/.gemini/config/plugins/kk/` (source `claude-code`). Wrote root `plugin.json`
(`author` flattened to a string, `description`, `name`, `version`). Copied `skills/` (symlinks
resolved), `profiles/`, `commands/`, `scripts/`, `hooks/`, `.claude-plugin/`, `README.md`.
`agents/*.md` unchanged (`model: claude-opus-5-5` kept → dropped at load). Root `hooks.json` is a
copy of Claude's (`{"hooks": {...}}`, matcher `Bash`, `${CLAUDE_PLUGIN_ROOT}` literal).
9 files still contain `${CLAUDE_PLUGIN_ROOT}`/`${TOOLBOX_PLUGIN_ROOT}`.

`agy plugin validate klaude-plugin` (unmodified) → "no plugin.json … This looks like a Claude Code
plugin: `plugin install` converts it, but it doesn't load as is". Adding `.antigravity-plugin/
plugin.json` or a root `plugin.json` → `skills 15 · agents 0 · rules 0 · hooks 0 · mcpServers 0`.
Adding agy-format `hooks.json`, `mcp_config.json`, `rules/AGENTS.md` + `rules/x.md` → all counted;
`--strict` clean with Claude-style extra manifest fields.

### 7.5 Coexistence with Codex
The scratch workspace contained both `.agents/plugins/marketplace.json` (copied from this repo) and
`.agents/plugins/kk/`; skills and hooks were discovered normally.

### 7.6 Status line payload (docs `cli/statusline`)
`cwd`, `session_id`/`conversation_id`, `transcript_path`, `model{id,display_name}`,
`workspace{current_dir,project_dir}`, `version`, `context_window{total_input_tokens,
total_output_tokens,context_window_size,used_percentage,remaining_percentage,current_usage{
input_tokens,output_tokens,cache_creation_input_tokens,cache_read_input_tokens}}`,
`exceeds_200k_tokens`, `product`, `quota{<bucket>{remaining_fraction,reset_time,reset_in_seconds}}`,
`agent_state`, `vcs{type,branch,client,dirty}`, `sandbox{enabled,allow_network}`,
`artifact_count`, `plan_tier`, `email`, `pending_input_count`, `tool_confirmation_pending`,
`task_count`, `terminal_width`, `execution_mode`, `vim{mode}` (+ `cost`, `conversation_title`).

### 7.7 Hook I/O contract (docs `hooks`)
Common stdin fields: `conversationId`, `workspacePaths[]`, `transcriptPath`,
`artifactDirectoryPath`, `modelName`. `PreToolUse` stdin adds `toolCall{name,args}`, `stepIdx`;
stdout `{decision, reason?, overwrite?, permissionOverrides?[]}`. `SessionStart`/`PreInvocation`
stdout `{injectSteps:[{systemMessage:{systemMessage}}|{userMessage}|{ephemeralMessage}|{toolCall}]}`.
`Stop` stdout `{decision:"continue", reason}`. Default timeout 30 s. Only `type: command`.

## 8. Reference material for the implementer

### 8.1 Antigravity doc pages consulted
All under `https://antigravity.google/docs/`; append `.md` to get raw markdown. Index:
`https://antigravity.google/llms.txt`.
`settings`, `permissions`, `mcp`, `skills`, `subagents`, `hooks`, `plugins`, `marketplace`, `rules`,
`slash-commands`, `sandbox`, `agent-settings`, `sidecars`, `ide/workflows`, `install`,
`getting-started`, `models`, `cli/using`, `cli/reference`, `cli/modes`, `cli/features`,
`cli/headless`, `cli/gcli-migration`, `cli/statusline`, `cli/title`, `cli/commands/statusline`,
`cli/commands/title`, `cli/commands/agents`, `cli/commands/permissions`.
Also: `https://agent-plugins.org/` (spec, `schemas/1.0.0/plugin.schema.json`), Codex
`https://developers.openai.com/codex/skills.md` and `/plugins/build/plugins.md` (for the shared
`.agents/` namespace), the example status line script at
`https://github.com/google-antigravity/antigravity-cli/blob/main/examples/statusline/statusline.sh`,
and the embedded changelog (`strings ~/.local/bin/agy | grep '^- Added'`).

### 8.2 Antigravity tool names and the Claude mapping
File: `view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`,
`list_dir`, `find_by_name`. Search: `grep_search`, `code_search`, `search_web`, `read_url_content`.
Execution: `run_command` (args `CommandLine`, `Cwd`, `WaitMsBeforeAsync`, `RunPersistent`),
`manage_task`, `schedule`, `list_permissions`, `ask_permission`. Agents: `invoke_subagent` (args
`Subagents[]{Prompt, Role, TypeName, Workspace}`), `define_subagent`, `send_message`,
`manage_subagents`. Interaction: `ask_question`, `generate_image`.

| Claude | Antigravity |
|---|---|
| `Read` | `view_file` |
| `Write` | `write_to_file` |
| `Edit` | `replace_file_content` / `multi_replace_file_content` |
| `Bash` | `run_command` |
| `Grep` | `grep_search` |
| `Glob` | `find_by_name` (+ `list_dir`) |
| `WebFetch` | `read_url_content` |
| `WebSearch` | `search_web` |
| `Agent` / `Task` | `invoke_subagent` with `TypeName` = agent `name` |
| `AskUserQuestion` | `ask_question` |
| `Skill` | `/kk:<name>` slash command (or natural-language mention) |
| `mcp__capy__capy_search` | MCP tool name inside Antigravity — unverified (§5.2) |

### 8.3 Worked hook example (Antigravity schema)
Plugin-root or `.agents/hooks.json`:
```json
{
  "kk-session": {
    "SessionStart": [{ "type": "command", "command": "bash scripts/session-start.sh" }]
  },
  "kk-command-guard": {
    "PreToolUse": [{ "matcher": "run_command",
                     "hooks": [{ "type": "command", "command": "bash scripts/pretooluse-run-command.sh", "timeout": 10 }] }]
  },
  "kk-read-guard": {
    "PreToolUse": [{ "matcher": "view_file|read_url_content|search_web",
                     "hooks": [{ "type": "command", "command": "bash scripts/pretooluse-read.sh" }] }]
  }
}
```
`scripts/pretooluse-run-command.sh` (sketch): `cmd=$(jq -r '.toolCall.args.CommandLine // empty')`,
loop over the same `FORBIDDEN_PATTERNS` as `klaude-plugin/scripts/validate-bash.sh`, on match print
`jq -n --arg r "…" '{decision:"deny", reason:$r}'`; otherwise print `{"decision":"allow"}` (an empty
decision string is tolerated since a recent fix, but be explicit). `scripts/session-start.sh`
(sketch): `root=$(pwd)` (hook cwd is the `hooks.json` directory), then print
`jq -n --arg m "Provider: Antigravity. Plugin root: $root. Tool mapping: …" '{injectSteps:[{systemMessage:{systemMessage:$m}}]}'`.
Both were loaded in the scratch run (§7.3, "loaded 2 named hooks"), but their execution was not
observed; the stdin/stdout contract comes from the docs (§7.7).

### 8.4 Repo touch points for the implementation
- `cmd/generate-kodex/`: `manifest.go` (`Manifest` struct and `ParseManifest` validation),
  `agents.go` (`formatAgentTOML`; add a Markdown writer that rewrites frontmatter), `transforms.go`
  (`ApplyTransforms` switch; add tool-name and model mapping), `main.go` (`run()` deletes
  `skills/`, `profiles/` and the agents target before regenerating), `manifest_gen.go` (hard-codes
  `.codex-plugin/plugin.json`; parametrize), `mcp.go` (`GenerateMCPConfig`, currently commented out
  in `run()`; Antigravity needs `mcp_config.json`). Tests in `main_test.go`,
  `agent_tools_test.go`, `plugin_root_test.go` with fixtures under `testdata/`.
- `scripts/kodex-generate-manifest.yml` → sibling manifest for the new target.
- `Makefile`: `generate-kodex`, `generate-all`, `test-structure`.
- `.github/workflows/release.yml` and `pre-release.yml`: the steps that read and bump
  `kodex-plugin/.codex-plugin/plugin.json` (`KODEX_CURRENT_VERSION`, "Regenerate Kodex Artifacts")
  need a twin for the new manifest. `docs.yml` / `docs-check.yml` path filters list
  `kodex-plugin/README.md`.
- `.claude/toolbox/scripts/template-sync.sh`: `fetch_upstream_templates()` (the
  `git sparse-checkout set .claude .codex …` line and the `.codex` copy/strip block),
  `compare_files()` and `apply_changes()` `dir_map`s, the `chmod +x .codex/scripts/*.sh` line, the
  `.gitignore` patch block for `.codex`, and the builtin `SYNC_EXCLUSIONS` (`.codex/scripts/capy.sh`,
  `.codex/capy-owner`).
- `.github/scripts/template-cleanup.sh`: the `find … ! -name '.codex'` keep-list, the Codex model
  substitution block, the `SKIP_CAPY` strip block. `.github/scripts/bootstrap.sh`: `git add .codex`.
- `.github/template-state.example.json`: no new variables unless a per-repo setting appears.
- Tests: `test/test-codex-structure.sh` (template for `test-agy-structure.sh`),
  `test/test-plugin-structure.sh` Section 11 (generated-output checks), `test/test-template-sync.sh`
  Codex fixtures (`create_codex_config_fixture`).
- Docs: `docs/providers/index.md` (two-column table → three), `docs/providers/codex.md` (template),
  `mkdocs.yml` nav, `docs/user-guide/mcp-servers.md`, `docs/user-guide/configuration.md`
  ("Project Instructions"), `docs/getting-started/template-setup.md` ("What You Get"),
  `docs/contributing/index.md` (repo structure lists `.agents/plugins/marketplace.json`),
  `README.md` ("Supported providers"), `kodex-plugin/README.md` (template), `AGENTS.md` (§Codex
  Support and §Testing), `.capy/AGENTS.md` (hook-coverage prose names Claude and Codex only).

### 8.5 Smaller verified facts
- `agy agents` printed nothing in a headless shell; `agy -p "/help"` lists only builtin slash
  commands. Use `agy --agent <bogus> -p x` to enumerate discovered agents and `agy -p "/skills"`
  for skills.
- `agy plugin import [gemini|claude]` exists (converts Gemini CLI extensions or Claude installs);
  not exercised.
- Changelog items relevant to packaging: plugins may ship a `bin/` folder of tools runnable by
  name, a per-plugin data dir exposed as `PLUGIN_DATA`, root `skills.json` / `rules.json` /
  `agents.json` manifests, `metadata.icon` in `SKILL.md`, `/skills reload`, and
  `disable-slash-command: true`.
- `.agents/skills.json` with `{"entries":[{"path":"klaude-plugin/skills"}]}` (workspace-relative)
  can register skills from a non-standard directory. Unverified, but it is an option for using the
  canonical `klaude-plugin/skills/` directly when developing inside this repo.
- Headless `-p` runs honor `settings.json` policies and soft-deny tools that would need a
  confirmation; `--dangerously-skip-permissions` only skips tool prompts.
- The scratch workspace was not in `trustedWorkspaces`, and headless read-only commands still
  worked.
- Install observed at `~/.gemini/config/plugins/<name>` with `"source": "claude-code"`; uninstall
  left no entry in `~/.gemini/config/config.json` (the file did not exist afterwards).
