# Template Setup

Use the GitHub template to create a new project with the full claude-toolbox configuration pre-wired.

## Steps

1. **Create from template**: Go to [serpro69/claude-toolbox](https://github.com/serpro69/claude-toolbox), click **Use this template** → **Create a new repository**

2. **Run template cleanup** (removes toolbox-specific files, keeps your config):

    === "GitHub Actions (recommended)"

        The `template-cleanup.yml` workflow runs automatically on first push. Check the Actions tab for status.

    === "Local"

        ```bash
        bash .github/scripts/template-cleanup.sh
        ```

3. **Install MCP servers** — add to `~/.claude.json` (Claude Code) or user-level config (Codex). See [MCP Servers](../user-guide/mcp-servers.md) for details.

4. **Set API keys** in your shell profile:

    ```bash
    export CONTEXT7_API_KEY="your-key"
    export GEMINI_API_KEY="your-key"
    ```

5. **Install the plugin** (Claude Code):

    ```
    /plugin install kk@claude-toolbox
    ```

6. **Verify**: Run `/kk:design "hello world feature"` to test the pipeline.

## What You Get

- `.claude/` — settings, statusline, sync infrastructure
- `.codex/` — Codex-equivalent configuration
- `CLAUDE.md` / `AGENTS.md` — project instructions
- Template sync — pull future updates from upstream

## Next Steps

- [Try It](quickstart.md) — run the pipeline in 5 minutes
- [Template Sync](../user-guide/template-sync.md) — how to receive upstream updates
