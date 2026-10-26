# kk — Claude Code Plugin

[![Documentation](https://img.shields.io/badge/docs-serpro69.github.io%2Fclaude--toolbox-blue?style=for-the-badge)](https://serpro69.github.io/claude-toolbox/latest/user-guide/skills/)

A development workflow plugin for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that gives your AI assistant a structured pipeline — from idea through design, implementation, code review, testing, to documentation. Part of the [claude-toolbox](https://github.com/serpro69/claude-toolbox) project.

Why `kk`? I have `jj` and `kk` mappings in nvim to go back to normal mode, and it seemed like a low-conflict/easy-to-type option for a plugin-prefixed skill names. We can also pretend it's an acronym for "klaude kode", if you need a better reason for the plugin naming.

## Installation

```
/plugin install kk@claude-toolbox
```

All skills appear as `/skill-name` in the slash command menu (annotated with `(kk)`). The permission guard is active without a separate policy file; its runtime requirements and exceptions are described below.

Use `/kk:brainstorm` for an optional conversation about a technical idea or decision. It asks one question at a time, adapts to the clarity you need, and ends with a chat-only recap of decisions, rationale, and open assumptions. Request `/kk:design` when you want written design documents, an implementation plan, and tasks; brainstorming creates no files and does not start that workflow automatically.

## What's Included

- **15 workflow and utility skills** — `/kk:design` → `/kk:review-design` → `/kk:implement` → `/kk:review-code` → `/kk:test` → `/kk:document`, plus utilities including `/kk:clarify-docs` for existing documentation and PR drafts
- **Commands** — isolated variants for code review, CoVe and spec review
- **Hooks** — permission guard for secrets, destructive operations and protected configuration on Bash, file tools and capy execution tools
- **Profiles** — per-domain content (Go, Java, JS/TS, Kotlin, K8s, Python) with review checklists, implementation gotchas, design prompts, test validators, and doc rubrics

See the [Skills](https://serpro69.github.io/claude-toolbox/latest/user-guide/skills/) and [Profiles](https://serpro69.github.io/claude-toolbox/latest/user-guide/profiles/) documentation for details.

## Permission guard

The [shipped declaration](scripts/guard/guard-rules.json), [wrapper](scripts/guard/guard.sh), [launcher](scripts/guard/run-guard.py) and [engine](scripts/guard/guard.py) enforce the same baseline even on plugin-only installs. Use Claude Code 2.1.295+, Bash, `jq` and Python 3.8+. The hook covers Bash, Read/Grep/Glob, Edit/Write/NotebookEdit and `capy_execute`, `capy_execute_file`, `capy_batch_execute` under any MCP server name.

The launcher imports the adjacent engine under isolated Python, allowing Python's normal bytecode cache to reduce startup time. Rules and configuration are reloaded on every call. Caches stay beside the installed engine; cold starts and runtimes that cannot write caches still evaluate source. Unexpected loading failures block through the wrapper.

Secrets are protected across those channels; destructive commands deny even in bypass mode. Literal `rm` cleanup beneath temporary roots is exempt, but secrets and protected configuration still apply. Baseline policy allows logs, dependencies, build output and `.env.example`. Grep/Glob checks only the search root; dynamically assembled interpreter paths and unregistered execution tools are outside complete coverage.

Guard failures block: missing interpreters, crashes or invalid output do not silently disable it. Ordinary allow is silent with exit 0; denial returns JSON, a reason on stderr and exit 2. The hook registration also blocks launch failures and timeouts. If you disable hooks, this plugin-only installation has no native settings baseline to fall back on.

Project `.claude/kk-guard.json` can add `secrets`, `destructive` rules and `selfmod` paths, with `"version": 1`. Only the user-owned `~/.claude/kk-guard.json` can loosen destructive categories or self-modification protection. Its `projects` object combines `*` with the longest physical absolute project-path prefix. `disable_categories` removes selected destructive categories; `allow_patterns` exempts individual simple commands only. Neither can loosen secrets.

Settings files are protected too: an agent cannot add a permission allow entry without a user exception. To permit settings/guard edits for one checkout, the user merges this entry into their user config:

```json
{"version":1,"projects":{"/absolute/path/to/repo":{"disable_selfmod":true}}}
```

This still protects secrets. Invalid configuration is reported through `systemMessage` and does not weaken the baseline. The Codex plugin distributes skills/profiles only; the separate template supplies Codex adapters and native rules, whose unconditional forbids can outrank these user exceptions.

## Isolated reviews with external models

`/kk:review-code:isolated` and `/kk:review-design:isolated` add reviewers that never saw the authoring conversation: one internal sub-agent (`code-reviewer` or `design-reviewer`) plus external review through the [PAL MCP server](https://github.com/serpro69/pal-mcp-server). Standard `/kk:review-code` and `/kk:review-design` do not call PAL.

### How the external backend is chosen

Once per review, after the criteria and evidence are prepared and before any external call, the skill inspects PAL's advertised tools and calls `listmodels`:

| PAL state at discovery | External review |
| --- | --- |
| `codereview` available and an eligible API model configured | One `pal codereview` review (the existing two-step flow with PAL's model policy) |
| No eligible API model (or `codereview` not advertised) and `clink` available with CLI metadata | One `pal clink` CLI review per eligible provider (roster below) |
| No eligible API model and `clink` unavailable, or an empty roster | Internal review only, with an explicit external coverage limit |
| Discovery fails, is ambiguous or lacks CLI metadata | No external review; the report states the coverage limit |

The decision is frozen for that review. A failed API review is reported as a failure and never switches to clink; run the review again to re-discover.

### Minimum PAL

The clink path needs a PAL build whose `listmodels` returns `cli_clients` metadata in every mode: PAL commit `c73dab7d` ("Expose CLI availability in API-mode discovery", 2026-10-23) or a release containing it. Unmodified PAL 1.4.2 exposes that metadata only in provider-free mode, so with an API provider configured but no eligible model the skill reports discovery as unresolved. PAL observes CLI executables at startup: restart it after changing provider or CLI configuration.

### Roster, providers and cost

Candidates are PAL's configured CLI clients whose executable was found. The provider that authored the reviewed change (for document review, the provider that produced the documents) is excluded; one client per remaining provider is attempted exactly once; a failed client is disclosed, not retried or replaced. Each CLI review of a real change takes minutes (this plugin's own final review took 3–8 minutes per client); PAL allows up to 30 minutes per client, and your host's MCP tool timeout must permit it (Claude Code completed 8-minute calls in this feature's verification; Codex's `tool_timeout_sec` is unverified for calls that long). Cost scales with the roster: with the three shipped clients and a Claude-authored change, two CLI reviews run (`codex` and `agy`).

Provider identity is resolved in this order and its source is printed next to each reviewer:

1. **declared** — a mapping you state in the request, in the project's `CLAUDE.md` or `AGENTS.md`, or in client configuration you identify. A declaration always wins.
2. **observed** — for a shipped client name, a model you identify in its client configuration or the model the CLI returns, when it belongs to another vendor. It overrides the default below, is labeled observed, and never resolves a custom name.
3. **assumed from shipped manifest** — without a declaration, PAL's shipped names map to their vendor: `claude` → Anthropic, `codex` → OpenAI, `agy` → Google. A reconfigured shipped client can point at another vendor, which is why the report labels these as assumed and notes that a declaration overrides them.
4. **undeclared** — any other client name. The skill never guesses a provider from a custom name; it asks one question before dispatch and leaves the client out until answered.

`gemini` is retired tooling and is never a candidate, even when PAL advertises it; `agy` is the Google client. A declaration is required only for custom client names, to override a default, or to choose between two clients that map to one provider (state the preferred client, as in the example's last line). Example for a project's `CLAUDE.md` or `AGENTS.md`:

```markdown
## External review clients

- `claude` → Anthropic
- `codex` → OpenAI
- `agy` → Google
- `mycli` → Mistral
- review client for Google: `agy`
```

The skill always requests PAL's `default` role; a client's model and arguments come from its manifest, not from a role.

### Models

On the API branch the skill selects the most capable available model from PAL's catalog, as before. On the clink branch it never names a model: each CLI review uses the model configured in that CLI or its PAL client manifest. The report shows the configured model when known and the returned model when the CLI reports one (`codex` and `agy` return none).

### What each CLI must be able to read

Clink launches each CLI with your project root as working directory, but the review criteria live in the plugin installation and the diff/evidence bundle in the directory `mktemp` uses (`$TMPDIR` when set, otherwise `/tmp`; on macOS usually `/var/folders/...`). A CLI that cannot read outside the project denies those reads; the skill then reports that reviewer as not adequately evidenced and qualifies its findings. It never enables edits or bypasses permissions to make a review work. Setups verified with this plugin:

- **Claude Code** — grant reads through a PAL client manifest override at `~/.pal/cli_clients/claude.json`. An override replaces the whole client definition, so it must contain `name`, `command` and your `additional_args`, for example `["--allowedTools", "Read,Glob,Grep"]` or a path-scoped rule covering that temp directory, such as `Read(//tmp/**)` on Linux. PAL caches the client registry: restart PAL after editing the file. Claude Code's permission settings for the project also apply to the launched CLI.
- **Antigravity (`agy`)** — where its mode does not already permit reads, add a native grant to `~/.gemini/antigravity-cli/settings.json`, for example `"permissions": {"allow": ["read_file(/tmp)"]}` (or your `$TMPDIR`) plus the plugin cache directory. No PAL restart is needed.
- **Codex** — the shipped manifest worked unchanged in the verified setup (`codex exec`); whether its reads are sandboxed depends on your Codex configuration and was not verified.

### No-edit contract and receipt limits

Every request is sent with `allow_edits=false`, and the prompt forbids edits, tests and commands that write files. This is a behavior contract, not an enforced sandbox: some clients (`agy` among them) keep their native permissions. The report records that limit and the skill never changes your permissions.

Each external reviewer is classified as requested, attempted, executed and adequately evidenced. Receipt of the criteria and source counts only when the CLI returns observable read evidence; of the verified clients only Claude returns a read trace, so `codex` and `agy` findings are kept with receipt unverified and cannot corroborate. A finding is **corroborated** only when two independent reviewers support it: an external reviewer counts only with observable receipt, the internal sub-agent counts through its source-tied report (its reads are never returned to the parent), and a corroboration resting on an assumed provider says so. With a Claude-authored change and the shipped clients no clink finding can be corroborated today: `claude` is excluded and `codex`/`agy` return no trace, so their findings stay attributed but uncorroborated. If every reviewer fails, the skill reports that isolated review did not complete and suggests standard mode instead of running it.

Isolated design review applies the same selection with document framing: every reviewer applies the shared design-review criteria, implementation the documents describe is planned work rather than missing code, and the default all-documents scope and explicit `design` / `implementation` / `tasks` subsets match standard mode.

## Guard attribution

The permission guard adapts tokenizer helpers and wrapper tables from
safe-claude-code, Copyright 2026 - present; serpro69. The modified engine
includes attribution, and its [Elastic License 2.0 terms](scripts/guard/LICENSE.md)
ship with the plugin.
