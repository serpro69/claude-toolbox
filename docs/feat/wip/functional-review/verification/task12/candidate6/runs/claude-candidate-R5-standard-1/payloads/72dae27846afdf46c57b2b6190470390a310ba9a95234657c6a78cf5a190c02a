#!/usr/bin/env python3
"""Package original review instructions for complete, bounded Read calls.

This helper never opens subject files or evaluates profile predicates. It checks
instruction membership/completeness and prints paths to read, not a review gate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[3]
COMMON = (
    "skills/review-code/packet-preparation.md",
    "skills/review-code/review-process.md",
    "skills/review-code/shared-capy-knowledge-protocol.md",
    "skills/review-code/shared-profile-detection.md",
    "skills/review-code/shared-review-scope-protocol.md",
    "skills/review-code/shared-change-context.md",
    "skills/review-code/functional-review.md",
)
PART_BYTES = 12000


def read_instruction(root, relative):
    path = root / relative
    resolved = path.resolve()
    if (Path(relative).is_absolute() or ".." in Path(relative).parts
            or any(part in {"evals", "oracle"} for part in Path(relative).parts)
            or not resolved.is_relative_to(root.resolve())
            or any(part in {"evals", "oracle"} for part in resolved.relative_to(root.resolve()).parts)):
        raise ValueError("Instruction path escapes the plugin boundary: " + relative)
    return path.read_bytes()


def known_profiles(root):
    text = read_instruction(root, "skills/review-code/shared-profile-detection.md").decode()
    match = re.search(r"^### Known profiles\s*\n(.*?)(?=^### |\Z)", text, re.M | re.S)
    profiles = re.findall(r"^- `([a-z0-9_-]+)`\s*$", match[1], re.M) if match else []
    if not profiles or len(profiles) != len(set(profiles)):
        raise ValueError("Cannot resolve the authoritative Known profiles list")
    return profiles


def checklist_entries(root, profile):
    text = read_instruction(root, f"profiles/{profile}/review-code/index.md").decode()
    sections = re.split(r"^## (Always load|Conditional)\s*$", text, flags=re.M)
    entries = {}
    for i in range(1, len(sections), 2):
        for name in re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", sections[i + 1]):
            if Path(name).name != name or name in entries:
                raise ValueError("Unsupported or duplicate index path: " + name)
            entries[name] = sections[i] == "Always load"
    if not entries:
        raise ValueError("Empty or unsupported review index: " + profile)
    return entries


def select_sources(root, phase, profiles=(), selected=(), skipped=()):
    known = known_profiles(root)
    if len(profiles) != len(set(profiles)) or any(p not in known for p in profiles):
        raise ValueError("Profiles must be distinct members of Known profiles")
    unavailable = []
    sources = []
    if phase == "bootstrap":
        sources.extend((p, read_instruction(root, p)) for p in COMMON)
        for profile in known:
            relative = f"profiles/{profile}/DETECTION.md"
            try:
                sources.append((relative, read_instruction(root, relative)))
            except FileNotFoundError:
                unavailable.append({"path": relative, "outcome": "ENOENT"})
    elif phase == "profiles":
        for profile in profiles:
            relative = f"profiles/{profile}/review-code/index.md"
            sources.append((relative, read_instruction(root, relative)))
    elif phase == "checklists":
        decisions = {}
        for path in selected:
            if path in decisions:
                raise ValueError("Duplicate checklist decision: " + path)
            decisions[path] = (True, "selected by actor routing")
        for entry in skipped:
            path, separator, reason = entry.partition("=")
            if not separator or not reason.strip() or path in decisions:
                raise ValueError("Skipped checklist needs one explicit reason: " + entry)
            decisions[path] = (False, reason)
        expected = {}
        for profile in profiles:
            expected.update({f"{profile}/{name}": required
                             for name, required in checklist_entries(root, profile).items()})
        if set(decisions) != set(expected):
            raise ValueError("Every active-profile index entry needs a load/skip decision")
        for path, required in expected.items():
            load, reason = decisions[path]
            if required and not load:
                raise ValueError("Cannot skip an always-load checklist: " + path)
            if load:
                profile, name = path.split("/")
                relative = f"profiles/{profile}/review-code/{name}"
                sources.append((relative, read_instruction(root, relative)))
            else:
                unavailable.append({"path": path, "outcome": "conditional not selected", "reason": reason})
    else:
        raise ValueError("Unknown packet phase")
    return sources, unavailable


def write_packet(root, phase, sources, unavailable):
    """Preserve source bytes; frame and split them without truncating content."""
    pieces, current, inventory = [], b"", []
    for relative, content in sources:
        digest = hashlib.sha256(content).hexdigest()
        inventory.append({"source": str(root / relative), "sha256": digest,
                          "bytes": len(content)})
        framed = (f"\nBEGIN SOURCE {root / relative}\nSHA256 {digest}\n"
                  "Resolve links relative to this original source path.\n\n").encode() + content + b"\nEND SOURCE\n"
        for line in framed.splitlines(keepends=True):
            if len(line) > PART_BYTES:
                raise ValueError("Instruction line exceeds packet bound; use direct Read")
            if len(current) + len(line) > PART_BYTES:
                pieces.append(current)
                current = b""
            current += line
    if current:
        pieces.append(current)
    # No caller-controlled destination, overwrite or subject-tree write.
    destination = Path(tempfile.mkdtemp(prefix="kk-review-instructions-"))
    manifest = {"phase": phase, "plugin_root": str(root), "sources": inventory,
                "routing_outcomes": unavailable, "parts": [],
                "gate": "NOT ESTABLISHED: read every complete part before investigation"}
    for number, content in enumerate(pieces, 1):
        path = destination / f"part-{number:02d}.md"
        header = f"Instruction packet {phase}: part {number}/{len(pieces)}\n\n".encode()
        footer = f"\nEND PACKET PART {number}/{len(pieces)}\n".encode()
        path.write_bytes(header + content + footer)
        path.chmod(0o400)
        manifest["parts"].append({"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest_path = destination / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    manifest_path.chmod(0o400)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("bootstrap", "profiles", "checklists"))
    parser.add_argument("--profile", action="append", default=[])
    parser.add_argument("--load", action="append", default=[])
    parser.add_argument("--skip", action="append", default=[])
    args = parser.parse_args()
    if args.phase != "checklists" and (args.load or args.skip):
        parser.error("--load/--skip belong to the checklists phase")
    sources, unavailable = select_sources(ROOT, args.phase, args.profile, args.load, args.skip)
    print(json.dumps(write_packet(ROOT, args.phase, sources, unavailable), indent=2))


if __name__ == "__main__":
    main()
