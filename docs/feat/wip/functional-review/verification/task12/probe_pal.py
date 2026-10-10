"""Read-only MCP startup diagnosis with the declared run-local environment."""
import argparse
import json
from pathlib import Path
import subprocess
import tomllib

import controller
from probe_state import Capy, run_environment


class Pal(Capy):
    def __init__(self, workspace, evidence):
        config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())["mcp_servers"]["pal"]
        env = run_environment(workspace)
        env.update({k: v for k, v in config.get("env", {}).items() if k != "PATH"})
        self.events, self.buffer, self.sequence = [], b"", 0
        self.error_log = (evidence / "stderr.txt").open("x")
        try:
            self.process = subprocess.Popen([config["command"], *config.get("args", [])],
                cwd=workspace, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.error_log)
        except BaseException:
            self.error_log.close()
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=False)
    client = Pal(args.workspace, args.evidence)
    try:
        client.initialize()
        result = client.call("tools/list", {})
        controller.seed.write_json(args.evidence / "result.json", {
            "status": "connected", "tools": [item["name"] for item in result["tools"]]})
    except (RuntimeError, TimeoutError) as exc:
        controller.seed.write_json(args.evidence / "result.json", {"status": "failed", "error": str(exc)})
        raise
    finally:
        client.close()
        controller.seed.write_json(args.evidence / "events.json", client.events)
        controller.seed.seal(args.evidence)


if __name__ == "__main__":
    main()
