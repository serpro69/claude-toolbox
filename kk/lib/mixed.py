"""Report the toolbox Git-marketplace copies alongside the machine-managed ones."""

import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

from . import claude, codex_plugins


GIT_GUARD = "kk-guard@claude-toolbox"


class Install(NamedTuple):
    plugin: str
    scope: str
    enabled: bool
    project: str


def inventory(tool, workspace, directory):
    if tool == "claude":
        return claude.vendor(workspace, "list")
    return codex_plugins.vendor(workspace, directory, "list", "--marketplace", "claude-toolbox")["installed"]


def git_copies(tool, rows):
    if tool == "claude":
        return [Install(p["id"], p["scope"], p.get("enabled") is not False, p.get("projectPath") or "")
                for p in rows if p["id"] == claude.GIT_PLUGIN]
    return [Install(p["pluginId"], p.get("scope", "user"), p.get("enabled") is not False, "")
            for p in rows if p["pluginId"] in (claude.GIT_PLUGIN, GIT_GUARD)]


def claude_managed(rows):
    return any(p["id"] == claude.PLUGIN_ID and p["scope"] == "user" and p.get("enabled") is True for p in rows)


def inspect(tool, workspace, directory=None):
    try:
        rows = inventory(tool, workspace, directory)
        installs = git_copies(tool, rows)
        issues = []
        if tool == "claude" and not claude_managed(rows):
            issues.append("managed user-scope plugin {} is missing or disabled".format(claude.PLUGIN_ID))
        guard = claude.GIT_PLUGIN if tool == "claude" else GIT_GUARD
        for entry in installs:
            if entry.plugin != guard or not entry.enabled:
                continue
            if entry.project and Path(entry.project).resolve() not in (workspace, *workspace.parents):
                continue
            issues.append("enabled Git-marketplace guard {} ({} scope); active hooks are ambiguous".format(guard, entry.scope))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        return [], ["could not verify {} plugin inventory: {}".format(tool, exc)]
    return installs, issues


def remove_user_copies(tool, workspace, directory, guard_issues=()):
    rows = inventory(tool, workspace, directory)
    copies = git_copies(tool, rows)
    for plugin in sorted({i.plugin for i in copies if i.scope == "user"}):
        if tool == "claude":
            peer = claude_managed(rows)
        else:
            local_id = plugin.split("@")[0] + "@" + claude.MARKETPLACE
            local = codex_plugins.vendor(workspace, directory, "list", "--marketplace", claude.MARKETPLACE)
            peer = any(p["pluginId"] == local_id and p.get("enabled") is True for p in local["installed"])
        if not peer:
            raise ValueError("enable the managed counterpart before removing " + plugin)
        if not sys.stdin.isatty():
            raise ValueError("removing a Git-marketplace install needs confirmation at a terminal")
        if plugin == GIT_GUARD and any(i.plugin == plugin and i.enabled for i in copies):
            for issue in guard_issues:
                print("  " + issue, file=sys.stderr)
            print("If the managed {} hooks still need review in /hooks, removing the Git guard "
                  "can leave Codex sessions unguarded.".format(codex_plugins.GUARD_ID), file=sys.stderr)
        print("Remove user-scope {} plugin {}? [y/N] ".format(tool, plugin), end="", file=sys.stderr, flush=True)
        if sys.stdin.readline().strip().lower() not in ("y", "yes"):
            continue
        if tool == "claude":
            claude.vendor(workspace, "uninstall", "--scope", "user", "--keep-data", plugin)
        else:
            codex_plugins.vendor(workspace, directory, "remove", plugin)
