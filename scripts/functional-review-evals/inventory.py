"""Create/verify an evidence inventory; never creates archives or deletes files."""
import argparse
import json
import os
from pathlib import Path
import stat

from grading import digest, write_json


def inventory(root):
    root = Path(root).resolve(strict=True)
    records, exclusions = [], []
    def visit(directory):
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                records.append({"path": relative, "kind": "symlink", "target": os.readlink(path)})
            elif stat.S_ISDIR(mode):
                if path.name == "__pycache__":
                    exclusions.append(relative + "/")
                else:
                    records.append({"path": relative, "kind": "directory"})
                    visit(path)
            elif stat.S_ISREG(mode):
                records.append({"path": relative, "kind": "file", "bytes": path.stat().st_size,
                                "sha256": digest(path), "mode": oct(stat.S_IMODE(mode))})
            else:
                raise ValueError("Unsupported member: " + relative)
    visit(root)
    return {"members": records, "exclusions": exclusions,
        "counts": {kind: sum(row["kind"] == kind for row in records)
                   for kind in ("file", "symlink", "directory")},
        "regular_file_bytes": sum(row.get("bytes", 0) for row in records)}


def create(root, output, prefix, revision):
    root, output = Path(root).resolve(strict=True), Path(output).resolve()
    if output.is_relative_to(root):
        raise ValueError("Write the manifest outside the evidence tree")
    member_root = Path(prefix)
    if not member_root.parts or member_root.is_absolute() or ".." in member_root.parts:
        raise ValueError("Archive prefix must be a relative member path")
    result = {"schema": 1, "archive_member_root": member_root.as_posix(),
              "original_revision": revision, "exclusion_policy": "directory basename __pycache__ only",
              **inventory(root)}
    write_json(output, result)
    return result


def verify(root, manifest):
    expected = json.loads(Path(manifest).read_text())
    actual = inventory(root)
    # Excluded cache directories may be absent after extraction.
    for key in ("members", "counts", "regular_file_bytes"):
        if actual[key] != expected[key]:
            raise ValueError("Inventory mismatch: " + key)
    return actual["counts"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    make = sub.add_parser("create")
    make.add_argument("root", type=Path)
    make.add_argument("output", type=Path)
    make.add_argument("--prefix", required=True)
    make.add_argument("--revision", required=True)
    check = sub.add_parser("verify")
    check.add_argument("root", type=Path)
    check.add_argument("manifest", type=Path)
    args = parser.parse_args()
    if args.operation == "create":
        print(json.dumps(create(args.root, args.output, args.prefix, args.revision)["counts"]))
    else:
        print(json.dumps(verify(args.root, args.manifest)))
