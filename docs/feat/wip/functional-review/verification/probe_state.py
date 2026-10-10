#!/usr/bin/env python3
"""Task 1: exercise real, separate Capy stdio servers without real vault state."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import select
import subprocess
import time


def run_environment(workspace):
    env = {key: value for key, value in os.environ.items() if not key.startswith("CAPY_")}
    env.update(CAPY_DB_KEY="synthetic-functional-review-probe-key-20261008",
               CAPY_VAULT_PATH=str(workspace / ".runner/vault"),
               XDG_CONFIG_HOME=str(workspace / ".runner/xdg"), PYTHONDONTWRITEBYTECODE="1")
    return env


def workspace_at(path):
    path.mkdir(parents=True, exist_ok=False)
    (path / ".runner").mkdir()
    (path / ".capy.toml").write_text('[store]\npath = ".runner/knowledge.db"\nkey_file = ""\n')
    fixture = b"# Disposable instruction-loading probe\n"
    (path / "README.md").write_bytes(fixture)
    git_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    git_env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    git = ["git", "-c", "core.hooksPath=" + os.devnull, "-C", str(path)]
    subprocess.run([*git, "init", "--template=", "-q"], env=git_env, check=True)
    (path / ".git/info").mkdir(exist_ok=True)
    (path / ".git/info/exclude").write_text(".runner/\n.capy.toml\n.agents/\n.codex/\n.claude/\nplugins/\n")
    subprocess.run([*git, "add", "README.md"], env=git_env, check=True)
    subprocess.run([*git, "-c", "user.name=Eval Probe", "-c",
                    "user.email=probe@example.invalid", "-c", "commit.gpgsign=false",
                    "commit", "-qm", "Create clean probe"], env=git_env, check=True)
    require((path / "README.md").read_bytes() == fixture, "Initial fixture mutated")
    require(not subprocess.check_output([*git, "status", "--porcelain"], env=git_env),
            "Initial worktree not clean")
    return path


class Capy:
    def __init__(self, workspace, evidence):
        self.events = []
        self.error_log = (evidence / (workspace.name + ".stderr")).open("w")
        try:
            self.process = subprocess.Popen(
                ["capy", "--project-dir", str(workspace), "serve"], cwd=workspace,
                env=run_environment(workspace), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self.error_log)
        except (OSError, ValueError):
            self.error_log.close()
            raise
        self.buffer = b""
        self.sequence = 0

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        finally:
            self.process.stdout.close()
            self.error_log.close()

    def call(self, method, params):
        self.sequence += 1
        request = {"jsonrpc": "2.0", "id": self.sequence, "method": method, "params": params}
        self.events.append({"request": request})
        self.process.stdin.write((json.dumps(request) + "\n").encode())
        self.process.stdin.flush()
        deadline = time.monotonic() + 30
        while True:
            while b"\n" not in self.buffer:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not select.select([self.process.stdout], [], [], remaining)[0]:
                    raise TimeoutError("Capy response timeout: " + method)
                chunk = os.read(self.process.stdout.fileno(), 65536)
                if not chunk:
                    raise RuntimeError("Capy closed stdout: " + method)
                self.buffer += chunk
            line, self.buffer = self.buffer.split(b"\n", 1)
            try:
                response = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError("Non-JSON Capy stdout: " + repr(line[:200])) from exc
            self.events.append({"response": response})
            if response.get("id") == self.sequence:
                if "error" in response:
                    raise RuntimeError(str(response["error"]))
                return response["result"]

    def initialize(self):
        self.call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                 "clientInfo": {"name": "functional-review-probe", "version": "1"}})
        self.process.stdin.write(b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
        self.process.stdin.flush()

    def tool(self, name, arguments):
        return self.call("tools/call", {"name": name, "arguments": arguments})


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("actors", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=False)
    summary = []
    for name, marker in (("state-a", "ambercapybara"), ("state-b", "violetheron")):
        workspace = workspace_at(args.actors.resolve() / name)
        db = subprocess.check_output(["capy", "--project-dir", str(workspace), "which"],
                                     env=run_environment(workspace), cwd=workspace, text=True).strip()
        expected = workspace / ".runner/knowledge.db"
        require(Path(db).resolve() == expected, "Unexpected Capy store: " + db)
        require(not expected.exists(), "Probe inherited a knowledge database")
        client = Capy(workspace, args.evidence)
        try:
            client.initialize()
            empty = client.tool("capy_search", {"queries": ["transport orchard"], "limit": 3})
            # Capy 0.16.7 reports an empty, newly created store as a tool error.
            require("The knowledge base is empty" in json.dumps(empty), "Initial knowledge not empty")
            indexed = client.tool("capy_index", {"source": "probe-isolation", "content":
                                  "# Transport orchard\n\nRetained marker " + marker + "."})
            require(not indexed.get("isError") and "Indexed 1 sections" in json.dumps(indexed),
                    "Indexing failed")
            found = client.tool("capy_search", {"queries": ["transport orchard"], "limit": 3})
            text = json.dumps(found)
            other = "violetheron" if marker == "ambercapybara" else "ambercapybara"
            require(marker in text and other not in text, "Knowledge isolation failed")
            doctor = client.tool("capy_doctor", {})
            require("Vault: disabled" in json.dumps(doctor), "Vault unexpectedly available")
            vault = client.tool("capy_vault_search", {"queries": ["transport orchard"]})
            require("CAPY_VAULT_KEY" in json.dumps(vault), "Unavailable vault not reported")
            summary.append({"workspace": str(workspace), "store": db, "initial_seed": "empty",
                            "fixture_sha256": hashlib.sha256((workspace / "README.md").read_bytes()).hexdigest(),
                            "index_search": "PASS", "foreign_marker_absent": True,
                            "vault": "unavailable; CAPY_VAULT_KEY unset", "status": "PASS"})
        finally:
            client.close()
            (args.evidence / (name + ".json")).write_text(json.dumps(client.events, indent=2) + "\n")
    (args.evidence / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
