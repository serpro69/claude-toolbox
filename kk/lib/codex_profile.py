"""Compose kk's Codex launch settings; validate and publish the Codex files the active release owns."""

import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

from . import codex_app, codex_plugins, mixed, payload, state
from .claude_launch import check_keys, object_value, switches
from .state import override_path


# Codex splits a -c key on every dot, even inside quotes, so only a plain name can head a launch flag.
PLAIN_KEY = re.compile(r"[A-Za-z0-9_-]+")
# These tables carry credentials, and launch flags are readable in process listings.
CREDENTIAL_TABLES = ("mcp_servers", "model_providers", "shell_environment_policy")
# Runs a session in its own server. A launch with kk's flags passes it (see codex_launch).
NO_DAEMON = "--no-daemon"


def codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").resolve()


def override_bytes():
    path = override_path()
    try:
        return path.read_bytes()
    except FileNotFoundError:
        if path.is_symlink():
            raise
        return None


def digest(raw):
    return hashlib.sha256(raw).hexdigest() if raw is not None else "missing"


def report_drift(record):
    if "codex_override_hash" not in record:
        return
    try:
        current = digest(override_bytes())
    except OSError as exc:
        print("kk: cannot check override changes at {}: {}".format(override_path(), exc), file=sys.stderr)
        return
    if record["codex_override_hash"] != current:
        print("kk: Codex overrides changed. Run kk apply to apply them.", file=sys.stderr)


