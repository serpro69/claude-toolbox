"""Register the local marketplace and verify Claude's effective source directory."""

import json
import os
from pathlib import Path
import shutil
import subprocess

from .state import write_json


MARKETPLACE = "toolbox"
PLUGIN_ID = "kk@" + MARKETPLACE
GIT_PLUGIN = "kk@claude-toolbox"


def vendor(home, *args):
    executable = shutil.which("claude")
    if executable is None:
        raise FileNotFoundError("claude executable not found on PATH")
    env = os.environ.copy()
    if env.get("CLAUDE_CONFIG_DIR"):
        env["CLAUDE_CONFIG_DIR"] = os.path.abspath(env["CLAUDE_CONFIG_DIR"])
    result = subprocess.run([os.path.abspath(executable), "plugin", *args, "--json"], cwd=home, env=env,
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True, check=True, timeout=60)
    return json.loads(result.stdout)


def marketplace_record(home):
    records = vendor(home, "marketplace", "list")
    for entry in records:
        if entry["name"] == MARKETPLACE:
            if not entry.get("installLocation") or Path(entry["installLocation"]).resolve() != home:
                raise ValueError("Claude marketplace {} already belongs to another source".format(MARKETPLACE))
            return entry
    return None


def verify_managed(rows, plugin):
    entry = next((p for p in rows if p["id"] == PLUGIN_ID and p["scope"] == "user"), {})
    source = entry.get("readFromFolder")
    if entry.get("enabled") is not True or not source or Path(source).resolve() != plugin:
        raise ValueError("Claude did not enable {} from {}; readFromFolder={!r}".format(PLUGIN_ID, plugin, source))


def settings_report(executable, workspace, env, sources, *flags):
    """Read vendor-resolved settings without a model turn or startup hooks."""
    request = {"type": "control_request", "request_id": "kk-settings", "request": {"subtype": "get_settings"}}
    result = subprocess.run(
        [executable, "--bare", "-p", "--input-format", "stream-json", "--output-format", "stream-json",
         "--verbose", "--no-session-persistence", "--strict-mcp-config", "--setting-sources", sources, *flags],
        cwd=workspace, env=env, input=json.dumps(request) + "\n", text=True, capture_output=True, timeout=15)
    for line in result.stdout.splitlines():
        event = json.loads(line)
        response = event.get("response", {}) if event.get("type") == "control_response" else {}
        if response.get("request_id") == "kk-settings" and response.get("subtype") == "success":
            return result.returncode, response["response"]
    raise ValueError("Claude could not report settings for " + str(workspace))


def activate(home, release, checkpoint):
    registered = marketplace_record(home)
    plugin = release / "klaude-plugin"
    manifest = {"name": MARKETPLACE, "owner": {"name": "claude-toolbox"},
                "plugins": [{"name": "kk", "source": "./" + plugin.relative_to(home).as_posix()}]}
    checkpoint("marketplace")
    write_json(home / ".claude-plugin/marketplace.json", manifest)
    if registered is None:
        checkpoint("register")
        vendor(home, "marketplace", "add", "--scope", "user", str(home))

    def user_install():
        return next((entry for entry in vendor(home, "list")
                     if entry["id"] == PLUGIN_ID and entry["scope"] == "user"), None)

    entry = user_install()
    if entry is None:
        checkpoint("install-plugin")
        vendor(home, "install", "--scope", "user", PLUGIN_ID)
    checkpoint("verify")
    verify_managed(vendor(home, "list"), plugin)
