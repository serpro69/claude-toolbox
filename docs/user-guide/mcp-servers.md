# MCP Servers

MCP servers are configured at the user level (not in the repo) to keep API keys safe. These configs are generic enough to reuse across all your projects.

You don't need all servers to get started. Add them incrementally:

1. **[Context7](https://context7.com/)** (needs API key) — up-to-date library documentation and code examples
2. **[Pal](https://github.com/serpro69/pal-mcp-server)** (API key optional) — multi-model AI integration for code review, debugging, planning, and security audit; without an API key, isolated reviews use your installed CLIs through `clink`
3. **[Capy](https://github.com/serpro69/capy)** (optional, auto-configured by bootstrap) — persistent knowledge base across sessions. Install with `brew install serpro69/tap/capy`.

| Server | Purpose |
|--------|---------|
| **[Context7](https://context7.com/)** | Up-to-date library documentation and code examples |
| **[Pal](https://github.com/serpro69/pal-mcp-server)** | Multi-model AI integration — chat, debugging, code review, planning, security audit |
| **[Capy](https://github.com/serpro69/capy)** | Persistent knowledge base — cross-session project memory with FTS5 search |

## Claude Code

!!! note
    Add MCP servers to `~/.claude.json` under the `mcpServers` key.

??? example "Example `mcpServers` configuration"

    ```json
    {
      "context7": {
        "type": "http",
        "url": "https://mcp.context7.com/mcp",
        "headers": {
          "CONTEXT7_API_KEY": "YOUR_CONTEXT7_API_KEY"
        }
      },
      "pal": {
        "command": "sh",
        "args": [
          "-c",
          "$HOME/.local/bin/uvx --from git+https://github.com/serpro69/pal-mcp-server.git pal-mcp-server"
        ],
        "env": {
          "PATH": "/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin",
          "DEFAULT_MODEL": "auto",
          "DEFAULT_THINKING_MODE_THINKDEEP": "high",
          "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY",
          "GOOGLE_ALLOWED_MODELS": "gemini-3.1-pro-preview,gemini-3-flash-preview"
        }
      }
    }
    ```

    See [Pal configuration docs](https://github.com/serpro69/pal-mcp-server/blob/main/docs/configuration.md) for model and thinking mode options.

!!! tip "Using claude-in-docker?"
    If you're using [claude-in-docker](https://github.com/serpro69/claude-in-docker) images, replace `npx` and `uvx` calls with direct tool invocations. The images come with MCP tools pre-installed, avoiding dependency downloads on each launch:

    ```json
    "pal": {
      "command": "pal-mcp-server",
      "args": [],
      "env": { "..." }
    }
    ```

    Check your `env` settings, especially the `PATH` variable — custom paths not available in the image may cause the server to fail to connect.

## Codex

!!! note
    MCP servers are added via `codex mcp add` and stored in `~/.codex/config.toml`.
    Capy registers itself at the project level: run `capy setup --platform codex` in the project to add its MCP server to `.codex/config.toml` and its own Codex hooks to `.codex/hooks.json`. Toolbox's hooks detect them and hand over guidance and HTTP routing, and template sync preserves both. See [Capy Hooks](../providers/codex.md#capy-hooks).

```bash
# Context7 — streamable HTTP, no API key env var needed (key is in the URL header)
codex mcp add context7 --url "https://mcp.context7.com/mcp"

# Pal — stdio server via uvx, with env vars for model config
codex mcp add pal \
  --env "PATH=/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin" \
  --env "DEFAULT_MODEL=auto" \
  --env "DEFAULT_THINKING_MODE_THINKDEEP=high" \
  --env "GEMINI_API_KEY=YOUR_GEMINI_API_KEY" \
  --env "GOOGLE_ALLOWED_MODELS=gemini-3.1-pro-preview,gemini-3-flash-preview" \
  -- sh -c "$HOME/.local/bin/uvx --from git+https://github.com/serpro69/pal-mcp-server.git pal-mcp-server"
```

??? example "Or manually add to `~/.codex/config.toml`"

    ```toml
    [mcp_servers.context7]
    url = "https://mcp.context7.com/mcp"
    http_headers = { "CONTEXT7_API_KEY" = "YOUR_CONTEXT7_API_KEY" }

    [mcp_servers.pal]
    command = "sh"
    args = ["-c", "$HOME/.local/bin/uvx --from git+https://github.com/serpro69/pal-mcp-server.git pal-mcp-server"]
    tool_timeout_sec = 1800 # increase timeout for clink-based reviews

    [mcp_servers.pal.env]
    DEFAULT_MODEL = "auto"
    DEFAULT_THINKING_MODE_THINKDEEP = "high"
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
    GOOGLE_ALLOWED_MODELS = "gemini-3.1-pro-preview,gemini-3-flash-preview"
    PATH = "/usr/local/bin:/usr/bin:/bin"
    ```

Verify with `codex mcp list`. See [Pal configuration docs](https://github.com/serpro69/pal-mcp-server/blob/main/docs/configuration.md) for model and thinking mode options.

## What Each Server Does

### Context7

Fetches current documentation for any library, framework, or SDK. Used by the **/kk:dependency-handling** skill to look up API signatures instead of guessing. Also available for ad-hoc queries.

### Pal

Multi-model AI integration. Powers the external reviewers of **/kk:review-code:isolated** and **/kk:review-design:isolated** — your change gets a second, independent review from an external model (another vendor's where the roster allows) in addition to the internal reviewer. Also provides: `debug`, `planner`, `secaudit`, `testgen`, and more.

The isolated review skills choose their external backend once per review from what Pal advertises (see [Isolated reviews and external models](skills.md#isolated-reviews-and-external-models)):

- **API model configured** (for example a Gemini key as above) → `pal codereview`.
- **No API model** → `pal clink`, one review per installed CLI from a vendor other than the author's. Pal ships client manifests for `claude`, `codex`, `agy` and `gemini`; the plugin treats the first three as default providers and never uses `gemini`. This needs a Pal build whose `listmodels` returns CLI metadata in every mode: commit `c73dab7d` (2026-10-23) or a release containing it. The `uvx --from git+…` launch above installs current `main`.

Pal observes CLI executables at startup and caches its client registry: restart it after changing providers or client manifests.

**CLI read access.** Clink runs each CLI in your project root, but review criteria live in the plugin installation and the review bundle in the directory `mktemp` uses (`$TMPDIR` when set, otherwise `/tmp`; on macOS usually `/var/folders/...`). Denied reads are reported as lost coverage, never bypassed, so grant them once:

| CLI | Setup verified with the plugin |
| --- | --- |
| Claude Code | Override the client manifest at `~/.pal/cli_clients/claude.json`. The override replaces the whole definition: keep `name` and `command`, add `additional_args` such as `["--allowedTools", "Read,Glob,Grep"]` or a path-scoped rule covering that temp directory (`Read(//tmp/**)` on Linux). Restart Pal afterwards. |
| Antigravity (`agy`) | Where its mode does not already permit reads, add `"permissions": {"allow": ["read_file(/tmp)"]}` (or your `$TMPDIR`, plus the plugin cache path) to `~/.gemini/antigravity-cli/settings.json`. No restart needed. |
| Codex | Shipped manifest worked unchanged in the verified setup; whether reads are sandboxed depends on your Codex configuration (not verified). Allow several minutes per CLI review and check `tool_timeout_sec` for long MCP calls. |

Models stay configured where they are: Pal's model policy for API reviews, each CLI or client manifest for CLI reviews. To map a custom client name to its vendor, or to override the shipped defaults, declare it in the project's `CLAUDE.md`/`AGENTS.md` (for example `- \`mycli\` → Anthropic`).

### Capy (Knowledge Base)

Skills are **knowledge-aware** via Capy. They search for relevant context before executing (architecture decisions, review findings, language idioms) and index valuable learnings after producing output. Knowledge persists across sessions per-project using an FTS5 full-text search index.

Without Capy, each session starts fresh — all skills still work, they just don't carry learnings forward. Install when you want cross-session memory.

**Installation:** `brew install serpro69/tap/capy` then run `capy setup` in your project directory. The bootstrap script sets up Capy automatically if the binary is on PATH.

**Codex:** capy v0.17.1 and later also provides its own Codex hooks. Run `capy setup --platform codex` to register them; toolbox's Codex hooks then stop injecting `.capy/AGENTS.md` and stop blocking HTTP commands, leaving both to capy. See [Capy Hooks](../providers/codex.md#capy-hooks) for the handoff rules.
