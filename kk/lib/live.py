"""Exercise the installed guard through one real vendor session in a private workspace."""

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from . import codex_plugins, codex_profile, mixed, state


def claude_errors(stream, canary):
    requests = set()
    for line in stream.splitlines():
        event = json.loads(line)
        if not isinstance(event, dict) or not isinstance(event.get("message"), dict):
            continue
        blocks = event["message"].get("content", [])
        for block in blocks if isinstance(blocks, list) else ():
            if not isinstance(block, dict):
                continue
            if event["type"] == "assistant" and block.get("type") == "tool_use" and block.get("name") == "Read":
                name = block.get("input", {}).get("file_path")
                if name and (canary.parent / name).resolve() == canary:
                    requests.add(block["id"])
            if (event["type"] == "user" and block.get("type") == "tool_result"
                    and block.get("is_error") is True and block.get("tool_use_id") in requests):
                content = block.get("content")
                if isinstance(content, str):
                    yield content
                elif isinstance(content, list):
                    yield from (part["text"] for part in content if isinstance(part, dict) and part.get("type") == "text")


def run(tool, home):
    # Never inherit a repository's TMPDIR, working tree, or project hooks.
    with tempfile.TemporaryDirectory(prefix="kk-live-", dir="/tmp") as temp:
        workspace = Path(temp).resolve()
        canary = workspace / (workspace.name + ".txt")
        canary.write_text("Public toolbox guard check fixture.\n", encoding="utf-8")
        # A unique, additive secret rule avoids native Read forbids and
        # attributes the denial to the guard anchored in this exact workspace.
        glob = "./**/" + canary.name
        state.write_json(workspace / ".claude/kk-guard.json", {"version": 1, "secrets": [glob]})
        env = dict(os.environ, KK_HOME=str(home))
        for key in ("CODEX_HOME", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME"):
            if env.get(key):
                env[key] = os.path.abspath(env[key])
        for key in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "CLAUDE_PROJECT_DIR", "KK_GUARD_PROJECT_ROOT"):
            env.pop(key, None)
        env["PATH"] = os.pathsep.join(os.path.abspath(p) for p in os.get_exec_path())
        subprocess.run(["git", "init", "--quiet", "--template=", "."], cwd=workspace, env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, check=True, timeout=10)
        _, issues = mixed.inspect(tool, workspace, codex_profile.codex_home())
        if issues:
            raise ValueError("; ".join(issues))
        session_timeout = 90
        if tool == "claude":
            args = ["-p", "--verbose", "--output-format", "stream-json", "--tools", "Read",
                    "--no-session-persistence", "Use Read once on {}. Then stop.".format(canary)]
        else:
            # Without hooks/list the batch launcher checks the inventory again
            # before Codex can start the live model session.
            session_timeout += codex_plugins.INVENTORY_TIMEOUT
            args = ["exec", "--ephemeral", "--sandbox", "read-only", "--json",
                    "Use the shell tool once to run the following command, then stop.\ncat {}".format(canary.name)]
            env["RUST_LOG"] = "codex_core::tools::router=error"
        result = subprocess.run([str(home / "bin/kk"), tool, *args], cwd=workspace, env=env,
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=session_timeout)
        if result.returncode:
            # Callers print this message behind their own "kk: " or "live: failed: ".
            message = next((line[4:] for line in result.stderr.splitlines() if line.startswith("kk: ")), "")
            raise ValueError(message[:500] or "vendor session exited {}; check {} authentication and guard settings".format(
                result.returncode, tool))
        if tool == "claude":
            errors = claude_errors(result.stdout, canary)
        else:
            errors = (line for line in result.stderr.splitlines()
                      if "codex_core::tools::router: error=Command blocked by PreToolUse hook:" in line)
        reason = re.compile(r"kk guard: secrets — [^\r\n]*? matches " + re.escape(glob) + r"(?=\. Way through:)")
        if any(reason.search(error) for error in errors):
            return "ok (guard denied the canary read)"
        raise ValueError("the vendor session did not report the installed guard denying the canary read")
