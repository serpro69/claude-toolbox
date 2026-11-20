"""Exercise the staged engine and its registered Claude adapter on inert events."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from .payload import read_json
from . import state


def check_event(command, event, expected, workspace, env, timeout=30):
    body = dict(event, cwd=str(workspace), hook_event_name="PreToolUse")
    result = subprocess.run(command, input=json.dumps(body), text=True, capture_output=True,
                            cwd=workspace, env=env, timeout=timeout)
    if expected == "allow" and result.returncode == 0 and not result.stdout.strip():
        return
    if expected != "allow" and result.returncode == 2:
        decision = json.loads(result.stdout).get("hookSpecificOutput", {})
        if (decision.get("permissionDecision") == "deny" and
                decision.get("permissionDecisionReason", "").startswith("kk guard: " + expected + " ")):
            return
    raise ValueError("guard self-test expected {} for {}, exit {}: {}".format(
        expected, event["tool_name"], result.returncode, result.stderr.strip()))


def validate(root):
    plugin = root / "klaude-plugin"
    cases = read_json(root / "kk/selftest/guard-cases.json")
    groups = read_json(plugin / "hooks/hooks.json")["hooks"]["PreToolUse"]
    with tempfile.TemporaryDirectory(prefix="kk-selftest-") as folder:
        workspace = Path(folder).resolve()
        env = {key: value for key, value in os.environ.items() if not key.startswith("KK_GUARD_")}
        env.update(HOME=str(workspace), KK_GUARD_PROJECT_ROOT=str(workspace),
                   CLAUDE_PROJECT_DIR=str(workspace), CLAUDE_PLUGIN_ROOT=str(plugin))
        # Verify both entry points against a private journal before staging.
        trial = workspace / "toolbox"
        trial_release = "local-" + "0" * 32
        (trial / "releases").mkdir(parents=True)
        (trial / "releases" / trial_release).symlink_to(root, target_is_directory=True)
        trial_state = state.load(trial)
        state.promote(trial_state, trial_release)
        state.write_json(trial / "state.json", trial_state)
        report = subprocess.run([str(root / "kk/bin/kk"), "status"], env=dict(env, KK_HOME=str(trial)),
                                cwd=workspace, check=True, stdout=subprocess.PIPE, text=True, timeout=30)
        if trial_release not in report.stdout or "ready" not in report.stdout:
            raise ValueError("candidate kk status did not report the trial release as ready")
        engine = [sys.executable, "-I", "-B", "-S", str(plugin / "scripts/guard/guard.py")]
        for expected in ("allow", "secrets", "destructive", "selfmod"):
            check_event(engine, cases[expected], expected, workspace, env)
        for expected in ("allow", "secrets"):
            event = cases[expected]
            handlers = [hook for group in groups
                        if re.fullmatch(group.get("matcher") or ".*", event["tool_name"])
                        for hook in group["hooks"] if hook.get("type") == "command"]
            if not handlers:
                raise ValueError("no Claude PreToolUse command registered for " + event["tool_name"])
            for hook in handlers:
                check_event(["bash", "-c", hook["command"]], event, expected, workspace, env,
                            timeout=min(30, hook.get("timeout", 30)))
        subprocess.run(["claude", "plugin", "validate", str(plugin)], cwd=workspace, check=True)
