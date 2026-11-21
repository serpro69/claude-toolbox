"""Read Codex's effective guard handlers for one workspace without changing trust."""

import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Timer

from . import codex_plugins, payload
from .codex_plugins import GUARD_ID


class NoTrustMethod(Exception):
    """The vendor explicitly reported that hooks/list is unavailable."""


def hooks(directory, workspace, flags, executable):
    with subprocess.Popen([executable, *flags, "app-server"], cwd=workspace,
                          env=dict(os.environ, CODEX_HOME=str(directory)), text=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
        timeout = Timer(10, proc.kill)
        timeout.start()

        def send(message):
            proc.stdin.write(json.dumps(dict(jsonrpc="2.0", **message)) + "\n")
            proc.stdin.flush()

        def request(number, method, params):
            send({"id": number, "method": method, "params": params})
            for line in proc.stdout:
                msg = json.loads(line)
                if msg.get("id") != number:
                    continue
                if "error" in msg:
                    if method == "hooks/list" and msg["error"].get("code") == -32601:
                        raise NoTrustMethod
                    raise ValueError("Codex {} failed: {}".format(method, msg["error"]))
                return msg["result"]
            raise ValueError("Codex app-server stopped or timed out during " + method)

        try:
            request(1, "initialize", {"clientInfo": {"name": "kk", "version": "1"}})
            send({"method": "initialized"})
            rows = request(2, "hooks/list", {"cwds": [str(workspace)]})["data"]
            if len(rows) != 1 or rows[0]["cwd"] != str(workspace) or rows[0]["errors"]:
                raise ValueError("Codex could not list hooks for " + str(workspace))
            return rows[0]["hooks"]
        finally:
            timeout.cancel()
            proc.kill()
            proc.wait()


def check(release, directory, workspace, flags=(), *, acknowledged=False, prompt=False, executable=None):
    groups = payload.read_json(release / "kodex-guard/hooks/hooks.json")["hooks"]["PreToolUse"]
    try:
        rows = hooks(directory, workspace, flags, executable or codex_plugins.executable())
    except NoTrustMethod:
        if not acknowledged and prompt and sys.stdin.isatty():
            print("Codex cannot report hook trust. Have you reviewed and enabled all kk-guard hooks "
                  "in /hooks? [y/N] ", end="", file=sys.stderr, flush=True)
            acknowledged = sys.stdin.readline().strip().lower() in ("y", "yes")
        if acknowledged:
            return "unverified", ["this Codex has no hooks/list method"]
        return "awaiting review", ["review the guard in /hooks, then run kk apply to acknowledge"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return "awaiting review", ["could not verify Codex guard: " + str(exc)]
    listed = {h["key"]: h for h in rows if h.get("pluginId") == GUARD_ID and h.get("source") == "plugin"}
    issues = []
    for i, group in enumerate(groups):
        for j, handler in enumerate(group["hooks"]):
            key = "{}:hooks/hooks.json:pre_tool_use:{}:{}".format(GUARD_ID, i, j)
            hook = listed.get(key)
            if hook is None:
                issue = "absent; check features.hooks, features.plugins and plugins.{}.enabled".format(GUARD_ID)
            elif hook.get("matcher") != group["matcher"] or hook.get("command") != handler["command"]:
                issue = "registration differs from the release; repair the installed guard"
            elif hook.get("enabled") is not True:
                issue = "disabled; enable it in /hooks"
            elif hook.get("trustStatus") != "trusted":
                issue = "{}; review it in /hooks".format(hook.get("trustStatus", "unknown"))
            else:
                continue
            issues.append("{}: {}".format(group["matcher"], issue))
    return ("awaiting review" if issues else "ready"), issues


def machine(release, saved, *, prompt=False):
    # A caller's cwd and TMPDIR can both be inside a trusted repository.
    return check(release, Path(saved["codex_snapshot"]["directory"]), Path("/"),
                 acknowledged=saved.get("tools", {}).get("codex") == "unverified", prompt=prompt)


def report(phase, issues):
    print("codex: " + phase)
    for issue in issues:
        print("  " + issue)
