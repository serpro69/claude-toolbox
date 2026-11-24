# MCP Servers

The kk installer leaves MCP setup to you. Configure shared services such as Context7 and Pal at user scope so you can reuse them across projects and keep API keys out of Git. Register Capy in each project where you want persistent memory.

You don't need all servers to get started. Add them incrementally:

1. **[Context7](https://context7.com/)** (needs API key) — up-to-date library documentation and code examples
2. **[Pal](https://github.com/serpro69/pal-mcp-server)** (API key optional) — multi-model AI integration for code review, debugging, planning, and security audit; without an API key, isolated reviews use your installed CLIs through `clink`
3. **[Capy](https://github.com/serpro69/capy)** (optional, configured per project) — persistent knowledge base across sessions. Install with `brew install serpro69/tap/capy`.

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
    Capy registers itself at the project level: run `capy setup --platform codex` in the project to add its MCP server to `.codex/config.toml` and its own Codex hooks to `.codex/hooks.json`. Capy’s hooks deliver guidance and HTTP routing. The machine guard covers supported capy execution calls. See [Capy Hooks](../providers/codex.md#capy-hooks).

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
| Claude Code | Use the machine launcher and a scoped read grant for temporary review files. See the client entry below. |
| Antigravity (`agy`) | Where its mode does not already permit reads, add `"permissions": {"allow": ["read_file(/tmp)"]}` (or your `$TMPDIR`, plus the plugin cache path) to `~/.gemini/antigravity-cli/settings.json`. No restart needed. |
| Codex | Shipped manifest worked unchanged in the verified setup; whether reads are sandboxed depends on your Codex configuration (not verified). Allow several minutes per CLI review and check `tool_timeout_sec` for long MCP calls. |

#### Claude client for machine installations

Copy PAL’s shipped `conf/cli_clients/claude.json` to `~/.pal/cli_clients/claude.json`, or edit your existing override. PAL replaces the whole client definition. Keep the existing roles, model arguments and permission-mode arguments. Set these two fields in that definition. This Linux example also supports reviews initiated from a managed Codex installation with the default Codex home:

```json
{
  "command": "kk claude",
  "additional_args": ["--allowedTools", "Read(//tmp/**)", "Read(~/.codex/plugins/cache/agentstakk-local/kk/**)"]
}
```

PAL splits `command` into the executable and its first argument. Put the directory containing `kk` on **PAL’s** `PATH`, or use the physical absolute path to the dispatcher followed by ` claude`. Keep the real Claude CLI available on that path too. PAL starts a new process for each review, so wrapping your interactive session alone does not apply its settings to the reviewer.

The launcher’s default `readRelease` permission covers criteria loaded from the managed Claude release. Codex can pass criteria from its installed skills cache, so the example grants access to that plugin’s directory too. If `CODEX_HOME` is elsewhere, substitute its physical location. A Git-marketplace installation can have a different plugin directory: use the installed skill’s path to identify it. Scope the read to the skills plugin whose criteria the reviewer needs.

The temp grant covers the directory where the originating review creates its diff with `mktemp`. Substitute that directory’s physical absolute path for `/tmp` when needed. For example, for `TMPDIR=/work/review-tmp` the rule is `Read(//work/review-tmp/**)`. On macOS check `cd "${TMPDIR:-/tmp}" && pwd -P` in the originating shell. Keep a dedicated review directory if other temporary files should stay outside this grant.

Restart PAL after editing the client. In a read-only `clink` review, check that the reviewer can read a criterion at the path supplied by the originating skill and the diff in the selected temporary directory.

Models stay configured where they are: Pal's model policy for API reviews, each CLI or client manifest for CLI reviews. To map a custom client name to its vendor, or to override the shipped defaults, declare it in the project's `CLAUDE.md`/`AGENTS.md` (for example `- \`mycli\` → Anthropic`).

### Capy (Knowledge Base)

Skills are **knowledge-aware** via Capy. They search for relevant context before executing (architecture decisions, review findings, language idioms) and index valuable learnings after producing output. Knowledge persists across sessions per-project using an FTS5 full-text search index.

Without Capy, each session starts fresh — all skills still work, they just don't carry learnings forward. Install when you want cross-session memory.

**Installation:** `brew install serpro69/tap/capy` then run `capy setup` in your project directory. Machine installation leaves capy registration to each project.

**Codex:** Run `capy setup --platform codex` to register its hooks and review them in `/hooks`. Wrapped sessions can also load `.capy/AGENTS.md` through a confirmed import in the root `AGENTS.md`. [Capy hooks](../providers/codex.md#capy-hooks)
