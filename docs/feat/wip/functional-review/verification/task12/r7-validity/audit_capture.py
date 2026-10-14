"""Verify retained capture hashes and record bounded instruction/access evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import runner

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(item.get("text", "") for item in content if item.get("type") == "text")
    return ""


def audit(source, binding=False):
    frozen = runner.configure()
    runner.controller.verify_frozen(frozen)
    seal = json.loads((source / "manifest.json").read_text())
    for relative, expected in seal.items():
        path = source / relative
        if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()) or sha(path) != expected:
            raise ValueError("Capture seal mismatch: " + relative)
    launch = json.loads((source / "launch.json").read_text())
    completion = json.loads((source / "completion.json").read_text())
    if completion["exit_code"] != 0 or completion.get("timed_out") or completion.get("interrupted_by"):
        raise ValueError("Capture did not complete normally")
    for relative, expected in launch["initial_files"].items():
        if completion["final_files"].get(relative) != expected:
            raise ValueError("Subject code/contract mutated: " + relative)
    bundle = Path(launch["workspace"]) / "plugins/kk"
    calls, results, initializations, messages, notices = {}, {}, [], [], []
    for line in (source / "events.jsonl").read_text().splitlines():
        item = json.loads(line)
        sequence, event = item["sequence"], item["event"]
        if event.get("subtype") == "init":
            initializations.append(event)
        message = event.get("message", {})
        if isinstance(message, str):
            notices.append({"event": sequence, "type": event.get("type"), "message": message})
        for block in message.get("content", []) if isinstance(message, dict) else []:
            if block.get("type") == "tool_use":
                calls[block["id"]] = (sequence, event.get("parent_tool_use_id"),
                                      block["name"], block.get("input", {}))
            elif block.get("type") == "tool_result":
                results[block["tool_use_id"]] = (sequence, block.get("is_error", False),
                                                text_content(block.get("content")))
            elif block.get("type") == "text":
                messages.append((sequence, block["text"]))
    if not initializations:
        raise ValueError("No runtime initialization evidence")
    for event in initializations:
        if event.get("model") != "claude-opus-5-5":
            raise ValueError("Unexpected actor model")
        mcp = event.get("mcp_servers", [])
        if not any(s.get("name") == "capy" and s.get("status") == "connected" for s in mcp):
            raise ValueError("Capy not connected")
        if any(s.get("name") == "pal" for s in mcp):
            raise ValueError("PAL unexpectedly present")
        if not any(p.get("name") == "kk" and p.get("path") == str(bundle)
                   for p in event.get("plugins", [])):
            raise ValueError("Selected plugin binding missing")
    retained = HERE / "source-inputs/retained/klaude-plugin"
    reads, shell, paths = [], [], []
    for ident, (sequence, parent, name, arguments) in calls.items():
        result = results.get(ident)
        if name == "Bash":
            shell.append({"event": sequence, "command": arguments.get("command"),
                          "result_event": result[0] if result else None,
                          "error": result[1] if result else None})
        if name in ("Read", "Glob", "Grep", "Write", "Edit"):
            paths.append({"event": sequence, "tool": name, "arguments": arguments})
        if name != "Read":
            continue
        path = Path(arguments.get("file_path", ""))
        if not path.is_relative_to(bundle) or not result or result[1]:
            continue
        relative = path.relative_to(bundle)
        original = retained / relative
        if not original.is_file():
            raise ValueError("Read claims unexpected instruction source")
        numbered = result[2].splitlines()
        decoded = [re.sub(r"^\s*\d+\t", "", line) for line in numbered]
        complete = "\n".join(decoded).rstrip("\n") == original.read_text().rstrip("\n")
        reads.append({"call": sequence, "result": result[0], "actor": "child" if parent else "main",
                      "path": str(relative), "complete_numbered_text": complete,
                      "source_sha256": sha(original)})
    root_receipts = [result[0] for ident, (_, _, name, args) in calls.items()
                     if name == "Bash" and args.get("command") == "printenv TOOLBOX_PLUGIN_ROOT"
                     and (result := results.get(ident)) and not result[1]
                     and result[2].strip() == str(bundle)]
    skill = (retained / "skills/review-code/SKILL.md").read_text()
    body = skill.split("---", 2)[2].strip().replace("${CLAUDE_PLUGIN_ROOT}", str(bundle))
    skill_receipts = [seq for seq, value in messages
                      if value.startswith("Base directory for this skill: " + str(bundle / "skills/review-code"))
                      and body in value]
    if binding:
        main_required = {
            "skills/review-code/" + name for name in (
                "packet-preparation.md", "review-process.md", "shared-capy-knowledge-protocol.md",
                "shared-profile-detection.md", "shared-review-scope-protocol.md",
                "shared-change-context.md", "functional-review.md")}
        child_required = {"skills/_shared/change-context.md", "skills/review-code/functional-review.md",
                          "skills/_shared/review-scope-protocol.md",
                          "skills/_shared/capy-knowledge-protocol.md", "skills/review-code/SKILL.md"}
        for actor, expected in (("main", main_required), ("child", child_required)):
            observed = {r["path"] for r in reads if r["actor"] == actor and r["complete_numbered_text"]}
            if not expected <= observed:
                raise ValueError("Incomplete binding reads for " + actor + ": " + str(expected - observed))
        if not root_receipts or not skill_receipts:
            raise ValueError("Missing root or registered skill delivery receipt")
    return {"run": source.name, "sealed_files": len(seal), "hashes": "PASS",
            "runtime_model_plugin_capy_no_pal": "PASS", "initial_subject_unchanged": "PASS",
            "root_receipts": root_receipts, "registered_skill_receipts": skill_receipts,
            "direct_instruction_reads": reads, "shell_requests": shell, "file_requests": paths,
            "runtime_notices": notices,
            "access_assessment": "manual review required; paths/commands are evidence, not OS confinement"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--binding", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.source.resolve(), args.binding), indent=2))
