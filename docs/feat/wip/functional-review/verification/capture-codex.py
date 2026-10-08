#!/usr/bin/env python3
"""Task 2 Codex capture through the installed client's public app-server protocol.

Schema source: codex 0.161.0 app-server generate-json-schema. In particular,
collabAgentToolCall.prompt exposes submitted handoffs without private reasoning.
"""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import time

SPEC = importlib.util.spec_from_file_location("seed_capture", Path(__file__).with_name("capture-seeds.py"))
seed = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(seed)


def public(value):
    if isinstance(value, dict):
        if value.get("type") in ("reasoning", "thinking", "redacted_thinking"):
            return {"type": "omitted_private_reasoning"}
        return {k: public(v) for k, v in value.items() if k not in ("encrypted_content",)}
    if isinstance(value, list):
        return [public(v) for v in value]
    return value


class Server:
    def __init__(self, workspace, evidence):
        self.workspace, self.evidence = workspace, evidence
        self.log = (evidence / "protocol.jsonl").open("x")
        self.errors = (evidence / "stderr.txt").open("w")
        self.process = subprocess.Popen(["codex", "app-server", "--stdio"], cwd=workspace,
            env=seed.run_environment(workspace), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.errors)
        self.buffer, self.sequence, self.request_id = b"", 0, 0
        self.received = []

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
        self.process.stdout.close()
        self.log.close()
        self.errors.close()

    def retain(self, direction, message):
        self.sequence += 1
        method = message.get("method", "")
        item = message.get("params", {}).get("item", {})
        if "reasoning" in method.lower() or method.startswith("codex/event/") or item.get("type") == "reasoning":
            return
        # Completed items contain full public text; do not duplicate token deltas.
        if method.endswith("/delta") or method.endswith("/outputDelta"):
            return
        record = {"sequence": self.sequence, "direction": direction, "message": public(message)}
        self.log.write(json.dumps(record) + "\n")
        self.log.flush()
        if method in ("item/started", "item/completed"):
            seed.capture_payloads(item, self.workspace, self.evidence, self.sequence)

    def send(self, message):
        self.retain("sent", message)
        self.process.stdin.write((json.dumps(message) + "\n").encode())
        self.process.stdin.flush()

    def receive(self, timeout=60):
        deadline = time.monotonic() + timeout
        while b"\n" not in self.buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([self.process.stdout], [], [], remaining)[0]:
                raise TimeoutError("No app-server event within timeout")
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError("App-server closed stdout")
            self.buffer += chunk
        line, self.buffer = self.buffer.split(b"\n", 1)
        message = json.loads(line)
        self.retain("received", message)
        self.received.append(message)
        # No controller-supplied requirement decisions. Approval mode is never.
        if "id" in message and "method" in message:
            method = message["method"]
            if method == "item/tool/requestUserInput":
                self.send({"id": message["id"], "result": {"answers": {}}})
            else:
                self.send({"id": message["id"], "error": {"code": -32601,
                    "message": "Controller provides no approval or supplemental decision"}})
        return message

    def call(self, method, params):
        self.request_id += 1
        current = self.request_id
        self.send({"jsonrpc": "2.0", "id": current, "method": method, "params": params})
        while True:
            message = self.receive()
            if message.get("id") == current and "method" not in message:
                if "error" in message:
                    raise RuntimeError(str(message["error"]))
                return message["result"]

    def initialize(self):
        self.call("initialize", {"clientInfo": {"name": "functional-review-seeds", "title": "Workflow capture", "version": "1"},
                                 "capabilities": {"experimentalApi": True}})
        self.send({"jsonrpc": "2.0", "method": "initialized", "params": {}})


def admin(workspaces, evidence):
    evidence.mkdir(parents=True, exist_ok=False)
    server = Server(workspaces[0], evidence)
    try:
        server.initialize()
        for workspace in workspaces:
            server.call("config/value/write", {"keyPath": 'projects.' + json.dumps(str(workspace)) + '.trust_level',
                        "value": "trusted", "mergeStrategy": "replace"})
        result = server.call("skills/list", {"cwds": [str(w) for w in workspaces], "forceReload": True})
        seed.write_json(evidence / "catalogs.json", result)
    finally:
        server.close()


