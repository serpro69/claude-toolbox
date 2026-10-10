"""Gate 2B controller for the declared Codex 0.162.1 receipt/use batch.

Python 3.11+, standard library. Reuses the retained seed staging/sanitization
code without changing it. Actor instructions and ordinary prompts stay frozen.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import tomllib


HERE = Path(__file__).resolve().parent
VERIFICATION = HERE.parent
ROOT = VERIFICATION.parents[4]
sys.path.insert(0, str(VERIFICATION))
spec = importlib.util.spec_from_file_location("codex_capture_v1", VERIFICATION / "capture-codex.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
seed = legacy.seed
MARKETPLACE = "fr-c2d28c9e-2b-20261010"
PLUGIN_ID = "kk@" + MARKETPLACE
SNAPSHOT = Path("/tmp/functional-review-2b-baseline-20261010")
PYTHON = sys.executable


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def secrets():
    config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    return [value for key, value in config["mcp_servers"]["pal"].get("env", {}).items()
            if any(part in key for part in ("KEY", "TOKEN", "SECRET")) and value]


def sanitized(value, credentials):
    text = json.dumps(legacy.public(value))
    for secret in credentials:
        text = text.replace(secret, "[credential redacted]")
    return json.loads(text)


def snapshot_payloads(item, workspace, evidence, sequence):
    """Capture references, not inferred receipt; Linux and macOS temporary paths.

    Temporary payload ownership is audited from actual creation/read events.
    Merely retaining bytes here is never evidence that a reviewer received them.
    """
    captured = []
    for name in sorted(set(re.findall(r'/[^\s"<>`\\]+', json.dumps(item)))):
        path = Path(name.rstrip(".,:;)\\"))
        try:
            resolved = path.resolve(strict=True)
        except (OSError, ValueError):
            continue
        actor_input = resolved.is_relative_to(workspace) and not resolved.is_relative_to(workspace / ".runner")
        review_temp = resolved.parent in {Path("/tmp"), Path("/private/tmp")} and resolved.name.startswith("kk-review-")
        if not (actor_input or review_temp) or not resolved.is_file():
            continue
        try:
            content = resolved.read_bytes()
        except OSError as exc:
            captured.append({"path": str(path), "status": type(exc).__name__, "receipt": "unverified"})
            continue
        if len(content) > 2_000_000:
            captured.append({"path": str(path), "status": "too large; incomplete"})
            continue
        digest = seed.sha(content)
        target = evidence / "payloads" / digest
        target.parent.mkdir(exist_ok=True)
        if not target.exists():
            target.write_bytes(content)
        captured.append({"path": str(path), "sha256": digest, "artifact": str(target.relative_to(evidence)),
                         "temporary_ownership": "requires event audit" if review_temp else "actor workspace"})
    if captured:
        with (evidence / "payload-events.jsonl").open("a") as stream:
            stream.write(json.dumps({"event_sequence": sequence, "files": captured}) + "\n")


class Server(legacy.Server):
    def __init__(self, workspace, evidence):
        self.workspace, self.evidence = workspace.resolve(), evidence
        self.credentials = secrets()
        self.log = (evidence / "protocol.jsonl").open("x")
        self.errors = (evidence / "stderr.txt").open("x")
        # Public config/value/write creates a temporary project trust before
        # model execution. CLI-scoped trust did not enable project configuration
        # on this runtime; preserve that failed setup as evidence.
        self.argv = ["codex", "app-server", "--stdio"]
        try:
            self.process = subprocess.Popen(self.argv, cwd=workspace,
                env=seed.run_environment(workspace), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=self.errors)
        except BaseException:
            self.log.close()
            self.errors.close()
            raise
        self.buffer, self.sequence, self.request_id = b"", 0, 0
        self.received = []

    def retain(self, direction, message):
        self.sequence += 1
        method = message.get("method", "")
        item = message.get("params", {}).get("item", {})
        if ("reasoning" in method.lower() or method.startswith("codex/event/")
                or item.get("type") == "reasoning" or method.endswith(("/delta", "/outputDelta"))):
            return
        self.log.write(json.dumps({"sequence": self.sequence, "direction": direction,
                                  "message": sanitized(message, self.credentials)}) + "\n")
        self.log.flush()
        if method in ("item/started", "item/completed"):
            snapshot_payloads(item, self.workspace, self.evidence, self.sequence)

    def initialize(self):
        self.call("initialize", {"clientInfo": {"name": "functional-review-gate-2b",
                  "title": "Receipt/use capture", "version": "2"},
                  "capabilities": {"experimentalApi": True}})
        self.send({"jsonrpc": "2.0", "method": "initialized", "params": {}})


def configure_workspace(workspace):
    path = workspace / ".codex/config.toml"
    config = path.read_text().replace("fr-c2d28c9e-seeds", MARKETPLACE)
    if "[mcp_servers.openaiDeveloperDocs]" not in config:
        config += '\n[mcp_servers.openaiDeveloperDocs]\nenabled = false\n'
    for name in ("context7", "linear"):
        if "[mcp_servers." + name + "]" not in config:
            config += '\n[mcp_servers.' + name + ']\nenabled = false\n'
    # PAL is a fresh stdio process per app-server run. Its conversation store is
    # process-local in the inspected c20d384 source, so no prior review persists.
    path.write_text(config)
    catalog = workspace / ".agents/plugins/marketplace.json"
    data = json.loads(catalog.read_text())
    data["name"] = MARKETPLACE
    catalog.write_text(json.dumps(data, indent=2) + "\n")


def verify_catalog(server, workspace, evidence):
    catalog = server.call("skills/list", {"cwds": [str(workspace)], "forceReload": True})
    selected = [s for row in catalog["data"] for s in row["skills"]
                if s["name"].startswith("kk:") and s.get("enabled")]
    if not selected or any(s.get("pluginId") != PLUGIN_ID for s in selected):
        raise ValueError("Missing selected or mixed enabled kk catalog")
    if any("/evals/" in s.get("path", "") for s in selected):
        raise ValueError("Evaluator fixture present in enabled catalog")
    roots = {Path(s["path"]).parents[2] for s in selected if Path(s["path"]).name == "SKILL.md"}
    if not roots:
        raise ValueError("No verifiable skill installation root")
    for root in roots:
        subprocess.run([PYTHON, "-B", str(VERIFICATION / "prepare-bundles.py"), "verify", str(root),
                        str(SNAPSHOT / "retained-manifest.json"), "kodex-plugin"], check=True,
                       stdout=subprocess.PIPE, text=True)
    for path in (SNAPSHOT / "retained/.codex/agents").glob("*.toml"):
        if path.read_bytes() != (workspace / ".codex/agents" / path.name).read_bytes():
            raise ValueError("Generated role bytes differ from baseline")
    write_json(evidence / "catalog.json", sanitized(catalog, server.credentials))
    write_json(evidence / "binding.json", {"plugin_id": PLUGIN_ID, "roots": sorted(map(str, roots)),
               "selected_skills": len(selected), "operative_manifest_verified": True,
               "generated_role_bytes_verified": True, "actor": seed.BASELINE})


def admin(operation, workspace, evidence, trust_record=None):
    evidence.mkdir(parents=True, exist_ok=False)
    server = Server(workspace, evidence)
    try:
        server.initialize()
        if operation == "trust":
            config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
            previous = config.get("projects", {}).get(str(workspace))
            if previous is not None:
                raise ValueError("Refuse to replace an existing project trust entry")
            write_json(evidence / "previous-project-entry.json", {"path": str(workspace), "previous": previous})
            result = server.call("config/value/write", {"keyPath": "projects." + json.dumps(str(workspace)) + ".trust_level",
                    "value": "trusted", "mergeStrategy": "replace"})
            write_json(evidence / "trust.json", sanitized(result, server.credentials))
        elif operation == "untrust":
            if trust_record is None:
                raise ValueError("Project trust removal requires its sealed prior-state record")
            prior = json.loads(trust_record.read_bytes())
            manifest = json.loads((trust_record.parent / "manifest.json").read_bytes())
            if (prior != {"path": str(workspace), "previous": None}
                    or seed.sha(trust_record.read_bytes()) != manifest.get(trust_record.name)):
                raise ValueError("Unverified prior project state")
            config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
            if config.get("projects", {}).get(str(workspace)) != {"trust_level": "trusted"}:
                raise ValueError("Temporary project entry changed; do not remove unrelated settings")
            result = server.call("config/value/write", {"keyPath": "projects." + json.dumps(str(workspace)),
                    "value": None, "mergeStrategy": "replace"})
            after = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
            if str(workspace) in after.get("projects", {}):
                raise ValueError("Temporary trust removal did not restore absence")
            write_json(evidence / "untrust.json", {"result": sanitized(result, server.credentials),
                       "workspace": str(workspace), "prior_absence_restored": True})
        elif operation == "verify":
            verify_catalog(server, workspace, evidence)
        elif operation == "install":
            result = server.call("plugin/install", {"marketplacePath": str(workspace / ".agents/plugins/marketplace.json"),
                                                       "pluginName": "kk"})
            write_json(evidence / "installation.json", sanitized(result, server.credentials))
            verify_catalog(server, workspace, evidence)
        else:
            result = server.call("plugin/uninstall", {"pluginId": PLUGIN_ID})
            write_json(evidence / "uninstall.json", sanitized(result, server.credentials))
    finally:
        server.close()
        seed.seal(evidence, server.credentials)


def verify_v2(path):
    frozen = json.loads(path.read_bytes())
    if frozen.get("revision") != 2 or frozen["rubric_sha256"] != seed.sha((VERIFICATION / "task2-rubric-v2.md").read_bytes()):
        raise ValueError("Revision-2 rubric mismatch")
    if frozen["controller_sha256"] != seed.sha(Path(__file__).read_bytes()):
        raise ValueError("Controller changed after freeze")
    for case in seed.SEEDS:
        if seed.files(seed.fixture(case)) != frozen["fixtures"][case]:
            raise ValueError("Fixture changed after revision-2 freeze: " + case)
    return frozen


def prepare(case, workspace, evidence):
    mode = "isolated" if case == "R3" else "standalone"
    args = argparse.Namespace(provider="codex", case=case, mode=mode, snapshot=SNAPSHOT,
                             workspace=workspace, evidence=evidence,
                             frozen=VERIFICATION / "task2-frozen-v2.json")
    # The retained staging helper hardcodes the revision-1 rubric path. Adapt
    # only that validation boundary in this single-operation process; never
    # change its on-disk bytes or bypass the successor fixture/rubric checks.
    original_validator = seed.verify_frozen
    seed.verify_frozen = verify_v2
    try:
        seed.prepare(args)
    finally:
        seed.verify_frozen = original_validator
    configure_workspace(workspace)


def child_ids(item):
    result = set(item.get("receiverThreadIds", [])) if item.get("type") == "collabAgentToolCall" else set()
    if item.get("type") == "subAgentActivity":
        result.add(item["agentThreadId"])
    return result


def collect_history(server, root_thread, evidence):
    pending, collected = [root_thread], set()
    for message in server.received:
        pending.extend(child_ids(message.get("params", {}).get("item", {})))
    while pending:
        thread = pending.pop(0)
        if thread in collected:
            continue
        collected.add(thread)
        items, cursor = [], None
        while True:
            params = {"threadId": thread, "limit": 100}
            if cursor:
                params["cursor"] = cursor
            page = server.call("thread/items/list", params)
            items.extend(page["data"])
            cursor = page.get("nextCursor")
            if not cursor:
                break
        write_json(evidence / ("items-" + thread + ".json"), sanitized(items, server.credentials))
        for row in items:
            pending.extend(child_ids(row["item"]))
        # Metadata links supplement activity events; no full raw/private history.
        metadata = server.call("thread/read", {"threadId": thread, "includeTurns": False})
        write_json(evidence / ("thread-" + thread + ".json"), sanitized(metadata, server.credentials))
    return sorted(collected)


def run(workspace, evidence, binding=False):
    if any((evidence / name).exists() for name in ("command.json", "protocol.jsonl", "manifest.json")):
        raise FileExistsError("Refuse to overwrite a captured attempt")
    meta = json.loads((evidence / "launch.json").read_text())
    if not binding:
        freeze = VERIFICATION / "task2-frozen-v2.json"
        verify_v2(freeze)
        if meta["fixture_manifest_sha256"] != seed.sha(freeze.read_bytes()):
            raise ValueError("Launch metadata belongs to a different freeze")
    write_json(evidence / "command.json", {"runtime": "codex-cli 0.162.1", "model": "gpt-6-astra",
        "effort": "xhigh", "history_mode": "paginated", "approval_policy": "never", "sandbox": "workspace-write",
        "controller_sha256": seed.sha(Path(__file__).read_bytes()), "rubric_version": 2,
        "mode": "binding/receipt probe" if binding else "measured baseline",
        "exact_prompt_content": "unverified; receipt/use contract selected"})
    server = None
    credentials = secrets()
    try:
        server = Server(workspace, evidence)
        server.initialize()
        verify_catalog(server, workspace, evidence)
        started = server.call("thread/start", {"cwd": str(workspace), "model": "gpt-6-astra",
            "approvalPolicy": "never", "sandbox": "workspace-write", "ephemeral": False,
            "historyMode": "paginated", "allowProviderModelFallback": False,
            "config": {"model_reasoning_effort": "xhigh"}})
        thread = started["thread"]["id"]
        write_json(evidence / "thread.json", sanitized(started, credentials))
        server.call("turn/start", {"threadId": thread, "input": [{"type": "text", "text": meta["prompt"]}],
                                   "model": "gpt-6-astra", "effort": "xhigh"})
        deadline = time.monotonic() + 2700
        while True:
            if time.monotonic() > deadline:
                raise TimeoutError("45-minute capture deadline reached")
            message = server.receive(timeout=120)
            if message.get("method") == "turn/completed" and message["params"]["threadId"] == thread:
                write_json(evidence / "turn-completion.json", sanitized(message["params"], credentials))
                break
        threads = collect_history(server, thread, evidence)
        reports = [m["params"]["item"].get("text", "") for m in server.received
                   if m.get("method") == "item/completed" and m.get("params", {}).get("threadId") == thread
                   and m["params"]["item"].get("type") == "agentMessage"]
        (evidence / "report.md").write_text("\n\n".join(reports) + "\n")
        write_json(evidence / "capture-status.json", {"status": "captured; audit pending", "threads": threads,
                   "exact_prompt_content": "unverified", "behavioral_grade": "not inferred from runtime completion"})
    except BaseException as exc:
        write_json(evidence / "capture-error.json", {"error": type(exc).__name__, "message": str(exc),
                                                    "coverage": "incomplete; retain attempt"})
        raise
    finally:
        try:
            if server:
                server.close()
            final = seed.subject_snapshot(workspace, evidence / "final")
            (evidence / "final.patch").write_bytes(seed.git(workspace, "diff", "HEAD", "--binary"))
            write_json(evidence / "completion.json", {"final_files": final, "grading": "pending evidence audit"})
        finally:
            seed.seal(evidence, credentials)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "trust", "untrust", "verify", "install", "uninstall", "run", "binding"))
    parser.add_argument("workspace", type=Path)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--case", choices=("R3", "I2"))
    parser.add_argument("--trust-record", type=Path)
    args = parser.parse_args()
    if args.operation == "prepare":
        if not args.case:
            parser.error("prepare requires --case")
        prepare(args.case, args.workspace.resolve(), args.evidence.resolve())
    elif args.operation in ("trust", "untrust", "verify", "install", "uninstall"):
        admin(args.operation, args.workspace.resolve(), args.evidence.resolve(), args.trust_record)
    else:
        run(args.workspace.resolve(), args.evidence.resolve(), binding=args.operation == "binding")
