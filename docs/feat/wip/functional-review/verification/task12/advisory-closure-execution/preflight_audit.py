"""Local post-capture binding audit. No network or model calls; no capture edits."""
import hashlib
import json
from pathlib import Path
import re

import inputs
import runner

HERE = Path(__file__).resolve().parent
PROFILES = ("go", "python", "java", "js_ts", "kotlin", "k8s", "k8s-operator", "skill-md")


def content_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(x.get("text", "") for x in value if isinstance(x, dict) and x.get("type") == "text")
    return ""


def source_returned(source, returned):
    """Accept complete plain bytes or contiguous numbered Read output only."""
    if source.strip() in returned:
        return True
    numbered = [re.match(r"^\s*(\d+)\t(.*)$", line) for line in returned.splitlines()]
    rows = [(int(m[1]), m[2]) for m in numbered if m]
    if rows and [n for n, _ in rows] == list(range(1, len(rows) + 1)):
        return "\n".join(text for _, text in rows).rstrip("\n") == source.rstrip("\n")
    return False


def required(side, provider, actor):
    if side == "baseline":
        if provider == "claude" and actor == "child":
            return ["skills/review-code/SKILL.md"]
        return ["skills/review-code/" + n for n in (
            "SKILL.md", "shared-capy-knowledge-protocol.md", "shared-profile-detection.md", "review-process.md")]
    if actor == "child":
        return ["skills/_shared/" + n + ".md" for n in (
            "change-context", "review-scope-protocol", "capy-knowledge-protocol")] + [
            "skills/review-code/functional-review.md", "skills/review-code/SKILL.md"]
    return ["skills/review-code/" + n for n in (
        "SKILL.md", "packet-preparation.md", "review-process.md", "shared-capy-knowledge-protocol.md",
        "shared-profile-detection.md", "shared-review-scope-protocol.md", "shared-change-context.md",
        "functional-review.md")] + [f"profiles/{p}/DETECTION.md" for p in PROFILES]


def claude(source, snapshot, side):
    launch = inputs.read(source / "launch.json")
    bundle = Path(launch["workspace"]) / "plugins/kk"
    calls, results, skill_receipts, models, services, children = {}, {}, [], set(), set(), []
    rows = [json.loads(line) for line in (source / "events.jsonl").read_text().splitlines()]
    entry = (snapshot / "skills/review-code/SKILL.md").read_text()
    body = re.sub(r"^---\n.*?\n---\n", "", entry, count=1, flags=re.S).strip()
    body = body.replace("${CLAUDE_PLUGIN_ROOT}", str(bundle))
    for row in rows:
        sequence, event = row["sequence"], row["event"]
        if event.get("subtype") == "init":
            models.add(event.get("model"))
            for server in event.get("mcp_servers", []):
                services.add((server["name"], server["status"]))
            if not any(p.get("name") == "kk" and p.get("path") == str(bundle) for p in event.get("plugins", [])):
                raise ValueError("Selected Claude plugin root missing")
        message = event.get("message", {})
        blocks = message.get("content", []) if isinstance(message, dict) else []
        for block in blocks if isinstance(blocks, list) else []:
            kind = block.get("type")
            if kind == "tool_use":
                calls[block["id"]] = {"event": sequence, "actor": event.get("agent_id", "main"),
                    "parent_tool_use_id": event.get("parent_tool_use_id"), "tool": block["name"], "args": block.get("input", {})}
            elif kind == "tool_result":
                results[block["tool_use_id"]] = {"event": sequence, "error": bool(block.get("is_error")),
                    "text": content_text(block.get("content")), "meta": event.get("tool_use_result")}
            elif (kind == "text" and event.get("isSynthetic") and event.get("type") == "user"
                    and body in block.get("text", "")):
                skill_receipts.append(sequence)
        meta = event.get("tool_use_result")
        if isinstance(meta, dict) and meta.get("agentType") == "kk:code-reviewer":
            children.append({"event": sequence, "agent_id": meta["agentId"], "model": meta["resolvedModel"]})
    if models != {"claude-opus-5-5"} or ("capy", "connected") not in services or any(n == "pal" for n, _ in services):
        raise ValueError("Claude model/service mismatch")
    if len(children) != 1 or children[0]["model"] != "claude-opus-5-5" or not skill_receipts:
        raise ValueError("Missing named child/model or registered skill receipt")
    child = children[0]["agent_id"]
    reads, shell, other = [], [], []
    root_receipts = []
    for identity, call in calls.items():
        result = results.get(identity)
        if call["tool"] == "Bash":
            command = call["args"].get("command", "")
            shell.append({"call": call["event"], "result": result["event"] if result else None,
                "command_sha256": hashlib.sha256(command.encode()).hexdigest(),
                "error": result["error"] if result else None})
            if command == "printenv TOOLBOX_PLUGIN_ROOT" and result and not result["error"] and result["text"].strip() == str(bundle):
                root_receipts.append(result["event"])
        elif call["tool"] == "Read":
            path = Path(call["args"]["file_path"])
            if not path.is_absolute():
                path = Path(launch["workspace"]) / path
            if not path.is_relative_to(bundle):
                other.append({"event": call["event"], "kind": "Read outside selected bundle"})
                continue
            relative = path.relative_to(bundle).as_posix()
            expected = snapshot / relative
            if not expected.is_file():
                raise ValueError("Read path absent from selected source")
            complete = bool(result and not result["error"] and source_returned(expected.read_text(), result["text"]))
            reads.append({"call": call["event"], "result": result["event"] if result else None,
                "actor": "child" if call["actor"] == child else "main", "path": relative,
                "complete": complete, "source_sha256": inputs.sha(expected)})
        elif call["tool"] not in ("Skill", "Agent"):
            other.append({"event": call["event"], "kind": call["tool"]})
    if not root_receipts or other:
        raise ValueError("Missing root receipt or unexpected binding tool/path")
    for actor in ("main", "child"):
        seen = {r["path"] for r in reads if r["actor"] == actor and r["complete"]}
        if actor == "main":
            seen.add("skills/review-code/SKILL.md")
        missing = set(required(side, "claude", actor)) - seen
        if missing:
            raise ValueError("Incomplete Claude instructions: " + str(missing))
    return {"models": sorted(models), "services": sorted(services), "child": children[0],
            "registered_skill_receipts": skill_receipts, "root_receipts": root_receipts,
            "reads": reads, "shell_requests_requiring_manual_access_review": shell}


