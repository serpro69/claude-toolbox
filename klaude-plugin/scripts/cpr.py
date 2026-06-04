#!/usr/bin/env python3
"""
Claude Plugin Root (CPR) Resolver

Usage:   cpr.py <plugin-name> [project-dir]
Returns: absolute path to the plugin installation directory that applies to the
         current project (printed to stdout)

Reads ~/.claude/plugins/installed_plugins.json and picks the install via a
fallback cascade scoped to `project-dir`:

  1. A project-bound entry (it carries a `projectPath`) whose `projectPath` is
     the current project directory, or an ancestor of it.
  2. Otherwise, a global entry (no `projectPath` — i.e. a user-scope install).
  3. Otherwise, the most-recently-installed entry, regardless of project.

Each tier returns only an install whose `installPath` exists on disk; if it
does not, the cascade falls through to the next tier.

`project-dir` defaults to the current working directory when omitted; the
SessionStart hook passes `$CLAUDE_PROJECT_DIR` explicitly.

KNOWN ISSUES:
    - problem:
        - `claude plugin list` shows the plugin as installed
        - ~/.claude/plugins/installed_plugins.json does not have a project entry for the plugin
      solution:
        - re-run `claude plugin install kk@claude-toolbox --scope project`
          (or the scope where you have the plugin installed as shown by the `claude plugin list` command)
"""

import json
import os
import sys
from pathlib import Path
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def plugin_name_from_key(key):
    """Extract the plugin name segment from a registry key.

    Keys look like "plugin-name@repo-name" (e.g. "kk@claude-toolbox").
    """
    return key.split("@")[0]


def _norm(path):
    return str(path or "").rstrip("/")


def _applies_to_project(entry, project_dir):
    """True if a project-bound entry's projectPath covers project_dir.

    Covers both an exact match and project_dir being a subdirectory of the
    recorded project root (the hook may run from a nested cwd).
    """
    pp = _norm(entry.get("projectPath"))
    if not pp:
        return False
    return project_dir == pp or project_dir.startswith(pp + "/")


def _pick_existing(entries):
    """Most-recently-installed entry whose installPath exists on disk, else None."""
    for entry in sorted(entries, key=lambda e: e.get("installedAt", ""), reverse=True):
        path = _norm(entry.get("installPath"))
        if path and os.path.isdir(path):
            return path
    return None


def _resolve_entries(entries, project_dir):
    """Pick the best install path for one plugin key, scoped to project_dir.

    Cascade: (1) an entry bound to the current project, (2) a global
    (user-scope, no projectPath) entry, (3) the most-recently-installed entry
    regardless of project. Each tier yields only an install whose path exists.
    """
    if not isinstance(entries, list):
        entries = [entries]
    project_bound = [e for e in entries if _applies_to_project(e, project_dir)]
    global_scope = [e for e in entries if not _norm(e.get("projectPath"))]
    for tier in (project_bound, global_scope, entries):
        path = _pick_existing(tier)
        if path:
            return path
    return None


def find_plugin_root(plugin_name, project_dir):
    """
    Find the plugin installation directory that applies to project_dir.

    Returns: (plugin_root_path, match_type)
        match_type: 'exact', 'fuzzy', or None
    """
    plugins_file = Path(os.environ["CPR_PLUGINS_FILE"]) if "CPR_PLUGINS_FILE" in os.environ else Path.home() / ".claude" / "plugins" / "installed_plugins.json"

    if not plugins_file.exists():
        return None, None

    try:
        with open(plugins_file, "r") as f:
            data = json.load(f)
            plugins = data.get("plugins", {})
    except (OSError, json.JSONDecodeError):
        return None, None

    project_dir = _norm(project_dir)

    # Exact match on the plugin name segment (case-insensitive).
    for key, entries in plugins.items():
        if plugin_name_from_key(key).lower() == plugin_name.lower():
            path = _resolve_entries(entries, project_dir)
            if path:
                return path, "exact"

    # Fuzzy match on the plugin name segment.
    matches = []
    for key, entries in plugins.items():
        ratio = similarity(plugin_name, plugin_name_from_key(key))
        if ratio > 0.6:
            path = _resolve_entries(entries, project_dir)
            if path:
                matches.append((ratio, path))

    if matches:
        matches.sort(reverse=True, key=lambda x: x[0])
        return matches[0][1], "fuzzy"

    return None, None


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <plugin-name> [project-dir]", file=sys.stderr)
        print(f"Example: python3 {sys.argv[0]} kk", file=sys.stderr)
        sys.exit(1)

    plugin_name = sys.argv[1]
    project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    plugin_root, match_type = find_plugin_root(plugin_name, project_dir)

    if plugin_root:
        if match_type == "fuzzy":
            # Fail loud: a fuzzy hit may resolve to the wrong plugin. Warn on
            # stderr only — stdout stays clean for command substitution.
            print(
                f"Warning: no exact match for '{plugin_name}'; "
                f"using closest fuzzy match: {plugin_root}",
                file=sys.stderr,
            )
        # Output just the path to stdout (for command substitution)
        print(plugin_root)
        sys.exit(0)
    else:
        print(
            f"Error: Could not locate plugin '{plugin_name}' for project '{project_dir}'",
            file=sys.stderr,
        )
        print(
            "Checked: ~/.claude/plugins/installed_plugins.json",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
