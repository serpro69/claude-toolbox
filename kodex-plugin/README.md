# kk — Codex Plugin

[![Documentation](https://img.shields.io/badge/docs-serpro69.github.io%2Fclaude--toolbox-blue?style=for-the-badge)](https://serpro69.github.io/claude-toolbox/latest/providers/codex/)

Development workflow skills generated from [klaude-plugin/](../klaude-plugin/) (the Claude Code source of truth). Part of the [claude-toolbox](https://github.com/serpro69/claude-toolbox) project.

## Installation

```bash
codex plugin marketplace add serpro69/claude-toolbox
```

Then open `/plugins` in the Codex TUI, select the **Claude Toolbox** marketplace, and install `kk`.

## What's Included

- **15 workflow and utility skills** — the same pipeline as the Claude Code plugin (`$kk:design` → `$kk:review-design` → `$kk:implement` → `$kk:review-code` → `$kk:test` → `$kk:document`, plus utilities)
- **Language-specific profiles** — review checklists, implementation gotchas, design prompts, test validators, and doc rubrics for Go, Java, JS/TS, Kotlin, Kubernetes, and Python

The plugin does **not** include hooks, sub-agents, Starlark rules, or project configuration. For the full Codex experience, use the [template setup](https://serpro69.github.io/claude-toolbox/latest/getting-started/template-setup/) or [adopt into an existing repo](https://serpro69.github.io/claude-toolbox/latest/getting-started/adopting/).

Use `$kk:brainstorm` for an optional conversation about a technical idea or decision. It asks one question at a time, adapts to the clarity you need, and ends with a chat-only recap of decisions, rationale, and open assumptions. Request `$kk:design` when you want written design documents, an implementation plan, and tasks; brainstorming creates no files and does not start that workflow automatically.

See the [Codex provider docs](https://serpro69.github.io/claude-toolbox/latest/providers/codex/) for configuration, known limitations, and the generation pipeline.

## Isolated reviews with external models

`$kk:review-code` and `$kk:review-design` describe an isolated mode that adds reviewers which never saw the authoring conversation: one independent reviewer plus external review through the [PAL MCP server](https://github.com/serpro69/pal-mcp-server) configured in `~/.codex/config.toml`. Standard mode does not call PAL.

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

Candidates are PAL's configured CLI clients whose executable was found. The provider that authored the reviewed change (for document review, the provider that produced the documents) is excluded; one client per remaining provider is attempted exactly once; a failed client is disclosed, not retried or replaced. Each CLI review of a real change takes minutes (this plugin's own final review took 3–8 minutes per client); PAL allows up to 30 minutes per client, and your host's MCP tool timeout must permit it (Claude Code completed 8-minute calls in this feature's verification; Codex's `tool_timeout_sec` is unverified for calls that long). Cost scales with the roster: with the three shipped clients and a Codex-authored change, two CLI reviews run (`claude` and `agy`).

Provider identity is resolved in this order and its source is printed next to each reviewer:

1. **declared** — a mapping you state in the request, in the project's `AGENTS.md` or `CLAUDE.md`, or in client configuration you identify. A declaration always wins.
2. **observed** — for a shipped client name, a model you identify in its client configuration or the model the CLI returns, when it belongs to another vendor. It overrides the default below, is labeled observed, and never resolves a custom name.
3. **assumed from shipped manifest** — without a declaration, PAL's shipped names map to their vendor: `claude` → Anthropic, `codex` → OpenAI, `agy` → Google. A reconfigured shipped client can point at another vendor, which is why the report labels these as assumed and notes that a declaration overrides them.
4. **undeclared** — any other client name. The skill never guesses a provider from a custom name; it asks one question before dispatch and leaves the client out until answered.

`gemini` is retired tooling and is never a candidate, even when PAL advertises it; `agy` is the Google client. A declaration is required only for custom client names, to override a default, or to choose between two clients that map to one provider (state the preferred client, as in the example's last line). Example for a project's `AGENTS.md`:

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
