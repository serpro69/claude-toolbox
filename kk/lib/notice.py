"""Check for a newer stable release at most once a day, outside the launcher."""

import fcntl
from contextlib import contextmanager
from http.client import HTTPException
import os
import subprocess
import sys
import time

from . import payload, state


DAY = 24 * 60 * 60


def read_cache(home):
    try:
        cached = payload.read_json(home / "update-notice.json")
        return cached if isinstance(cached, dict) else {}
    except (OSError, ValueError):
        return {}


def fresh(cache, repository):
    try:
        return 0 <= time.time() - cache[repository]["checked"] < DAY
    except (TypeError, KeyError):
        return False


def newer(latest, installed):
    stable = payload.tag_name(latest)[1:].split("+")[0]
    current = payload.tag_name(installed)[1:].split("+")[0]
    if "-" in stable:
        return False
    base, prerelease, _ = current.partition("-")
    upstream = tuple(map(int, stable.split(".")))
    local = tuple(map(int, base.split(".")))
    return upstream > local or (upstream == local and bool(prerelease))


def installed_tag(home, record):
    active = record["active"]
    source = record["releases"][active].get("source", {})
    return source.get("tag") or "v" + payload.read_json(
        home / "releases" / active / "klaude-plugin/.claude-plugin/plugin.json")["version"]


def check(home, record):
    active = record["active"]
    if not active:
        raise ValueError("no active release; finish installing kk first")
    try:
        latest = payload.latest_tag(payload.upgrade_repository())
    except (OSError, HTTPException) as exc:
        raise ValueError("could not check the latest stable release: {}".format(exc)) from exc
    installed = installed_tag(home, record)
    if newer(latest, installed):
        print("{} is available (installed {}).".format(latest, installed))
    else:
        print("No newer stable release (installed {}, latest {}).".format(installed, latest))


@contextmanager
def cache_lock(home):
    with (home / "update-notice.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def refresh(home, repository):
    try:
        with cache_lock(home):
            cache = read_cache(home)
            if fresh(cache, repository):
                return
            previous = cache.get(repository, {})
            if not isinstance(previous, dict):
                previous = {}
            try:
                latest = payload.latest_tag(repository)
            except (OSError, HTTPException, ValueError, KeyError, TypeError):
                latest = previous.get("latest")
            cache[repository] = {"checked": time.time(), "latest": latest,
                                 "shown": previous.get("latest") == latest and previous.get("shown", False)}
            state.write_json(home / "update-notice.json", cache)
    except (OSError, ValueError):
        return  # An optional notification must never make a launch fail.


def on_launch(home, record):
    if not (sys.stdin.isatty() and sys.stderr.isatty()):
        return
    try:
        try:
            config = payload.read_json(state.override_path())
        except FileNotFoundError:
            config = {}
        if not isinstance(config, dict) or config.get("launchNotice", True) is not True:
            return
        active = record["active"]
        source = record["releases"][active].get("source", {})
        repo = source.get("repository", os.environ.get("KK_REPOSITORY", "serpro69/claude-toolbox"))
        release = home / "releases" / payload.release_id(active)
        with cache_lock(home):
            cache = read_cache(home)
            entry = cache.get(repo, {})
            if isinstance(entry, dict) and entry.get("latest") and not entry.get("shown"):
                installed = installed_tag(home, record)
                if newer(entry["latest"], installed):
                    print("kk: {} is available (installed {}).".format(entry["latest"], installed),
                          file=sys.stderr, flush=True)
                    entry["shown"] = True
                    state.write_json(home / "update-notice.json", cache)
            if fresh(cache, repo):
                return
        # Reap the short-lived shell before exec. Its detached worker has no
        # terminal descriptors and does all network I/O after the handoff.
        subprocess.run(["/bin/sh", "-c", '"$@" &', "kk-notice", sys.executable, "-I", "-B",
                        str(release / "kk/lib/run.py"), "--refresh-notice", str(home), repo],
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       start_new_session=True)
    except (OSError, ValueError, KeyError, TypeError):
        return