def run(evidence, probe=False):
    if any((evidence / name).exists() for name in ("command.json", "protocol.jsonl", "manifest.json")):
        raise FileExistsError("Refuse to overwrite a run")
    meta = json.loads((evidence / "launch.json").read_text())
    workspace = Path(meta["workspace"])
    seed.write_new_json(evidence / "command.json", {"argv": ["codex", "app-server", "--stdio"],
        "model": "gpt-6-astra", "effort": "xhigh", "approval_policy": "never",
        "sandbox": "workspace-write", "controller_sha256": seed.sha(Path(__file__).read_bytes()),
        "mode": "loading probe" if probe else "measured baseline", "plaintext_surface": "collabAgentToolCall.prompt"})
    server = Server(workspace, evidence)
    try:
        server.initialize()
        catalog = server.call("skills/list", {"cwds": [str(workspace)], "forceReload": True})
        selected = [s for row in catalog["data"] for s in row["skills"] if s["name"].startswith("kk:") and s.get("enabled")]
        if not selected or any(s.get("pluginId") != "kk@fr-c2d28c9e-seeds" for s in selected):
            raise ValueError("Mixed or missing kk catalog")
        seed.write_json(evidence / "catalog.json", catalog)
        started = server.call("thread/start", {"cwd": str(workspace), "model": "gpt-6-astra",
            "approvalPolicy": "never", "sandbox": "workspace-write", "ephemeral": False,
            "config": {"model_reasoning_effort": "xhigh"}})
        thread = started["thread"]["id"]
        seed.write_json(evidence / "thread.json", started)
        server.call("turn/start", {"threadId": thread, "input": [{"type": "text", "text": meta["prompt"]}],
                                   "model": "gpt-6-astra", "effort": "xhigh"})
        while True:
            message = server.receive()
            if message.get("method") == "turn/completed" and message["params"]["threadId"] == thread:
                seed.write_json(evidence / "turn-completion.json", message["params"])
                break
        # Preserve full public item records from every actual child discovered.
        children = set()
        for message in server.received:
            item = message.get("params", {}).get("item", {})
            if item.get("type") == "collabAgentToolCall":
                children.update(item.get("receiverThreadIds", []))
            if item.get("type") == "subAgentActivity":
                children.add(item["agentThreadId"])
        pending, collected = [thread, *sorted(children - {thread})], set()
        while pending:
            tid = pending.pop(0)
            if tid in collected:
                continue
            collected.add(tid)
            items, cursor = [], None
            while True:
                params = {"threadId": tid, "limit": 100}
                if cursor:
                    params["cursor"] = cursor
                page = server.call("thread/items/list", params)
                items.extend(page["data"])
                cursor = page.get("nextCursor")
                if not cursor:
                    break
            seed.write_json(evidence / ("items-" + tid + ".json"), public(items))
            for entry in items:
                item = entry["item"]
                if item.get("type") == "subAgentActivity":
                    pending.append(item["agentThreadId"])
                if item.get("type") == "collabAgentToolCall":
                    pending.extend(item.get("receiverThreadIds", []))
        reports = [m["params"]["item"].get("text", "") for m in server.received
                   if m.get("method") == "item/completed" and m.get("params", {}).get("threadId") == thread
                   and m["params"]["item"].get("type") == "agentMessage"]
        (evidence / "report.md").write_text("\n\n".join(reports) + "\n")
    except BaseException as exc:
        seed.write_json(evidence / "capture-error.json", {"error": type(exc).__name__, "message": str(exc),
                                                        "coverage": "incomplete; retain attempt"})
        raise
    finally:
        try:
            server.close()
            for name in ("tool-events", "payloads"):
                source = workspace / ".runner" / name
                if source.exists():
                    shutil.copytree(source, evidence / ("hook-" + name))
            final = seed.subject_snapshot(workspace, evidence / "final")
            (evidence / "final.patch").write_bytes(seed.git(workspace, "diff", "HEAD", "--binary"))
            seed.write_json(evidence / "completion.json", {"final_files": final, "grading": "pending Task 8"})
        finally:
            seed.seal(evidence)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("admin", "run", "probe"))
    parser.add_argument("evidence", type=Path)
    parser.add_argument("workspaces", nargs="*", type=Path)
    args = parser.parse_args()
    if args.mode == "admin":
        admin(args.workspaces, args.evidence)
    else:
        run(args.evidence, probe=args.mode == "probe")
