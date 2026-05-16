# Adopting into Existing Repositories

Want the full claude-toolbox setup (configuration, plugin, sync infrastructure) in an existing project? Follow these steps.

## Steps

1. **Copy the configuration files** from a fresh template instance or the claude-toolbox repo:

    ```bash
    # Core configuration
    cp -r .claude/ your-project/.claude/
    cp CLAUDE.md your-project/
    cp AGENTS.md your-project/

    # Codex support (optional)
    cp -r .codex/ your-project/.codex/

    # Sync infrastructure
    cp -r .github/scripts/template-sync.sh your-project/.github/scripts/
    cp -r .github/workflows/template-sync.yml your-project/.github/workflows/
    ```

2. **Create a template state file** at `.github/template-state.json`:

    ```json
    {
      "template_version": "v0.14.0",
      "template_repo": "serpro69/claude-toolbox"
    }
    ```

3. **Install MCP servers and the plugin** — see [MCP Servers](../user-guide/mcp-servers.md) and [Plugin-Only Setup](plugin-only.md).

## After Adoption

- Run [template sync](../user-guide/template-sync.md) to verify the setup: `/kk:template:sync --dry-run`
- Customize `.claude/settings.json` for your project's permission needs
- Edit `CLAUDE.md` with project-specific instructions
