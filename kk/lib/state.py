"""Persistent installation state and ownership of one writer transaction."""

import fcntl
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

from .payload import release_id


def toolbox_home():
    data = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return Path(os.environ.get("KK_HOME") or data / "kk").resolve()


def override_path():
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "kk/config.json"


def atomic_write(path, data, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(data)
            output.flush()
            os.fchmod(output.fileno(), mode)
            os.fsync(output.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def write_json(path, value):
    atomic_write(path, (json.dumps(value, indent=2) + "\n").encode())


def load(home):
    try:
        with (home / "state.json").open() as stream:
            state = json.load(stream)
    except FileNotFoundError:
        return {"format_version": 1, "active": None, "rollback_target": None,
                "candidate": None, "releases": {}, "installed_paths": []}
    if not isinstance(state, dict) or type(state.get("format_version")) is not int or state["format_version"] != 1:
        raise ValueError("unsupported kk state format; state.json was left intact")
    return state


@contextmanager
def writer(home):
    home.mkdir(parents=True, exist_ok=True)
    with (home / "lock").open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            lock.seek(0)
            holder = lock.read().strip() or "unknown"
            raise ValueError("another kk writer holds {} (PID {})".format(lock.name, holder)) from exc
        lock.seek(0)
        lock.truncate()
        lock.write(str(os.getpid()))
        lock.flush()
        yield


@contextmanager
def codex_access(home, *, batch=False):
    """Share admission among batch sessions, or reserve it to change the installation."""
    with (home / "codex-activation.lock").open("a") as lock:
        mode = fcntl.LOCK_SH if batch else fcntl.LOCK_EX
        try:
            fcntl.flock(lock, mode | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            reason = ("Codex files are changing; retry after activation" if batch else
                      "a managed Codex batch is running; retry after it finishes")
            raise ValueError(reason) from exc
        try:
            yield lock
        finally:
            # Release the shared open-file description once the vendor exits,
            # even if a vendor subprocess retained a duplicate descriptor.
            fcntl.flock(lock, fcntl.LOCK_UN)


def record_codex_phase(release, phase):
    tools = release.setdefault("tools", {})
    if phase in ("ready", "unverified") or tools.get("codex") in ("ready", "unverified"):
        release["codex_rollback_eligible"] = True
    tools["codex"] = phase


def promote(state, version, claude_phase="ready"):
    previous = state["active"]
    if previous and previous != version:
        old = state["releases"][previous]
        old["superseded_at"] = datetime.now(timezone.utc).isoformat()
        qualified = [name for name, release in state["releases"].items()
                     if name != version and release.get("superseded_at")
                     and release.get("tools", {}).get("claude") == "ready"  # A promoted release.
                     and all(status in ("ready", "unverified") or (tool == "codex" and release.get("codex_rollback_eligible"))
                             for tool, status in release["tools"].items())]
        state["rollback_target"] = max(
            qualified, key=lambda name: state["releases"][name]["superseded_at"], default=previous
        )
    release = state["releases"].setdefault(version, {})
    release.setdefault("tools", {})["claude"] = claude_phase
    release["superseded_at"] = None
    state["active"] = version
    state["candidate"] = None


def rollback_version(record):
    candidate = record["candidate"] or {}
    if candidate.get("operation") == "rollback":
        return candidate["version"]
    if candidate.get("phase") == "activating":
        return record["active"]
    return record["rollback_target"]


def checkpoint(home, record, step):
    record["candidate"].update(phase="activating", step=step)
    write_json(home / "state.json", record)


def remember_candidate(record, candidate):
    entry = record["releases"].setdefault(candidate["version"], {})
    for key in ("source", "digest", "digest_format"):
        if key in candidate:
            entry[key] = candidate[key]


def remember_placed(home, record, abandoned):
    """Start the retention clock now for directories whose earlier use is unknown."""
    now = datetime.now(timezone.utc).isoformat()
    for path in (home / "releases").iterdir():
        if path.is_symlink() or not path.is_dir() or path.name == record["active"]:
            continue
        try:
            release_id(path.name)
        except ValueError:
            continue
        entry = record["releases"].setdefault(path.name, {})
        if path.name == abandoned or not entry.get("superseded_at"):
            entry["superseded_at"] = now


def prune(home, record, now=None):
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=14)
    keep = {record["active"], record["rollback_target"], (record["candidate"] or {}).get("version")}
    for version, release in list(record["releases"].items()):
        since = release.get("superseded_at")
        if version in keep or not since or datetime.fromisoformat(since) >= cutoff:
            continue
        try:
            path = home / "releases" / release_id(version)
            if path.is_symlink():
                raise ValueError("refusing to prune a symlink: {}".format(path))
            if path.exists():
                shutil.rmtree(path)
        except (OSError, ValueError) as exc:
            print("kk: {} remains active; pruning {} deferred: {}".format(record["active"], version, exc),
                  file=sys.stderr)
            continue
        del record["releases"][version]
        write_json(home / "state.json", record)
