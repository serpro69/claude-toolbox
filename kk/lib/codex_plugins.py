"""Install and verify the two plugins from the release's local Codex marketplace."""

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

from . import payload, state
from .claude import MARKETPLACE
from .guard_identity import MANIFEST, guard_identity, with_version


PLUGINS = {"kk": "kodex-plugin", "kk-guard": "kodex-guard"}
GUARD_ID = "kk-guard@" + MARKETPLACE
# The full inventory may wait for the remote catalog before listing local plugins.
INVENTORY_TIMEOUT = 120


def saved_receipt(record, directory, name):
    return record.get("codex_plugins", {}).get(str(directory), {}).get(name, {})


def receipt(record, directory, name):
    saved = saved_receipt(record, directory, name)
    if saved and saved.get("path") == str(Path(directory) / "plugins/cache" / MARKETPLACE / name / saved["version"]):
        return saved
    return {}


def activation_hint(saved):
    source = saved.get("source", {})
    if "tag" in source:
        repository = payload.canonical_repository(source["repository"])
        prefix = ("KK_REPOSITORY=" + shlex.quote(repository) + " "
                  if repository != payload.upgrade_repository() else "")
        return "run " + prefix + "kk upgrade --version " + source["tag"]
    if "local" in source:
        return "run kk upgrade --local " + shlex.quote(source["local"])
    return "run kk upgrade"


def stage_guard(release, record, directory, local):
    guard = release / PLUGINS["kk-guard"]
    installed = receipt(record, directory, "kk-guard")
    identity = guard_identity(guard)
    manifest = guard / MANIFEST
    version = payload.read_json(manifest)["version"]
    if local:
        separator = "." if "+" in version else "+"
        version = (installed["version"] if installed.get("identity") == identity
                   else version + separator + "kk." + identity[:12])
        state.atomic_write(manifest, with_version(manifest.read_bytes(), version), mode=manifest.stat().st_mode & 0o777)
    elif installed.get("version") == version and installed["identity"] != identity:
        raise ValueError("Codex guard content changed under installed version " + version)


def confirm_change(record, release, directory):
    installed = saved_receipt(record, directory, "kk-guard")
    identity = guard_identity(release / PLUGINS["kk-guard"])
    if not installed:
        return
    # A retained tag can be staged again without going through stage_guard.
    version = payload.read_json(release / PLUGINS["kk-guard"] / MANIFEST)["version"]
    same_market = bool(receipt(record, directory, "kk-guard"))
    if same_market and installed["version"] == version and installed["identity"] != identity:
        raise ValueError("Codex guard content changed under installed version " + version)
    if same_market and installed["identity"] == identity:
        return
    pair = [installed["identity"], identity] if same_market else [installed["path"], GUARD_ID, identity]
    candidate = record["candidate"]
    if candidate.get("confirmed_guard_change") == pair:
        return
    if not same_market:
        print("Codex requires a fresh review for {} in plain codex.".format(GUARD_ID), file=sys.stderr)
    print("Changing the Codex guard leaves open sessions without its protection at least until "
          "the new hooks are reviewed. Continue? [y/N] ", file=sys.stderr, end="", flush=True)
    if not sys.stdin.isatty() or sys.stdin.readline().strip().lower() not in ("y", "yes"):
        raise ValueError("guard change declined; candidate remains staged")
    candidate["confirmed_guard_change"] = pair


def executable():
    found = shutil.which("codex")
    if not found:
        raise FileNotFoundError("codex executable not found on PATH")
    return os.path.abspath(found)


def vendor(home, directory, *args, timeout=30):
    result = subprocess.run([executable(), "plugin", *args, "--json"], cwd=home,
                            env=dict(os.environ, CODEX_HOME=str(directory)), timeout=timeout,
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, check=True, text=True)
    return json.loads(result.stdout)


def manifest(home, release):
    return {"name": MARKETPLACE, "interface": {"displayName": "Agentstakk"},
            "plugins": [{"name": name, "category": "Productivity",
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "source": {"source": "local", "path": "./" + (release / folder).relative_to(home).as_posix()}}
                        for name, folder in PLUGINS.items()]}


def verify_tree(name, source, directory, version, path):
    expected = directory / "plugins/cache" / MARKETPLACE / name / version
    if not path.is_absolute() or path.resolve(strict=True) != expected or not expected.is_dir():
        raise ValueError("unexpected Codex install path for {}: {}".format(name, path))
    if payload.read_json(path / MANIFEST)["version"] != version:
        raise ValueError("Codex installed manifest differs from reported version for " + name)
    result = {"version": version, "path": str(expected)}
    if name == "kk-guard":
        result["identity"] = guard_identity(source)
        matches = guard_identity(path) == result["identity"]
    else:
        matches = (version == payload.read_json(source / MANIFEST)["version"]
                   and payload.fingerprint(source) == payload.fingerprint(path))
    if not matches:
        raise ValueError("installed Codex plugin bytes differ from release: " + name)
    return result


