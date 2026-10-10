"""Seal only allowlisted, nonsensitive PAL history-receipt metadata.

The raw log stays local. Only preselected successful-embedding lines are checked
for exact equality; no prompt, response, credential or unrelated line is emitted
or copied. Link every line to one sealed actual call and its captured payload.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

import controller
import prepare_grades


HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "pal-receipts"
SERVER_ROOT = Path("/home/sergio/.cache/uv/archive-v0/tA__Bny_AWlVfU9_18s9G/lib/python3.12/site-packages")
LOG = SERVER_ROOT / "logs/mcp_server.log"
SOURCE = SERVER_ROOT / "utils/conversation_memory.py"
CACHED_SOURCE = Path("/home/sergio/.cache/uv/git-v0/checkouts/e408457349e99dab/c20d384/utils/conversation_memory.py")
RUNS = ("codex-r3-isolated-1", "codex-i2-standalone-1", "codex-r3-isolated-2", "codex-i2-standalone-2")
LINE = re.compile(r"^(\d+):(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - utils\.conversation_memory - DEBUG - File embedded in conversation history: (/tmp/[^\n]+) \(([\d,]+) tokens\)$")


def load_allowed_lines():
    selected = {}
    for text in (RECEIPTS / "observed-lines.txt").read_text().splitlines():
        match = LINE.fullmatch(text)
        if not match:
            raise ValueError("Non-allowlisted receipt line")
        number = int(match[1])
        if number in selected or int(match[4].replace(",", "")) <= 0:
            raise ValueError("Duplicate or empty receipt")
        timestamp = datetime.strptime(match[2], "%Y-%m-%d %H:%M:%S,%f").replace(tzinfo=timezone(timedelta(hours=2)))
        selected[number] = {"line": number, "raw_line": text.split(":", 1)[1],
                            "path": match[3], "timestamp_ms": round(timestamp.timestamp() * 1000)}
    # The local check reads only up to the last selected line, retaining a digest
    # rather than the intervening contents. Nothing raw is sent to an MCP service.
    prefix_hash, prefix_size, seen = hashlib.sha256(), 0, set()
    with LOG.open("rb") as stream:
        for number, raw in enumerate(stream, 1):
            prefix_hash.update(raw)
            prefix_size += len(raw)
            if number in selected:
                if raw.decode("utf-8").rstrip("\n") != selected[number]["raw_line"]:
                    raise ValueError(f"Local log does not match selected metadata line {number}")
                seen.add(number)
            if number == max(selected):
                break
    if seen != set(selected):
        raise ValueError("Missing selected receipt metadata")
    return selected, {"path": str(LOG), "through_line": max(selected), "prefix_bytes": prefix_size,
                      "prefix_sha256": prefix_hash.hexdigest(), "raw_log_copied": False}


def actual_calls(run):
    root = HERE / run
    seal = json.loads((root / "manifest.json").read_bytes())
    for relative, sha in seal.items():
        prepare_grades.previous.checked_file(root, relative, sha)
    protocol = [json.loads(row) for row in (root / "protocol.jsonl").read_text().splitlines()]
    payloads = [json.loads(row) for row in (root / "payload-events.jsonl").read_text().splitlines()]
    for name in seal:
        if not (name.startswith("items-") and name.endswith(".json")):
            continue
        for row in json.loads((root / name).read_bytes()):
            item = row["item"]
            if (item.get("type") != "mcpToolCall" or item.get("server") != "pal"
                    or item.get("tool") != "codereview" or item["arguments"].get("step_number") != 2):
                continue
            sequences = {record["sequence"] for record in protocol
                         if record["message"].get("method") in {"item/started", "item/completed"}
                         and record["message"].get("params", {}).get("item", {}).get("id") == item["id"]}
            files = {}
            for event in payloads:
                if event["event_sequence"] in sequences:
                    for entry in event["files"]:
                        if "sha256" in entry:
                            files.setdefault(entry["path"], set()).add((entry["sha256"], entry["artifact"]))
            yield {"run": run, "call_id": item["id"], "source_item_file": name,
                   "continuation_id": item["arguments"].get("continuation_id"),
                   "start_ms": row["startedAtMs"], "end_ms": row["completedAtMs"],
                   "relevant_files": item["arguments"].get("relevant_files", []), "payloads": files,
                   "source_manifest_sha256": prepare_grades.previous.digest(root / "manifest.json")}


def main():
    selected, origin = load_allowed_lines()
    if SOURCE.read_bytes() != CACHED_SOURCE.read_bytes():
        raise ValueError("Installed PAL history implementation differs from declared source")
    calls = [call for run in RUNS for call in actual_calls(run)]
    by_run = {run: [] for run in RUNS}
    for record in selected.values():
        matches = [call for call in calls if record["path"] in call["relevant_files"]
                   and call["start_ms"] <= record["timestamp_ms"] <= call["end_ms"]]
        if len(matches) != 1:
            raise ValueError("Receipt is not linked to exactly one actual invocation")
        call = matches[0]
        payload = call["payloads"].get(record["path"], set())
        if len(payload) != 1:
            raise ValueError("Receipt has missing or changing dispatch-snapshot content")
        sha, artifact = next(iter(payload))
        root = HERE / call["run"]
        prepare_grades.previous.checked_file(root, artifact, sha)
        by_run[call["run"]].append({**record, "call_id": call["call_id"],
            "continuation_id": call["continuation_id"], "call_start_ms": call["start_ms"],
            "call_end_ms": call["end_ms"], "source_item_file": call["source_item_file"],
            "payload_sha256": sha, "original_payload_artifact": artifact})
    for run, records in by_run.items():
        destination = RECEIPTS / run
        destination.mkdir(parents=True, exist_ok=False)
        controller.write_json(destination / "receipts.json", records)
        controller.write_json(destination / "origin.json", {**origin,
            "source_manifest_sha256": prepare_grades.previous.digest(HERE / run / "manifest.json"),
            "installed_source_path": str(SOURCE), "installed_source_sha256": prepare_grades.previous.digest(SOURCE),
            "installed_source_matches_commit": "c20d384a9c5a38ab8d58c780d2e269c537e409fa",
            "clock": "Europe/Oslo, UTC+02:00 on 2026-10-10; timestamps matched exact sealed call bounds",
            "collector_sha256": prepare_grades.previous.digest(Path(__file__))})
        shutil.copyfile(RECEIPTS / "source-semantics.md", destination / "source-semantics.md")
        # Bound source excerpt explains exactly when the observed log is emitted;
        # no private model prompt or full MCP log enters this supplement.
        lines = SOURCE.read_text().splitlines()
        (destination / "source-excerpt.txt").write_text("\n".join(f"{n + 1}: {lines[n]}" for n in range(834, 886)) + "\n")
        files = [{"path": p.name, "sha256": prepare_grades.previous.digest(p), "role": p.name}
                 for p in sorted(destination.iterdir()) if p.is_file()]
        controller.write_json(destination / "manifest.json", {"run": run, "evidence_root": ".", "files": files,
            "kind": "supplemental existing-runtime receipt metadata", "integrity": "selected lines verified locally; unique call/time/path links and sealed payload hashes verified",
            "limits": "shared log; attribution requires unique run paths and exact call windows; exact model prompt unverified; reviewer use still judged from original result"})
        print(json.dumps({"run": run, "receipts": len(records), "manifest": str(destination / "manifest.json"),
                          "sha256": prepare_grades.previous.digest(destination / "manifest.json")}))


if __name__ == "__main__":
    main()
