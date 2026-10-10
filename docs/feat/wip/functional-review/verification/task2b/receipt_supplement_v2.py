"""Seal successful PAL reads, formatting and history inclusion from existing logs.

Version 1 remains intact. Its history marker alone can also describe an error.
This collector exports only three strict metadata patterns for the same owned
path, then binds their counts and call window to the original sealed payload.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

import controller
import prepare_grades
import receipt_supplement as prior


HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "pal-receipts-v2"
FILE_SOURCE = prior.SERVER_ROOT / "utils/file_utils.py"
FILE_CACHED_SOURCE = prior.CACHED_SOURCE.with_name("file_utils.py")
STAMP = r"(?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
OWNED = r"(?P<path>/tmp/[A-Za-z0-9_./-]+)"
READ = re.compile(STAMP + r" - utils\.file_utils - DEBUG - \[FILES\] Successfully read (?P<chars>\d+) characters from " + OWNED)
FORMAT = re.compile(STAMP + r" - utils\.file_utils - DEBUG - \[FILES\] Formatted content for " + OWNED + r": (?P<chars>\d+) chars, (?P<tokens>\d+) tokens")
EMBED = re.compile(STAMP + r" - utils\.conversation_memory - DEBUG - File embedded in conversation history: " + OWNED + r" \((?P<tokens>[\d,]+) tokens\)")


def parse_triplet(lines, first_line):
    """Reject errors or ambiguous/nonconsecutive read/format/embed sequences."""
    parsed = []
    for offset, pattern in enumerate((READ, FORMAT, EMBED)):
        match = pattern.fullmatch(lines[offset])
        if not match:
            raise ValueError("Missing allowlisted successful read/format/embed metadata")
        fields = match.groupdict()
        timestamp = datetime.strptime(fields.pop("stamp"), "%Y-%m-%d %H:%M:%S,%f").replace(
            tzinfo=timezone(timedelta(hours=2)))
        for name in ("chars", "tokens"):
            if name in fields:
                fields[name] = int(fields[name].replace(",", ""))
                if fields[name] <= 0:
                    raise ValueError("Empty read/format/embed metadata")
        parsed.append({**fields, "line": first_line + offset, "raw_line": lines[offset],
                       "timestamp_ms": round(timestamp.timestamp() * 1000)})
    read, formatted, embedded = parsed
    if len({row["path"] for row in parsed}) != 1:
        raise ValueError("Read/format/embed paths differ")
    if not read["timestamp_ms"] <= formatted["timestamp_ms"] <= embedded["timestamp_ms"]:
        raise ValueError("Read/format/embed timestamps are out of order")
    if formatted["tokens"] != embedded["tokens"] or formatted["chars"] <= read["chars"]:
        raise ValueError("Formatting and embedding counts disagree")
    return parsed


def bind_payload(triplet, call, content):
    read, _, embedded = triplet
    if read["path"] not in call["relevant_files"]:
        raise ValueError("Receipt path absent from actual invocation")
    if not call["start_ms"] <= read["timestamp_ms"] <= embedded["timestamp_ms"] <= call["end_ms"]:
        raise ValueError("Receipt outside actual invocation window")
    # Match PAL's UTF-8 replacement decoding and text-mode universal newlines.
    text = content.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    if len(text) != read["chars"]:
        raise ValueError("Successful-read character count differs from sealed payload")


def collect_triplets():
    selected, origin = prior.load_allowed_lines()
    numbers = {n for end in selected for n in (end - 2, end - 1, end)}
    retained, prefix_hash, prefix_size = {}, hashlib.sha256(), 0
    with prior.LOG.open("rb") as stream:
        for number, raw in enumerate(stream, 1):
            prefix_hash.update(raw)
            prefix_size += len(raw)
            if number in numbers:
                retained[number] = raw.decode("utf-8").rstrip("\n")
            if number == origin["through_line"]:
                break
    if (prefix_hash.hexdigest() != origin["prefix_sha256"] or prefix_size != origin["prefix_bytes"]
            or set(retained) != numbers):
        raise ValueError("Local log prefix changed or required metadata is missing")
    triplets = []
    for end, record in selected.items():
        if retained[end] != record["raw_line"]:
            raise ValueError("History marker differs from original metadata")
        triplets.append(parse_triplet([retained[n] for n in range(end - 2, end + 1)], end - 2))
    return triplets, origin


def main():
    triplets, origin = collect_triplets()
    sources = ((prior.SOURCE, prior.CACHED_SOURCE, 835, 886),
               (FILE_SOURCE, FILE_CACHED_SOURCE, 421, 520))
    for installed, cached, _, _ in sources:
        if installed.read_bytes() != cached.read_bytes():
            raise ValueError("Installed PAL implementation differs from declared source")
    calls = [call for run in prior.RUNS for call in prior.actual_calls(run)]
    by_run = {run: [] for run in prior.RUNS}
    for triplet in triplets:
        read, formatted, embedded = triplet
        matches = [call for call in calls if read["path"] in call["relevant_files"]
                   and call["start_ms"] <= read["timestamp_ms"] <= embedded["timestamp_ms"] <= call["end_ms"]]
        if len(matches) != 1:
            raise ValueError("Receipt is not linked to exactly one actual invocation")
        call = matches[0]
        payload = call["payloads"].get(read["path"], set())
        if len(payload) != 1:
            raise ValueError("Receipt has missing or changing dispatch-snapshot content")
        sha, artifact = next(iter(payload))
        root = HERE / call["run"]
        prepare_grades.previous.checked_file(root, artifact, sha)
        bind_payload(triplet, call, (root / artifact).read_bytes())
        by_run[call["run"]].append({**embedded, "successful_read": read, "formatted_content": formatted,
            "call_id": call["call_id"], "continuation_id": call["continuation_id"],
            "call_start_ms": call["start_ms"], "call_end_ms": call["end_ms"],
            "source_item_file": call["source_item_file"], "payload_sha256": sha,
            "original_payload_artifact": artifact})
    if any(not records for records in by_run.values()):
        raise ValueError("A declared run has no successful-read receipts")
    for run, records in by_run.items():
        destination = RECEIPTS / run
        destination.mkdir(parents=True, exist_ok=False)
        controller.write_json(destination / "receipts.json", records)
        controller.write_json(destination / "origin.json", {**origin,
            "source_manifest_sha256": prepare_grades.previous.digest(HERE / run / "manifest.json"),
            "supersedes_receipt_manifest_sha256": prepare_grades.previous.digest(prior.RECEIPTS / run / "manifest.json"),
            "installed_sources": [{"path": str(installed), "sha256": prepare_grades.previous.digest(installed)}
                                  for installed, _, _, _ in sources],
            "installed_sources_match_commit": "c20d384a9c5a38ab8d58c780d2e269c537e409fa",
            "clock": "Europe/Oslo, UTC+02:00 on 2026-10-10; timestamps matched exact sealed call bounds",
            "collector_sources": {p.name: prepare_grades.previous.digest(p) for p in
                                  (Path(__file__), Path(prior.__file__), Path(controller.__file__), Path(prepare_grades.__file__))}})
        shutil.copyfile(RECEIPTS / "source-semantics.md", destination / "source-semantics.md")
        for installed, _, start, end in sources:
            lines = installed.read_text().splitlines()
            (destination / (installed.stem + "-excerpt.txt")).write_text(
                "\n".join(f"{n + 1}: {lines[n]}" for n in range(start - 1, end)) + "\n")
        files = [{"path": p.name, "sha256": prepare_grades.previous.digest(p), "role": p.name}
                 for p in sorted(destination.iterdir()) if p.is_file()]
        controller.write_json(destination / "manifest.json", {"run": run, "evidence_root": ".", "files": files,
            "kind": "supplemental existing-runtime successful-read, format and history-inclusion metadata",
            "integrity": "strict consecutive metadata verified locally; same path/time/call, matching format/embed tokens, read count matched to sealed payload",
            "limits": "shared log; unique paths/windows and stable dispatch snapshots establish attribution, not a runtime content digest; exact model prompt unverified; use judged from original result"})
        print(json.dumps({"run": run, "receipts": len(records), "manifest": str(destination / "manifest.json"),
                          "sha256": prepare_grades.previous.digest(destination / "manifest.json")}))


if __name__ == "__main__":
    main()