def restore_absent(home, record, directory, checkpoint):
    """Undo kk's registrations when the rollback target had no managed Codex."""
    receipts = record.get("codex_plugins", {}).get(directory)
    if receipts is None:
        return
    checkpoint("codex-restore-absent")
    path = Path(directory)
    if path.resolve() != path:
        raise ValueError("Codex home has moved; restore its original directory before rollback: " + directory)
    try:
        path.stat()
    except FileNotFoundError:
        # The adopter removed this home. Starting the vendor could recreate it.
        installed = set()
        record.pop("codex_plugin_pending", None)
    else:
        if not path.is_dir():
            raise ValueError("recorded Codex home is not a directory: " + directory)
        try:
            installed = remove_registrations(home, record, directory, receipts, checkpoint)
        except (OSError, subprocess.SubprocessError) as exc:
            raise ValueError("Claude and the owned Codex files were restored. Codex plugin cleanup is pending "
                             "in {} ({}); repair the Codex CLI or the reported error and rerun kk rollback."
                             .format(directory, exc)) from exc
    if len(record["codex_plugins"]) == 1 and not installed:
        # Older journals do not prove who registered the marketplace. A
        # retained registration still needs a catalog without stale B paths.
        catalog = home / ".agents/plugins/marketplace.json"
        if catalog.is_file():
            data = payload.read_json(catalog)
            data["plugins"] = []
            state.write_json(catalog, data)
    record.get("codex_marketplaces", {}).pop(directory, None)
    del record["codex_plugins"][directory]
    checkpoint("codex-restored-absent")


def remove_registrations(home, record, directory, receipts, checkpoint):
    markets = vendor(home, directory, "marketplace", "list")["marketplaces"]
    market = next((m for m in markets if m["name"] == MARKETPLACE), None)
    if market and Path(market["root"]).resolve() != home:
        raise ValueError("Codex marketplace {} already belongs to another source".format(MARKETPLACE))
    installed = {p["pluginId"] for p in vendor(home, directory, "list", "--marketplace", MARKETPLACE)["installed"]}
    pending = record.get("codex_plugin_pending")
    for name in PLUGINS:
        plugin_id = name + "@" + MARKETPLACE
        if receipt(record, directory, name) or pending == plugin_id:
            if plugin_id in installed:
                vendor(home, directory, "remove", plugin_id)
                installed.remove(plugin_id)
            receipts.pop(name, None)
            if pending == plugin_id:
                record.pop("codex_plugin_pending", None)
            checkpoint("codex-restored-absent-" + name)
    if market and record.get("codex_marketplaces", {}).get(directory) == MARKETPLACE and not any(
            item.endswith("@" + MARKETPLACE) for item in installed):
        vendor(home, directory, "marketplace", "remove", MARKETPLACE)
    return installed


def activate(home, record, release, directory, checkpoint):
    directory = Path(directory)
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    rollback = record["candidate"].get("operation") == "rollback"
    receipts = record.setdefault("codex_plugins", {}).setdefault(str(directory), {})
    # If the vendor executable broke after promotion, identical installed
    # trees can still be verified locally and the offline files restored.
    offline = False
    try:
        markets = vendor(home, directory, "marketplace", "list")["marketplaces"]
    except (OSError, subprocess.SubprocessError) as exc:
        if not rollback:
            raise
        checkpoint("codex-restore-plugins")
        try:
            if record.get("codex_plugin_pending"):
                raise ValueError("a vendor installation is unfinished")
            for name, folder in PLUGINS.items():
                saved = receipts[name]
                verify_tree(name, release / folder, directory, saved["version"], Path(saved["path"]))
        except (OSError, KeyError, ValueError) as cause:
            raise ValueError("Claude and the owned Codex files were restored. Codex plugin recovery is pending "
                             "({}); repair the Codex executable and rerun kk rollback: {}".format(cause, exc)) from exc
        offline = True
    if not offline:
        market = next((m for m in markets if m["name"] == MARKETPLACE), None)
        if market and Path(market["root"]).resolve() != home:
            raise ValueError("Codex marketplace {} already belongs to another source".format(MARKETPLACE))
    checkpoint("codex-marketplace")
    state.write_json(home / ".agents/plugins/marketplace.json", manifest(home, release))
    if offline:
        return
    if market is None:
        record.setdefault("codex_marketplaces", {})[str(directory)] = MARKETPLACE
        checkpoint("codex-register")
        vendor(home, directory, "marketplace", "add", str(home))
    entries = {p["pluginId"]: p for p in vendor(home, directory, "list", "--marketplace", MARKETPLACE)["installed"]}
    for name, folder in PLUGINS.items():
        source = release / folder
        wanted = payload.read_json(source / MANIFEST)["version"]
        plugin_id = name + "@" + MARKETPLACE
        entry = entries.get(plugin_id)
        version = entry["version"] if entry else None
        path = None
        if version is not None:
            payload.tag_name("v" + version)
            saved = receipt(record, directory, name)
            # list reports the version but only add reports installedPath. If add
            # committed just before interruption, reconcile its versioned cache.
            path = (Path(saved["path"]) if saved.get("version") == version else
                    directory / "plugins/cache" / MARKETPLACE / name / version)
        replace = version != wanted
        if name == "kk-guard" and path is not None:
            replace = guard_identity(path) != guard_identity(source)
        elif name == "kk" and not replace:
            # Local checkouts can edit a skill without bumping the manifest.
            replace = not path.is_dir() or payload.fingerprint(source) != payload.fingerprint(path)
        if replace:
            record["codex_plugin_pending"] = plugin_id
            checkpoint("codex-add-" + name)
            added = vendor(home, directory, "add", plugin_id)
            if added["pluginId"] != plugin_id or added["version"] != wanted:
                raise ValueError("Codex installed the wrong plugin or version for " + plugin_id)
            path, version = Path(added["installedPath"]), wanted
        receipts[name] = verify_tree(name, source, directory, version, path)
        if record.get("codex_plugin_pending") == plugin_id:
            del record["codex_plugin_pending"]
        checkpoint("codex-verified-" + name)
