"""Original Claude receipt audit plus validated instruction filename discovery."""
import hashlib
import json
from pathlib import Path
import re

import successor

original = successor.host.preflight_audit
inputs = successor.inputs
PATTERNS = {
    "agents/*.md": {"agents"},
    "skills/{_shared,review-code}/*.md": {"skills/_shared", "skills/review-code"},
}


def instruction_listing(call, result, workspace, bundle, snapshot):
    args = call["args"]
    if (set(args) != {"path", "pattern"} or args["path"] != str(bundle)
            or args["pattern"] not in PATTERNS):
        raise ValueError("Unexpected instruction listing base/pattern")
    meta = result.get("meta") if result else None
    if (not result or result["error"] or not isinstance(meta, dict)
            or meta.get("truncated") is not False or meta.get("countIsComplete") is not True):
        raise ValueError("Incomplete or failed instruction listing")
    names = meta.get("filenames")
    if (not isinstance(names, list) or not names or not all(isinstance(n, str) for n in names)
            or len(names) != len(set(names)) or meta.get("numFiles") != len(names)
            or meta.get("totalMatches") != len(names) or result["text"].splitlines() != names):
        raise ValueError("Instruction listing count/text mismatch")
    paths = []
    for name in names:
        path = Path(name)
        if ".." in path.parts or path.as_posix() != name:
            raise ValueError("Unnormalized instruction listing path")
        path = path if path.is_absolute() else workspace / path
        if not path.is_relative_to(bundle):
            raise ValueError("Instruction listing outside selected bundle")
        relative = path.relative_to(bundle)
        source = snapshot / relative
        if (relative.parent.as_posix() not in PATTERNS[args["pattern"]]
                or relative.suffix != ".md" or not source.is_file()
                or not source.resolve().is_relative_to(snapshot.resolve())):
            raise ValueError("Instruction listing outside frozen instruction paths")
        paths.append(relative.as_posix())
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate normalized instruction listing paths")
    return {"call": call["event"], "result": result["event"], "actor": call["actor"],
            "pattern": args["pattern"], "paths": paths, "receipt": "filenames only; not instruction Reads"}


def claude(source, snapshot, side):
    # Preserve the pinned original algorithm; only the Glob branch and its
    # separate returned provenance are additions. Never rewrite captured events.
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
                    "text": original.content_text(block.get("content")), "meta": event.get("tool_use_result")}
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
    reads, shell, other, listings = [], [], [], []
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
            complete = bool(result and not result["error"] and original.source_returned(expected.read_text(), result["text"]))
            reads.append({"call": call["event"], "result": result["event"] if result else None,
                "actor": "child" if call["actor"] == child else "main", "path": relative,
                "complete": complete, "source_sha256": inputs.sha(expected)})
        elif call["tool"] == "Glob":
            listings.append(instruction_listing(call, result, Path(launch["workspace"]), bundle, snapshot))
        elif call["tool"] not in ("Skill", "Agent"):
            other.append({"event": call["event"], "kind": call["tool"]})
    if not root_receipts or other:
        raise ValueError("Missing root receipt or unexpected binding tool/path")
    for actor in ("main", "child"):
        seen = {r["path"] for r in reads if r["actor"] == actor and r["complete"]}
        if actor == "main":
            seen.add("skills/review-code/SKILL.md")
        missing = set(original.required(side, "claude", actor)) - seen
        if missing:
            raise ValueError("Incomplete Claude instructions: " + str(missing))
    audit = {"models": sorted(models), "services": sorted(services), "child": children[0],
             "registered_skill_receipts": skill_receipts, "root_receipts": root_receipts,
             "reads": reads, "shell_requests_requiring_manual_access_review": shell}
    if listings:
        audit["instruction_listings"] = listings
    return audit