def toml_value(value):
    """TOML basic strings, scalars, arrays and inline tables for JSON values."""
    if isinstance(value, dict):
        return "{ " + ", ".join(toml_value(k) + " = " + toml_value(v) for k, v in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    if value is None:
        raise ValueError("Codex settings cannot be null")
    return json.dumps(value, ensure_ascii=False, allow_nan=False).replace(chr(127), r"\u007f")


def codex_settings(raw):
    try:
        config = object_value(json.loads(raw) if raw is not None else {}, str(override_path()))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid JSON in {}: {}".format(override_path(), exc)) from exc
    check_keys(config, ("claude", "codex", "launchNotice", "$schema"), str(override_path()))
    config = object_value(config.get("codex", {}), "codex")
    check_keys(config, ("defaults", "settings", "optIn"), "codex")
    return config


def leaves(table, path=()):
    """Flatten nested tables into (path tuple, value) pairs; an empty table is its own leaf."""
    for key, value in table.items():
        if isinstance(value, dict) and value:
            yield from leaves(value, path + (key,))
        else:
            yield path + (key,), value


def put(table, path, value):
    for part in path[:-1]:
        if not isinstance(table.get(part), dict):
            table[part] = {}
        table = table[part]
    # An empty table carries no value of its own, so it must not replace leaves already collected.
    if value != {} or not isinstance(table.get(path[-1]), dict):
        table[path[-1]] = value


def merge(pairs):
    """Build the table that leaves describe; a later leaf replaces an earlier one at its path."""
    table = {}
    for path, value in pairs:
        put(table, path, value)
    return table


def config_flags(table):
    # One flag per top-level key: a second inline table for a key would replace the first.
    return [part for key, value in table.items() for part in ("-c", key + "=" + toml_value(value))]


def compose(release, config):
    """Check the overrides against the release baseline and return what a launch is built from.

    Returns baseline leaves, explicit leaves, the instructions and the native switch.
    Leaves are (path tuple, value) pairs. Baseline leaves are kk's defaults left on by
    codex.defaults. Explicit leaves are the selected opt-ins followed by codex.settings,
    so the later of two leaves at one path is the one to use.
    """
    baseline = payload.read_json(release / "kk/baseline/codex.json")
    selected = config.get("optIn", {})
    switches(selected, set(baseline["optIn"]) | {"nativeForbids"}, "codex.optIn")
    profile = baseline["profile"]
    defaults = config.get("defaults", {})
    switches(defaults, set(profile), "codex.defaults")
    settings = object_value(config.get("settings", {}), "codex.settings")
    features = object_value(settings.get("features", {}), "codex.settings.features")
    plugins = object_value(settings.get("plugins", {}), "codex.settings.plugins")
    if ("hooks" in settings or {"hooks", "plugins"} & features.keys()
            or any(isinstance(plugin, dict) and "enabled" in plugin for plugin in plugins.values())):
        raise ValueError("configure hook and plugin enablement in native Codex configuration")
    for key in CREDENTIAL_TABLES:
        if key in settings:
            raise ValueError("configure {} in native Codex configuration".format(key))
    if "developer_instructions" in settings:
        raise ValueError("kk composes developer_instructions; use confirmed AGENTS.md imports for extra text")
    for key in settings:
        if not PLAIN_KEY.fullmatch(key):
            raise ValueError("codex.settings key {} is not a plain name; write a nested table as a JSON object".format(
                json.dumps(key)))
    profile = {k: v for k, v in profile.items() if defaults.get(k, True)}
    opted = {k: v for k, v in baseline["optIn"].items() if selected.get(k)}
    rules = payload.read_json(release / "kodex-guard/scripts/guard/guard-rules.json")
    advisory = ("Protected files: reading paths matching these secrets globs is prohibited by policy: "
                + ", ".join(rules["secrets"]) + ". Ask the user for the needed value or a redacted copy.")
    instructions = "\n\n".join([p.read_text(encoding="utf-8").rstrip() for p in (
        release / "kk/baseline/codex/bootstrap.md", release / "klaude-plugin/instructions/behavior.md"
    )] + [advisory]) + "\n"
    return (list(leaves(profile)), [*leaves(opted), *leaves(settings)], instructions,
            selected.get("nativeForbids", False))


def validate_files(release, directory, settings, rules, executable):
    """Stop publication when Codex rejects a value kk may pass at launch, or the candidate rules."""
    # An isolated working directory avoids a trusted project's config masking
    # candidate errors. Retain base user configuration (e.g. custom providers).
    with tempfile.TemporaryDirectory(prefix="kk-codex-check-") as temp:
        scratch = Path(temp)
        base = directory / "config.toml"
        if base.exists():
            (scratch / "config.toml").symlink_to(base)
        env = dict(os.environ, CODEX_HOME=str(scratch))
        def run(operation, args, capture=False):
            # The arguments carry codex.settings values, so a failure names only the operation.
            try:
                result = subprocess.run([executable] + args, cwd=scratch, env=env, stdin=subprocess.DEVNULL,
                                        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                                        stderr=subprocess.PIPE, text=True, timeout=30)
            except subprocess.TimeoutExpired:
                raise ValueError("Codex {} timed out".format(operation)) from None
            if result.returncode:
                raise ValueError("Codex rejected {}: {}".format(operation, result.stderr.strip()))
            return result.stdout
        # A Codex that does not know --no-daemon would refuse every interactive launch, so it stops here.
        try:
            run("debug prompt-input", [NO_DAEMON] + config_flags(settings) + ["debug", "prompt-input"])
        except ValueError as exc:
            # Only Codex's own wording for an unknown flag: its errors can also quote a rejected value.
            if "unexpected argument '{}'".format(NO_DAEMON) not in str(exc):
                raise
            # The adopter never typed the flag, so say where it comes from and what helps.
            raise ValueError("kk codex passes {} to its sessions, and this Codex CLI refused it; update Codex. {}".format(
                NO_DAEMON, exc)) from None

        def unreported(table):
            """Return the leaves Codex does not report under kk's name, and the other names it reported."""
            try:
                layers, _ = codex_app.layers(scratch, scratch, config_flags(table), executable, 30)
            except (codex_app.NoMethod, ValueError) as exc:
                # Required, not skipped with a warning: every launch depends on the same request, and
                # a skipped check would let a misnamed key through after a single timeout.
                raise ValueError("kk checks setting names through Codex config/read, which failed: {}. Run the command "
                                 "again; if this Codex CLI has no config/read, update Codex".format(exc)) from exc
            names = {key for key, layer in layers.items() if layer == "sessionFlags"}
            missing = []
            for path, value in leaves(table):
                # Any layer vouches for a name: a managed layer outranks a flag and is reported in its place.
                keys = codex_app.origin_keys(layers, path)
                names.difference_update(keys)
                # Codex reports no origin for an empty array or table.
                if not keys and value not in ([], {}):
                    missing.append((path, value))
            return missing, sorted(names)

        # A launch finds out what other layers set by these names. A value Codex reports under
        # another name, such as an alias, would never yield to the account or a repository.
        missing, _ = unreported(settings)
        if missing:
            # Passed alone, they show the names Codex uses, which another kk value may share.
            _, names = unreported(merge(missing))
            raise ValueError("Codex config/read does not report {} under the name kk passes; it reported {} instead. "
                             "Use the name Codex reports in codex.settings. For one of kk's own defaults, switch "
                             "it off in codex.defaults and update kk".format(
                                 ", ".join(".".join(path) for path, _ in missing), ", ".join(names) or "no other name"))
        if rules is None:
            return
        candidate = scratch / "kk.rules"
        candidate.write_bytes(rules)
        command = ["execpolicy", "check", "--rules", str(candidate)]
        declaration = payload.read_json(release / "kodex-guard/scripts/guard/guard-rules.json")
        for category in declaration["destructive"].values():
            for rule in category:
                for native in rule.get("codex", []):
                    for example in native["match"]:
                        decision = json.loads(run("execpolicy check", command + ["--"] + shlex.split(example), True))
                        if not isinstance(decision, dict) or decision.get("decision") != "forbidden":
                            raise ValueError("candidate kk.rules does not forbid " + example)
        for path in sorted((directory / "rules").glob("*.rules")):
            if path.name != "kk.rules":
                command.extend(["--rules", str(path)])
        run("execpolicy check", command + ["--", "echo", "ok"])


def check_destinations(paths, owned):
    for path in paths:
        if path.parent.resolve() != path.parent:
            raise ValueError("install directory is a symlink: {}".format(path.parent))
        if os.path.lexists(path) and (str(path) not in owned or path.is_symlink() or not path.is_file()):
            raise ValueError("install path already exists: {}".format(path))


def prepare(release, record, *, required=False, snapshot=...):
    executable = shutil.which("codex")
    if not executable and snapshot is ...:
        if required or record.get("codex_paths"):
            raise ValueError("codex executable not found on PATH")
        return None
    if snapshot is not ...:
        saved = snapshot
        if saved is None:
            return {}, [Path(p) for p in record.get("codex_paths", [])], None, None
        directory = Path(saved["directory"])
    else:
        directory = codex_home()
        raw = override_bytes()
        saved = {"directory": str(directory), "settings": codex_settings(raw), "override_hash": digest(raw)}
    baseline, explicit, instructions, native = compose(release, saved["settings"])
    files = {}
    agents = release / "kk/baseline/codex/agents"
    for agent in sorted(agents.iterdir()):
        if agent.suffix == ".toml":
            files[directory / "agents" / ("kk-" + agent.name)] = agent.read_bytes()
    rules = None
    if native:
        rules = (release / "kk/baseline/codex/kk.rules").read_bytes()
        files[directory / "rules/kk.rules"] = rules
    obsolete = [Path(p) for p in record.get("codex_paths", []) if Path(p) not in files]
    if any(str(path) not in record["installed_paths"] for path in obsolete):
        raise ValueError("inconsistent Codex installed-paths record")
    check_destinations(list(files) + obsolete, record["installed_paths"])
    # The target's immutable payload and saved overrides reproduce its validated
    # files. A broken vendor CLI must not strand recovery of the Claude release.
    if snapshot is ...:
        settings = merge([*baseline, *explicit, (("developer_instructions",), instructions)])
        validate_files(release, directory, settings, rules, str(Path(executable).absolute()))
    return files, obsolete, instructions.encode(), saved


def prepare_activation(release, record):
    candidate = record["candidate"]
    home = release.parent.parent
    if candidate["phase"] == "activating" and "codex_inputs" in candidate:
        saved = candidate["codex_inputs"]
        mixed.check_claude_pilot(home)
        mixed.check_codex_pilot(home, record, saved["directory"] if saved else None)
        return None if saved is None else prepare(release, record, snapshot=saved)
    plan = prepare(release, record)
    if plan:
        directory = Path(plan[3]["directory"])
        # A previous release's staging code may predate guard stamping. Its
        # preflight runs here before the private staging directory is placed.
        if not candidate.get("codex_guard_staged") and release.parent.name == "staging":
            codex_plugins.stage_guard(release, record, directory, "local" in candidate["source"])
            candidate["digest"] = payload.fingerprint(release)
            candidate["codex_guard_staged"] = True
        previous = candidate.get("confirmed_guard_change")
        codex_plugins.confirm_change(record, release, directory)
        if candidate.get("confirmed_guard_change") != previous:
            # A pilot still has its working guard here. A confirmed switch may
            # pause for vendor cleanup; resuming the same change needs no new consent.
            state.write_json(home / "state.json", record)
    mixed.check_claude_pilot(home)
    mixed.check_codex_pilot(home, record, plan[3]["directory"] if plan else None)
    # The place checkpoint persists exactly the inputs validated at staging.
    candidate["codex_inputs"] = None if plan is None else plan[3]
    return plan


def reconcile_claim(home, record):
    """Finish or relinquish an interrupted create-only publication under the writer lock."""
    claim = record.get("codex_claim")
    if not claim:
        return
    path = Path(claim["path"])
    temporary = Path(claim["temporary"])
    if temporary.parent != path.parent or path.parent.resolve() != path.parent:
        raise ValueError("cannot recover Codex destination in a replaced directory: {}".format(path))
    try:
        info = temporary.lstat()
    except FileNotFoundError:
        if "linked" not in claim:
            raise ValueError("missing Codex publication evidence: {}".format(temporary))
    else:
        if [info.st_dev, info.st_ino] != claim["identity"]:
            raise ValueError("Codex publication temporary file was replaced: {}".format(temporary))
        if "linked" not in claim:
            try:
                destination = path.lstat()
                linked = os.path.samestat(info, destination)
            except FileNotFoundError:
                linked = False
            if not linked:
                record["installed_paths"].remove(str(path))
                record["codex_paths"].remove(str(path))
            claim["linked"] = linked
            state.write_json(home / "state.json", record)
        temporary.unlink()
    del record["codex_claim"]
    state.write_json(home / "state.json", record)


def publish_new(home, record, path, data):
    # Keep the source inode until the ownership decision is durable. On retry,
    # a file someone else created after our reservation remains theirs.
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".kk-", delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            info = os.fstat(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    # Once journal publication starts we may already have committed the claim,
    # even if the write raises. Recovery must still have its proof inode.
    record["codex_claim"] = {"path": str(path), "temporary": str(temporary),
                             "identity": [info.st_dev, info.st_ino]}
    record["installed_paths"].append(str(path))
    record["codex_paths"].append(str(path))
    state.write_json(home / "state.json", record)
    try:
        os.link(temporary, path)
    finally:
        reconcile_claim(home, record)


def publish(home, record, version, plan):
    if plan is None:
        return
    files, obsolete, instructions, saved = plan
    if any(str(path) not in record["installed_paths"] for path in obsolete):
        raise ValueError("inconsistent Codex installed-paths record")
    check_destinations(list(files) + obsolete, record["installed_paths"])
    record["codex_write_pending"] = True
    state.write_json(home / "state.json", record)
    record.setdefault("codex_paths", [])
    for path, data in files.items():
        if str(path) in record["installed_paths"]:
            state.atomic_write(path, data)
        else:
            publish_new(home, record, path, data)
    for path in obsolete:
        path.unlink(missing_ok=True)
        record["installed_paths"].remove(str(path))
        if path.name == "kk.config.toml":
            # Releases that launched Codex with this profile let Codex save session choices in it.
            print("kk: removed the managed Codex profile {}; kk codex now passes its settings as launch flags. "
                  "A model or hook approval Codex saved in that profile no longer applies: choose it again in "
                  "plain codex, or set it in config.toml.".format(path))
    sidecar = home / "codex-instructions.md"
    release_state = record["releases"].setdefault(version, {})
    if saved is None:
        sidecar.unlink(missing_ok=True)
        record.pop("codex_override_hash", None)
        release_state.setdefault("tools", {}).pop("codex", None)
    else:
        state.atomic_write(sidecar, instructions)
        record["codex_override_hash"] = saved["override_hash"]
        release_state["codex_snapshot"] = saved
        release_state.setdefault("tools", {}).setdefault("codex", "awaiting review")
    if any(path.name == "kk.rules" for path in files) and not record.get("codex_rules_announced"):
        print("kk: native forbids now affect every Codex session on this account, including bare Codex and temporary cleanup.")
        record["codex_rules_announced"] = True
    record["codex_paths"] = sorted(str(p) for p in files)
    del record["codex_write_pending"]
    state.write_json(home / "state.json", record)
