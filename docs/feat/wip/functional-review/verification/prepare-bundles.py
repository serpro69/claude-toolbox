#!/usr/bin/env python3
"""Task 1 controller utility: immutable Git inputs to filtered actor bundles.

Run outside the actor. Manifests and the source archive must never be mounted
in an actor workspace. Python standard library only; Python 3.9 or newer.
"""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile


TREES = ("klaude-plugin", "kodex-plugin", ".codex/agents")
EXCLUDED_PARTS = {"evals", "oracle", "grading-fixtures", "verification", "results", "reports"}
EXCLUDED_NAMES = {"eval.json", "gold-claims.json", "expected-verdicts.json"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def excluded(path):
    return bool(set(Path(path).parts) & EXCLUDED_PARTS) or Path(path).name in EXCLUDED_NAMES


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def manifest(root):
    """Inspect every retained file, including hidden files and link targets."""
    records = []
    root = root.resolve(strict=True)
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if excluded(rel):
            raise ValueError("Evaluator material in actor bundle: " + rel)
        if path.is_symlink():
            target = os.readlink(path)
            resolved = path.resolve(strict=True)
            if os.path.isabs(target) or not resolved.is_relative_to(root):
                raise ValueError("Escaping link: " + rel)
            if not resolved.is_file():
                raise ValueError("Only file links are supported: " + rel)
            records.append({"path": rel, "kind": "symlink", "target": target,
                            "sha256": digest(resolved.read_bytes())})
        elif path.is_file():
            records.append({"path": rel, "kind": "file", "mode": oct(path.stat().st_mode & 0o777),
                            "sha256": digest(path.read_bytes())})
        elif not path.is_dir():
            raise ValueError("Unsupported file type: " + rel)
    return records


def build(repo, revision, destination):
    git_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    git_env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    full = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--verify", revision + "^{commit}"],
        env=git_env, text=True).strip()
    committed = {}
    entries = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-rz", full, "--", *TREES],
                                      env=git_env)
    for entry in entries.split(b"\0"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, kind, oid = metadata.decode().split()
            if kind != "blob":
                raise ValueError("Unsupported Git object: " + path.decode())
            committed[path.decode()] = (mode, oid)
    # Refuse reuse even when a previous invocation failed part-way through.
    destination.mkdir(parents=True, exist_ok=False)
    source = subprocess.check_output(["git", "-C", str(repo), "archive", full, *TREES], env=git_env)
    (destination / "source.tar").write_bytes(source)
    source_records, exclusions = [], []
    with tarfile.open(fileobj=io.BytesIO(source)) as archive:
        for member in archive:
            if member.isdir():
                continue
            rel = Path(member.name)
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("Unsafe source path: " + member.name)
            if not member.isfile() and not member.issym():
                raise ValueError("Unsupported archive member: " + member.name)
            if member.issym():
                data = member.linkname.encode()
            else:
                with archive.extractfile(member) as stream:
                    data = stream.read()
            mode, oid = committed[member.name]
            blob = b"blob " + str(len(data)).encode() + b"\0" + data
            algorithm = "sha1" if len(oid) == 40 else "sha256"
            if hashlib.new(algorithm, blob).hexdigest() != oid:
                raise ValueError("Archive differs from Git blob (export-subst?): " + member.name)
            expected_mode = "120000" if member.issym() else ("100755" if member.mode & 0o111 else "100644")
            if mode != expected_mode:
                raise ValueError("Archive changed Git mode: " + member.name)
            record = {"path": member.name, "sha256": digest(data),
                      "mode": oct(member.mode), "kind": "symlink" if member.issym() else "file"}
            if member.issym():
                record["target"] = member.linkname
            source_records.append(record)
            if excluded(member.name):
                exclusions.append(member.name)
                continue
            target = destination / "retained" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if member.issym():
                target.symlink_to(member.linkname)
            else:
                target.write_bytes(data)
                target.chmod(member.mode)
    if {record["path"] for record in source_records} != set(committed):
        raise ValueError("Archive omitted committed files (export-ignore?)")
    write_json(destination / "source-manifest.json", source_records)
    write_json(destination / "exclusions.json", exclusions)
    retained = {}
    for tree in TREES:
        retained[tree] = manifest(destination / "retained" / tree)
    # Establish byte identity separately from the link-resolution scan.
    for record in source_records:
        if record["path"] in exclusions:
            continue
        path = destination / "retained" / record["path"]
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        if digest(data) != record["sha256"]:
            raise ValueError("Retained byte mismatch: " + record["path"])
    write_json(destination / "retained-manifest.json", retained)
    identity = {"revision": full, "archive_sha256": digest(source),
                "source_files": len(source_records), "excluded_files": len(exclusions),
                "retained_files": sum(map(len, retained.values())),
                "retained_manifest_sha256": digest((destination / "retained-manifest.json").read_bytes())}
    write_json(destination / "identity.json", identity)
    return identity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("build")
    prepare.add_argument("repo", type=Path)
    prepare.add_argument("revision")
    prepare.add_argument("destination", type=Path)
    verify = sub.add_parser("verify")
    verify.add_argument("bundle", type=Path)
    verify.add_argument("manifest", type=Path)
    verify.add_argument("tree", choices=TREES)
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build(args.repo, args.revision, args.destination), sort_keys=True))
    else:
        expected = json.loads(args.manifest.read_text())[args.tree]
        actual = manifest(args.bundle)
        if actual != expected:
            raise ValueError("Bundle/cache differs from retained manifest: " + str(args.bundle))
        print(json.dumps({"status": "PASS", "files": len(actual), "root": str(args.bundle)}))


if __name__ == "__main__":
    main()
