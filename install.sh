#!/usr/bin/env bash
# Run from a checkout or pipe this standalone installer to bash.
set -euo pipefail

root=${KK_HOME:-${XDG_DATA_HOME:-"$HOME/.local/share"}/kk}
link=$HOME/.local/bin/kk
found=$(command -v kk || true)
if [[ -n "$found" && "$found" != "$link" && ! "$found" -ef "$link" ]]; then
    printf 'kk: PATH selects %s ahead of the installer link %s\n' "$found" "$link" >&2
fi

# Hold the same writer lock while resolving the journal,
# downloading the pinned archive, and handing it to the release's install code.
exec python3 -I -B - "$root" "$@" <<'PY'
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import runpy
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.request import urlopen


def package(root):
    lib = root / "kk/lib"
    return runpy.run_path(str(lib / "run.py"))["load_cli"](lib, "_kk_bootstrap")


def intact(directory, candidate):
    reader = directory / "kk/lib/payload.py"
    try:
        if directory.is_symlink() or directory not in reader.resolve().parents or not reader.is_file():
            return False
        if hashlib.sha256(reader.read_bytes()).hexdigest() != candidate["reader_sha256"]:
            return False
        fingerprint = runpy.run_path(str(reader))["fingerprint"]
        return fingerprint(directory) == candidate["digest"]
    except (OSError, ValueError, RuntimeError) as error:
        print("kk: cannot verify pending candidate {}: {}".format(directory, error), file=sys.stderr)
        return False


def install(home, args):
    journal = home / "state.json"
    try:
        record = json.loads(journal.read_bytes())
    except FileNotFoundError:
        record = {}
    else:
        if not isinstance(record, dict) or type(record.get("format_version")) is not int or record["format_version"] != 1:
            raise ValueError("unsupported kk state format")
    if record.get("active"):
        if record.get("pending_entry"):
            raise ValueError("dispatcher publication pending; run kk upgrade to finish or kk rollback to restore")
        if record.get("candidate"):
            raise ValueError("mixed installation; run kk status for recovery commands")
        print("Already installed:", record["active"])
        return

    candidate = record.get("candidate")
    if args.local and (not candidate or {"local": str(args.local.resolve())} != candidate["source"]):
        package(args.local.resolve()).install_locked(home, args)
        return
    if candidate and args.version:
        requested = {"tag": args.version, "repository": os.environ.get("KK_REPOSITORY", "serpro69/claude-toolbox")}
        if requested != candidate["source"]:
            candidate = None
    if candidate:
        version = candidate["version"]
        if not re.fullmatch(r"(v[0-9][0-9A-Za-z.+-]*|local-[0-9a-f]{32})", version):
            raise ValueError("invalid candidate in state.json")
        for directory in (home / "staging" / version, home / "releases" / version):
            if intact(directory, candidate):
                package(directory).install_locked(home, args)
                return
        if args.local:
            package(args.local.resolve()).install_locked(home, args)
            return
        if not args.version and not args.local:
            source = candidate["source"]
            if "local" in source:
                args.local = Path(source["local"])
                package(args.local).install_locked(home, args)
                return
            args.version = source["tag"]
            os.environ["KK_REPOSITORY"] = source["repository"]

    repo = os.environ.get("KK_REPOSITORY", "serpro69/claude-toolbox")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or any(
            part in (".", "..") for part in repo.split("/")):
        raise ValueError("KK_REPOSITORY must be a GitHub owner/repository")
    api = "https://api.github.com/repos/" + repo
    if not args.version:
        with urlopen(api + "/releases/latest", timeout=30) as response:
            args.version = json.load(response)["tag_name"]
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", args.version):
        raise ValueError("invalid release tag")

    with tempfile.TemporaryDirectory(prefix="kk-bootstrap-") as scratch:
        work = Path(scratch)
        archive = work / "release.tar.gz"
        with urlopen(api + "/tarball/" + args.version, timeout=60) as response, archive.open("wb") as output:
            shutil.copyfileobj(response, output)
        # Bootstrap only ordinary installer source files from the same archive.
        # Destination ancestors are created here and archive links are never followed.
        with tarfile.open(archive, "r:*") as tar:
            prefix = None
            for member in tar:
                name = PurePosixPath(member.name)
                parts = name.parts
                if not parts or name.is_absolute() or ".." in parts:
                    raise ValueError("unsafe archive member: " + member.name)
                if prefix is None:
                    prefix = parts[0]
                elif parts[0] != prefix:
                    raise ValueError("multiple roots in release archive")
                name = parts[1:]
                if name != ("kk", "payload.json") and not (
                        len(name) == 3 and name[:2] == ("kk", "lib") and re.fullmatch(r"[A-Za-z_]+\.py", name[2])):
                    continue
                if not member.isreg():
                    raise ValueError("bootstrap source must be a regular file: " + member.name)
                destination = work.joinpath(*name)
                destination.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source, destination.open("xb") as output:
                    shutil.copyfileobj(source, output)
        package(work).install_locked(home, args, archive_file=archive)


parser = argparse.ArgumentParser(prog="install.sh")
source = parser.add_mutually_exclusive_group()
source.add_argument("--version", metavar="TAG")
source.add_argument("--local", type=Path, metavar="CHECKOUT")
args = parser.parse_args(sys.argv[2:])
args.command = "install"
home = Path(sys.argv[1]).resolve()
try:
    home.mkdir(parents=True, exist_ok=True)
    with (home / "lock").open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            lock.seek(0)
            raise SystemExit("kk: another kk writer holds {} (PID {})".format(lock.name, lock.read().strip()))
        lock.seek(0)
        lock.truncate()
        lock.write(str(os.getpid()))
        lock.flush()
        install(home, args)
except (OSError, ValueError, KeyError, tarfile.TarError, subprocess.SubprocessError) as error:
    sys.exit("kk: " + str(error))
PY
