"""Package one sealed capture using explicit fixture/rubric/grader inputs.

Offline only. Input seals are verified before output creation. This is a
portable extraction of Task 8 packaging, not a behavioral grading engine.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from receipts import public


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def checked_file(root, relative, expected):
    root = Path(root)
    rel = Path(relative)
    if not rel.parts or rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Unsafe manifest path: " + str(relative))
    path = root / rel
    current = path
    while current != root:
        if current.is_symlink():
            raise ValueError("Symlink in evidence path: " + str(relative))
        current = current.parent
    if not path.is_file() or digest(path) != expected:
        raise ValueError("Evidence hash mismatch: " + str(path))
    return path


def observable_events(source, provider, source_manifest):
    events = []
    if provider == "claude":
        path = checked_file(source, "events.jsonl", source_manifest["events.jsonl"])
        with path.open() as stream:
            for raw in stream:
                row = json.loads(raw)
                event = row["event"]
                message = event.get("message")
                if not isinstance(message, dict):
                    continue
                for offset, block in enumerate(message.get("content", [])):
                    if not isinstance(block, dict) or block.get("type") not in {"tool_use", "tool_result", "text"}:
                        continue
                    if event.get("type") == "user" and block["type"] == "text":
                        continue
                    parent = event.get("parent_tool_use_id")
                    events.append({"id": f"e{row['sequence']}.{offset}",
                        "source_sequence": row["sequence"], "session_id": event.get("session_id"),
                        "actor": "child-of:" + parent if parent else "main",
                        "parent_tool_use_id": parent, "block": public(block)})
    elif provider == "codex":
        names = sorted(name for name in source_manifest
            if Path(name).name == name and name.startswith("items-") and name.endswith(".json"))
        if not names:
            raise ValueError("No sealed Codex event files")
        for name in names:
            path = checked_file(source, name, source_manifest[name])
            for row in json.loads(path.read_text()):
                item = row["item"]
                if item["type"] in {"reasoning", "omitted_private_reasoning", "userMessage"}:
                    continue
                events.append({"id": item["id"], "actor": path.stem,
                    "source_file": path.name, **public(row)})
    else:
        raise ValueError("Provider must be claude or codex")
    return events


def prepare(request_path, destination):
    request_path, destination = Path(request_path).resolve(), Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(destination)
    request = json.loads(request_path.read_text())
    source = Path(request["capture"]).resolve(strict=True)
    fixture = Path(request["fixture"]).resolve(strict=True)
    for root in (source, fixture):
        if destination.is_relative_to(root) or root.is_relative_to(destination):
            raise ValueError("Output overlaps input")
    for field in ("run", "identity"):
        if not isinstance(request[field], dict) or not request[field]:
            raise ValueError(field + " must explicitly describe this comparison")
    source_seal = checked_file(source, "manifest.json", request["capture_manifest_sha256"])
    seal = json.loads(source_seal.read_text())
    for rel, sha in seal.items():
        checked_file(source, rel, sha)
    for rel, sha in request["fixture_manifest"].items():
        checked_file(fixture, rel, sha)
    definition = checked_file(fixture, "eval.json", request["fixture_manifest"]["eval.json"])
    assertions = json.loads(definition.read_text())["assertions"]
    pinned = {}
    for role in ("rubric", "grader"):
        record = request[role]
        path = Path(record["path"]).resolve(strict=True)
        pinned[role] = checked_file(path.parent, path.name, record["sha256"])
    events = observable_events(source, request["provider"], seal)
    destination.mkdir(parents=True, exist_ok=False)
    for rel, sha in seal.items():
        if (rel.startswith(("initial/", "final/", "payloads/")) or rel in {
            "initial.patch", "final.patch", "report.md", "payload-events.jsonl",
            "released-provider.py", "launch.json", "prompt.txt", "credential-redactions.json"}):
            target = destination / "captured" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checked_file(source, rel, sha), target)
            checked_file(destination / "captured", rel, sha)
    for rel, sha in request["fixture_manifest"].items():
        if rel.startswith("oracle/"):
            target = destination / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checked_file(fixture, rel, sha), target)
            checked_file(destination, rel, sha)
    for role, path in pinned.items():
        shutil.copyfile(path, destination / (role + ".md"))
        checked_file(destination, role + ".md", request[role]["sha256"])
    write_json(destination / "request.json", request)
    write_json(destination / "assertions.json", assertions)
    (destination / "events.jsonl").write_text("".join(json.dumps(event) + "\n" for event in events))
    (destination / "events.txt").write_text("\n\n".join(
        "EVENT " + event["id"] + "\n" + json.dumps(event, indent=2) for event in events) + "\n")
    files = [{"path": path.relative_to(destination).as_posix(), "sha256": digest(path), "role": path.name}
        for path in sorted(destination.rglob("*")) if path.is_file()]
    manifest = {"run": request["run"], "identity": request["identity"],
        "source_manifest_sha256": request["capture_manifest_sha256"],
        "source_path": str(source), "evidence_root": ".", "files": files,
        "adapter_sources": {name: digest(Path(__file__).with_name(name))
                            for name in ("grading.py", "receipts.py")},
        "completeness": {
            "events": "observable retained blocks/items; original IDs and source order retained per actor; no inferred global ordering",
            "children": "actual runtime links only; read coverage requires returned tool content",
            "dispatches": "receipt/use only; exact submitted prompt content remains unverified",
            "snapshots": "only explicitly sealed initial/final files",
            "user_decisions": "only captured decisions; none supplied by this adapter"},
        "redactions": ["private reasoning/encrypted fields omitted from derived events; supplied captures must already be credential-redacted"],
        "integrity": "all input seal entries verified; derived file hashes listed; no behavioral verdict inferred",
        "actor_grading_material_access": "not assessed by offline packaging"}
    write_json(destination / "manifest.json", manifest)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    prepare(args.request, args.destination)
