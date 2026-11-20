"""Release staging, activation and offline recovery under one writer lock."""

import argparse
import hashlib
import os
from pathlib import Path
import shlex
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
    if (home / "bin").is_symlink():
        raise ValueError("toolbox bin directory is a symlink: {}".format(home / "bin"))
    if os.path.lexists(link):
        if str(link) not in record["installed_paths"] or not link.is_symlink():
            raise ValueError("install path already exists: {}".format(link))
        destination = link.parent / os.readlink(link)
        # Check this link's destination. The stable dispatcher at that path
        # may itself be broken and is precisely what rollback must replace.
        if destination.parent.resolve() / destination.name != home / "bin/kk":
            raise ValueError("install path already exists: {}".format(link))


def recovery_command(home, version):
    return shlex.quote(str(home / "releases" / payload.release_id(version) / "kk/bin/kk")) + " rollback"


def entry_digest(path):
    if not path.is_symlink() and path.is_file() and os.access(path, os.R_OK | os.X_OK):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return None


def complete_publication(home, record):
    """A promoted release can finish publishing its dispatcher after a crash."""
    version = payload.release_id(record["pending_entry"])
    if version != record["active"]:
        raise ValueError("journaled dispatcher does not belong to the active release")
    expected = record["pending_entry_sha256"]
    draft = home / "bin/.kk-next"
    entry = home / "bin/kk"
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError("invalid journaled dispatcher digest")
    if entry_digest(entry) != expected:
        if entry_digest(draft) != expected:
            wanted = (home / "releases" / version / "kk/bin/kk").read_bytes()
            if hashlib.sha256(wanted).hexdigest() != expected:
                raise ValueError("dispatcher bytes differ from the validated release; run kk rollback")
            state.atomic_write(draft, wanted, mode=0o755)
        os.replace(draft, entry)
    draft.unlink(missing_ok=True)
    del record["pending_entry"]
    del record["pending_entry_sha256"]
    state.write_json(home / "state.json", record)


def finish_install(home, record, release):
    """Run in the release being activated, under the caller's writer lock."""
    check_link(home, record)
    def checkpoint(step):
        state.checkpoint(home, record, step)

    claude.activate(home, release, checkpoint)
    checkpoint("entry-point")
    entry = home / "bin/kk"
    draft = home / "bin/.kk-next"
    wanted = (release / "kk/bin/kk").read_bytes()
    expected = hashlib.sha256(wanted).hexdigest()
    publication_due = entry_digest(entry) != expected
    if publication_due:
        state.atomic_write(draft, wanted, mode=0o755)
        if not record["active"]:
            os.replace(draft, entry)
            publication_due = False
    link = entry_link()
    if str(link) not in record["installed_paths"]:
        record["installed_paths"].append(str(link))
    checkpoint("entry-link")
    link.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.lexists(link):
        link.symlink_to(entry)  # Atomic create-only publication of the recorded path.
    check_link(home, record)
    checkpoint("promote")
    pending = record["candidate"]
    state.remember_candidate(record, pending)
    state.promote(record, release.name)
    state.remember_placed(home, record, pending.get("abandoned"))
    if publication_due:
        record["pending_entry"] = release.name
        record["pending_entry_sha256"] = expected
    else:
        record.pop("pending_entry", None)
        record.pop("pending_entry_sha256", None)
    state.write_json(home / "state.json", record)
    print("Claude ready:", release.name)
    if record["rollback_target"]:
        print("Recovery command:", recovery_command(home, record["rollback_target"]), flush=True)
    if publication_due:
        complete_publication(home, record)
    else:
        draft.unlink(missing_ok=True)
    state.prune(home, record)


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
    if record["active"] and candidate and candidate["phase"] == "activating" and source != candidate["source"]:
        raise ValueError("upgrade in progress; run kk upgrade to resume or kk rollback to restore the active release")
    if candidate and source == candidate["source"]:
        version = payload.release_id(candidate["version"])
        stage = home / "staging" / version
        existing = stage if stage.is_dir() else home / "releases" / version
        try:
            payload.verify_saved(existing, candidate)
            validation.validate(existing)
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
            if record["active"] and candidate["phase"] == "activating":
                raise ValueError("cannot resume candidate {}; run kk rollback: {}".format(version, exc)) from exc
            print("kk: rebuilding incomplete candidate {}: {}".format(version, exc), file=sys.stderr)
        else:
            return version
    elif candidate:
        print("kk: staging the requested source in place of the pending candidate", file=sys.stderr)
    local = Path(source["local"]) if "local" in source else None
    if record["active"] and local is None:
        version = payload.tag_name(source["tag"]) if source["tag"] else payload.latest_tag(source["repository"])
        source["tag"] = version
        existing = record["releases"].get(version, {})
        if existing.get("source") == source:
            if version == record["active"]:
                print("Already active:", version)
                if record["rollback_target"]:
                    print("Recovery command:", recovery_command(home, record["rollback_target"]))
                state.prune(home, record)
                return None
            placed = home / "releases" / version
            payload.verify_saved(placed, existing)
            validation.validate(placed)
            record["candidate"] = {"version": version, "phase": "staged", "source": source,
                                   "digest_format": 2, "digest": payload.fingerprint(placed)}
            state.write_json(home / "state.json", record)
            return version
    with tempfile.TemporaryDirectory(dir=work) as temp:
        stage = Path(temp) / "payload"
        stage.mkdir()
        version = payload.stage(stage, local, source.get("tag"), archive_file, source.get("repository"))
        if local is None:
            source["tag"] = version
        placed = home / "releases" / version
        if placed.exists() and (record["active"] or not (
                candidate and candidate["version"] == version and candidate["source"] == source)):
            raise ValueError("retained release {} already occupies {}; choose a different tag or --local".format(
                version, placed))
        validation.validate(stage)
        digest = payload.fingerprint(stage)
        reader_hash = hashlib.sha256((stage / "kk/lib/payload.py").read_bytes()).hexdigest()
        replace_pending(stage, home / "staging" / version, work)
    if candidate and candidate["version"] != version and (home / "releases" / payload.release_id(candidate["version"])).is_dir():
        state.remember_candidate(record, candidate)
    record["candidate"] = {"version": version, "phase": "staged", "source": source,
                           "digest_format": 2, "digest": digest, "reader_sha256": reader_hash}
    state.write_json(home / "state.json", record)
    return version


