"""Register the local marketplace and verify Claude's effective source directory."""

import json
from pathlib import Path
import subprocess

from .state import write_json


MARKETPLACE = "toolbox"
PLUGIN_ID = "kk@" + MARKETPLACE


def vendor(home, *args):
    result = subprocess.run(["claude", "plugin", *args, "--json"], cwd=home,
                            stdout=subprocess.PIPE, text=True, check=True)
    return json.loads(result.stdout)


def marketplace_record(home):
    records = vendor(home, "marketplace", "list")
    for entry in records:
        if entry["name"] == MARKETPLACE:
            if not entry.get("installLocation") or Path(entry["installLocation"]).resolve() != home:
                raise ValueError("Claude marketplace {} already belongs to another source".format(MARKETPLACE))
            return entry
    return None


def activate(home, release):
    registered = marketplace_record(home)
    plugin = release / "klaude-plugin"
    manifest = {"name": MARKETPLACE, "owner": {"name": "claude-toolbox"},
                "plugins": [{"name": "kk", "source": "./" + plugin.relative_to(home).as_posix()}]}
    write_json(home / ".claude-plugin/marketplace.json", manifest)
    if registered is None:
        vendor(home, "marketplace", "add", "--scope", "user", str(home))

    def user_install():
        return next((entry for entry in vendor(home, "list")
                     if entry["id"] == PLUGIN_ID and entry["scope"] == "user"), None)

    entry = user_install()
    if entry is None:
        vendor(home, "install", "--scope", "user", PLUGIN_ID)
        entry = user_install()
    source = (entry or {}).get("readFromFolder")
    if not entry or entry.get("enabled") is not True or not source or Path(source).resolve() != plugin:
        raise ValueError("Claude did not enable {} from {}; readFromFolder={!r}".format(PLUGIN_ID, plugin, source))
