"""Persistent installation state and ownership of one writer transaction."""

import fcntl
import json
import os
from pathlib import Path
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone


def toolbox_home():
    data = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return Path(os.environ.get("KK_HOME") or data / "kk").resolve()


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


def promote(state, version):
    previous = state["active"]
    if previous and previous != version:
        old = state["releases"][previous]
        old["superseded_at"] = datetime.now(timezone.utc).isoformat()
        qualified = [name for name, release in state["releases"].items()
                     if name != version and release.get("superseded_at") and release.get("tools")
                     and all(status in ("ready", "unverified") for status in release["tools"].values())]
        state["rollback_target"] = max(
            qualified, key=lambda name: state["releases"][name]["superseded_at"], default=previous
        )
    release = state["releases"].setdefault(version, {})
    release.setdefault("tools", {})["claude"] = "ready"
    release["superseded_at"] = None
    state["active"] = version
    state["candidate"] = None