def install_locked(home, args, archive_file=None):
    record = state.load(home)
    if record.get("pending_entry"):
        check_link(home, record)
        complete_publication(home, record)
        print("Published dispatcher for:", record["active"])
        if not args.local and not args.version and not record["candidate"]:
            if record["rollback_target"]:
                print("Recovery command:", recovery_command(home, record["rollback_target"]))
            state.prune(home, record)
            return
    if record["active"] and args.command == "install":
        if record["candidate"]:
            raise ValueError("mixed installation; run kk status for recovery commands")
        print("Already installed:", record["active"])
        return
    if (record["candidate"] or {}).get("operation") == "rollback":
        raise ValueError("rollback in progress; run kk rollback to finish restoring the release")
    check_link(home, record)
    work = home / ".first-install-work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    try:
        version = prepare(home, record, args, archive_file, work)
        if version is None:
            return
        state.checkpoint(home, record, "place")
        stage = home / "staging" / version
        release = home / "releases" / version
        if record["active"]:
            print("If activation stops, restore the active release with",
                  recovery_command(home, record["active"]), flush=True)
        if stage.exists():
            if record["active"]:
                if release.exists():
                    raise ValueError("cannot overwrite a placed release: {}".format(release))
                stage.rename(release)
            else:
                replace_pending(stage, release, work)
        # Staging is private to this writer. Placed releases may already
        # service hooks in open sessions and follow the retention policy.
        if (home / "staging").is_dir():
            shutil.rmtree(home / "staging")
        candidate = load_cli(release / "kk/lib", "_kk_candidate")
        candidate.finish_install(home, record, release)
    finally:
        shutil.rmtree(work)


def rollback_locked(home, record):
    target = state.rollback_version(record)
    if not target:
        raise ValueError("no previous release to restore")
    release = home / "releases" / payload.release_id(target)
    check_link(home, record)
    saved = record["releases"][target]
    for tool, phase in saved.get("tools", {}).items():
        if phase not in ("ready", "unverified"):
            print("Restoring {} with {} previously {}.".format(target, tool, phase))
    payload.verify_saved(release, saved)
    validation.validate(release)
    previous = record["candidate"]
    if not previous or previous.get("operation") != "rollback":
        rollback = {"operation": "rollback", "phase": "activating", "version": target}
        if previous and previous["version"] != target:
            rollback["abandoned"] = previous["version"]
            if (home / "releases" / payload.release_id(previous["version"])).is_dir():
                state.remember_candidate(record, previous)
        record["candidate"] = rollback
        record.pop("pending_entry", None)
        record.pop("pending_entry_sha256", None)
    state.checkpoint(home, record, "restore")
    finish_install(home, record, release)
    staging = home / "staging"
    if staging.is_dir():
        shutil.rmtree(staging)


def status(home):
    record = state.load(home)
    active = record["active"]
    print("Active:", active or "none")
    if active:
        for tool, phase in record["releases"][active]["tools"].items():
            print("{}: {}".format(tool, phase))
    if record.get("pending_entry"):
        print("Dispatcher publication pending. Run kk upgrade to finish, or kk rollback to restore the rollback target.")
    if record["candidate"]:
        print("Candidate: {version} ({phase})".format(**record["candidate"]))
        candidate = record["candidate"]
        if not active:
            print("Run install.sh again to finish the first install.")
        elif candidate.get("operation") == "rollback":
            print("Mixed installation. Finish rollback with kk rollback.")
            print("Recovery command:", recovery_command(home, candidate["version"]))
        elif candidate["phase"] == "activating":
            print("Mixed installation. Resume with kk upgrade or restore the active release with kk rollback.")
            print("Recovery command:", recovery_command(home, active))
        else:
            print("Run kk upgrade to activate the staged release.")
        if candidate.get("step"):
            print("Journaled step:", candidate["step"])
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
    commands.add_parser("rollback")
    args = parser.parse_args()
    home = state.toolbox_home()
    try:
        if args.command == "status":
            status(home)
        else:
            with state.writer(home):
                record = state.load(home)
                owner = state.rollback_version(record) if args.command == "rollback" else record["active"]
                if owner and Path(__file__).resolve().parents[2] != home / "releases" / payload.release_id(owner):
                    # The lock may have changed hands since the shell read state.
                    raise ValueError("release selection changed; rerun kk " + args.command)
                if args.command == "rollback":
                    rollback_locked(home, record)
                else:
                    install_locked(home, args)
        return 0
    except (OSError, ValueError, KeyError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print("kk:", exc, file=sys.stderr)
        return 1
