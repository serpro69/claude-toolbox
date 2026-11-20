"""First install and status. Writers own the lock across validation and activation."""

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

from . import claude, payload, state, validation
from .run import load_cli


def entry_link():
    return Path.home() / ".local/bin/kk"


def check_link(home, record):
    link = entry_link()
    if os.path.lexists(link):
        if str(link) not in record["installed_paths"] or not link.is_symlink() or link.resolve() != home / "bin/kk":
            raise ValueError("install path already exists: {}".format(link))


def finish_install(home, record, release):
    """Called in the validated release's package while the bootstrap owns the lock."""
    check_link(home, record)
    claude.activate(home, release)
    entry = home / "bin/kk"
    state.atomic_write(entry, (release / "kk/bin/kk").read_bytes(), mode=0o755)
    link = entry_link()
    if str(link) not in record["installed_paths"]:
        record["installed_paths"].append(str(link))
        state.write_json(home / "state.json", record)
    link.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.lexists(link):
        link.symlink_to(entry)  # Atomic create-only publication of the recorded path.
    check_link(home, record)
    state.promote(record, release.name)
    state.write_json(home / "state.json", record)
    print("Claude ready:", release.name)


def replace_pending(source, destination, work):
    """Replace only an unpromoted directory owned by this first installation."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        with tempfile.TemporaryDirectory(dir=work) as backup:
            destination.rename(Path(backup) / "previous")
            source.rename(destination)
    else:
        source.rename(destination)


def prepare(home, record, args, archive_file, work):
    candidate = record["candidate"]
    source = {"local": str(args.local.resolve())} if args.local else {
        "tag": args.version, "repository": os.environ.get("KK_REPOSITORY", "serpro69/claude-toolbox")}
    if candidate and not args.local and not args.version:
        source = candidate["source"]
    if candidate and source == candidate["source"]:
        version = payload.release_id(candidate["version"])
        stage = home / "staging" / version
        existing = stage if stage.is_dir() else home / "releases" / version
        try:
            if not existing.is_dir() or existing.is_symlink() or payload.fingerprint(existing) != candidate["digest"]:
                raise ValueError("journaled payload is missing or changed")
            payload.validate_layout(existing, version)
            validation.validate(existing)
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
            print("kk: rebuilding incomplete candidate {}: {}".format(version, exc), file=sys.stderr)
        else:
            return version
    elif candidate:
        print("kk: restarting first install from the requested source", file=sys.stderr)
    local = Path(source["local"]) if "local" in source else None
    with tempfile.TemporaryDirectory(dir=work) as temp:
        stage = Path(temp) / "payload"
        stage.mkdir()
        version = payload.stage(stage, local, source.get("tag"), archive_file, source.get("repository"))
        if local is None:
            source["tag"] = version
        placed = home / "releases" / version
        if placed.exists() and not (candidate and candidate["version"] == version and candidate["source"] == source):
            raise ValueError("retained release {} already occupies {}; choose a different tag or --local".format(
                version, placed))
        validation.validate(stage)
        digest = payload.fingerprint(stage)
        reader_hash = hashlib.sha256((stage / "kk/lib/payload.py").read_bytes()).hexdigest()
        replace_pending(stage, home / "staging" / version, work)
    record["candidate"] = {"version": version, "phase": "staged", "source": source,
                           "digest": digest, "reader_sha256": reader_hash}
    state.write_json(home / "state.json", record)
    return version


def install_locked(home, args, archive_file=None):
    record = state.load(home)
    if record["active"]:
        if args.command == "install" and not record["candidate"]:
            print("Already installed:", record["active"])
            return
        raise ValueError("upgrading an active release is not implemented in this first-install version")
    check_link(home, record)
    work = home / ".first-install-work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    try:
        version = prepare(home, record, args, archive_file, work)
        record["candidate"]["phase"] = "activating"
        state.write_json(home / "state.json", record)
        stage = home / "staging" / version
        release = home / "releases" / version
        if stage.exists():
            replace_pending(stage, release, work)
        # Staging is private to this writer. Placed releases may already
        # service hooks in open sessions and follow the retention policy.
        if (home / "staging").is_dir():
            shutil.rmtree(home / "staging")
        candidate = load_cli(release / "kk/lib", "_kk_candidate")
        candidate.finish_install(home, record, release)
    finally:
        shutil.rmtree(work)


def status(home):
    record = state.load(home)
    active = record["active"]
    print("Active:", active or "none")
    if active:
        for tool, phase in record["releases"][active]["tools"].items():
            print("{}: {}".format(tool, phase))
    if record["candidate"]:
        print("Candidate: {version} ({phase})".format(**record["candidate"]))
        if not active:
            print("Run install.sh again to finish the first install.")
    print("Rollback target:", record["rollback_target"] or "none")


def main():
    parser = argparse.ArgumentParser(prog="kk")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("install", "upgrade"):
        action = commands.add_parser(command)
        source = action.add_mutually_exclusive_group()
        source.add_argument("--local", type=Path, metavar="CHECKOUT")
        source.add_argument("--version", metavar="TAG")
    commands.add_parser("status")
    args = parser.parse_args()
    home = state.toolbox_home()
    try:
        if args.command == "status":
            status(home)
        else:
            with state.writer(home):
                install_locked(home, args)
        return 0
    except (OSError, ValueError, KeyError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print("kk:", exc, file=sys.stderr)
        return 1