def codex(source, snapshot, side):
    binding = inputs.read(source / "binding.json")
    expected_revision = inputs.read(snapshot.parent.parent / "identity.json")["revision"]
    if (binding["actor"] != expected_revision or not binding["operative_manifest_verified"]
            or not binding["generated_role_bytes_verified"]):
        raise ValueError("Codex installation/role identity mismatch")
    parent = inputs.read(source / "thread.json")["thread"]["id"]
    reads, threads, commands, services = [], [], [], []
    for path in sorted(source.glob("thread-*.json")):
        thread = inputs.read(path)["thread"]
        actor = "main" if thread["id"] == parent else "child"
        expected_model = "gpt-6-astra" if actor == "main" else "gpt-6.1-sol"
        if thread["model"] != expected_model:
            raise ValueError("Codex model mismatch")
        if actor == "child":
            origin = thread["source"]["subAgent"]["thread_spawn"]
            if thread["agentRole"] != "code-reviewer" or origin["parent_thread_id"] != parent:
                raise ValueError("Named child linkage mismatch")
        threads.append({"id": thread["id"], "actor": actor, "model": thread["model"], "role": thread.get("agentRole")})
        items_path = path.with_name(path.name.replace("thread-", "items-"))
        items = [r["item"] for r in inputs.read(items_path)]
        executions = [r for r in items if r.get("type") == "commandExecution"]
        for item in executions:
            commands.append({"actor": actor, "item": item["id"], "exit_code": item["exitCode"],
                             "status": item["status"], "command_sha256": hashlib.sha256(item["command"].encode()).hexdigest()})
        for relative in required(side, "codex", actor):
            expected = snapshot / relative
            matched = [r["id"] for r in executions if r["exitCode"] == 0 and r["status"] == "completed"
                       and source_returned(expected.read_text(), r.get("aggregatedOutput") or "")]
            if not matched:
                raise ValueError("Incomplete Codex instruction receipt: " + actor + "/" + relative)
            reads.append({"actor": actor, "path": relative, "items": matched, "source_sha256": inputs.sha(expected)})
    if len(threads) != 2 or sum(t["actor"] == "child" for t in threads) != 1:
        raise ValueError("Expected one main and one named child")
    for line in (source / "protocol.jsonl").read_text().splitlines():
        msg = json.loads(line).get("message", {})
        if msg.get("method") == "mcpServer/startupStatus/updated":
            p = msg["params"]
            services.append({"thread": p["threadId"], "name": p["name"], "status": p["status"]})
    if any(s["name"] == "pal" for s in services) or not any(s["thread"] == parent and s["name"] == "capy" and s["status"] == "ready" for s in services):
        raise ValueError("Codex Capy/PAL startup mismatch")
    return {"plugin_id": binding["plugin_id"], "threads": threads, "services": services,
            "reads": reads, "commands_requiring_manual_access_review": commands,
            "exact_submitted_child_prompt": "unverified; no fallback extended"}


def main():
    adapter = runner.Adapter()
    adapter.verify()
    adapter.calibration_ready()
    destination = HERE / "preflight-audits"
    destination.mkdir(exist_ok=False)
    for provider in ("claude", "codex"):
        for side in ("baseline", "candidate"):
            name = f"binding-{provider}-{side}"
            source = HERE / name
            seal = inputs.read(source / "manifest.json")
            runner.checked_files(source, seal)
            if adapter.prior.matrix.runtime.completion_status(source):
                raise ValueError("Binding runtime failed")
            launch, completion = inputs.read(source / "launch.json"), inputs.read(source / "completion.json")
            if (launch["fixture_manifest_sha256"] != inputs.sha(runner.FROZEN)
                    or launch["purpose"] != "binding probe" or launch["provider"] != provider
                    or launch["side"] != side or completion["final_files"] != launch["initial_files"]):
                raise ValueError("Binding identity or subject changed")
            tree = "klaude-plugin" if provider == "claude" else "kodex-plugin"
            snapshot = adapter.root / side / "retained" / tree
            detail = claude(source, snapshot, side) if provider == "claude" else codex(source, snapshot, side)
            inputs.write_new(destination / (name + ".json"), {
                "run": name, "status": "PASS for checked identity/receipt obligations; manual access review pending",
                "manifest_sha256": inputs.sha(source / "manifest.json"), "sealed_files": len(seal),
                "subject_unchanged": True, "audit_tool_sha256": inputs.sha(Path(__file__)), **detail})
    print("Four sealed bindings match source/model/role and full instruction receipts; manual access review remains.")


if __name__ == "__main__":
    main()
