"""Read Codex's effective guard handlers for one workspace without changing trust."""

from pathlib import Path
import sys

from . import claude, codex_app, codex_plugins, mixed, payload
from .codex_plugins import GUARD_ID


REVIEW_UI = "/hooks in plain codex (without --profile)"
NoTrustMethod = codex_app.NoMethod  # hooks/list is the only method the trust read requests.


def hooks(directory, workspace, flags, executable):
    result, = codex_app.session(directory, workspace, flags, executable,
                                [("hooks/list", {"cwds": [str(workspace)]})], 10)
    rows = result["data"]
    if len(rows) != 1 or rows[0]["cwd"] != str(workspace) or rows[0]["errors"]:
        raise ValueError("Codex could not list hooks for " + str(workspace))
    return rows[0]["hooks"]


def check(release, directory, workspace, flags=(), *, acknowledged=False, prompt=False, executable=None):
    groups = payload.read_json(release / "kodex-guard/hooks/hooks.json")["hooks"]["PreToolUse"]
    try:
        rows = hooks(directory, workspace, flags, executable or codex_plugins.executable())
    except NoTrustMethod:
        _, issues = mixed.inspect("codex", workspace, directory)
        if issues:
            return "awaiting review", issues
        if not acknowledged and prompt and sys.stdin.isatty():
            print("Codex cannot report hook trust. Have you reviewed and enabled all kk-guard hooks "
                  "in {}? [y/N] ".format(REVIEW_UI), end="", file=sys.stderr, flush=True)
            acknowledged = sys.stdin.readline().strip().lower() in ("y", "yes")
        if acknowledged:
            return "unverified", ["this Codex has no hooks/list method"]
        return "awaiting review", ["review the guard in {}, then run kk apply to acknowledge".format(REVIEW_UI)]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return "awaiting review", ["could not verify Codex guard: " + str(exc)]
    listed = {h["key"]: h for h in rows if h.get("pluginId") == GUARD_ID and h.get("source") == "plugin"}
    issues = []
    if any(h.get("source") == "plugin" and h.get("enabled") is True
           and h.get("pluginId") in (*claude.OTHER_PLUGINS, *mixed.OTHER_GUARDS) for h in rows):
        issues.append("other marketplace hooks also apply in this workspace")
    for i, group in enumerate(groups):
        for j, handler in enumerate(group["hooks"]):
            key = "{}:hooks/hooks.json:pre_tool_use:{}:{}".format(GUARD_ID, i, j)
            hook = listed.get(key)
            if hook is None:
                issue = "absent; check features.hooks, features.plugins and plugins.{}.enabled".format(GUARD_ID)
            elif hook.get("matcher") != group["matcher"] or hook.get("command") != handler["command"]:
                issue = "registration differs from the release; repair the installed guard"
            elif hook.get("enabled") is not True:
                issue = "disabled; enable it in " + REVIEW_UI
            elif hook.get("trustStatus") != "trusted":
                issue = "{}; review it in {}".format(hook.get("trustStatus", "unknown"), REVIEW_UI)
            else:
                continue
            issues.append("{}: {}".format(group["matcher"], issue))
    return ("awaiting review" if issues else "ready"), issues


def machine(release, saved, *, prompt=False, inventory_issues=None, workspace=Path("/")):
    # A caller's cwd and TMPDIR can both be inside a trusted repository.
    directory = Path(saved["codex_snapshot"]["directory"])
    if inventory_issues is None:
        _, inventory_issues = mixed.inspect("codex", workspace, directory)
    phase, details = check(release, directory, workspace,
                           acknowledged=saved.get("tools", {}).get("codex") == "unverified",
                           prompt=prompt and not inventory_issues)
    if inventory_issues:
        return "awaiting review", list(dict.fromkeys([*inventory_issues, *details]))
    return phase, details


def report(phase, issues):
    print("codex: " + phase)
    for issue in issues:
        print("  " + issue)
