"""Reconcile public and pilot registrations with the machine-managed marketplace."""

import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

from . import claude, codex_plugins, payload


GIT_GUARD = "kk-guard@" + claude.PUBLIC_MARKETPLACE
PUBLIC_GUARDS = (GIT_GUARD, "kk-guard@" + claude.FORMER_PUBLIC_MARKETPLACE)
OTHER_GUARDS = (*PUBLIC_GUARDS, "kk-guard@" + claude.PILOT_MARKETPLACE)


def is_pilot_catalog(path):
    return path.is_file() and payload.read_json(path).get("name") == claude.PILOT_MARKETPLACE


def check_claude_pilot(home):
    """RC4 and its successor publish different names at the same physical catalog."""
    if not is_pilot_catalog(home / ".claude-plugin/marketplace.json"):
        return
    markets = claude.vendor(home, "marketplace", "list")
    if any(m["name"] == claude.PILOT_MARKETPLACE and Path(m["installLocation"]).resolve() == home for m in markets):
        raise ValueError("the RC4 Claude marketplace toolbox still uses {}. Follow the install guide's "
                         "RC4 marketplace switch, then rerun this command.".format(home))


def check_codex_pilot(home, record, directory):
    if not is_pilot_catalog(home / ".agents/plugins/marketplace.json"):
        return
    homes = set(record.get("codex_plugins", {}))
    if directory is not None:
        homes.add(str(directory))
    for previous in sorted(homes):
        if not Path(previous).is_dir():
            continue
        markets = codex_plugins.vendor(home, previous, "marketplace", "list")["marketplaces"]
        if any(m["name"] == claude.PILOT_MARKETPLACE and Path(m["root"]).resolve() == home for m in markets):
            raise ValueError("the RC4 Codex marketplace toolbox still uses {} in CODEX_HOME {}. Follow the "
                             "install guide's RC4 marketplace switch, then rerun this command.".format(home, previous))


class Install(NamedTuple):
    plugin: str
    scope: str
    enabled: bool
    project: str


def inventory(tool, workspace, directory):
    if tool == "claude":
        return claude.vendor(workspace, "list")
    return codex_plugins.vendor(workspace, directory, "list", timeout=codex_plugins.INVENTORY_TIMEOUT)["installed"]


def other_copies(tool, rows):
    if tool == "claude":
        return [Install(p["id"], p["scope"], p.get("enabled") is not False, p.get("projectPath") or "")
                for p in rows if p["id"] in claude.OTHER_PLUGINS]
    return [Install(p["pluginId"], p.get("scope", "user"), p.get("enabled") is not False, "")
            for p in rows if p["pluginId"] in (*claude.OTHER_PLUGINS, *OTHER_GUARDS)]


def claude_managed(rows):
    return any(p["id"] == claude.PLUGIN_ID and p["scope"] == "user" and p.get("enabled") is True for p in rows)


def inspect(tool, workspace, directory=None, *, claude_plugin=None):
    try:
        rows = inventory(tool, workspace, directory)
        installs = other_copies(tool, rows)
        issues = []
        if tool == "claude":
            if not claude_managed(rows):
                issues.append("managed user-scope plugin {} is missing or disabled".format(claude.PLUGIN_ID))
            elif claude_plugin is not None:
                try:
                    enabled = claude.verify_workspace(rows, claude_plugin, workspace)
                    for plugin in claude.OTHER_PLUGINS:
                        if enabled.get(plugin) is True:
                            issues.append("settings also enable {} in {}".format(plugin, workspace))
                except (ValueError, OSError, subprocess.SubprocessError) as exc:
                    issues.append(str(exc))
        elif not any(p["pluginId"] == codex_plugins.GUARD_ID and p.get("enabled") is True for p in rows):
            issues.append("managed guard {} is missing or disabled".format(codex_plugins.GUARD_ID))
        guards = claude.OTHER_PLUGINS if tool == "claude" else OTHER_GUARDS
        for entry in installs:
            if entry.plugin not in guards or not entry.enabled:
                continue
            if entry.project and Path(entry.project).resolve() not in (workspace, *workspace.parents):
                continue
            issues.append("enabled guard {} ({} scope); active hooks are ambiguous".format(entry.plugin, entry.scope))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        return [], ["could not verify {} plugin inventory: {}".format(tool, exc)]
    return installs, issues


def remove_user_copies(tool, workspace, directory, guard_issues=()):
    rows = inventory(tool, workspace, directory)
    copies = other_copies(tool, rows)
    for plugin in sorted({i.plugin for i in copies if i.scope == "user" and i.plugin in (*claude.PUBLIC_PLUGINS, *PUBLIC_GUARDS)}):
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
        if plugin in PUBLIC_GUARDS and any(i.plugin == plugin and i.enabled for i in copies):
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
